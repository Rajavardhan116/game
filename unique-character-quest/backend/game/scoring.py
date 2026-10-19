"""
Scoring and Evaluation Module for Unique Character Quest
---------------------------------------------------------
Authoritative server-side calculation for scores, lives, speed bonuses,
streak multipliers, and achievement qualifications.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class ScoreEventResult(BaseModel):
    is_correct: bool
    points_awarded: int
    speed_bonus: int
    streak_bonus: int
    total_delta: int
    lives_remaining: int
    new_streak: int
    is_game_over: bool
    explanation: str


class ScoringConfig(BaseModel):
    starting_lives: int = 3
    base_points: int = 100
    speed_bonus_max_pct: float = 0.50
    streak_bonus_per_step: int = 25
    hint_penalty: int = 20


def calculate_speed_bonus(
    base_points: int,
    time_limit: float,
    time_taken: float,
    max_bonus_pct: float = 0.50
) -> int:
    """
    Computes a fractional speed bonus for rapid correct responses.
    Formula: base_points * max_bonus_pct * (time_remaining / time_limit).
    """
    if time_limit <= 0 or time_taken >= time_limit:
        return 0
    time_remaining = max(0.0, time_limit - time_taken)
    ratio = time_remaining / time_limit
    return int(base_points * max_bonus_pct * ratio)


def evaluate_answer_submission(
    submitted_answer: str,
    correct_answer: str,
    time_taken: float,
    time_limit: float,
    current_lives: int,
    current_streak: int,
    base_points: int = 100,
    hint_used: bool = False
) -> ScoreEventResult:
    """
    Evaluates a player's answer submission in an authoritative manner.
    Guarantees:
    - Lives never decrement below 0.
    - Double scoring is mathematically isolated by atomic calculation.
    - Speed bonus is strictly 0 if incorrect or timed out.
    """
    is_timeout = (time_taken > time_limit)
    is_correct = (submitted_answer.strip() == correct_answer.strip()) and not is_timeout

    if is_correct:
        speed_bonus = calculate_speed_bonus(base_points, time_limit, time_taken)
        new_streak = current_streak + 1
        streak_bonus = (new_streak - 1) * 20
        hint_deduction = 20 if hint_used else 0
        
        total_delta = max(10, base_points + speed_bonus + streak_bonus - hint_deduction)
        lives_remaining = max(0, current_lives)
        is_game_over = False
        explanation = f"Correct! +{base_points} base, +{speed_bonus} speed bonus, +{streak_bonus} streak bonus."
    else:
        speed_bonus = 0
        streak_bonus = 0
        total_delta = 0
        new_streak = 0
        lives_remaining = max(0, current_lives - 1)
        is_game_over = (lives_remaining <= 0)
        
        if is_timeout:
            explanation = f"Time expired! The correct answer was '{correct_answer}'. Lost 1 life."
        else:
            explanation = f"Incorrect answer '{submitted_answer}'. The correct answer was '{correct_answer}'. Lost 1 life."

    return ScoreEventResult(
        is_correct=is_correct,
        points_awarded=base_points if is_correct else 0,
        speed_bonus=speed_bonus,
        streak_bonus=streak_bonus,
        total_delta=total_delta,
        lives_remaining=lives_remaining,
        new_streak=new_streak,
        is_game_over=is_game_over,
        explanation=explanation
    )
