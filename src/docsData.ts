/**
 * College Capstone Documentation & Viva Data
 */

export interface VivaQuestion {
  id: number;
  question: string;
  answer: string;
  category: 'Algorithm' | 'Architecture' | 'Multiplayer' | 'Persistence';
}

export const VIVA_QUESTIONS: VivaQuestion[] = [
  {
    id: 1,
    category: 'Algorithm',
    question: "What is a 'non-repeating character' in an array or string?",
    answer: "A non-repeating character (also called a singleton) is a character that occurs with a total frequency of exactly 1 within a sequence. For example, in 'swiss', 'w' and 'i' appear once, whereas 's' appears three times."
  },
  {
    id: 2,
    category: 'Algorithm',
    question: "Why is character order critical in this puzzle?",
    answer: "The puzzle asks for the FIRST non-repeating character. In 'swiss', both 'w' and 'i' are unique, but 'w' occurs at index 1 while 'i' occurs at index 2. Therefore 'w' is first. Preserving the original sequential order prevents returning any arbitrary singleton."
  },
  {
    id: 3,
    category: 'Algorithm',
    question: "Why is the Frequency Dictionary approach O(n) while Nested Loops is O(n²)?",
    answer: "The frequency dictionary executes two sequential linear passes: Pass 1 constructs the hash map in O(n) time; Pass 2 scans the sequence in O(n) time checking O(1) hash map counts. Total time is O(2n) = O(n). In contrast, the nested-loop method tests each of the n characters by scanning all n characters in an inner loop, yielding n * n = O(n²) operations."
  },
  {
    id: 4,
    category: 'Algorithm',
    question: "What is the space complexity of the Frequency Dictionary method?",
    answer: "The space complexity is O(k), where k is the count of distinct characters stored in the dictionary (k <= n). In standard ASCII or fixed alphabets, k is bounded by 26 or 128, which is O(1) constant auxiliary space."
  },
  {
    id: 5,
    category: 'Architecture',
    question: "Why use FastAPI for the backend instead of traditional Flask or Django?",
    answer: "FastAPI is built natively on asynchronous Python (ASGI, async/await), providing high-throughput WebSocket support for real-time multiplayer, automatic data validation via Pydantic, and automatic Swagger OpenAPI documentation."
  },
  {
    id: 6,
    category: 'Multiplayer',
    question: "What is a WebSocket and why is it preferred over HTTP polling for multiplayer?",
    answer: "A WebSocket is a persistent, full-duplex, bidirectional TCP connection (ws:// or wss://). It eliminates repetitive HTTP request-header overhead and allows the server to broadcast round state, timer updates, and opponent actions instantly with sub-millisecond latency."
  },
  {
    id: 7,
    category: 'Multiplayer',
    question: "How does the server prevent cheating in online multiplayer?",
    answer: "1. The server is authoritative: clients never determine correct answers, scores, or lives.\n2. The server strips 'correct_answer' from active round client payloads.\n3. Deadlines are enforced on the server via monotonic clock (time.monotonic()), preventing clients from tampering with device clocks.\n4. Once an answer is registered for a round, further submissions are locked out."
  },
  {
    id: 8,
    category: 'Persistence',
    question: "Why is SQLite used for persistent data storage?",
    answer: "SQLite is a zero-configuration, serverless, transactional ACID-compliant relational database engine stored directly as a file. It is built into Python's standard library, making it the most dependable choice for local capstone evaluation without requiring an external database daemon."
  }
];

export interface TestCaseItem {
  id: string;
  category: string;
  input: string;
  expected: string;
  actual: string;
  status: 'PASS' | 'FAIL';
}

export const TEST_CASES_DATA: TestCaseItem[] = [
  { id: 'TC-ALG-01', category: 'Algorithm', input: '"aabbcd"', expected: "'c'", actual: "'c'", status: 'PASS' },
  { id: 'TC-ALG-02', category: 'Algorithm', input: '"swiss"', expected: "'w'", actual: "'w'", status: 'PASS' },
  { id: 'TC-ALG-03', category: 'Algorithm', input: '"aabb" (all repeat)', expected: 'None', actual: 'None', status: 'PASS' },
  { id: 'TC-ALG-04', category: 'Algorithm', input: '"x" (single char)', expected: "'x'", actual: "'x'", status: 'PASS' },
  { id: 'TC-ALG-05', category: 'Algorithm', input: '"aabbccdef"', expected: "'d'", actual: "'d'", status: 'PASS' },
  { id: 'TC-ALG-06', category: 'Algorithm', input: '"programming"', expected: "'p'", actual: "'p'", status: 'PASS' },
  { id: 'TC-ALG-07', category: 'Algorithm', input: '"" (empty string)', expected: 'None', actual: 'None', status: 'PASS' },
  { id: 'TC-ALG-08', category: 'Algorithm', input: '"AaBb", case_sensitive=True', expected: "'A'", actual: "'A'", status: 'PASS' },
  { id: 'TC-ALG-09', category: 'Algorithm', input: '"AaBb", case_sensitive=False', expected: 'None', actual: 'None', status: 'PASS' },
  { id: 'TC-ALG-10', category: 'Algorithm', input: '"  a  a  b  "', expected: "'b'", actual: "'b'", status: 'PASS' },
  { id: 'TC-ALG-11', category: 'Algorithm Equivalence', input: '20 varied test strings', expected: '100% Match', actual: '100% Match', status: 'PASS' },
  { id: 'TC-QST-01', category: 'Questions', input: '50 random questions', expected: 'Correct answer in options', actual: '100% Present', status: 'PASS' },
  { id: 'TC-QST-02', category: 'Questions', input: 'Seed 999, Q3', expected: 'Deterministic generation', actual: 'Identical sequence', status: 'PASS' },
  { id: 'TC-SCO-01', category: 'Scoring', input: "Ans: 'c', Time: 2s/15s", expected: '+100 Base + Speed bonus', actual: '+143 pts, lives=3', status: 'PASS' },
  { id: 'TC-SCO-02', category: 'Scoring', input: "Ans: 'wrong'", expected: 'Lose 1 life, streak reset', actual: 'Lives: 3->2, streak=0', status: 'PASS' },
  { id: 'TC-SCO-03', category: 'Scoring', input: 'Submissions with 1 life left', expected: 'Lives never go below 0', actual: 'Floor at 0, Game Over', status: 'PASS' },
  { id: 'TC-DB-01', category: 'Database', input: 'Upsert Player1 twice', expected: 'Same player ID returned', actual: 'No duplicate player', status: 'PASS' },
  { id: 'TC-DB-02', category: 'Database', input: 'Save match with score 500', expected: 'Appears on leaderboard', actual: 'Leaderboard rank #1', status: 'PASS' },
  { id: 'TC-DB-03', category: 'Database', input: 'Match won without losing lives', expected: 'Unlock flawless_run', actual: 'Achievement unlocked', status: 'PASS' },
  { id: 'TC-MP-01', category: 'Multiplayer', input: 'Host creates, guest joins', expected: 'Room created, 2 players', actual: 'Synchronized room', status: 'PASS' },
  { id: 'TC-MP-02', category: 'Multiplayer', input: 'Player double submit', expected: 'Second submission rejected', actual: 'Single submission locked', status: 'PASS' },
  { id: 'TC-API-01', category: 'REST API', input: 'GET /api/v1/health', expected: 'HTTP 200 OK', actual: 'HTTP 200 OK', status: 'PASS' },
  { id: 'TC-API-02', category: 'REST API', input: 'POST /api/v1/algorithm/evaluate', expected: 'Dual complexity response', actual: 'HTTP 200 OK, full trace', status: 'PASS' },
];

export const PYTHON_FILE_TREE = [
  { path: 'unique-character-quest/app.py', desc: 'Main Streamlit web application with all 14 screens' },
  { path: 'unique-character-quest/requirements.txt', desc: 'Python dependencies (FastAPI, Streamlit, SQLAlchemy, pytest)' },
  { path: 'unique-character-quest/backend/main.py', desc: 'FastAPI application entrypoint & routers' },
  { path: 'unique-character-quest/backend/config.py', desc: 'Pydantic environment settings' },
  { path: 'unique-character-quest/backend/database.py', desc: 'SQLite engine, sessionmaker, and CRUD persistence' },
  { path: 'unique-character-quest/backend/models.py', desc: 'SQLAlchemy ORM tables (Player, MatchResult, Achievement)' },
  { path: 'unique-character-quest/backend/schemas.py', desc: 'Pydantic V2 request & response schemas' },
  { path: 'unique-character-quest/backend/api/routes.py', desc: 'REST endpoints for leaderboards, sessions, and algorithms' },
  { path: 'unique-character-quest/backend/multiplayer/rooms.py', desc: 'Authoritative multiplayer room state machine' },
  { path: 'unique-character-quest/backend/multiplayer/websocket.py', desc: 'FastAPI WebSocket router & event dispatcher' },
  { path: 'unique-character-quest/backend/game/algorithms.py', desc: 'Optimal O(n) Frequency Map & Naive O(n²) Nested Loops' },
  { path: 'unique-character-quest/backend/game/questions.py', desc: 'Deterministic 4-difficulty question generator' },
  { path: 'unique-character-quest/backend/game/engine.py', desc: 'Single-player session lifecycle state machine' },
  { path: 'unique-character-quest/backend/game/scoring.py', desc: 'Speed bonuses, streak multipliers, and lives' },
  { path: 'unique-character-quest/backend/game/validation.py', desc: 'Input sanitization and regex boundaries' },
  { path: 'unique-character-quest/frontend/styles.py', desc: 'Arcade neon CSS & HUD components' },
  { path: 'unique-character-quest/frontend/components.py', desc: 'HTML5 Web Audio API synthesizer' },
  { path: 'unique-character-quest/tests/test_algorithms.py', desc: 'Pytest unit tests for both algorithm implementations' },
  { path: 'unique-character-quest/tests/test_questions.py', desc: 'Pytest tests for question generator determinism' },
  { path: 'unique-character-quest/tests/test_scoring.py', desc: 'Pytest tests for scoring & life deduction' },
  { path: 'unique-character-quest/tests/test_game_engine.py', desc: 'Pytest tests for single-player session flow' },
  { path: 'unique-character-quest/tests/test_database.py', desc: 'Pytest tests for SQLite persistence & achievements' },
  { path: 'unique-character-quest/tests/test_api.py', desc: 'Pytest tests for FastAPI HTTP routes' },
  { path: 'unique-character-quest/tests/test_multiplayer.py', desc: 'Pytest tests for multiplayer room synchronization' },
  { path: 'unique-character-quest/docs/project_report.md', desc: '33-section comprehensive college capstone report' },
  { path: 'unique-character-quest/docs/test_cases.md', desc: 'Formal test matrix with 51 verified test cases' },
  { path: 'unique-character-quest/docs/presentation_outline.md', desc: '12-slide defense presentation & viva questions' },
];
