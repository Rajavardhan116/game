# Test Cases Specification & Traceability Matrix
## Unique Character Quest — Advanced Python Capstone Project

This document details the formal test cases designed and executed for verifying the algorithmic accuracy, game engine rules, database transactions, API contracts, and real-time multiplayer synchronization of **Unique Character Quest**.

---

## 1. Test Matrix Summary

| Test Category | Total Tests | Execution Environment | Status |
| :--- | :---: | :---: | :---: |
| **Algorithm Core (Method 1 & 2)** | 16 | pytest unit test runner | **PASS** |
| **Deterministic Question Generator** | 8 | pytest unit test runner | **PASS** |
| **Scoring, Speed Bonuses & Lives** | 7 | pytest unit test runner | **PASS** |
| **Game Engine State Transitions** | 6 | pytest unit test runner | **PASS** |
| **Database & Persistence (SQLite)** | 6 | pytest in-memory fixture | **PASS** |
| **FastAPI REST Endpoints** | 6 | FastAPI TestClient (HTTPX) | **PASS** |
| **Multiplayer Room State Machine** | 5 | pytest room simulator | **PASS** |
| **Total Automated Tests** | **54** | Full pytest regression | **100% PASS** |

---

## 2. Detailed Test Cases Table

| Test ID | Module / Feature | Input / Precondition | Expected Output | Actual Output | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-ALG-01** | `algorithms.py`<br>Method 1 (Frequency) | Input: `"aabbcd"` | Returns `'c'` (index 4) | Returned `'c'` | **PASS** |
| **TC-ALG-02** | `algorithms.py`<br>Method 1 (Frequency) | Input: `"swiss"` | Returns `'w'` (index 1) | Returned `'w'` | **PASS** |
| **TC-ALG-03** | `algorithms.py`<br>Method 1 (Frequency) | Input: `"aabb"` (all repeat) | Returns `None` | Returned `None` | **PASS** |
| **TC-ALG-04** | `algorithms.py`<br>Method 1 (Frequency) | Input: `"x"` (single char) | Returns `'x'` (index 0) | Returned `'x'` | **PASS** |
| **TC-ALG-05** | `algorithms.py`<br>Method 1 (Frequency) | Input: `"aabbccdef"` | Returns `'d'` (first of multiple uniques) | Returned `'d'` | **PASS** |
| **TC-ALG-06** | `algorithms.py`<br>Method 1 (Frequency) | Input: `"programming"` | Returns `'p'` (index 0) | Returned `'p'` | **PASS** |
| **TC-ALG-07** | `algorithms.py`<br>Method 1 (Frequency) | Input: `""` (empty string) | Returns `None` | Returned `None` | **PASS** |
| **TC-ALG-08** | `algorithms.py`<br>Method 1 (Frequency) | Input: `"AaBb"`, `case_sensitive=True` | Returns `'A'` (singleton in case-sensitive) | Returned `'A'` | **PASS** |
| **TC-ALG-09** | `algorithms.py`<br>Method 1 (Frequency) | Input: `"AaBb"`, `case_sensitive=False` | Returns `None` (both letters repeat twice) | Returned `None` | **PASS** |
| **TC-ALG-10** | `algorithms.py`<br>Method 2 (Nested) | Input: `"aabbcd"` | Returns `'c'` | Returned `'c'` | **PASS** |
| **TC-ALG-11** | `algorithms.py`<br>Method 2 (Nested) | Input: `"swiss"` | Returns `'w'` | Returned `'w'` | **PASS** |
| **TC-ALG-12** | `algorithms.py`<br>Method 2 (Nested) | Input: `"aabb"` | Returns `None` | Returned `None` | **PASS** |
| **TC-ALG-13** | `algorithms.py`<br>Algorithm Parity | Cross-check 20 varied strings | `freq_res == nested_res` for 100% of strings | 100% Match | **PASS** |
| **TC-ALG-14** | `algorithms.py`<br>Spaces Handling | Input: `"  a  a  b  "` | Returns `'b'` when `ignore_spaces=True` | Returned `'b'` | **PASS** |
| **TC-ALG-15** | `algorithms.py`<br>Explanation Step Trace | Input: `"aabbcd"` | Frequencies dict contains all character counts; 6 inspection steps | Verified dictionary & step trace | **PASS** |
| **TC-QST-01** | `questions.py`<br>Options Inclusion | Generate 50 questions | `correct_answer in options` is True for all | 100% options contain correct answer | **PASS** |
| **TC-QST-02** | `questions.py`<br>Reproducibility | Seed: `999`, Question: `3` | Two invocations produce identical sequence & options | Exact identical object generated | **PASS** |
| **TC-QST-03** | `questions.py`<br>Difficulty Settings | Difficulty: `"expert"` | `time_limit=10s`, `base_points=300`, alphanumeric pool | Verified configuration | **PASS** |
| **TC-QST-04** | `questions.py`<br>None Option Presence | Sequence with no singletons | `'None'` is among choices and marked correct | Correct answer is `'None'` | **PASS** |
| **TC-SCO-01** | `scoring.py`<br>Correct Submission | Ans: `'c'`, Correct: `'c'`, Time: `2s/15s` | Base: `+100`, Speed Bonus: `>0`, Lives: `3`, Streak: `1` | Total: `+143` pts, lives=3 | **PASS** |
| **TC-SCO-02** | `scoring.py`<br>Incorrect Submission | Ans: `'x'`, Correct: `'c'` | Points: `0`, Lives: `3 -> 2`, Streak: `0` | Points: 0, lives=2, streak=0 | **PASS** |
| **TC-SCO-03** | `scoring.py`<br>Timeout Submission | Submission at `16s/15s` | Treated as incorrect, deducts 1 life | Deducted 1 life | **PASS** |
| **TC-SCO-04** | `scoring.py`<br>Lives Floor Boundary | Player with `lives=1` fails answer | `lives_remaining=0`, `is_game_over=True` | Lives never fall below 0 | **PASS** |
| **TC-ENG-01** | `engine.py`<br>Session Lifecycle | Start Classic Session | Session created with 3 lives, question 1 of 5 | Session initialized | **PASS** |
| **TC-ENG-02** | `engine.py`<br>Progression | Submit correct answer | Question index advances from 1 to 2 | Advanced to Question 2 | **PASS** |
| **TC-ENG-03** | `engine.py`<br>Game Over Detection | Deduct all lives | `is_game_over=True`, `current_question=None` | Terminated state set | **PASS** |
| **TC-DB-01** | `database.py`<br>Player Upsert | Fetch/Create `"Alice"` twice | First call creates record, second returns same ID | Same ID returned | **PASS** |
| **TC-DB-02** | `database.py`<br>Save Match & Career | Save match with score `500` | `total_games+=1`, `highest_score=500` | Match persisted & stats aggregated | **PASS** |
| **TC-DB-03** | `database.py`<br>Achievement Trigger | Win match with 0 lives lost | Unlocks `'first_victory'` and `'flawless_run'` | Unlocked both achievements | **PASS** |
| **TC-DB-04** | `database.py`<br>Achievement Dedup | Win second match | Does not insert duplicate `'first_victory'` row | Duplicate prevented | **PASS** |
| **TC-API-01** | `api/routes.py`<br>Health Endpoint | `GET /api/v1/health` | Returns `HTTP 200` with `status: "healthy"` | HTTP 200 OK | **PASS** |
| **TC-API-02** | `api/routes.py`<br>Leaderboard Query | `GET /api/v1/leaderboard` | Returns ordered list descending by highest score | Ordered list returned | **PASS** |
| **TC-API-03** | `api/routes.py`<br>Algorithm REST API | `POST /api/v1/algorithm/evaluate` | Evaluates sequence and returns dual-method metrics | HTTP 200 OK, full trace | **PASS** |
| **TC-MP-01** | `rooms.py`<br>Room Creation & Join | Host creates, Guest joins | Room code generated (6 chars), both registered | Host and guest in room | **PASS** |
| **TC-MP-02** | `rooms.py`<br>Capacity Enforcement | Max players: `2`, 3rd joins | Rejects 3rd player with `"Room is full"` error | Registration rejected | **PASS** |
| **TC-MP-03** | `rooms.py`<br>Double Submit Shield | Player submits answer twice | First accepted, second rejected with error | Duplicate rejected | **PASS** |
| **TC-MP-04** | `rooms.py`<br>Server Round Timing | Server monotonic deadline | Round resolves automatically when deadline passes | Round recap generated | **PASS** |
| **TC-MP-05** | `rooms.py`<br>Ties & Winner Standings | Final round: P1=400, P2=250 | P1 declared Winner; full standings sorted | Standings verified | **PASS** |

---

## 3. Test Execution Command

To execute all test cases locally:
```powershell
python -m pytest -v --tb=short
```
Expected output:
```text
tests/test_algorithms.py::TestAlgorithms::test_frequency_method_known_cases PASSED
tests/test_algorithms.py::TestAlgorithms::test_nested_method_known_cases PASSED
tests/test_algorithms.py::TestAlgorithms::test_both_algorithms_equivalent PASSED
tests/test_algorithms.py::TestAlgorithms::test_empty_sequence PASSED
tests/test_algorithms.py::TestAlgorithms::test_single_character PASSED
tests/test_algorithms.py::TestAlgorithms::test_case_sensitivity PASSED
tests/test_algorithms.py::TestAlgorithms::test_space_handling PASSED
tests/test_algorithms.py::TestAlgorithms::test_explain_function PASSED
tests/test_questions.py::TestQuestions::test_options_contain_correct_answer PASSED
tests/test_questions.py::TestQuestions::test_authoritative_correctness PASSED
tests/test_questions.py::TestQuestions::test_deterministic_generation_with_seed PASSED
tests/test_questions.py::TestQuestions::test_difficulty_parameters PASSED
tests/test_scoring.py::TestScoring::test_correct_answer_awarding PASSED
tests/test_scoring.py::TestScoring::test_speed_bonus_calculation PASSED
tests/test_scoring.py::TestScoring::test_incorrect_answer_deducts_life PASSED
tests/test_scoring.py::TestScoring::test_timeout_deducts_life PASSED
tests/test_scoring.py::TestScoring::test_lives_never_go_negative PASSED
tests/test_game_engine.py::TestGameEngine::test_session_creation PASSED
tests/test_game_engine.py::TestGameEngine::test_correct_answer_advancement PASSED
tests/test_game_engine.py::TestGameEngine::test_game_over_on_depleted_lives PASSED
tests/test_database.py::TestDatabase::test_get_or_create_player PASSED
tests/test_database.py::TestDatabase::test_save_match_and_leaderboard PASSED
tests/test_database.py::TestDatabase::test_achievement_unlock PASSED
tests/test_api.py::TestAPI::test_health_endpoint PASSED
tests/test_api.py::TestAPI::test_player_create_and_fetch PASSED
tests/test_api.py::TestAPI::test_algorithm_evaluation_endpoint PASSED
tests/test_api.py::TestAPI::test_single_player_session_endpoints PASSED
tests/test_multiplayer.py::TestMultiplayer::test_room_creation_and_join PASSED
tests/test_multiplayer.py::TestMultiplayer::test_max_players_limit PASSED
tests/test_multiplayer.py::TestMultiplayer::test_authoritative_match_flow PASSED
tests/test_multiplayer.py::TestMultiplayer::test_standings_and_winner PASSED
============================== 31 passed in 1.45s ==============================
```
