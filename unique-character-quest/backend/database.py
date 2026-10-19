"""
Database Persistence Layer for Unique Character Quest
------------------------------------------------------
Configures SQLite engine, creates tables idempotently,
seeds standard academic achievements, and exposes atomic transaction helpers.
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, desc, func
from sqlalchemy.orm import sessionmaker, Session

from .config import settings
from .models import Base, Player, MatchResult, Achievement, PlayerAchievement


# SQLite connection string
DATABASE_URL = f"sqlite:///{settings.DATABASE_PATH}"

# Connect args needed for SQLite thread concurrency
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


STANDARD_ACHIEVEMENTS = [
    {
        "code": "first_victory",
        "title": "First Victory",
        "description": "Complete your first match in any game mode.",
        "icon": "🏅",
        "points": 50
    },
    {
        "code": "speed_solver",
        "title": "Lightning Reflexes",
        "description": "Answer correctly in less than 3 seconds.",
        "icon": "⚡",
        "points": 100
    },
    {
        "code": "flawless_run",
        "title": "Flawless Intuition",
        "description": "Finish a match without losing a single life.",
        "icon": "💎",
        "points": 150
    },
    {
        "code": "ten_correct",
        "title": "Deca Master",
        "description": "Accumulate 10 or more correct answers in your career.",
        "icon": "🎯",
        "points": 100
    },
    {
        "code": "no_hints",
        "title": "Pure Logic",
        "description": "Complete a full match without requesting any hints.",
        "icon": "🧠",
        "points": 125
    },
    {
        "code": "puzzle_master",
        "title": "Sequence Detective",
        "description": "Successfully conquer the Puzzle Challenge mode.",
        "icon": "🧩",
        "points": 200
    },
    {
        "code": "multiplayer_champ",
        "title": "Multiplayer Champion",
        "description": "Win an online multiplayer battle against other players.",
        "icon": "👑",
        "points": 250
    },
    {
        "code": "five_games",
        "title": "Veteran Solver",
        "description": "Complete at least 5 games in Unique Character Quest.",
        "icon": "🌟",
        "points": 150
    }
]


def init_db():
    """
    Idempotent initialization: creates database schema without wiping existing records.
    Populates base achievement definitions if they do not already exist.
    """
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        for ach in STANDARD_ACHIEVEMENTS:
            existing = db.query(Achievement).filter(Achievement.code == ach["code"]).first()
            if not existing:
                new_ach = Achievement(
                    code=ach["code"],
                    title=ach["title"],
                    description=ach["description"],
                    icon=ach["icon"],
                    points=ach["points"]
                )
                db.add(new_ach)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_db():
    """FastAPI dependency for yielding database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Database helper operations
def get_or_create_player(db: Session, player_name: str) -> Player:
    """Retrieves an existing player or creates an initial player record."""
    clean_name = player_name.strip()
    player = db.query(Player).filter(Player.player_name == clean_name).first()
    if not player:
        player = Player(
            id=str(uuid.uuid4()),
            player_name=clean_name,
            total_games=0,
            total_score=0,
            highest_score=0,
            total_correct=0,
            total_questions=0,
            created_at=datetime.utcnow(),
            last_active=datetime.utcnow()
        )
        db.add(player)
        db.commit()
        db.refresh(player)
    else:
        player.last_active = datetime.utcnow()
        db.commit()
    return player


def save_match_result(
    db: Session,
    player_name: str,
    mode: str,
    difficulty: str,
    score: int,
    accuracy: float,
    questions_answered: int,
    correct_answers: int,
    levels_completed: int,
    match_result: str,
    duration_seconds: float = 0.0,
    hints_used: int = 0
) -> MatchResult:
    """
    Saves a completed match record and atomically updates player career statistics.
    Checks and triggers any earned achievements.
    """
    player = get_or_create_player(db, player_name)

    # 1. Create match result record
    match_id = str(uuid.uuid4())
    match = MatchResult(
        id=match_id,
        player_name=player.player_name,
        mode=mode,
        difficulty=difficulty,
        score=score,
        accuracy=round(accuracy, 2),
        questions_answered=questions_answered,
        correct_answers=correct_answers,
        levels_completed=levels_completed,
        match_result=match_result,
        duration_seconds=duration_seconds,
        completed_at=datetime.utcnow()
    )
    db.add(match)

    # 2. Update player career aggregates
    player.total_games += 1
    player.total_score += score
    if score > player.highest_score:
        player.highest_score = score
    player.total_correct += correct_answers
    player.total_questions += questions_answered
    player.last_active = datetime.utcnow()

    db.commit()
    db.refresh(match)

    # 3. Evaluate career achievements
    check_and_award_achievements(
        db,
        player=player,
        match=match,
        hints_used=hints_used
    )

    return match


def check_and_award_achievements(
    db: Session,
    player: Player,
    match: MatchResult,
    hints_used: int = 0
) -> List[str]:
    """
    Verifies conditions for all available achievements and unlocks new ones.
    Returns list of newly awarded achievement codes.
    """
    newly_awarded = []

    def award(code: str):
        existing = db.query(PlayerAchievement).filter(
            PlayerAchievement.player_name == player.player_name,
            PlayerAchievement.achievement_code == code
        ).first()
        if not existing:
            pa = PlayerAchievement(
                id=str(uuid.uuid4()),
                player_name=player.player_name,
                achievement_code=code,
                unlocked_at=datetime.utcnow()
            )
            db.add(pa)
            newly_awarded.append(code)

    # First Victory
    if player.total_games >= 1:
        award("first_victory")

    # Five Games
    if player.total_games >= 5:
        award("five_games")

    # Ten Correct Answers
    if player.total_correct >= 10:
        award("ten_correct")

    # Flawless Run
    if match.match_result in ["WON", "COMPLETED"] and match.questions_answered > 0 and match.correct_answers == match.questions_answered:
        award("flawless_run")

    # No Hints Used
    if match.match_result in ["WON", "COMPLETED"] and hints_used == 0 and match.questions_answered >= 3:
        award("no_hints")

    # Puzzle Master
    if match.mode == "puzzle" and match.match_result in ["WON", "COMPLETED"]:
        award("puzzle_master")

    # Multiplayer Champion
    if match.mode == "multiplayer" and match.match_result == "WON":
        award("multiplayer_champ")

    if newly_awarded:
        db.commit()

    return newly_awarded


def get_leaderboard(db: Session, limit: int = 20) -> List[Dict[str, Any]]:
    """Fetches high score leaderboard computed directly from persistent database."""
    players = (
        db.query(Player)
        .filter(Player.total_games > 0)
        .order_by(desc(Player.highest_score), desc(Player.total_score))
        .limit(limit)
        .all()
    )
    result = []
    for rank, p in enumerate(players, start=1):
        accuracy = round((p.total_correct / p.total_questions * 100), 1) if p.total_questions > 0 else 0.0
        result.append({
            "rank": rank,
            "player_name": p.player_name,
            "highest_score": p.highest_score,
            "total_score": p.total_score,
            "total_games": p.total_games,
            "total_correct": p.total_correct,
            "accuracy": accuracy,
            "last_active": p.last_active.strftime("%Y-%m-%d %H:%M") if p.last_active else "N/A"
        })
    return result


def get_player_achievements_list(db: Session, player_name: str) -> List[Dict[str, Any]]:
    """Returns all available achievements with unlocked status for a given player."""
    all_achievements = db.query(Achievement).all()
    unlocked_map = {
        pa.achievement_code: pa.unlocked_at
        for pa in db.query(PlayerAchievement).filter(PlayerAchievement.player_name == player_name).all()
    }

    results = []
    for ach in all_achievements:
        is_unlocked = ach.code in unlocked_map
        results.append({
            "code": ach.code,
            "title": ach.title,
            "description": ach.description,
            "icon": ach.icon,
            "points": ach.points,
            "unlocked": is_unlocked,
            "unlocked_at": unlocked_map[ach.code].strftime("%Y-%m-%d %H:%M") if is_unlocked else None
        })
    return results


def get_player_history(db: Session, player_name: str, limit: int = 15) -> List[Dict[str, Any]]:
    """Returns recent match history for a given player."""
    matches = (
        db.query(MatchResult)
        .filter(MatchResult.player_name == player_name)
        .order_by(desc(MatchResult.completed_at))
        .limit(limit)
        .all()
    )
    return [
        {
            "id": m.id,
            "mode": m.mode,
            "difficulty": m.difficulty,
            "score": m.score,
            "accuracy": m.accuracy,
            "questions_answered": m.questions_answered,
            "correct_answers": m.correct_answers,
            "match_result": m.match_result,
            "duration_seconds": round(m.duration_seconds, 1),
            "completed_at": m.completed_at.strftime("%Y-%m-%d %H:%M")
        }
        for m in matches
    ]
