# 🧩 Unique Character Quest
### Advanced Python Capstone Project — Online Multiplayer Web Game

> **Core Educational Concept:** Finding the First Non-Repeating Character in a Sequence (String / Array).  
> **Tech Stack:** Python 3.10+, FastAPI, WebSockets, Streamlit, SQLite, SQLAlchemy, Pydantic, pytest.

---

## 🌟 Executive Summary

**Unique Character Quest** transforms a foundational computer science interview algorithm—*finding the first non-repeating character in an ordered sequence*—into a vibrant, arcade-style puzzle game.

The project demonstrates:
- **Algorithmic Mastery:** Implementing both the optimal $O(n)$ Frequency Dictionary (Hash Map) method and the naive $O(n^2)$ Nested-Loop brute force approach.
- **Full-Stack Engineering:** A decoupled architecture with a high-performance **FastAPI** REST & WebSocket backend and an energetic **Streamlit** arcade frontend with custom CSS and Web Audio API synthesized sound.
- **Real-Time Multiplayer:** Authoritative, server-synchronized rooms where 2 to 6 players battle against synchronized questions, timers, and live scoreboards across separate devices.
- **Robust Persistence:** SQLite database tracking player profiles, match history, global high scores, and career achievements.
- **Academic Rigor:** Full pytest test suite, test matrix, comprehensive 33-section capstone report, and viva presentation guide.

---

## 🗂️ Project Structure

```text
unique-character-quest/
│
├── app.py                      # Main Streamlit web frontend
├── requirements.txt            # Python dependencies
├── README.md                   # Complete setup and execution guide
├── .env.example                # Template environment variables
├── .gitignore                  # Git ignore rules
│
├── backend/                    # Server-side business logic & persistence
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entrypoint
│   ├── config.py               # Environment configuration
│   ├── database.py             # SQLite engine, sessions, and CRUD operations
│   ├── models.py               # SQLAlchemy ORM models (Player, Match, Achievement)
│   ├── schemas.py              # Pydantic validation & serialization models
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # REST API endpoints (players, matches, leaderboard)
│   ├── multiplayer/
│   │   ├── __init__.py
│   │   ├── connection_manager.py # Live WebSocket connections registry
│   │   ├── rooms.py            # Authoritative multiplayer room state machine
│   │   └── websocket.py        # Real-time WebSocket event handler
│   └── game/
│       ├── __init__.py
│       ├── algorithms.py       # Core algorithms: Frequency dict O(n) & Nested loops O(n^2)
│       ├── questions.py        # Deterministic puzzle generator across 4 difficulties
│       ├── engine.py           # Single-player state machine & progression
│       ├── scoring.py          # Authoritative scoring, speed bonuses, and lives
│       └── validation.py       # Input boundaries and sanitization
│
├── frontend/                   # Streamlit UI modules & client connectors
│   ├── __init__.py
│   ├── components.py           # Reusable UI cards & Web Audio API synthesizer
│   ├── styles.py               # Arcade neon theme CSS and character tile components
│   ├── api_client.py           # HTTP client with offline fallback
│   └── websocket_client.py     # Browser-side WebSocket sync bridge
│
├── tests/                      # Automated test suite (pytest)
│   ├── test_algorithms.py      # Algorithm verification & complexity comparison
│   ├── test_questions.py       # Deterministic generator and options validation
│   ├── test_scoring.py         # Lives, speed bonuses, and streak mechanics
│   ├── test_game_engine.py     # Single-player session transitions
│   ├── test_database.py        # SQLite schema, transactions, and achievements
│   ├── test_api.py             # FastAPI HTTP routes
│   └── test_multiplayer.py     # Room creation, sync rounds, and tie resolution
│
├── docs/                       # College capstone documentation
│   ├── project_report.md       # Comprehensive 33-section academic report
│   ├── test_cases.md           # Structured test case execution matrix
│   └── presentation_outline.md # 10-12 slide viva presentation & Q&A guide
│
└── assets/
    └── README.md               # Asset directory notice
```

---

## 🚀 Quickstart Installation Guide (Windows & PowerShell)

Follow these steps to set up and run the project locally on your machine.

### Step 1: Clone or Navigate to the Project Directory
Open **PowerShell** and navigate to the project directory:
```powershell
cd unique-character-quest
```

### Step 2: Create a Python Virtual Environment
Create an isolated Python 3.10+ virtual environment named `.venv`:
```powershell
python -m venv .venv
```

### Step 3: Activate the Virtual Environment
Activate the environment in PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
*(Note: If PowerShell throws an execution policy error, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and rerun the activate command).*

### Step 4: Install Dependencies
Install all required packages from `requirements.txt`:
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
Copy the `.env.example` file to create your local `.env`:
```powershell
Copy-Item .env.example .env
```

---

## 🎮 Running the Application

Unique Character Quest uses a decoupled architecture. You will run the **FastAPI Backend** in one terminal and the **Streamlit Frontend** in a second terminal.

### Terminal 1: Start the FastAPI Backend
In your first PowerShell terminal (with `.venv` activated):
```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
- **Backend API:** `http://127.0.0.1:8000`
- **Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`
- **WebSocket Endpoint:** `ws://127.0.0.1:8000/ws/match/{room_code}/{player_name}`

### Terminal 2: Start the Streamlit Frontend
Open a **second PowerShell window**, navigate to the project folder, activate the virtual environment, and run:
```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```
Streamlit will automatically open your web browser at:
👉 **`http://localhost:8501`**

---

## 🧪 Running Automated Tests

Run the full automated pytest suite with verbose output:
```powershell
python -m pytest -v
```

To run individual test modules:
```powershell
# Test core algorithms and edge cases:
python -m pytest tests/test_algorithms.py -v

# Test question generator and difficulty scaling:
python -m pytest tests/test_questions.py -v

# Test multiplayer room mechanics:
python -m pytest tests/test_multiplayer.py -v
```

---

## ⚔️ How to Test Multiplayer Between Two Players

### Local Multiplayer Testing (Single Computer)
1. Open your primary browser window at `http://localhost:8501`.
2. Set your player name (e.g., `HostAlice`).
3. Click **⚔️ Online Multiplayer** ➔ **Create Match Room** ➔ **Create Room & Generate Code**.
4. Note the generated 6-character Room Code (e.g., `QUEST7`).
5. Open an **Incognito / Private Window** (or a second browser like Chrome vs Firefox/Edge) at `http://localhost:8501`.
6. Set a different player name (e.g., `FriendBob`).
7. Click **⚔️ Online Multiplayer** ➔ **Join Existing Room** ➔ Enter the code `QUEST7` and click **Join Room**.
8. In the Host window, click **🚀 Start Match Now**.
9. Both browser windows will receive the **exact same puzzle sequence**, synchronized countdown bar, and live answers in real-time!

### Remote Multiplayer Testing (Two Separate Devices / Mobile)
1. Find your computer's local IP address on your Wi-Fi network (run `ipconfig` in PowerShell, look for IPv4 Address, e.g. `192.168.1.15`).
2. Start the FastAPI backend bound to `0.0.0.0`:
   ```powershell
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```
3. In `frontend/api_client.py` or `.env`, set:
   ```env
   BACKEND_URL=http://192.168.1.15:8000
   WS_BASE_URL=ws://192.168.1.15:8000
   ```
4. Start Streamlit bound to your network:
   ```powershell
   python -m streamlit run app.py --server.address 0.0.0.0
   ```
5. From your phone or a laptop connected to the same Wi-Fi, open `http://192.168.1.15:8501`. You can now battle in real-time!

---

## 🌐 Production Deployment Guidance

To make your game playable over the public internet across remote players:

1. **Deploying Backend (Render / Railway / Fly.io / GCP Cloud Run):**
   - Host `backend.main:app` with Uvicorn.
   - Set environment variable `PORT=8000`.
   - Your host will provide an HTTPS/WSS URL: e.g., `https://unique-quest-api.onrender.com`.
2. **Deploying Frontend (Streamlit Community Cloud / HuggingFace Spaces):**
   - Connect your GitHub repository.
   - Configure secrets/environment variables in Streamlit Cloud:
     - `BACKEND_URL=https://unique-quest-api.onrender.com`
     - `WS_BASE_URL=wss://unique-quest-api.onrender.com`
3. **Persistent SQLite Storage:**
   - On ephemeral hosts (Render free tier, Heroku), local SQLite databases reset upon server restart. For persistent storage in production, attach a Persistent Disk volume or configure a PostgreSQL database URL.

---

## 🎓 Academic Capstone Materials

All college submission reports and viva presentation documents are located in `docs/`:
- **`docs/project_report.md`**: 33-section detailed engineering report formatted for university submission.
- **`docs/test_cases.md`**: Complete test case execution matrix with input/output trace.
- **`docs/presentation_outline.md`**: 12-slide defense presentation with anticipated viva questions and answers.

---

## 📄 License
Created for academic capstone presentation. Open-source under the MIT License.
