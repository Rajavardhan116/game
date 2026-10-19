"""
Authoritative Room State Machine for Online Multiplayer
--------------------------------------------------------
Controls game state, synchronized rounds, server-side timer deadlines,
answer evaluation, tie-breaks, and prevents client-side cheating.
"""

import time
import random
import string
import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from ..game.questions import Question, generate_question
from ..game.scoring import evaluate_answer_submission

logger = logging.getLogger("multiplayer.rooms")


class RoomPlayer(BaseModel):
    player_name: str
    is_host: bool = False
    is_ready: bool = True
    score: int = 0
    lives: int = 3
    has_submitted: bool = False
    submitted_answer: Optional[str] = None
    time_taken: float = 0.0
    connected: bool = True
    last_ping: float = Field(default_factory=time.time)


class RoundRecap(BaseModel):
    round_number: int
    sequence: str
    correct_answer: str
    explanation: str
    player_answers: Dict[str, Dict[str, Any]]  # name -> {answer, is_correct, points_earned, time_taken}


class MultiplayerRoom:
    def __init__(
        self,
        room_code: str,
        host_name: str,
        difficulty: str = "medium",
        total_rounds: int = 5,
        round_duration: int = 15,
        max_players: int = 6
    ):
        self.room_code = room_code.upper()
        self.host_name = host_name
        self.difficulty = difficulty.lower()
        self.total_rounds = total_rounds
        self.round_duration = round_duration
        self.max_players = max_players
        
        self.status: str = "waiting"  # "waiting", "in_round", "round_recap", "match_finished"
        self.players: Dict[str, RoomPlayer] = {}
        self.current_round: int = 0
        self.current_question: Optional[Question] = None
        
        self.round_start_monotonic: float = 0.0
        self.round_deadline_monotonic: float = 0.0
        
        self.past_recaps: List[RoundRecap] = []
        self.latest_recap: Optional[RoundRecap] = None
        self.winner: Optional[str] = None
        self.created_at: float = time.time()
        self.match_seed: int = random.randint(10000, 99999)

        # Register host
        self.add_player(host_name, is_host=True)

    def add_player(self, player_name: str, is_host: bool = False) -> tuple[bool, str]:
        """Adds a player to the room if conditions are met."""
        clean_name = player_name.strip()
        if self.status != "waiting" and clean_name not in self.players:
            return False, "Match has already started. Cannot join in-progress game."
        
        if clean_name in self.players:
            # Reconnection
            self.players[clean_name].connected = True
            self.players[clean_name].last_ping = time.time()
            return True, "Reconnected to room."
            
        if len(self.players) >= self.max_players:
            return False, f"Room is full (max {self.max_players} players)."

        self.players[clean_name] = RoomPlayer(
            player_name=clean_name,
            is_host=is_host,
            lives=3,
            score=0
        )
        return True, "Joined room successfully."

    def remove_player(self, player_name: str):
        """Marks a player disconnected."""
        if player_name in self.players:
            self.players[player_name].connected = False
            # If all players left in waiting room, host might change
            if self.players[player_name].is_host:
                connected_players = [p for p in self.players.values() if p.connected and p.player_name != player_name]
                if connected_players:
                    connected_players[0].is_host = True
                    self.host_name = connected_players[0].player_name

    def start_match(self) -> tuple[bool, str]:
        """Begins the match from the waiting lobby."""
        if self.status != "waiting":
            return False, "Match has already commenced."
        if len(self.players) < 1:
            return False, "At least 1 player is required."

        self.status = "in_round"
        self.current_round = 0
        return self.next_round()

    def next_round(self) -> tuple[bool, str]:
        """Advances to the next synchronized round."""
        self.current_round += 1
        if self.current_round > self.total_rounds:
            return self.finalize_match()

        # Reset player round states
        for p in self.players.values():
            p.has_submitted = False
            p.submitted_answer = None
            p.time_taken = 0.0

        # Generate deterministic authoritative question for all players
        round_seed = self.match_seed + (self.current_round * 31)
        self.current_question = generate_question(
            difficulty=self.difficulty,
            seed=round_seed,
            question_index=self.current_round,
            force_curated=False
        )
        self.current_question.time_limit_seconds = self.round_duration

        now_mono = time.monotonic()
        self.round_start_monotonic = now_mono
        self.round_deadline_monotonic = now_mono + self.round_duration
        self.status = "in_round"
        self.latest_recap = None

        logger.info(f"Room {self.room_code} started Round {self.current_round}/{self.total_rounds}.")
        return True, "Round started."

    def submit_answer(self, player_name: str, answer: str) -> tuple[bool, str]:
        """
        Processes answer submission from a player.
        Enforces server-authoritative deadline and prevents duplicate submissions.
        """
        if self.status != "in_round":
            return False, "No active round is currently accepting answers."

        player = self.players.get(player_name)
        if not player:
            return False, "Player not found in room."

        if player.has_submitted:
            return False, "You have already submitted an answer for this round."

        now_mono = time.monotonic()
        # Add a 1.0 second network latency tolerance for submission timestamp
        is_timed_out = (now_mono > (self.round_deadline_monotonic + 1.0))
        time_taken = max(0.1, min(self.round_duration, now_mono - self.round_start_monotonic))

        player.has_submitted = True
        player.submitted_answer = "TIMEOUT" if is_timed_out else answer
        player.time_taken = time_taken

        logger.info(f"Room {self.room_code}: {player_name} submitted '{answer}' in {time_taken:.2f}s.")

        # If all connected players have submitted, resolve the round immediately!
        all_active_submitted = all(
            p.has_submitted for p in self.players.values() if p.connected
        )
        if all_active_submitted:
            self.resolve_round()

        return True, "Answer registered."

    def check_deadline_and_resolve(self) -> bool:
        """Called periodically or on client poll. Resolves round if deadline expired."""
        if self.status == "in_round":
            if time.monotonic() >= self.round_deadline_monotonic:
                self.resolve_round()
                return True
        return False

    def resolve_round(self):
        """Authoritatively tallies answers, updates points/lives, and generates round recap."""
        if not self.current_question:
            return

        self.status = "round_recap"
        recap_answers: Dict[str, Dict[str, Any]] = {}
        correct_ans = self.current_question.correct_answer

        for p_name, p in self.players.items():
            if not p.has_submitted:
                # Mark as timed out
                p.has_submitted = True
                p.submitted_answer = "TIMEOUT"
                p.time_taken = self.round_duration

            eval_res = evaluate_answer_submission(
                submitted_answer=p.submitted_answer,
                correct_answer=correct_ans,
                time_taken=p.time_taken,
                time_limit=self.round_duration,
                current_lives=p.lives,
                current_streak=0,
                base_points=self.current_question.base_points,
                hint_used=False
            )

            p.score += eval_res.total_delta
            p.lives = eval_res.lives_remaining

            recap_answers[p_name] = {
                "answer": p.submitted_answer,
                "is_correct": eval_res.is_correct,
                "points_earned": eval_res.total_delta,
                "speed_bonus": eval_res.speed_bonus,
                "time_taken": round(p.time_taken, 2),
                "lives_remaining": p.lives
            }

        self.latest_recap = RoundRecap(
            round_number=self.current_round,
            sequence=self.current_question.sequence,
            correct_answer=correct_ans,
            explanation=self.current_question.explanation or f"Correct answer is '{correct_ans}'.",
            player_answers=recap_answers
        )
        self.past_recaps.append(self.latest_recap)
        logger.info(f"Room {self.room_code} resolved Round {self.current_round}.")

    def finalize_match(self) -> tuple[bool, str]:
        """Determines the final winner and ends the match."""
        self.status = "match_finished"
        
        # Sort players by score descending, then by remaining lives
        sorted_players = sorted(
            self.players.values(),
            key=lambda p: (p.score, p.lives),
            reverse=True
        )

        if sorted_players:
            top_player = sorted_players[0]
            # Check for ties
            ties = [p for p in sorted_players if p.score == top_player.score and p.lives == top_player.lives]
            if len(ties) > 1:
                self.winner = "Tie: " + ", ".join(p.player_name for p in ties)
            else:
                self.winner = top_player.player_name
        else:
            self.winner = "None"

        return True, "Match concluded."

    def get_seconds_remaining(self) -> float:
        """Returns floating seconds remaining in the active round."""
        if self.status != "in_round":
            return 0.0
        remaining = self.round_deadline_monotonic - time.monotonic()
        return max(0.0, round(remaining, 1))

    def to_client_payload(self, player_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Builds a safe, sanitized client payload.
        Crucial security: DOES NOT leak the correct answer while round is in progress!
        """
        players_info = []
        for p in sorted(self.players.values(), key=lambda x: x.score, reverse=True):
            players_info.append({
                "player_name": p.player_name,
                "is_host": p.is_host,
                "score": p.score,
                "lives": p.lives,
                "has_submitted": p.has_submitted,
                "connected": p.connected,
                "last_answer": p.submitted_answer if (self.status != "in_round" or p.player_name == player_name) else None
            })

        payload = {
            "room_code": self.room_code,
            "host_name": self.host_name,
            "status": self.status,
            "difficulty": self.difficulty,
            "current_round": self.current_round,
            "total_rounds": self.total_rounds,
            "round_duration": self.round_duration,
            "seconds_remaining": self.get_seconds_remaining(),
            "players": players_info,
            "winner": self.winner
        }

        if self.current_question and self.status == "in_round":
            payload["sequence"] = self.current_question.sequence
            payload["options"] = self.current_question.options
            # Notice: correct_answer is deliberately NOT included here!
        elif self.status == "round_recap" and self.latest_recap:
            payload["sequence"] = self.latest_recap.sequence
            payload["correct_answer"] = self.latest_recap.correct_answer
            payload["explanation"] = self.latest_recap.explanation
            payload["recap"] = self.latest_recap.dict()

        return payload


class RoomManager:
    """Manages active rooms in memory with thread safety and code generation."""

    def __init__(self):
        self.rooms: Dict[str, MultiplayerRoom] = {}

    def generate_unique_code(self) -> str:
        """Produces a 6-character memorable alphanumeric room code."""
        chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # omit ambiguous O, 0, I, 1
        for _ in range(100):
            code = "".join(random.choices(chars, k=6))
            if code not in self.rooms:
                return code
        return str(random.randint(100000, 999999))

    def create_room(
        self,
        host_name: str,
        difficulty: str = "medium",
        total_rounds: int = 5,
        round_duration: int = 15
    ) -> MultiplayerRoom:
        code = self.generate_unique_code()
        room = MultiplayerRoom(
            room_code=code,
            host_name=host_name,
            difficulty=difficulty,
            total_rounds=total_rounds,
            round_duration=round_duration
        )
        self.rooms[code] = room
        logger.info(f"Created room {code} by host '{host_name}'.")
        return room

    def get_room(self, room_code: str) -> Optional[MultiplayerRoom]:
        return self.rooms.get(room_code.upper())

    def delete_room(self, room_code: str):
        code = room_code.upper()
        if code in self.rooms:
            del self.rooms[code]


room_manager = RoomManager()
