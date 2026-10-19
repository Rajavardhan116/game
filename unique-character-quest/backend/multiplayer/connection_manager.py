"""
WebSocket Connection Manager for Real-Time Multiplayer
------------------------------------------------------
Tracks live WebSocket client connections grouped by room code.
Handles broadcasting events, individual player messages, and disconnection cleanup.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from fastapi import WebSocket

logger = logging.getLogger("multiplayer.connection_manager")


class ConnectionManager:
    def __init__(self):
        # room_code -> dict(player_name: WebSocket)
        self.active_rooms: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, room_code: str, player_name: str, websocket: WebSocket):
        """Accepts a WebSocket connection and registers it in the room."""
        await websocket.accept()
        room_code = room_code.upper()
        if room_code not in self.active_rooms:
            self.active_rooms[room_code] = {}
        self.active_rooms[room_code][player_name] = websocket
        logger.info(f"Player '{player_name}' connected to room '{room_code}'. Total in room: {len(self.active_rooms[room_code])}")

    def disconnect(self, room_code: str, player_name: str):
        """Unregisters a player's connection upon disconnect."""
        room_code = room_code.upper()
        if room_code in self.active_rooms:
            if player_name in self.active_rooms[room_code]:
                del self.active_rooms[room_code][player_name]
                logger.info(f"Player '{player_name}' disconnected from room '{room_code}'.")
            if not self.active_rooms[room_code]:
                del self.active_rooms[room_code]

    async def send_personal_message(self, room_code: str, player_name: str, message: Dict[str, Any]):
        """Sends a JSON message to a specific player in a room."""
        room_code = room_code.upper()
        if room_code in self.active_rooms and player_name in self.active_rooms[room_code]:
            ws = self.active_rooms[room_code][player_name]
            try:
                await ws.send_text(json.dumps(message))
            except Exception as e:
                logger.warning(f"Failed sending personal message to '{player_name}': {e}")

    async def broadcast(self, room_code: str, message: Dict[str, Any]):
        """Broadcasts a JSON message to all active players in a room."""
        room_code = room_code.upper()
        if room_code not in self.active_rooms:
            return

        payload = json.dumps(message)
        dead_connections: List[str] = []

        for p_name, ws in self.active_rooms[room_code].items():
            try:
                await ws.send_text(payload)
            except Exception as e:
                logger.warning(f"Error broadcasting to {p_name} in {room_code}: {e}")
                dead_connections.append(p_name)

        # Cleanup failed connections
        for dead_player in dead_connections:
            self.disconnect(room_code, dead_player)


manager = ConnectionManager()
