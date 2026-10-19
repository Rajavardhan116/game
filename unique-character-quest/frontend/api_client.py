"""
HTTP API Client for Unique Character Quest Frontend
---------------------------------------------------
Encapsulates communication between the Streamlit UI and the FastAPI backend.
Includes automatic fallback to local engine logic if backend is launching.
"""

import os
import requests
from typing import Dict, Any, List, Optional

# Configurable backend base URL via environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


class APIClient:
    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url.rstrip("/")

    def is_backend_online(self) -> bool:
        """Verifies if the FastAPI backend service is responding."""
        try:
            r = requests.get(f"{self.base_url}/api/v1/health", timeout=1.5)
            return r.status_code == 200
        except Exception:
            return False

    def get_or_create_player(self, player_name: str) -> Optional[Dict[str, Any]]:
        """Registers or fetches player details."""
        try:
            r = requests.post(
                f"{self.base_url}/api/v1/players",
                json={"player_name": player_name},
                timeout=3.0
            )
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None

    def get_leaderboard(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Retrieves global high scores."""
        try:
            r = requests.get(f"{self.base_url}/api/v1/leaderboard?limit={limit}", timeout=3.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return []

    def get_achievements(self, player_name: str) -> List[Dict[str, Any]]:
        """Fetches career achievements for the specified player."""
        try:
            r = requests.get(f"{self.base_url}/api/v1/achievements/{player_name}", timeout=3.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return []

    def get_history(self, player_name: str) -> List[Dict[str, Any]]:
        """Fetches match history records for a player."""
        try:
            r = requests.get(f"{self.base_url}/api/v1/history/{player_name}", timeout=3.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return []

    def save_match(
        self,
        player_name: str,
        mode: str,
        difficulty: str,
        score: int,
        accuracy: float,
        questions_answered: int,
        correct_answers: int,
        levels_completed: int,
        match_result: str,
        duration_seconds: float = 0.0
    ) -> Optional[Dict[str, Any]]:
        """Persists match records and evaluates achievements."""
        try:
            payload = {
                "player_name": player_name,
                "mode": mode,
                "difficulty": difficulty,
                "score": score,
                "accuracy": accuracy,
                "questions_answered": questions_answered,
                "correct_answers": correct_answers,
                "levels_completed": levels_completed,
                "match_result": match_result,
                "duration_seconds": duration_seconds
            }
            r = requests.post(f"{self.base_url}/api/v1/game/match/save", json=payload, timeout=3.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None

    def create_room(self, host_name: str, difficulty: str = "medium", total_rounds: int = 5, round_duration: int = 15) -> Optional[Dict[str, Any]]:
        """Creates a synchronized multiplayer match room."""
        try:
            payload = {
                "host_name": host_name,
                "difficulty": difficulty,
                "total_rounds": total_rounds,
                "round_duration": round_duration
            }
            r = requests.post(f"{self.base_url}/api/v1/rooms", json=payload, timeout=3.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None

    def join_room(self, room_code: str, player_name: str) -> Optional[Dict[str, Any]]:
        """Registers a player in a room."""
        try:
            payload = {
                "room_code": room_code,
                "player_name": player_name
            }
            r = requests.post(f"{self.base_url}/api/v1/rooms/join", json=payload, timeout=3.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None

    def get_room_state(self, room_code: str, player_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Polls current room status and synchronized countdown."""
        try:
            url = f"{self.base_url}/api/v1/rooms/{room_code}"
            if player_name:
                url += f"?player_name={player_name}"
            r = requests.get(url, timeout=2.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None

    def evaluate_algorithm(self, sequence: str, case_sensitive: bool = True, ignore_spaces: bool = True) -> Optional[Dict[str, Any]]:
        """Calls the educational algorithm analyzer endpoint."""
        try:
            payload = {
                "sequence": sequence,
                "case_sensitive": case_sensitive,
                "ignore_spaces": ignore_spaces
            }
            r = requests.post(f"{self.base_url}/api/v1/algorithm/evaluate", json=payload, timeout=3.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return None


api_client = APIClient()
