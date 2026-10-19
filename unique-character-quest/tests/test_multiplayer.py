"""
Unit Tests for Online Multiplayer Mechanics & Synchronization
--------------------------------------------------------------
Tests room creation, joining, authoritative countdowns, and answer submission.
"""

import pytest
from backend.multiplayer.rooms import RoomManager, MultiplayerRoom


class TestMultiplayer:
    def test_room_creation_and_join(self):
        """Host creates room and second player joins successfully."""
        rm = RoomManager()
        room = rm.create_room(host_name="HostPlayer", difficulty="medium", total_rounds=5, round_duration=15)
        assert len(room.room_code) == 6
        assert room.host_name == "HostPlayer"
        assert len(room.players) == 1

        ok, msg = room.add_player("FriendPlayer")
        assert ok is True
        assert len(room.players) == 2

    def test_max_players_limit(self):
        """Room rejects players beyond max capacity."""
        room = MultiplayerRoom(room_code="TEST99", host_name="H", max_players=2)
        room.add_player("Player2")
        ok, msg = room.add_player("Player3")
        assert ok is False
        assert "full" in msg.lower()

    def test_authoritative_match_flow(self):
        """Room starts match, starts round, accepts answers, and resolves recap."""
        room = MultiplayerRoom(room_code="GAME01", host_name="Alice", total_rounds=2, round_duration=10)
        room.add_player("Bob")

        # Start match
        ok, _ = room.start_match()
        assert ok is True
        assert room.status == "in_round"
        assert room.current_round == 1
        assert room.current_question is not None

        correct_ans = room.current_question.correct_answer

        # Both submit answers
        sub_ok1, _ = room.submit_answer("Alice", correct_ans)
        assert sub_ok1 is True

        # Alice cannot submit twice
        sub_dup, dup_msg = room.submit_answer("Alice", "x")
        assert sub_dup is False

        sub_ok2, _ = room.submit_answer("Bob", "WRONG")
        assert sub_ok2 is True

        # All players submitted -> round automatically resolved
        assert room.status == "round_recap"
        assert room.players["Alice"].score > 0
        assert room.players["Bob"].lives == 2  # Lost 1 life

    def test_standings_and_winner(self):
        """Finalizing match identifies highest scoring player as winner."""
        room = MultiplayerRoom(room_code="WIN001", host_name="P1", total_rounds=1)
        room.add_player("P2")
        room.players["P1"].score = 400
        room.players["P2"].score = 250

        room.finalize_match()
        assert room.status == "match_finished"
        assert room.winner == "P1"
