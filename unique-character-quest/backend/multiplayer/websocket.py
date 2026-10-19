"""
FastAPI WebSocket Router for Real-Time Multiplayer Gameplay
-----------------------------------------------------------
Processes incoming WebSocket connections from clients, routes commands,
synchronizes room states, and broadcasts live events.
"""

import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from .connection_manager import manager
from .rooms import room_manager
from ..database import SessionLocal, save_match_result

logger = logging.getLogger("multiplayer.websocket")
ws_router = APIRouter()


@ws_router.websocket("/ws/match/{room_code}/{player_name}")
async def match_websocket_endpoint(websocket: WebSocket, room_code: str, player_name: str):
    """
    Main WebSocket endpoint for multiplayer communication.
    
    Path params:
    - room_code: 6-character room identifier.
    - player_name: Display name of the connecting player.
    """
    room_code = room_code.upper()
    player_name = player_name.strip()

    room = room_manager.get_room(room_code)
    if not room:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Room does not exist.")
        return

    # Join room in state machine
    success, msg = room.add_player(player_name)
    if not success:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason=msg)
        return

    # Accept connection and register in manager
    await manager.connect(room_code, player_name, websocket)

    try:
        # Broadcast player joined to entire room
        await manager.broadcast(room_code, {
            "event": "player_joined",
            "player_name": player_name,
            "state": room.to_client_payload()
        })

        while True:
            # Check deadline expiry on tick/poll
            if room.status == "in_round" and room.check_deadline_and_resolve():
                await manager.broadcast(room_code, {
                    "event": "round_ended",
                    "reason": "deadline_expired",
                    "state": room.to_client_payload()
                })

            data_str = await websocket.receive_text()
            try:
                data = json.loads(data_str)
            except Exception:
                await websocket.send_text(json.dumps({"error": "Malformed JSON payload"}))
                continue

            action = data.get("action")

            if action == "ping":
                # Heartbeat and time sync
                room.check_deadline_and_resolve()
                await websocket.send_text(json.dumps({
                    "event": "pong",
                    "state": room.to_client_payload(player_name)
                }))

            elif action == "start_match":
                # Only the room host can initiate the match
                if player_name != room.host_name:
                    await websocket.send_text(json.dumps({"error": "Only the host can start the match."}))
                    continue

                ok, start_msg = room.start_match()
                if ok:
                    await manager.broadcast(room_code, {
                        "event": "match_started",
                        "state": room.to_client_payload()
                    })
                else:
                    await websocket.send_text(json.dumps({"error": start_msg}))

            elif action == "submit_answer":
                answer = data.get("answer", "")
                ok, sub_msg = room.submit_answer(player_name, answer)
                
                if ok:
                    # Notify everyone that this player submitted
                    await manager.broadcast(room_code, {
                        "event": "player_submitted",
                        "player_name": player_name,
                        "state": room.to_client_payload()
                    })
                    # If submitting closed the round, broadcast round recap
                    if room.status == "round_recap":
                        await manager.broadcast(room_code, {
                            "event": "round_ended",
                            "reason": "all_submitted",
                            "state": room.to_client_payload()
                        })
                else:
                    await websocket.send_text(json.dumps({"error": sub_msg}))

            elif action == "next_round":
                # Advance from round recap to next round
                if player_name != room.host_name:
                    await websocket.send_text(json.dumps({"error": "Only the host can trigger the next round."}))
                    continue

                if room.status == "round_recap":
                    room.next_round()
                    if room.status == "match_finished":
                        # Persist multiplayer results to database
                        persist_multiplayer_records(room)
                        await manager.broadcast(room_code, {
                            "event": "match_finished",
                            "winner": room.winner,
                            "state": room.to_client_payload()
                        })
                    else:
                        await manager.broadcast(room_code, {
                            "event": "round_started",
                            "state": room.to_client_payload()
                        })

            elif action == "get_state":
                await websocket.send_text(json.dumps({
                    "event": "state_sync",
                    "state": room.to_client_payload(player_name)
                }))

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for {player_name} in {room_code}")
        manager.disconnect(room_code, player_name)
        room.remove_player(player_name)
        await manager.broadcast(room_code, {
            "event": "player_left",
            "player_name": player_name,
            "state": room.to_client_payload()
        })
    except Exception as e:
        logger.error(f"Unexpected WebSocket error in {room_code} for {player_name}: {e}")
        manager.disconnect(room_code, player_name)
        room.remove_player(player_name)


def persist_multiplayer_records(room):
    """Saves match outcomes for all participants to the persistent database."""
    try:
        db = SessionLocal()
        for p in room.players.values():
            result_str = "WON" if p.player_name == room.winner else "COMPLETED"
            save_match_result(
                db=db,
                player_name=p.player_name,
                mode="multiplayer",
                difficulty=room.difficulty,
                score=p.score,
                accuracy=100.0,  # aggregate placeholder
                questions_answered=room.total_rounds,
                correct_answers=max(0, p.score // 100),
                levels_completed=room.total_rounds,
                match_result=result_str,
                duration_seconds=room.total_rounds * room.round_duration,
                hints_used=0
            )
        db.close()
    except Exception as e:
        logger.error(f"Failed to persist multiplayer match results: {e}")
