"""
Unique Character Quest - Core Algorithm Module
-----------------------------------------------
Academic focus: First Non-Repeating Character in a Sequence.

This module provides two independent implementations:
1. Frequency Dictionary Approach: O(n) time complexity, O(k) space complexity.
2. Nested-Loop Approach: O(n^2) worst-case time complexity, O(1) auxiliary space.

Both functions follow identical input normalization rules:
- Matching is case-sensitive by default (can be toggled).
- Spaces are ignored by default in standard gameplay unless explicitly configured.
- Original character sequence order is strictly preserved.
- Returns the first unique character (str of length 1) or None if all repeat.
"""

from typing import Optional, Dict, Any, List, Tuple
from collections import Counter


def normalize_sequence(sequence: str, case_sensitive: bool = True, ignore_spaces: bool = True) -> str:
    """
    Normalizes an input sequence according to game rules.
    
    Args:
        sequence: The raw input string.
        case_sensitive: Whether 'A' and 'a' should be treated as distinct characters.
        ignore_spaces: Whether whitespace characters should be omitted from candidate analysis.
        
    Returns:
        The filtered sequence as a string.
    """
    if sequence is None:
        return ""
    result = sequence
    if not case_sensitive:
        result = result.lower()
    if ignore_spaces:
        result = "".join(ch for ch in result if not ch.isspace())
    return result


def first_non_repeating_frequency(
    sequence: str,
    case_sensitive: bool = True,
    ignore_spaces: bool = True
) -> Optional[str]:
    """
    Method 1: Frequency Dictionary Approach (Hash Map / Counter)
    
    Algorithm:
    1. Clean / normalize the sequence based on rules.
    2. Traverse the sequence once to count the frequency of each character (O(n)).
    3. Traverse the sequence a second time in original left-to-right order (O(n)).
    4. Return the first character whose frequency count is exactly 1.
    5. If no character has a count of 1, return None.
    
    Complexity Analysis:
    - Time Complexity: O(n)
      Pass 1 takes n iterations to build frequencies.
      Pass 2 takes up to n iterations to locate the first count == 1.
      Total time = O(2n) = O(n).
    - Space Complexity: O(k), where k <= n is the number of distinct characters
      stored in the hash map / frequency dictionary. In ASCII/Unicode subsets, k <= 256 or k <= charset size.
    """
    normalized = normalize_sequence(sequence, case_sensitive, ignore_spaces)
    if not normalized:
        return None

    # Step 1: Count frequency of every character (preserves count)
    counts: Dict[str, int] = {}
    for ch in normalized:
        counts[ch] = counts.get(ch, 0) + 1

    # Step 2: Second pass in original order to find the first character with frequency 1
    for ch in normalized:
        if counts[ch] == 1:
            return ch

    return None


def first_non_repeating_nested(
    sequence: str,
    case_sensitive: bool = True,
    ignore_spaces: bool = True
) -> Optional[str]:
    """
    Method 2: Nested-Loop Approach (Brute Force / Naive)
    
    Algorithm:
    1. Clean / normalize the sequence.
    2. Outer loop: Iterate over each index i from 0 to len-1.
    3. Inner loop: For candidate sequence[i], scan the entire sequence from index 0 to len-1.
    4. Count how many times sequence[i] occurs.
    5. If the total count is exactly 1, return sequence[i] immediately (first encountered).
    6. If the outer loop finishes without finding any count of 1, return None.
    
    Complexity Analysis:
    - Time Complexity: O(n^2) worst-case
      For a sequence of length n, the outer loop runs n times.
      The inner loop scans all n characters for each outer iteration.
      Total operations = n * n = O(n^2).
    - Space Complexity: O(1) auxiliary space (excluding input storage).
      Only indices and scalar counters are maintained.
    """
    normalized = normalize_sequence(sequence, case_sensitive, ignore_spaces)
    n = len(normalized)
    if n == 0:
        return None

    for i in range(n):
        candidate = normalized[i]
        count = 0
        for j in range(n):
            if normalized[j] == candidate:
                count += 1
                if count > 1:
                    # Early termination optimization for inner loop
                    break
        if count == 1:
            return candidate

    return None


def explain_first_non_repeating(
    sequence: str,
    case_sensitive: bool = True,
    ignore_spaces: bool = True
) -> Dict[str, Any]:
    """
    Generates educational diagnostic steps, frequency breakdown, and algorithmic justification.
    Used for in-game hint explanations, post-answer review, and pedagogical visualizations.
    """
    normalized = normalize_sequence(sequence, case_sensitive, ignore_spaces)
    
    # Frequency counts
    counts: Dict[str, int] = {}
    for ch in normalized:
        counts[ch] = counts.get(ch, 0) + 1
        
    unique_candidates = [ch for ch in normalized if counts[ch] == 1]
    # Remove duplicates from candidates while preserving order
    seen = set()
    distinct_uniques: List[str] = []
    for ch in unique_candidates:
        if ch not in seen:
            seen.add(ch)
            distinct_uniques.append(ch)

    first_unique = distinct_uniques[0] if distinct_uniques else None
    
    # Step-by-step trace
    steps: List[Dict[str, Any]] = []
    for idx, ch in enumerate(normalized):
        steps.append({
            "index": idx,
            "character": ch,
            "frequency": counts[ch],
            "is_unique": (counts[ch] == 1),
            "is_first_unique": (ch == first_unique)
        })

    if first_unique is not None:
        first_index = normalized.find(first_unique)
        explanation = (
            f"The first non-repeating character is '{first_unique}' at index {first_index}. "
            f"It occurs exactly 1 time in '{normalized}'. "
        )
        if len(distinct_uniques) > 1:
            other_uniques = ", ".join(f"'{c}'" for c in distinct_uniques[1:])
            explanation += (
                f"Other unique characters exist ({other_uniques}), but '{first_unique}' "
                f"appears first in the sequence order."
            )
    else:
        explanation = (
            f"No non-repeating character exists in '{normalized}'. "
            f"Every single character appears 2 or more times. The correct answer is 'None'."
        )

    return {
        "raw_sequence": sequence,
        "normalized_sequence": normalized,
        "result": first_unique,
        "frequencies": counts,
        "distinct_unique_chars": distinct_uniques,
        "total_unique_count": len(distinct_uniques),
        "steps": steps,
        "explanation": explanation,
        "frequency_method_time_complexity": "O(n)",
        "frequency_method_space_complexity": f"O({len(counts)}) distinct keys",
        "nested_method_time_complexity": "O(n^2)",
        "nested_method_space_complexity": "O(1) auxiliary"
    }
