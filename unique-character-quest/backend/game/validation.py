"""
Validation and Boundary Checks for Unique Character Quest
---------------------------------------------------------
Enforces sanitization, length boundaries, character restrictions,
and room code formatting across both HTTP and WebSocket boundaries.
"""

import re
from typing import Optional, Tuple


PLAYER_NAME_REGEX = re.compile(r"^[a-zA-Z0-9_\-\s]{2,20}$")
ROOM_CODE_REGEX = re.compile(r"^[A-Z0-9]{4,8}$")


def validate_player_name(name: Optional[str]) -> Tuple[bool, str]:
    """
    Validates a player's display name.
    Must be 2-20 characters, alphanumeric with optional underscores/hyphens.
    """
    if not name or not name.strip():
        return False, "Player name cannot be empty."
    clean = name.strip()
    if len(clean) < 2:
        return False, "Player name must be at least 2 characters."
    if len(clean) > 20:
        return False, "Player name cannot exceed 20 characters."
    if not PLAYER_NAME_REGEX.match(clean):
        return False, "Player name may only contain letters, numbers, hyphens, and underscores."
    return True, clean


def validate_room_code(code: Optional[str]) -> Tuple[bool, str]:
    """
    Validates a multiplayer room code.
    Must be 4-8 uppercase alphanumeric characters.
    """
    if not code or not code.strip():
        return False, "Room code cannot be empty."
    clean = code.strip().upper()
    if not ROOM_CODE_REGEX.match(clean):
        return False, "Room code must be 4 to 8 alphanumeric characters."
    return True, clean


def validate_sequence_input(seq: Optional[str]) -> Tuple[bool, str]:
    """
    Validates a raw custom sequence input for the educational sandbox.
    """
    if seq is None or len(seq.strip()) == 0:
        return False, "Sequence cannot be empty."
    if len(seq) > 200:
        return False, "Sequence cannot exceed 200 characters in educational mode."
    return True, seq.strip()
