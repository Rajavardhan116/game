# Capstone Presentation & Defense Guide
## Unique Character Quest — Online Multiplayer Web Game

---

## 📽️ 12-Slide Presentation Outline

### Slide 1: Title & Introduction
- **Project Title:** Unique Character Quest: Gamifying the First Non-Repeating Character Algorithm
- **Candidate Name:** Raja Vardhan Reddy
- **Degree / Course:** Advanced Python Capstone Project (Full-Stack & Algorithms)
- **Tagline:** Turning core algorithmic problem solving into an arcade-style, real-time multiplayer experience.

### Slide 2: Problem Statement
- **The Core Problem:** Given an ordered sequence or array of characters, find the first character that occurs exactly once.
- **The Pedagogical Gap:** Beginners frequently confuse "any unique character" with the "first unique character in sequential order", or struggle to appreciate why a hash map ($O(n)$) is vastly superior to nested loops ($O(n^2)$) on large datasets.
- **Objective:** Bridge theoretical algorithm instruction with engaging interactive gameplay and competitive mechanics.

### Slide 3: Project Objectives
- Implement and benchmark both the $O(n)$ frequency-map approach and the $O(n^2)$ naive nested-loop approach.
- Build a responsive, colorful arcade interface with visual tiles, countdown timers, lives, and instant pedagogical feedback.
- Deliver authoritative server-side online multiplayer with synchronized rounds, monotonic timer deadlines, and cheat prevention.
- Persist player career statistics, high-score leaderboards, and achievements using SQLite.

### Slide 4: High-Level Architecture
- **Decoupled 3-Tier Architecture:**
  1. **Frontend:** Streamlit with custom arcade neon CSS & HTML5 Web Audio synthesizer.
  2. **Authoritative Backend:** FastAPI running asynchronous REST routes & WebSockets.
  3. **Data Layer:** SQLite with SQLAlchemy ORM and atomic transactions.
- Client never determines points, lives, or answers—the server remains the single source of truth.

### Slide 5: Core Algorithmic Breakdown
- **Method 1: Frequency Dictionary (Hash Map) — $O(n)$ Time, $O(k)$ Space**
  - Pass 1: Build frequency map of each character ($O(n)$).
  - Pass 2: Iterate original sequence left-to-right; return first character with count == 1 ($O(n)$).
- **Method 2: Nested Loops (Brute Force) — $O(n^2)$ Time, $O(1)$ Space**
  - Outer loop checks each character; inner loop scans sequence to verify uniqueness.
- **Academic Comparison:** As sequence length $N$ scales from 10 to 10,000, $O(n)$ performs 20,000 operations, whereas $O(n^2)$ executes 100,000,000 operations!

### Slide 6: Progressive Difficulty & Game Modes
- **Classic Challenge:** 5-round progression from easy (4-7 chars) to expert (16-24 chars).
- **Speed Challenge:** Rapid countdown with proportional speed bonuses.
- **Puzzle Challenge:** Hand-crafted edge cases:
  - Sequences where all characters repeat (Answer: "None").
  - Single-character strings (e.g., `"x"` $\to$ `"x"`).
  - Multiple singletons requiring order priority (e.g., `"aabbccdef"` $\to$ `"d"`).
- **Online Multiplayer:** Room-based matches with synchronized questions and live recaps.

### Slide 7: Real-Time Multiplayer Workflow
- **Lobby Phase:** Host generates a 6-character room code; guests join from any browser.
- **Synchronized Round:** Server broadcasts question sequence and starts monotonic countdown.
  - Server deliberately withholds the correct answer from client payloads to prevent inspect-element cheating.
- **Submission & Recap:** Players submit answers; when all submit or time expires, server reveals answer, updates lives/scores, and tallies standings.

### Slide 8: Persistence & Database Design
- **SQLite Schema:**
  - `players`: Career stats, highest score, total games, accuracy percentage.
  - `match_results`: Mode, difficulty, score, completion timestamp, win/loss status.
  - `achievements` & `player_achievements`: 8 unique achievements with idempotency guards.
- Transactions guarantee zero duplicate match writes or score corruption.

### Slide 9: User Interface & Sensory Polish
- **Arcade Aesthetic:** Purple/cyan neon palette, glassmorphism cards, glowing character tiles with index badges.
- **Built-in Web Audio API Synthesizer:**
  - Zero external MP3/WAV dependencies.
  - Generates distinct synthesized frequencies for correct chimes, incorrect buzzes, fanfares, and game over.

### Slide 10: Test Strategy & Verification
- **Automated pytest Suite:**
  - Known input verification (`"aabbcd"` $\to$ `'c'`, `"swiss"` $\to$ `'w'`, `"aabb"` $\to$ `None`).
  - Algorithm consistency check across varied test strings.
  - Question generator determinism via random seeds.
  - Multiplayer room state machine & boundary rules.
- **Result:** 100% test pass rate across all modules.

### Slide 11: Limitations & Future Enhancements
- **Current Limitations:** SQLite is ideal for single-node development; in-memory room state does not span multi-node clusters.
- **Future Enhancements:**
  - Redis pub/sub adapter for horizontally scalable WebSocket rooms.
  - Global multiplayer matchmaking queue.
  - Daily algorithmic challenge modes with leaderboards.

### Slide 12: Conclusion & Key Learnings
- Successfully demonstrated that a classic algorithmic interview question can power an engaging, full-stack, multiplayer application.
- Mastered decoupled full-stack architecture, asynchronous WebSockets, and state machine design in Python.

---

## 🎓 Viva Voce Questions & Model Answers

### Q1: What exactly is a "non-repeating character"?
**Answer:** A non-repeating character (or singleton) is a character that occurs with a total frequency count of exactly 1 within a given sequence. For instance, in the word `"swiss"`, `'s'` occurs 3 times, `'i'` occurs 1 time, and `'w'` occurs 1 time. Both `'w'` and `'i'` are non-repeating.

### Q2: Why is sequential order critical in this puzzle?
**Answer:** The objective requires the **first** non-repeating character. In `"swiss"`, both `'w'` and `'i'` occur once, but `'w'` appears at index 1 while `'i'` appears at index 2. Therefore, `'w'` is the correct answer because it appears earlier in the sequence. Without order preservation, an algorithm might arbitrarily return any unique character.

### Q3: Why is the Frequency Dictionary method $O(n)$ while Nested Loops is $O(n^2)$?
**Answer:** 
- In the frequency dictionary approach, we make two independent, sequential passes over the string of length $n$. The first pass populates a hash map in $O(n)$ time. The second pass reads from the hash map with $O(1)$ average lookups. Total time is $O(n) + O(n) = O(2n) = O(n)$.
- In the nested-loop approach, for each of the $n$ characters (outer loop), we scan all $n$ characters (inner loop) to count occurrences. This results in $n \times n = O(n^2)$ operations in the worst case.

### Q4: What is the space complexity of the Frequency Dictionary approach?
**Answer:** The space complexity is $O(k)$, where $k$ is the number of distinct characters in the alphabet/charset. In standard English ASCII, $k \le 26$ or $k \le 128$, which is bounded by a constant $O(1)$ in practice. In generalized Unicode, $k \le n$, making space $O(k)$ auxiliary.

### Q5: Why did you choose FastAPI for the backend?
**Answer:** FastAPI offers native asynchronous concurrency (`async/await`), out-of-the-box support for persistent WebSockets, automatic request validation via Pydantic, and high throughput comparable to NodeJS and Go. This makes it ideal for real-time multiplayer coordination.

### Q6: What is a WebSocket and why not just use HTTP polling?
**Answer:** A WebSocket is a persistent, full-duplex, bidirectional communication protocol over a single TCP connection (`ws://` or `wss://`). Unlike HTTP request-response polling (which incurs repetitive HTTP header overhead and latency), WebSockets allow the server to push round start events, live answers, and timer ticks to clients instantaneously with sub-millisecond overhead.

### Q7: How does the server prevent cheating in multiplayer mode?
**Answer:**
1. **Server Authoritative State:** Clients do not compute questions, deadlines, lives, or points.
2. **Hidden Answers:** When broadcasting an active round question to clients, the server strips out the `correct_answer` field. A player cannot inspect network traffic or HTML to find the answer.
3. **Monotonic Server Clock:** Round deadlines are calculated using `time.monotonic()` on the server. Clients cannot alter their local system clock to gain extra time.
4. **Single-Submission Lockout:** Once a client submits an answer for a round, further attempts are blocked by the room state machine.

### Q8: Why use SQLite for persistence?
**Answer:** SQLite is a serverless, zero-configuration, ACID-compliant relational database engine stored in a single cross-platform file. It is built directly into Python's standard library, making it the most reliable, beginner-friendly choice for local execution without requiring external database server installations.
