"""
Unit Tests for First Non-Repeating Character Algorithms
-------------------------------------------------------
Verifies correctness, boundary edge cases, and equivalence between
Method 1 (Frequency Dictionary) and Method 2 (Nested Loops).
"""

import pytest
from backend.game.algorithms import (
    first_non_repeating_frequency,
    first_non_repeating_nested,
    explain_first_non_repeating,
    normalize_sequence
)


class TestAlgorithms:
    """Core academic verification test suite."""

    KNOWN_TEST_CASES = [
        ("aabbcd", "c"),
        ("swiss", "w"),
        ("aabb", None),
        ("x", "x"),
        ("aabbccdef", "d"),
        ("programming", "p"),
        ("racecar", "e"),
        ("teammate", None),
        ("success", "u"),
        ("1122334A55", "4"),
        ("!@#$!@#", "$")
    ]

    @pytest.mark.parametrize("sequence,expected", KNOWN_TEST_CASES)
    def test_frequency_method_known_cases(self, sequence, expected):
        """Method 1: Frequency dictionary must produce exact expected outputs."""
        result = first_non_repeating_frequency(sequence)
        assert result == expected, f"Failed for '{sequence}': got '{result}', expected '{expected}'"

    @pytest.mark.parametrize("sequence,expected", KNOWN_TEST_CASES)
    def test_nested_method_known_cases(self, sequence, expected):
        """Method 2: Nested loop brute force must produce exact expected outputs."""
        result = first_non_repeating_nested(sequence)
        assert result == expected, f"Failed for '{sequence}': got '{result}', expected '{expected}'"

    def test_both_algorithms_equivalent(self):
        """Both algorithms must yield 100% identical results across arbitrary strings."""
        test_strings = [
            "",
            "a",
            "aa",
            "ab",
            "aba",
            "abab",
            "abcdef",
            "fedcba",
            "The quick brown fox jumps over the lazy dog",
            "1234567890123456789",
            "!!@@##$$%%^^&&**()_+",
            "RepeatedRepeated",
            "MixedCaseAndNumbers123321A",
            "   sp a c e s   "
        ]
        for s in test_strings:
            res_freq = first_non_repeating_frequency(s)
            res_nested = first_non_repeating_nested(s)
            assert res_freq == res_nested, f"Mismatch on '{s}': freq='{res_freq}' vs nested='{res_nested}'"

    def test_empty_sequence(self):
        """Empty or None sequences must safely return None."""
        assert first_non_repeating_frequency("") is None
        assert first_non_repeating_nested("") is None
        assert first_non_repeating_frequency(None) is None
        assert first_non_repeating_nested(None) is None

    def test_single_character(self):
        """A single character is unconditionally non-repeating."""
        assert first_non_repeating_frequency("z") == "z"
        assert first_non_repeating_nested("z") == "z"

    def test_case_sensitivity(self):
        """'A' and 'a' must be distinguished when case_sensitive=True, and merged when False."""
        seq = "AaBb"
        # Case sensitive: 'A' occurs once, 'a' occurs once -> first is 'A'
        assert first_non_repeating_frequency(seq, case_sensitive=True) == "A"
        # Case insensitive: 'a' occurs twice ('A' and 'a'), 'b' occurs twice -> None
        assert first_non_repeating_frequency(seq, case_sensitive=False) is None

    def test_space_handling(self):
        """Spaces are ignored by default in standard gameplay."""
        seq = "  a  a  b  "
        assert first_non_repeating_frequency(seq, ignore_spaces=True) == "b"

    def test_explain_function(self):
        """Educational explanation dictionary must include frequencies and step-by-step breakdown."""
        data = explain_first_non_repeating("aabbcd")
        assert data["result"] == "c"
        assert data["frequencies"]["a"] == 2
        assert data["frequencies"]["b"] == 2
        assert data["frequencies"]["c"] == 1
        assert data["frequencies"]["d"] == 1
        assert "c" in data["distinct_unique_chars"]
        assert len(data["steps"]) == 6
