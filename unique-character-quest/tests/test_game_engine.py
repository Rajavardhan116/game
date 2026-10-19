"""
Unit Tests for Game Engine State Machine
----------------------------------------
Tests single-player session creation, round progression, and game completion.
"""

import pytest
from backend.game.engine import GameEngine


class TestGameEngine:
    def test_session_creation(self):
        """GameEngine must properly initialize sessions with configured questions and lives."""
        engine = GameEngine()
        session = engine.create_session(player_name="Alice", mode="classic", difficulty="easy")
        assert session.player_name == "Alice"
        assert session.mode == "classic"
        assert session.lives == 3
        assert session.score == 0
        assert session.current_question is not None
        assert session.current_question_index == 1

    def test_correct_answer_advancement(self):
        """Submitting a correct answer advances the question index and increments score."""
        engine = GameEngine()
        session = engine.create_session(player_name="Bob", mode="classic", difficulty="easy", seed=10)
        q1_ans = session.current_question.correct_answer

        res = engine.submit_answer(session.session_id, q1_ans)
        assert res["success"] is True
        assert session.score > 0
        assert session.current_question_index == 2
        assert len(session.history) == 1

    def test_game_over_on_depleted_lives(self):
        """Depleting all lives terminates the game session."""
        engine = GameEngine()
        session = engine.create_session(player_name="Charlie", mode="speed", difficulty="easy", seed=10)
        session.lives = 1  # Force 1 life left

        res = engine.submit_answer(session.session_id, "WRONG_ANSWER_GUARANTEED")
        assert res["success"] is True
        assert session.is_game_over is True
        assert session.lives == 0
        assert session.current_question is None
