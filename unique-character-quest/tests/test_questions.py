"""
Unit Tests for Question Generation and Difficulty Scaling
---------------------------------------------------------
Validates deterministic question generation, options coverage, and constraints.
"""

import pytest
from backend.game.questions import generate_question, DIFFICULTY_CONFIGS
from backend.game.algorithms import first_non_repeating_frequency


class TestQuestions:
    def test_options_contain_correct_answer(self):
        """Authoritative invariant: correct answer MUST be present in generated options."""
        for diff in ["easy", "medium", "hard", "expert"]:
            for q_idx in range(1, 10):
                q = generate_question(difficulty=diff, question_index=q_idx, seed=q_idx * 100)
                assert q.correct_answer in q.options, f"Answer {q.correct_answer} missing from {q.options} in {diff}"

    def test_authoritative_correctness(self):
        """Computed answer must match the algorithm's output on the sequence."""
        for diff in ["easy", "medium", "hard", "expert"]:
            q = generate_question(difficulty=diff, question_index=1, seed=42)
            expected = first_non_repeating_frequency(q.sequence)
            expected_str = expected if expected is not None else "None"
            assert q.correct_answer == expected_str

    def test_deterministic_generation_with_seed(self):
        """Supplying the same seed must produce the exact identical question."""
        q1 = generate_question(difficulty="hard", seed=999, question_index=3)
        q2 = generate_question(difficulty="hard", seed=999, question_index=3)
        assert q1.sequence == q2.sequence
        assert q1.correct_answer == q2.correct_answer
        assert q1.options == q2.options

    def test_difficulty_parameters(self):
        """Difficulty constraints (time limits, base rewards) must match configuration."""
        for diff, cfg in DIFFICULTY_CONFIGS.items():
            q = generate_question(difficulty=diff, seed=123)
            assert q.time_limit_seconds == cfg["time_limit"]
            assert q.base_points == cfg["base_points"]
