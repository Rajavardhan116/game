"""
Unit Tests for Database Persistence and Achievements
----------------------------------------------------
Tests SQLite schema initialization, atomic updates, and achievement unlocks.
"""

import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import Base, Player, MatchResult, Achievement, PlayerAchievement
from backend.database import (
    STANDARD_ACHIEVEMENTS,
    get_or_create_player,
    save_match_result,
    get_leaderboard,
    get_player_achievements_list
)


@pytest.fixture
def test_db():
    """Provides an isolated in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSession()

    # Seed achievements
    for ach in STANDARD_ACHIEVEMENTS:
        db.add(Achievement(**ach))
    db.commit()

    yield db
    db.close()


class TestDatabase:
    def test_get_or_create_player(self, test_db):
        """Creates new player and retrieves existing without duplication."""
        p1 = get_or_create_player(test_db, "Tester1")
        assert p1.player_name == "Tester1"
        assert p1.total_games == 0

        p2 = get_or_create_player(test_db, "Tester1")
        assert p1.id == p2.id

    def test_save_match_and_leaderboard(self, test_db):
        """Saving match updates player statistics and appears on leaderboard."""
        match = save_match_result(
            db=test_db,
            player_name="Champion",
            mode="classic",
            difficulty="medium",
            score=500,
            accuracy=100.0,
            questions_answered=5,
            correct_answers=5,
            levels_completed=5,
            match_result="WON",
            duration_seconds=45.0
        )
        assert match.score == 500

        leaderboard = get_leaderboard(test_db)
        assert len(leaderboard) >= 1
        assert leaderboard[0]["player_name"] == "Champion"
        assert leaderboard[0]["highest_score"] == 500

    def test_achievement_unlock(self, test_db):
        """Winning a match unlocks 'first_victory' and 'flawless_run' achievements."""
        save_match_result(
            db=test_db,
            player_name="Achiever",
            mode="classic",
            difficulty="easy",
            score=300,
            accuracy=100.0,
            questions_answered=3,
            correct_answers=3,
            levels_completed=3,
            match_result="WON"
        )
        achievements = get_player_achievements_list(test_db, "Achiever")
        unlocked_codes = [a["code"] for a in achievements if a["unlocked"]]
        assert "first_victory" in unlocked_codes
        assert "flawless_run" in unlocked_codes
