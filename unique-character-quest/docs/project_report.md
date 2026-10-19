# Advanced Capstone Project Report
# UNIQUE CHARACTER QUEST
### An Interactive Arcade Puzzle Game & Real-Time Multiplayer Web Platform Powered by Python

---

## 1. Project Title
**Unique Character Quest: Gamifying the First Non-Repeating Character Algorithm with Real-Time Multiplayer Architecture and Dual-Algorithm Analysis.**

---

## 2. Abstract
"Unique Character Quest" is an educational web-based puzzle game engineered in Python that transforms a core computer science data structures and algorithms (DSA) concept—*finding the first non-repeating character in an ordered sequence*—into a gamified, real-time multiplayer application. The platform provides two algorithmic implementations: an optimal two-pass Frequency Dictionary (Hash Map) method operating in $O(n)$ time complexity, and a brute-force Nested-Loop method operating in $O(n^2)$ worst-case time complexity. Built upon a decoupled full-stack architecture comprising a **FastAPI** asynchronous backend, a **Streamlit** reactive frontend with retro-arcade styling and Web Audio API sound synthesis, persistent **SQLite** relational storage via **SQLAlchemy**, and bidirectional **WebSockets**, the application provides single-player progression across four difficulty tiers, live multi-device multiplayer matches, deterministic question generation, career statistics, achievement unlocks, and an interactive Algorithm Laboratory.

---

## 3. Introduction
Algorithmic literacy is foundational to computer science education and technical software interviews. Among sequence traversal problems, finding the first non-repeating character in a string or array is an archetypal problem used to assess candidates' understanding of hash tables, time-space trade-offs, and order preservation. However, conventional textbook and automated grading platforms present such problems through dry text prompts and binary pass/fail assertions. 

Unique Character Quest bridges the gap between theoretical algorithm design and practical software engineering by encapsulating algorithmic logic within a game environment featuring responsive visual character tiles, synchronized timers, lives deduction, sound effects, and multi-user room competition.

---

## 4. Problem Statement
Given an arbitrary sequence or string of characters $S = [c_0, c_1, \dots, c_{n-1}]$, the objective is to locate the index $i$ and character $c_i$ such that:
1. $\text{count}(c_i) = 1$ in $S$.
2. For all $j < i$, $\text{count}(c_j) \ge 2$.
3. If no such character exists ($\forall k, \text{count}(c_k) \ge 2$ or $S$ is empty), the result is defined as `None`.

Beginners frequently stumble on three common pitfalls:
- Confusing *any* non-repeating character with the *first* one in original sequential order.
- Inefficiency of brute-force checking ($O(n^2)$), causing timeouts on large datasets.
- Handling tricky boundary edge cases, such as sequences with all repeating characters, singletons at the extreme tail, or whitespace and casing variances.

---

## 5. Motivation
Gamification has proven to increase cognitive retention and engagement in STEM disciplines. By combining dynamic puzzle generation with competitive multiplayer, players actively analyze frequency distributions and character orders under time constraints. Furthermore, this project demonstrates end-to-end full-stack capabilities—API design, WebSocket synchronization, state machine modeling, relational database persistence, and software testing.

---

## 6. Project Objectives
1. **Algorithmic Correctness:** Deliver clean, independently testable Python implementations of both $O(n)$ frequency-counting and $O(n^2)$ brute-force algorithms.
2. **Pedagogical Visualization:** Provide an Algorithm Laboratory with step-by-step pointers, operations counts, and character inspection tables.
3. **Progressive Game Modes:** Design Classic, Speed, and Puzzle modes across Easy, Medium, Hard, and Expert difficulties.
4. **Authoritative Real-Time Multiplayer:** Facilitate synchronized competitive matches across separate devices via WebSockets, eliminating client-side cheating.
5. **Persistent Player Progression:** Implement SQLite storage for personal high scores, global leaderboards, career history, and achievement unlocks.
6. **Automated Verification:** Achieve 100% test pass rate across unit, integration, and API tests using `pytest`.

---

## 7. Scope of the Project
The application covers:
- Complete single-player gameplay and dual-player/multi-player room lobbies.
- In-browser sound synthesis utilizing HTML5 Web Audio API (zero external audio file dependency).
- Server-authoritative timing, preventing client-side timer manipulation.
- Mathematical verification of algorithm equivalence across identical datasets.
- Deployment readiness for local network and cloud hosting platforms.

---

## 8. Existing Approach vs. Proposed Solution

| Feature | Existing Coding Platforms (LeetCode, HackerRank) | Proposed Solution: Unique Character Quest |
| :--- | :--- | :--- |
| **Interface** | Plain code editor and text stdout console | Arcade neon UI, animated character tiles, HUD indicators |
| **Feedback** | Static test case pass/fail boolean | Visual frequency map, algorithm explanation, and audio chimes |
| **Engagement** | Solitary, asynchronous submission | 4 game modes + synchronized live online multiplayer |
| **Pedagogy** | User writes code from scratch with no visual steps | Dual-algorithm sandbox with step-by-step traversal tables |
| **Audio/UX** | Silent | Real-time synthesized retro 8-bit sound effects |

---

## 9. Functional Requirements
- **FR-1:** System must accept character sequences of varying lengths (1 to 200 chars).
- **FR-2:** System must compute the first non-repeating character using $O(n)$ frequency mapping.
- **FR-3:** System must compute the answer using $O(n^2)$ nested loops for complexity comparison.
- **FR-4:** System must support deterministic question generation when provided a seed.
- **FR-5:** System must award base points and proportional speed bonuses for correct answers.
- **FR-6:** System must deduct exactly 1 life for incorrect answers or round timeouts.
- **FR-7:** Host must be able to create a room and receive a 6-character room code.
- **FR-8:** Secondary players must be able to join using the room code from separate browsers/devices.
- **FR-9:** Server must synchronize round questions, deadlines, and scoring over WebSockets.
- **FR-10:** Database must persist player profiles, match results, and achievement records idempotently.

---

## 10. Non-Functional Requirements
- **Performance:** Algorithm execution under 1ms for inputs up to 10,000 characters. WebSocket message propagation under 50ms.
- **Reliability:** Server-authoritative state ensures game integrity even if client disconnects or reloads.
- **Usability:** Intuitive responsive UI requiring zero technical setup from the end user.
- **Security:** Sanitized inputs, strict string boundary checks, hidden correct answers in round payloads.
- **Maintainability:** Modular package structure with loose coupling between backend, algorithms, and UI.

---

## 11. Hardware and Software Requirements
- **Hardware (Development & Deployment):**
  - Processor: Dual-core 2.0 GHz or higher.
  - RAM: Minimum 2 GB (4 GB recommended).
  - Storage: 100 MB free disk space for repository and SQLite database.
  - Network: Standard TCP/IP networking supporting WebSockets.
- **Software Environment:**
  - Operating System: Windows 10/11, macOS, or Linux.
  - Runtime: Python 3.10, 3.11, or 3.12.
  - Web Browser: Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari with Web Audio API support.

---

## 12. Technology Stack & Justification
- **Python:** Primary language chosen for expressiveness, standard library maturity, and educational clarity.
- **FastAPI:** High-performance asynchronous framework supporting native WebSockets and automatic OpenAPI documentation.
- **Streamlit:** Rapid, reactive Python web UI framework with custom HTML/CSS and Web Audio embedding.
- **SQLite:** Serverless, ACID-compliant relational database built into Python's standard library, eliminating external database engine installation hurdles.
- **SQLAlchemy:** Robust ORM providing schema management, transactions, and migration readiness.
- **Pydantic:** Robust data modeling and runtime validation at API and WebSocket boundaries.
- **pytest & HTTPX:** Industry-standard automated testing suite for unit tests and asynchronous API simulation.

---

## 13. System Architecture

```mermaid
graph TD
    Client1[Streamlit Frontend - Host Player] <-->|HTTP REST & WebSockets| Backend[FastAPI Server]
    Client2[Streamlit Frontend - Guest Player] <-->|HTTP REST & WebSockets| Backend
    
    subgraph Backend Architecture
        Backend --> Router[API & WebSocket Router]
        Router --> ConnMgr[WebSocket Connection Manager]
        Router --> RoomMgr[Multiplayer Room State Machine]
        Router --> Engine[Game Engine & Scoring]
        
        Engine --> Algo[Algorithm Module: O(n) & O(n²)]
        Engine --> Questions[Deterministic Question Generator]
        
        Router --> DB[(SQLite Database via SQLAlchemy)]
        DB --> Players[Players Table]
        DB --> Matches[Match Results Table]
        DB --> Achievements[Achievements Table]
    end
```

---

## 14. Module Descriptions
1. `backend/game/algorithms.py`: Contains `first_non_repeating_frequency`, `first_non_repeating_nested`, and `explain_first_non_repeating`.
2. `backend/game/questions.py`: Generates balanced questions across Easy, Medium, Hard, and Expert difficulties.
3. `backend/game/scoring.py`: Authoritative score delta, speed bonus, streak multiplier, and life decrement logic.
4. `backend/game/engine.py`: Single-player state machine handling session creation, level advance, and game-over states.
5. `backend/database.py` & `models.py`: Database engine setup, idempotent table creation, and transactional CRUD operations.
6. `backend/multiplayer/rooms.py`: Server-authoritative room state machine, monotonic clock deadlines, and round resolution.
7. `backend/multiplayer/connection_manager.py`: Live WebSocket client registry and broadcast dispatcher.
8. `frontend/styles.py` & `components.py`: Neon arcade CSS, tile components, and HTML5 Web Audio synthesizer.
9. `app.py`: Streamlit entrypoint organizing 14 functional screens.

---

## 15. Data Flow
1. **Match Initialization:** Client sends `create_room` or `join_room` request to FastAPI.
2. **Round Trigger:** Server broadcasts synchronized question sequence and monotonic deadline timestamp to all room clients.
3. **Answer Submission:** Client sends selected option; server validates against monotonic clock and logs answer.
4. **Round Resolution:** When all clients submit or deadline expires, server executes `resolve_round()`, tallies scores, updates lives, and broadcasts `round_recap`.
5. **Persistence:** Match completion automatically commits results to `match_results` and triggers achievement evaluations.

---

## 16. Algorithm Explanation
In computer programming, a character string in Python is an immutable, ordered sequence of individual character elements. The relationship between an array of characters (e.g., `['a', 'a', 'b', 'b', 'c', 'd']`) and a string (e.g., `"aabbcd"`) is isomorphic: both allow indexed access $O(1)$ and sequential traversal from index 0 to $n-1$.

---

## 17. Method 1: Frequency Dictionary Algorithm ($O(n)$)
1. **Pass 1 (Frequency Map):** Traverse string $S$ from left to right. Maintain a hash map/dictionary where keys are characters and values are integer occurrence counts. Time taken: $O(n)$.
2. **Pass 2 (Ordered Scan):** Traverse string $S$ a second time in original sequential order. For each character $c$, check hash map count. The first character encountered with $\text{count} == 1$ is returned immediately. Time taken: $O(n)$.
3. If the loop completes without finding any count of 1, return `None`.
- **Total Time Complexity:** $O(n) + O(n) = O(2n) = O(n)$.
- **Space Complexity:** $O(k)$ distinct characters stored in dictionary ($k \le n$).

---

## 18. Method 2: Nested-Loop Algorithm ($O(n^2)$)
1. Iterate an outer loop index $i$ from 0 to $n-1$. Let candidate $= S[i]$.
2. Initialize inner count $= 0$.
3. Iterate an inner loop index $j$ from 0 to $n-1$. If $S[j] == \text{candidate}$, increment count. (Early exit if count $> 1$).
4. After inner loop completes, if count $== 1$, return candidate immediately.
5. If outer loop completes, return `None`.
- **Total Time Complexity:** $n \times n = O(n^2)$ worst-case.
- **Space Complexity:** $O(1)$ auxiliary memory (only integer loop counters).

---

## 19. Pseudocode for Both Methods

```python
# Method 1: Frequency Dictionary Approach
FUNCTION first_non_repeating_frequency(sequence):
    counts = EMPTY_DICTIONARY
    FOR EACH char IN sequence:
        counts[char] = counts.GET(char, 0) + 1
        
    FOR EACH char IN sequence:
        IF counts[char] == 1:
            RETURN char
            
    RETURN None

# Method 2: Nested-Loop Approach
FUNCTION first_non_repeating_nested(sequence):
    n = LENGTH(sequence)
    FOR i FROM 0 TO n - 1:
        candidate = sequence[i]
        count = 0
        FOR j FROM 0 TO n - 1:
            IF sequence[j] == candidate:
                count = count + 1
                IF count > 1:
                    BREAK
        IF count == 1:
            RETURN candidate
            
    RETURN None
```

---

## 20. Algorithmic Flowchart

```mermaid
flowchart TD
    Start([Start: Input Sequence S]) --> CheckEmpty{Is S Empty?}
    CheckEmpty -- Yes --> ReturnNone([Return None])
    CheckEmpty -- No --> Pass1[Pass 1: Build Frequency Map Counts]
    Pass1 --> Pass2[Pass 2: Scan S from Left to Right]
    Pass2 --> CheckFreq{Counts[char] == 1?}
    CheckFreq -- Yes --> ReturnChar([Return First Unique Character])
    CheckFreq -- No --> NextChar[Advance to Next Character]
    NextChar --> MoreChars{End of String?}
    MoreChars -- No --> CheckFreq
    MoreChars -- Yes --> ReturnNone
```

---

## 21. Game Rules and Scoring
- **Starting Lives:** 3 hearts.
- **Base Score:** Easy: 100 pts | Medium: 150 pts | Hard: 200 pts | Expert: 300 pts.
- **Speed Bonus:** $\text{Base} \times 0.50 \times \left(\frac{\text{Time Remaining}}{\text{Time Limit}}\right)$.
- **Streak Bonus:** Consecutive correct answers award $+20 \times \text{streak}$ bonus points.
- **Penalty:** Incorrect answer or timeout deducts 1 life and resets streak to 0.
- **Termination:** Game ends when lives reach 0 or configured final round is completed.

---

## 22. Multiplayer Workflow
1. **Lobby:** Host creates room with specific difficulty, round duration (e.g., 15s), and total rounds (e.g., 5).
2. **Joining:** Guests input room code. Server accepts connection up to room limit (6 players).
3. **Round Start:** Host initiates match. Server broadcasts synchronized sequence and sets monotonic deadline.
4. **Answer Lockout:** Each player may submit once per round. Client payload hides correct answer.
5. **Round Evaluation:** When all players submit or deadline passes, server tallies answers, updates lives/scores, and sends round recap.
6. **Next Round / Finale:** Host advances to next round until total rounds completed. Highest score wins (ties resolved by remaining lives).

---

## 23. Database Design & Table Descriptions
SQLite database file: `unique_quest.db`.

1. **`players` Table:**
   - `id` (VARCHAR(50), PK): Unique player UUID.
   - `player_name` (VARCHAR(50), UNIQUE, INDEX): Display handle.
   - `total_games` (INT): Total matches finished.
   - `total_score` (INT): Cumulative career score.
   - `highest_score` (INT): Personal best score.
   - `total_correct` (INT): Career correct answers.
   - `total_questions` (INT): Total questions answered.
   - `created_at` (DATETIME), `last_active` (DATETIME).
2. **`match_results` Table:**
   - `id` (VARCHAR(50), PK): Match UUID.
   - `player_name` (VARCHAR(50), FK `players.player_name`).
   - `mode` (VARCHAR(20)), `difficulty` (VARCHAR(20)).
   - `score` (INT), `accuracy` (FLOAT), `questions_answered` (INT), `correct_answers` (INT).
   - `match_result` (VARCHAR(20)): "WON", "GAME_OVER", "COMPLETED".
   - `completed_at` (DATETIME).
3. **`achievements` Table:**
   - `code` (VARCHAR(50), PK): Unique code (e.g., `first_victory`, `flawless_run`).
   - `title`, `description`, `icon`, `points`.
4. **`player_achievements` Table:**
   - `id` (VARCHAR(50), PK): Unlock UUID.
   - `player_name` (VARCHAR(50), FK), `achievement_code` (VARCHAR(50), FK).
   - `unlocked_at` (DATETIME).
   - Composite Unique constraint on `(player_name, achievement_code)`.

---

## 24. Implementation Details
- Modularized under `unique-character-quest/` with strict separation between game logic, persistence, and interface.
- Thread-safe SQLite connection pooling with `check_same_thread=False`.
- Pydantic V2 schema serialization ensuring strict validation across HTTP and WebSocket payloads.

---

## 25. User Interface Description
- **Color Palette:** Neon purple (`#a855f7`), cyan (`#06b6d4`), amber (`#f59e0b`), emerald (`#10b981`), and dark radial background (`#0d081f`).
- **Character Sequence Tiles:** 3D raised cards displaying the character glyph and corresponding array index.
- **HUD Banner:** Real-time lives indicator (hearts), streak flame counter, score counter, and progress bar.
- **Audio:** Custom JavaScript Web Audio API oscillators producing 8-bit retro sound effects.

---

## 26. Test Strategy
Testing follows a multi-tier verification methodology:
1. **Unit Testing:** Algorithm boundary checks, known test cases, and consistency checks.
2. **Deterministic Generator Testing:** Ensuring generated multiple-choice options always contain the authoritative correct answer.
3. **State Machine Testing:** Game engine transitions, streak scaling, life decrements, and session completion.
4. **Integration Testing:** In-memory SQLite transaction tests, unique constraints, and leaderboard aggregations.
5. **API & Contract Testing:** FastAPI endpoints verified using `TestClient` (HTTPX).

---

## 27. Test Cases & Expected Outputs
Refer to `docs/test_cases.md` for the full test case matrix covering 51 specific automated test cases.

---

## 28. Actual Test Results
All 51 test cases were formally executed using `pytest` inside the project environment:
```text
======================== 51 passed, 1 warning in 1.47s =========================
```
- Core algorithm tests: 100% Passed.
- Question generator tests: 100% Passed.
- Scoring & lives tests: 100% Passed.
- Game engine tests: 100% Passed.
- Database & persistence tests: 100% Passed.
- FastAPI REST API tests: 100% Passed.
- Multiplayer room tests: 100% Passed.

---

## 29. Time and Space Complexity Analysis

| Algorithm | Best-Case Time | Worst-Case Time | Auxiliary Space | Practical Recommendation |
| :--- | :---: | :---: | :---: | :--- |
| **Frequency Dictionary (Hash Map)** | $O(n)$ | $O(n)$ | $O(k)$ | **Recommended for production & gameplay** |
| **Nested-Loop (Brute Force)** | $O(n)$ | $O(n^2)$ | $O(1)$ | Educational baseline for beginner comparison |

For an input sequence of length $N = 10,000$:
- Frequency Dictionary executes $\approx 20,000$ operations ($< 1\text{ ms}$).
- Nested Loops executes up to $100,000,000$ operations ($\approx 1.8\text{ seconds}$).

---

## 30. Limitations
1. In-memory multiplayer room state is maintained within a single server instance process. Scaling across multiple container replicas would require an external pub/sub layer (such as Redis).
2. SQLite files on serverless ephemeral cloud hosts (e.g. Heroku, free tier Render) reset upon container restart; persistent volume storage or hosted PostgreSQL is required for long-term database durability.

---

## 31. Future Enhancements
- Global matchmaking lobby with automated ELO rating.
- Daily algorithmic challenge with time-decay global rankings.
- AI bot opponent that simulates human response times with configurable accuracy.

---

## 32. Conclusion
"Unique Character Quest" successfully accomplishes all pedagogical and architectural goals outlined in the capstone project brief. By converting a standard algorithm into a competitive, multiplayer web game, the project demonstrates proficiency in Python algorithms, FastAPI backend services, WebSocket real-time protocols, database management, and interactive frontend design.

---

## 33. References
1. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
2. Tiangolo, S. (2024). *FastAPI Framework Documentation*. https://fastapi.tiangolo.com
3. Streamlit Inc. (2024). *Streamlit Documentation*. https://docs.streamlit.io
4. Mozilla Developer Network (MDN). (2024). *Web Audio API Standard*. https://developer.mozilla.org
5. SQLAlchemy Authors. (2024). *SQLAlchemy 2.0 Unified Documentation*. https://docs.sqlalchemy.org
