"""
HTTP API Endpoints for Unique Character Quest
----------------------------------------------
Provides RESTful endpoints for players, matches, leaderboards, achievements,
room management, and interactive educational algorithm evaluations.
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..database import (
    get_db,
    get_or_create_player,
    save_match_result,
    get_leaderboard,
    get_player_achievements_list,
    get_player_history
)
from ..schemas import (
    PlayerCreateRequest,
    PlayerResponse,
    MatchSaveRequest,
    MatchResponse,
    LeaderboardEntry,
    AchievementResponse,
    RoomCreateRequest,
    RoomJoinRequest,
    RoomStateResponse,
    AlgorithmEvaluateRequest,
    AlgorithmEvaluateResponse
)
from ..game.engine import GameEngine
from ..game.algorithms import (
    first_non_repeating_frequency,
    first_non_repeating_nested,
    explain_first_non_repeating
)
from ..game.validation import validate_player_name, validate_room_code, validate_sequence_input
from ..multiplayer.rooms import room_manager

api_router = APIRouter()
game_engine = GameEngine()


@api_router.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Unique Character Quest Backend",
        "active_rooms": len(room_manager.rooms),
        "active_single_player_sessions": len(game_engine.active_sessions)
    }


# -------------------------------------------------------------
# Players & Profiles
# -------------------------------------------------------------
@api_router.post("/players", response_model=PlayerResponse)
def create_or_fetch_player(payload: PlayerCreateRequest, db: Session = Depends(get_db)):
    """Registers or fetches an existing player identity."""
    valid, name_or_err = validate_player_name(payload.player_name)
    if not valid:
        raise HTTPException(status_code=400, detail=name_or_err)

    player = get_or_create_player(db, name_or_err)
    acc = round((player.total_correct / player.total_questions * 100), 1) if player.total_questions > 0 else 0.0

    return PlayerResponse(
        id=player.id,
        player_name=player.player_name,
        total_games=player.total_games,
        total_score=player.total_score,
        highest_score=player.highest_score,
        total_correct=player.total_correct,
        total_questions=player.total_questions,
        accuracy_percentage=acc,
        created_at=player.created_at,
        last_active=player.last_active
    )


@api_router.get("/players/{player_name}", response_model=PlayerResponse)
def get_player_profile(player_name: str, db: Session = Depends(get_db)):
    """Fetches player stats and accuracy."""
    player = get_or_create_player(db, player_name)
    acc = round((player.total_correct / player.total_questions * 100), 1) if player.total_questions > 0 else 0.0
    return PlayerResponse(
        id=player.id,
        player_name=player.player_name,
        total_games=player.total_games,
        total_score=player.total_score,
        highest_score=player.highest_score,
        total_correct=player.total_correct,
        total_questions=player.total_questions,
        accuracy_percentage=acc,
        created_at=player.created_at,
        last_active=player.last_active
    )


# -------------------------------------------------------------
# Leaderboards & Achievements
# -------------------------------------------------------------
@api_router.get("/leaderboard", response_model=List[LeaderboardEntry])
def get_global_leaderboard(limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    """Retrieves server-authoritative leaderboard from SQLite records."""
    raw_leaderboard = get_leaderboard(db, limit=limit)
    return [
        LeaderboardEntry(
            rank=item["rank"],
            player_name=item["player_name"],
            highest_score=item["highest_score"],
            total_games=item["total_games"],
            total_correct=item["total_correct"],
            accuracy=item["accuracy"]
        )
        for item in raw_leaderboard
    ]


@api_router.get("/achievements/{player_name}", response_model=List[AchievementResponse])
def get_player_achievements(player_name: str, db: Session = Depends(get_db)):
    """Fetches all achievements and their unlock status for the given player."""
    return get_player_achievements_list(db, player_name)


@api_router.get("/history/{player_name}")
def get_player_match_history(player_name: str, limit: int = Query(15, ge=1, le=50), db: Session = Depends(get_db)):
    """Fetches recent completed matches for a given player."""
    return get_player_history(db, player_name, limit)


# -------------------------------------------------------------
# Single-Player Game Engine Session Endpoints
# -------------------------------------------------------------
@api_router.post("/game/session")
def start_game_session(
    player_name: str = Query(..., min_length=2),
    mode: str = Query("classic"),
    difficulty: str = Query("easy"),
    seed: Optional[int] = Query(None)
):
    """Initializes a new single-player game session."""
    session = game_engine.create_session(
        player_name=player_name,
        mode=mode,
        difficulty=difficulty,
        seed=seed
    )
    return session.model_dump() if hasattr(session, "model_dump") else session.dict()


@api_router.get("/game/session/{session_id}")
def get_session_state(session_id: str):
    """Retrieves the current state of a single player session."""
    session = game_engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session.model_dump() if hasattr(session, "model_dump") else session.dict()


@api_router.post("/game/session/{session_id}/answer")
def submit_session_answer(
    session_id: str,
    answer: str = Query(...),
    hint_used: bool = Query(False)
):
    """Authoritatively evaluates a single-player answer."""
    result = game_engine.submit_answer(
        session_id=session_id,
        submitted_answer=answer,
        hint_used=hint_used
    )
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to evaluate answer"))
    return result


@api_router.post("/game/match/save", response_model=MatchResponse)
def record_match_result(payload: MatchSaveRequest, db: Session = Depends(get_db)):
    """Persists a finished game match to the database and evaluates achievements."""
    match = save_match_result(
        db=db,
        player_name=payload.player_name,
        mode=payload.mode,
        difficulty=payload.difficulty,
        score=payload.score,
        accuracy=payload.accuracy,
        questions_answered=payload.questions_answered,
        correct_answers=payload.correct_answers,
        levels_completed=payload.levels_completed,
        match_result=payload.match_result,
        duration_seconds=payload.duration_seconds
    )
    return match


# -------------------------------------------------------------
# Multiplayer Room HTTP Management
# -------------------------------------------------------------
@api_router.post("/rooms")
def create_multiplayer_room(payload: RoomCreateRequest):
    """Creates a new synchronized multiplayer room."""
    valid, host = validate_player_name(payload.host_name)
    if not valid:
        raise HTTPException(status_code=400, detail=host)

    room = room_manager.create_room(
        host_name=host,
        difficulty=payload.difficulty,
        total_rounds=payload.total_rounds,
        round_duration=payload.round_duration
    )
    return room.to_client_payload()


@api_router.post("/rooms/join")
def join_multiplayer_room(payload: RoomJoinRequest):
    """Joins an existing multiplayer room."""
    valid_name, clean_name = validate_player_name(payload.player_name)
    if not valid_name:
        raise HTTPException(status_code=400, detail=clean_name)

    valid_code, clean_code = validate_room_code(payload.room_code)
    if not valid_code:
        raise HTTPException(status_code=400, detail=clean_code)

    room = room_manager.get_room(clean_code)
    if not room:
        raise HTTPException(status_code=404, detail="Room code does not exist.")

    ok, msg = room.add_player(clean_name)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)

    return room.to_client_payload()


@api_router.get("/rooms/{room_code}")
def get_room_state(room_code: str, player_name: Optional[str] = None):
    """Fetches sanitized room state for polling clients."""
    room = room_manager.get_room(room_code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found.")

    # Check time deadline
    room.check_deadline_and_resolve()
    return room.to_client_payload(player_name)


# -------------------------------------------------------------
# Educational Algorithm Sandbox
# -------------------------------------------------------------
@api_router.post("/algorithm/evaluate", response_model=AlgorithmEvaluateResponse)
def evaluate_custom_algorithm_sequence(payload: AlgorithmEvaluateRequest):
    """
    Evaluates both algorithm methods side-by-side on any custom input string.
    Generates step-by-step visual trace for academic demonstrations and college presentations.
    """
    valid, seq = validate_sequence_input(payload.sequence)
    if not valid:
        raise HTTPException(status_code=400, detail=seq)

    # Method 1: Frequency dictionary O(n)
    freq_result = first_non_repeating_frequency(
        seq,
        case_sensitive=payload.case_sensitive,
        ignore_spaces=payload.ignore_spaces
    )

    # Method 2: Nested loop O(n^2)
    nested_result = first_non_repeating_nested(
        seq,
        case_sensitive=payload.case_sensitive,
        ignore_spaces=payload.ignore_spaces
    )

    # In-depth breakdown
    breakdown = explain_first_non_repeating(
        seq,
        case_sensitive=payload.case_sensitive,
        ignore_spaces=payload.ignore_spaces
    )

    return AlgorithmEvaluateResponse(
        raw_sequence=breakdown["raw_sequence"],
        normalized_sequence=breakdown["normalized_sequence"],
        result=freq_result,
        frequencies=breakdown["frequencies"],
        distinct_unique_chars=breakdown["distinct_unique_chars"],
        total_unique_count=breakdown["total_unique_count"],
        steps=breakdown["steps"],
        explanation=breakdown["explanation"],
        frequency_method_time_complexity=breakdown["frequency_method_time_complexity"],
        frequency_method_space_complexity=breakdown["frequency_method_space_complexity"],
        nested_method_time_complexity=breakdown["nested_method_time_complexity"],
        nested_method_space_complexity=breakdown["nested_method_space_complexity"],
        both_methods_match=(freq_result == nested_result)
    )
