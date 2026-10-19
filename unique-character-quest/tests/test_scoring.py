"""
Unit Tests for Scoring Rules, Speed Bonuses, and Lives
------------------------------------------------------
Validates authoritative scoring, streak escalation, and life deduction boundaries.
"""

import pytest
from backend.game.scoring import evaluate_answer_submission, calculate_speed_bonus


class TestScoring:
    def test_correct_answer_awarding(self):
        """Correct answers must award base points and increment streak."""
        res = evaluate_answer_submission(
            submitted_answer="c",
            correct_answer="c",
            time_taken=2.0,
            time_limit=15.0,
            current_lives=3,
            current_streak=0,
            base_points=100
        )
        assert res.is_correct is True
        assert res.points_awarded == 100
        assert res.speed_bonus > 0
        assert res.lives_remaining == 3
        assert res.new_streak == 1
        assert res.is_game_over is False

    def test_speed_bonus_calculation(self):
        """Faster responses must receive greater speed bonuses."""
        b_fast = calculate_speed_bonus(base_points=100, time_limit=10.0, time_taken=1.0)
        b_slow = calculate_speed_bonus(base_points=100, time_limit=10.0, time_taken=9.0)
        assert b_fast > b_slow
        assert calculate_speed_bonus(base_points=100, time_limit=10.0, time_taken=12.0) == 0

    def test_incorrect_answer_deducts_life(self):
        """Incorrect answers deduct 1 life, reset streak, and award 0 points."""
        res = evaluate_answer_submission(
            submitted_answer="x",
            correct_answer="c",
            time_taken=2.0,
            time_limit=15.0,
            current_lives=3,
            current_streak=4,
            base_points=100
        )
        assert res.is_correct is False
        assert res.total_delta == 0
        assert res.lives_remaining == 2
        assert res.new_streak == 0
        assert res.is_game_over is False

    def test_timeout_deducts_life(self):
        """Submissions beyond time limit are marked timed out and deduct 1 life."""
        res = evaluate_answer_submission(
            submitted_answer="c",
            correct_answer="c",
            time_taken=16.0,
            time_limit=15.0,
            current_lives=2,
            current_streak=1
        )
        assert res.is_correct is False
        assert res.lives_remaining == 1

    def test_lives_never_go_negative(self):
        """When lives reach 0, lives_remaining is 0 and is_game_over is True."""
        res = evaluate_answer_submission(
            submitted_answer="wrong",
            correct_answer="correct",
            time_taken=1.0,
            time_limit=10.0,
            current_lives=1,
            current_streak=0
        )
        assert res.lives_remaining == 0
        assert res.is_game_over is True
