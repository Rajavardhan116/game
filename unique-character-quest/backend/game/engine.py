"""
Game Engine Module for Unique Character Quest
---------------------------------------------
Controls single-player and match state transitions, level progressions,
question flows, and win/loss states for Classic, Speed, and Puzzle Challenge modes.
"""

import time
import uuid
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

from .questions import Question, generate_question
from .scoring import evaluate_answer_submission, ScoreEventResult


class GameRoundHistory(BaseModel):
    question_index: int
    sequence: str
    submitted_answer: str
    correct_answer: str
    is_correct: bool
    points_earned: int
    speed_bonus: int
    time_taken: float
    explanation: str


class GameSession(BaseModel):
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    player_name: str
    mode: str = "classic"  # classic, speed, puzzle
    difficulty: str = "easy"
    score: int = 0
    lives: int = 3
    max_lives: int = 3
    streak: int = 0
    max_streak: int = 0
    current_question_index: int = 1
    total_questions: int = 5
    current_question: Optional[Question] = None
    question_start_time: float = Field(default_factory=time.time)
    history: List[GameRoundHistory] = []
    is_game_over: bool = False
    is_completed: bool = False
    hints_used: int = 0
    created_at: float = Field(default_factory=time.time)
    seed: Optional[int] = None


class GameEngine:
    """
    State machine for executing game sessions with authoritative rules.
    """

    MODE_TOTAL_QUESTIONS = {
        "classic": 5,
        "speed": 8,
        "puzzle": 6
    }

    def __init__(self):
        self.active_sessions: Dict[str, GameSession] = {}

    def create_session(
        self,
        player_name: str,
        mode: str = "classic",
        difficulty: str = "easy",
        seed: Optional[int] = None
    ) -> GameSession:
        """
        Initializes and registers a brand new game session.
        """
        total_q = self.MODE_TOTAL_QUESTIONS.get(mode.lower(), 5)
        lives = 3
        if mode.lower() == "speed":
            lives = 2
        elif mode.lower() == "puzzle":
            lives = 3

        session = GameSession(
            player_name=player_name,
            mode=mode.lower(),
            difficulty=difficulty.lower(),
            lives=lives,
            max_lives=lives,
            total_questions=total_q,
            seed=seed
        )

        # Generate first question
        q = generate_question(
            difficulty=session.difficulty,
            seed=session.seed,
            question_index=1,
            force_curated=(session.mode == "puzzle")
        )
        session.current_question = q
        session.question_start_time = time.time()
        self.active_sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[GameSession]:
        return self.active_sessions.get(session_id)

    def submit_answer(
        self,
        session_id: str,
        submitted_answer: str,
        hint_used: bool = False
    ) -> Dict[str, Any]:
        """
        Authoritatively evaluates an answer submitted by a player.
        Updates score, streak, lives, and transitions to the next round or end screen.
        """
        session = self.get_session(session_id)
        if not session:
            return {"error": "Session not found", "success": False}

        if session.is_game_over or session.is_completed:
            return {"error": "Game is already over", "success": False}

        q = session.current_question
        if not q:
            return {"error": "No active question", "success": False}

        time_taken = time.time() - session.question_start_time
        
        # In speed mode, time limit is enforced strictly
        eval_res: ScoreEventResult = evaluate_answer_submission(
            submitted_answer=submitted_answer,
            correct_answer=q.correct_answer,
            time_taken=time_taken,
            time_limit=q.time_limit_seconds,
            current_lives=session.lives,
            current_streak=session.streak,
            base_points=q.base_points,
            hint_used=hint_used
        )

        if hint_used:
            session.hints_used += 1

        # Apply state updates
        session.score += eval_res.total_delta
        session.lives = eval_res.lives_remaining
        session.streak = eval_res.new_streak
        if session.streak > session.max_streak:
            session.max_streak = session.streak

        # Log history
        round_history = GameRoundHistory(
            question_index=session.current_question_index,
            sequence=q.sequence,
            submitted_answer=submitted_answer,
            correct_answer=q.correct_answer,
            is_correct=eval_res.is_correct,
            points_earned=eval_res.total_delta,
            speed_bonus=eval_res.speed_bonus,
            time_taken=round(time_taken, 2),
            explanation=q.explanation or eval_res.explanation
        )
        session.history.append(round_history)

        # Check termination or advance
        if eval_res.is_game_over:
            session.is_game_over = True
            session.current_question = None
        else:
            if session.current_question_index >= session.total_questions:
                session.is_completed = True
                session.current_question = None
            else:
                # Advance to next level / question
                session.current_question_index += 1
                
                # In classic mode, automatically ramp difficulty
                next_diff = session.difficulty
                if session.mode == "classic":
                    progression = ["easy", "easy", "medium", "hard", "expert"]
                    idx = min(len(progression) - 1, session.current_question_index - 1)
                    next_diff = progression[idx]

                next_seed = (session.seed + session.current_question_index * 17) if session.seed else None
                session.current_question = generate_question(
                    difficulty=next_diff,
                    seed=next_seed,
                    question_index=session.current_question_index,
                    force_curated=(session.mode == "puzzle")
                )
                session.question_start_time = time.time()

        def to_dict(obj):
            return obj.model_dump() if hasattr(obj, "model_dump") else obj.dict()

        return {
            "success": True,
            "evaluation": to_dict(eval_res),
            "session": to_dict(session),
            "last_round": to_dict(round_history)
        }
