"""
Reusable UI Components and Web Audio Synthesizer for Unique Character Quest
----------------------------------------------------------------------------
Implements modular visual components and synthesizer audio playback.
Zero external audio files required: leverages HTML5 Web Audio API oscillators.
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, Any, List, Optional
from .styles import get_character_tiles_html, get_arcade_header_html


def play_audio_synth(sound_type: str):
    """
    Synthesizes arcade sound effects using the browser's native Web Audio API.
    Guarantees reliable playback without relying on external MP3/WAV files.
    """
    js_code = f"""
    <script>
    (function() {{
        try {{
            var AudioContext = window.AudioContext || window.webkitAudioContext;
            if (!AudioContext) return;
            var ctx = new AudioContext();
            var now = ctx.currentTime;

            function playTone(freq, type, start, duration, gainVal) {{
                var osc = ctx.createOscillator();
                var gain = ctx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(freq, start);
                gain.gain.setValueAtTime(gainVal, start);
                gain.gain.exponentialRampToValueAtTime(0.0001, start + duration);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(start);
                osc.stop(start + duration);
            }}

            var sound = "{sound_type}";
            if (sound === "correct") {{
                // Bright ascending major chord
                playTone(523.25, "sine", now, 0.12, 0.2);        // C5
                playTone(659.25, "sine", now + 0.08, 0.15, 0.25); // E5
                playTone(783.99, "sine", now + 0.16, 0.25, 0.3);  // G5
            }} else if (sound === "incorrect") {{
                // Low descending buzz
                playTone(220.0, "sawtooth", now, 0.18, 0.25);
                playTone(174.6, "sawtooth", now + 0.12, 0.28, 0.25);
            }} else if (sound === "game_over") {{
                // Retro game-over descent
                playTone(392.0, "triangle", now, 0.2, 0.3);
                playTone(329.6, "triangle", now + 0.18, 0.2, 0.3);
                playTone(261.6, "triangle", now + 0.36, 0.2, 0.3);
                playTone(196.0, "triangle", now + 0.54, 0.4, 0.35);
            }} else if (sound === "level_up") {{
                // Fanfare
                playTone(440, "square", now, 0.1, 0.15);
                playTone(554.37, "square", now + 0.09, 0.1, 0.15);
                playTone(659.25, "square", now + 0.18, 0.1, 0.15);
                playTone(880, "square", now + 0.27, 0.35, 0.2);
            }} else if (sound === "achievement") {{
                // Shimmering chimes
                playTone(659.25, "sine", now, 0.1, 0.2);
                playTone(830.61, "sine", now + 0.08, 0.1, 0.2);
                playTone(987.77, "sine", now + 0.16, 0.1, 0.2);
                playTone(1318.5, "sine", now + 0.24, 0.3, 0.25);
            }} else if (sound === "tick") {{
                playTone(800, "triangle", now, 0.03, 0.05);
            }}
        }} catch(e) {{
            console.log("Audio synthesis notice: " + e);
        }}
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)


def render_explanation_box(explanation: str, frequencies: Dict[str, int], correct_answer: str):
    """Renders visual frequency distribution and post-round algorithmic justification."""
    st.markdown("### 🔍 Algorithmic Explanation & Analysis")
    
    st.info(explanation)

    st.markdown("#### 📊 Character Frequency Map:")
    freq_badges = []
    for ch, count in frequencies.items():
        disp = ch if not ch.isspace() else "␣"
        css_class = "freq-one" if count == 1 else "freq-multi"
        star = " ★ FIRST UNIQUE" if ch == correct_answer else (" (unique)" if count == 1 else "")
        freq_badges.append(f'<span class="freq-badge {css_class}">\'{disp}\': {count}{star}</span>')

    st.markdown(f'<div style="margin: 10px 0;">{"".join(freq_badges)}</div>', unsafe_allow_html=True)


def render_leaderboard_table(leaderboard: List[Dict[str, Any]]):
    """Renders formatted arcade leaderboard table."""
    if not leaderboard:
        st.markdown("*No leaderboard records found yet. Play a game to claim 1st place!*")
        return

    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    
    rows = []
    for item in leaderboard:
        rank = item.get("rank", 1)
        rank_badge = medals.get(rank, f"#{rank}")
        rows.append({
            "Rank": rank_badge,
            "Player": item.get("player_name"),
            "High Score": f"{item.get('highest_score', 0):,}",
            "Games": item.get("total_games", 0),
            "Correct": item.get("total_correct", 0),
            "Accuracy": f"{item.get('accuracy', 0.0):.1f}%"
        })

    st.table(rows)


def render_achievements_display(achievements: List[Dict[str, Any]]):
    """Renders badges grid for all available achievements."""
    cols = st.columns(2)
    for idx, ach in enumerate(achievements):
        col = cols[idx % 2]
        is_unlocked = ach.get("unlocked", False)
        bg = "rgba(16, 185, 129, 0.15)" if is_unlocked else "rgba(30, 20, 56, 0.4)"
        border = "#10b981" if is_unlocked else "#475569"
        status_txt = f"<span style='color: #34d399;'>Unlocked: {ach.get('unlocked_at', '')}</span>" if is_unlocked else "<span style='color: #64748b;'>Locked</span>"
        
        with col:
            st.markdown(f"""
            <div style="background: {bg}; border: 1px solid {border}; border-radius: 12px; padding: 14px; margin-bottom: 12px;">
                <div style="font-size: 24px; float: left; margin-right: 12px;">{ach.get('icon', '🏆')}</div>
                <div style="font-weight: 800; font-size: 16px; color: #f8fafc;">{ach.get('title')} (+{ach.get('points')} pts)</div>
                <div style="font-size: 13px; color: #94a3b8; margin: 4px 0;">{ach.get('description')}</div>
                <div style="font-size: 11px; font-weight: bold;">{status_txt}</div>
            </div>
            """, unsafe_allow_html=True)
