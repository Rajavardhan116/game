"""
Question Generator Module for Unique Character Quest
----------------------------------------------------
Generates balanced, deterministic (when seeded), and pedagogically structured 
character sequence puzzles across 4 difficulty levels: Easy, Medium, Hard, and Expert.

Features:
- Guarantees the correct answer is computed by the authoritative algorithm.
- Produces meaningful distractor options (including 'None' and secondary unique characters).
- Includes preset curated edge cases (e.g., 'swiss', 'aabbcd', 'aabb', 'programming', 'x').
- Supports deterministic seed-based generation for automated testing and multiplayer sync.
"""

import random
import string
from typing import List, Optional, Dict, Any, Tuple
from pydantic import BaseModel, Field

from .algorithms import first_non_repeating_frequency, explain_first_non_repeating


class Question(BaseModel):
    id: str
    sequence: str
    difficulty: str
    options: List[str]
    correct_answer: str
    time_limit_seconds: int
    base_points: int
    hint: str
    explanation: Optional[str] = None
    category: str = "standard"


CURATED_PUZZLES = {
    "easy": [
        {"seq": "aabbcd", "hint": "Look past 'a' and 'b' which both occur in pairs."},
        {"seq": "swiss", "hint": "'s' appears 3 times. What is the very first letter that only appears once?"},
        {"seq": "hello", "hint": "Count the 'l's carefully. What about the beginning of the word?"},
        {"seq": "letter", "hint": "Both 'e' and 't' repeat twice. Check the remaining letters in order."},
        {"seq": "apple", "hint": "'p' is duplicated. Check from left to right."},
        {"seq": "speed", "hint": "Double 'e' repeats. What unique letter comes first?"},
    ],
    "medium": [
        {"seq": "programming", "hint": "'r', 'g', and 'm' repeat. Scan from left to right for the first singleton."},
        {"seq": "character", "hint": "'c', 'a', and 'r' repeat. Notice which unique letter appears earliest."},
        {"seq": "racecar", "hint": "Is 'e' the only letter without a twin?"},
        {"seq": "teammate", "hint": "Look closely at 't', 'e', 'a', and 'm'."},
        {"seq": "success", "hint": "'s' and 'c' repeat. Which unique letter comes first?"},
        {"seq": "repetition", "hint": "'e', 't', and 'i' appear multiple times."},
    ],
    "hard": [
        {"seq": "aabbccdef", "hint": "Multiple unique candidates exist ('d', 'e', 'f'). The rule requires the FIRST one."},
        {"seq": "xyzxzywab", "hint": "Scan in original order once you filter out all repeating characters."},
        {"seq": "abacabadabacaba", "hint": "A fractal-like pattern where 'a', 'b', and 'c' repeat heavily."},
        {"seq": "abcdeabcdeX", "hint": "Every character from a-e repeats twice before the unique character appears."},
        {"seq": "112233445A6677", "hint": "A sequence containing numbers and letters. Letters follow the same rule!"},
        {"seq": "k!k!m@m@q#", "hint": "Punctuation characters also follow the frequency rule."},
    ],
    "expert": [
        {"seq": "aabb", "hint": "Every single character repeats. What special option represents this case?"},
        {"seq": "x", "hint": "A single character sequence. Can a character repeat if it stands alone?"},
        {"seq": "abcdefgabcdefg", "hint": "Full cycle repeat. Check if any character has a count of 1."},
        {"seq": "1234554321", "hint": "A numeric palindrome where every number repeats exactly twice."},
        {"seq": "z9y8x7w6z9y8x7w6Q", "hint": "High-complexity alphanumeric pattern with 1 isolated unique character."},
        {"seq": "::::;;;;!!!!", "hint": "All punctuation symbols. Are all symbols repeated?"},
        {"seq": "aabbccddeeffgghhiijj", "hint": "Long sequence where every letter is paired."},
    ]
}


DIFFICULTY_CONFIGS = {
    "easy": {
        "time_limit": 25,
        "base_points": 100,
        "min_len": 4,
        "max_len": 7,
        "char_pool": string.ascii_lowercase,
        "num_options": 4
    },
    "medium": {
        "time_limit": 18,
        "base_points": 150,
        "min_len": 8,
        "max_len": 12,
        "char_pool": string.ascii_lowercase,
        "num_options": 4
    },
    "hard": {
        "time_limit": 14,
        "base_points": 200,
        "min_len": 12,
        "max_len": 18,
        "char_pool": string.ascii_lowercase + string.digits,
        "num_options": 4
    },
    "expert": {
        "time_limit": 10,
        "base_points": 300,
        "min_len": 16,
        "max_len": 24,
        "char_pool": string.ascii_letters + string.digits + "!@#$%",
        "num_options": 4
    }
}


def generate_synthetic_sequence(difficulty: str, rng: random.Random) -> Tuple[str, bool]:
    """
    Generates a synthetic sequence tailored to the difficulty tier.
    Returns (sequence, force_none_flag).
    """
    diff_cfg = DIFFICULTY_CONFIGS.get(difficulty.lower(), DIFFICULTY_CONFIGS["medium"])
    target_len = rng.randint(diff_cfg["min_len"], diff_cfg["max_len"])
    pool = diff_cfg["char_pool"]

    # In Expert/Hard, 25% chance of generating a sequence with NO unique character (answer: None)
    want_none = (difficulty.lower() in ["hard", "expert"]) and (rng.random() < 0.28)
    
    if want_none:
        # Generate pairs or triples so every character repeats
        chars = rng.sample(pool, max(2, target_len // 2))
        raw_list = []
        for ch in chars:
            repeat_count = rng.randint(2, 3)
            raw_list.extend([ch] * repeat_count)
        rng.shuffle(raw_list)
        return "".join(raw_list), True

    # Otherwise, generate with 1 or more unique characters
    num_uniques = 1 if difficulty.lower() == "easy" else rng.randint(1, 3)
    repeat_chars_count = max(2, (target_len - num_uniques) // 2)
    
    all_selected = rng.sample(pool, min(len(pool), repeat_chars_count + num_uniques))
    unique_chars = all_selected[:num_uniques]
    repeating_chars = all_selected[num_uniques:]

    seq_elements = []
    for ch in repeating_chars:
        reps = rng.randint(2, 4)
        seq_elements.extend([ch] * reps)
        
    # Place unique characters into sequence
    seq_elements.extend(unique_chars)
    rng.shuffle(seq_elements)
    
    return "".join(seq_elements), False


def build_options(correct_answer: str, sequence: str, rng: random.Random, num_options: int = 4) -> List[str]:
    """
    Constructs high-quality multiple choice options including the correct answer,
    plausible distractors (frequent chars, other unique chars), and 'None'.
    """
    options = {correct_answer}
    
    # Extract distinct characters present in sequence
    distinct_in_seq = list(dict.fromkeys(sequence))
    
    # Always consider 'None' as a viable distractor option
    if "None" not in options and len(options) < num_options and rng.random() < 0.45:
        options.add("None")

    # Add characters from sequence as distractors
    rng.shuffle(distinct_in_seq)
    for ch in distinct_in_seq:
        if ch != correct_answer:
            options.add(ch)
            if len(options) >= num_options:
                break

    # If still not enough options, add letters from pool
    extra_chars = list(string.ascii_lowercase)
    rng.shuffle(extra_chars)
    for ch in extra_chars:
        if len(options) >= num_options:
            break
        if ch != correct_answer:
            options.add(ch)

    # Ensure "None" is an option if correct_answer is "None"
    if correct_answer == "None":
        options.add("None")

    options_list = list(options)[:num_options]
    if correct_answer not in options_list:
        options_list[0] = correct_answer

    rng.shuffle(options_list)
    return options_list


def generate_question(
    difficulty: str = "easy",
    seed: Optional[int] = None,
    question_index: int = 1,
    force_curated: bool = False
) -> Question:
    """
    Generates a deterministic or randomized puzzle Question.
    
    Args:
        difficulty: 'easy', 'medium', 'hard', 'expert'.
        seed: Optional integer seed for reproducibility in tests and multiplayer.
        question_index: Question number in the current session.
        force_curated: If True, pulls from curated academic test bank.
    """
    diff_key = difficulty.lower()
    if diff_key not in DIFFICULTY_CONFIGS:
        diff_key = "easy"
        
    rng = random.Random(seed if seed is not None else random.randint(1, 1000000))
    cfg = DIFFICULTY_CONFIGS[diff_key]

    curated_list = CURATED_PUZZLES.get(diff_key, CURATED_PUZZLES["easy"])
    use_curated = force_curated or (rng.random() < 0.35)

    if use_curated and curated_list:
        selected_curated = curated_list[question_index % len(curated_list)]
        sequence = selected_curated["seq"]
        hint = selected_curated["hint"]
        category = "curated_puzzle"
    else:
        sequence, _ = generate_synthetic_sequence(diff_key, rng)
        hint = "Count occurrences from left to right. Identify the first character that appears only once."
        category = "synthetic_puzzle"

    # Authority: compute exact correct answer using frequency algorithm
    computed_res = first_non_repeating_frequency(sequence)
    correct_str = computed_res if computed_res is not None else "None"

    # Build options
    options = build_options(correct_str, sequence, rng, cfg["num_options"])
    
    # Detailed explanation
    explanation_data = explain_first_non_repeating(sequence)

    q_id = f"q_{diff_key}_{question_index}_{rng.randint(1000, 9999)}"
    
    return Question(
        id=q_id,
        sequence=sequence,
        difficulty=diff_key,
        options=options,
        correct_answer=correct_str,
        time_limit_seconds=cfg["time_limit"],
        base_points=cfg["base_points"],
        hint=hint,
        explanation=explanation_data["explanation"],
        category=category
    )
