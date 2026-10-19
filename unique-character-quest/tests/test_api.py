"""
Unit Tests for FastAPI HTTP Endpoints
-------------------------------------
Tests RESTful endpoints using FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import init_db

@pytest.fixture(autouse=True)
def setup_database():
    init_db()

client = TestClient(app)


class TestAPI:
    def test_health_endpoint(self):
        """Health check returns 200 OK and service metadata."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    def test_player_create_and_fetch(self):
        """Player creation and profile lookup endpoint."""
        res = client.post("/api/v1/players", json={"player_name": "APITester"})
        assert res.status_code == 200
        data = res.json()
        assert data["player_name"] == "APITester"

        res_get = client.get("/api/v1/players/APITester")
        assert res_get.status_code == 200

    def test_algorithm_evaluation_endpoint(self):
        """Educational algorithm endpoint returns step trace and complexity."""
        payload = {
            "sequence": "aabbcd",
            "case_sensitive": True,
            "ignore_spaces": True
        }
        res = client.post("/api/v1/algorithm/evaluate", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["result"] == "c"
        assert data["both_methods_match"] is True
        assert len(data["steps"]) == 6

    def test_single_player_session_endpoints(self):
        """Full cycle: start session, submit answer."""
        res = client.post("/api/v1/game/session?player_name=Gamer1&mode=classic&difficulty=easy&seed=42")
        assert res.status_code == 200
        session_data = res.json()
        s_id = session_data["session_id"]
        correct_ans = session_data["current_question"]["correct_answer"]

        # Submit answer
        ans_res = client.post(f"/api/v1/game/session/{s_id}/answer?answer={correct_ans}")
        assert ans_res.status_code == 200
        assert ans_res.json()["success"] is True
