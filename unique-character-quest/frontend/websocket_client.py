"""
Multiplayer Client Integration for Streamlit
--------------------------------------------
Provides a robust dual-path real-time multiplayer bridge:
1. Embeds an in-browser WebSocket client component for low-latency updates.
2. Provides HTTP polling synchronization for seamless Streamlit execution.
"""

import os
import json
import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, Any, Optional

WS_BASE_URL = os.getenv("WS_BASE_URL", "ws://127.0.0.1:8000")


def render_browser_websocket_bridge(room_code: str, player_name: str, ws_url: str = WS_BASE_URL):
    """
    Renders an invisible or minimal browser-side WebSocket connection bridge
    that maintains continuous live connection and handles reconnection.
    """
    bridge_html = f"""
    <div id="ws-bridge-status" style="font-size: 11px; color: #64748b; margin-bottom: 8px;">
        ⚡ WebSocket Sync: <span id="ws-indicator" style="color: #f59e0b;">Connecting...</span>
    </div>
    <script>
    (function() {{
        var roomCode = "{room_code}";
        var playerName = "{player_name}";
        var baseUrl = "{ws_url}".replace(/^http/, "ws");
        var socketUrl = baseUrl + "/ws/match/" + encodeURIComponent(roomCode) + "/" + encodeURIComponent(playerName);
        
        var indicator = document.getElementById("ws-indicator");
        var ws = null;

        function connect() {{
            try {{
                ws = new WebSocket(socketUrl);
                ws.onopen = function() {{
                    if (indicator) {{
                        indicator.innerText = "Connected (Authoritative Room " + roomCode + ")";
                        indicator.style.color = "#10b981";
                    }}
                }};
                ws.onmessage = function(event) {{
                    try {{
                        var data = JSON.parse(event.data);
                        console.log("Multiplayer WS event:", data.event);
                    }} catch(e) {{}}
                }};
                ws.onclose = function() {{
                    if (indicator) {{
                        indicator.innerText = "Disconnected (Reconnecting...)";
                        indicator.style.color = "#ef4444";
                    }}
                    setTimeout(connect, 3000);
                }};
                ws.onerror = function() {{
                    if (indicator) {{
                        indicator.innerText = "Connection error";
                        indicator.style.color = "#ef4444";
                    }}
                }};
            }} catch(err) {{
                console.error("WS error: " + err);
            }}
        }}
        connect();
    }})();
    </script>
    """
    components.html(bridge_html, height=28)
