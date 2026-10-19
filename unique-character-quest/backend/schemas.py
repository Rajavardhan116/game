"""
Pydantic Schemas for API Serialization & Validation
----------------------------------------------------
Defines request and response structures for HTTP endpoints and WebSockets.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# Player & Session Schemas
class PlayerCreateRequest(BaseModel):
    player_name: str = Field(..., min_length=2, max_length=20)


class PlayerResponse(BaseModel):
    id: str
    player_name: str
    total_games: int
    total_score: int
    highest_score: int
    total_correct: int
    total_questions: int
    accuracy_percentage: float
    created_at: datetime
    last_active: datetime

    model_config = {"from_attributes": True}


# Match Submission Schemas
class MatchSaveRequest(BaseModel):
    player_name: str
    mode: str
    difficulty: str
    score: int
    accuracy: float
    questions_answered: int
    correct_answers: int
    levels_completed: int
    match_result: str  # WON, LOST, COMPLETED
    duration_seconds: float = 0.0


class MatchResponse(BaseModel):
    id: str
    player_name: str
    mode: str
    difficulty: str
    score: int
    accuracy: float
    questions_answered: int
    correct_answers: int
    levels_completed: int
    match_result: str
    duration_seconds: float
    completed_at: datetime

    model_config = {"from_attributes": True}


# Achievement Schemas
class AchievementResponse(BaseModel):
    code: str
    title: str
    description: str
    icon: str
    points: int
    unlocked: bool = False
    unlocked_at: Optional[datetime] = None


class LeaderboardEntry(BaseModel):
    rank: int
    player_name: str
    highest_score: int
    total_games: int
    total_correct: int
    accuracy: float


# Educational Algorithm Sandbox Schemas
class AlgorithmEvaluateRequest(BaseModel):
    sequence: str = Field(..., max_length=200)
    case_sensitive: bool = True
    ignore_spaces: bool = True


class AlgorithmStep(BaseModel):
    index: int
    character: str
    frequency: int
    is_unique: bool
    is_first_unique: bool


class AlgorithmEvaluateResponse(BaseModel):
    raw_sequence: str
    normalized_sequence: str
    result: Optional[str]
    frequencies: Dict[str, int]
    distinct_unique_chars: List[str]
    total_unique_count: int
    steps: List[AlgorithmStep]
    explanation: str
    frequency_method_time_complexity: str
    frequency_method_space_complexity: str
    nested_method_time_complexity: str
    nested_method_space_complexity: str
    both_methods_match: bool


# Multiplayer Schemas
class RoomCreateRequest(BaseModel):
    host_name: str = Field(..., min_length=2, max_length=20)
    difficulty: str = "medium"
    total_rounds: int = 5
    round_duration: int = 15


class RoomJoinRequest(BaseModel):
    room_code: str = Field(..., min_length=4, max_length=8)
    player_name: str = Field(..., min_length=2, max_length=20)


class RoomPlayerInfo(BaseModel):
    player_name: str
    is_host: bool
    is_ready: bool
    score: int
    lives: int
    has_submitted: bool
    last_answer: Optional[str] = None
    connected: bool = True


class RoomStateResponse(BaseModel):
    room_code: str
    host_name: str
    status: str  # waiting, in_round, round_recap, match_finished
    difficulty: str
    current_round: int
    total_rounds: int
    round_duration: int
    deadline: Optional[float] = None
    seconds_remaining: Optional[float] = None
    players: List[RoomPlayerInfo]
    current_sequence: Optional[str] = None
    options: Optional[List[str]] = None
    winner: Optional[str] = None
