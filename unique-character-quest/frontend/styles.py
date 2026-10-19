"""
Custom Arcade Styling for Unique Character Quest
------------------------------------------------
Provides CSS styles for an energetic, colorful, arcade-inspired game interface
featuring purple, cyan, electric blue, amber, and emerald accents.
"""

ARCADE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Outfit:wght@400;600;700;900&display=swap');

/* Main Container Theming */
.stApp {
    background: radial-gradient(circle at 50% 10%, #1e1338 0%, #0d081f 50%, #06040d 100%);
    color: #f1f5f9;
    font-family: 'Outfit', sans-serif;
}

/* Typography Overrides */
h1, h2, h3 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.arcade-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 26px;
    background: linear-gradient(135deg, #a855f7 0%, #06b6d4 50%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 24px rgba(168, 85, 247, 0.4);
    text-align: center;
    margin-bottom: 8px;
}

.arcade-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 15px;
    margin-bottom: 24px;
}

/* Glassmorphism Cards */
.arcade-card {
    background: rgba(30, 20, 56, 0.65);
    border: 1px solid rgba(168, 85, 247, 0.3);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(12px);
    margin-bottom: 20px;
}

/* Character Tiles */
.character-sequence-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 12px;
    padding: 24px;
    background: rgba(15, 10, 30, 0.7);
    border-radius: 20px;
    border: 2px dashed rgba(6, 182, 212, 0.4);
    margin: 20px 0;
}

.character-tile {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-width: 54px;
    height: 64px;
    background: linear-gradient(180deg, #2e1d5e 0%, #170d38 100%);
    border: 2px solid #a855f7;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(168, 85, 247, 0.35), inset 0 2px 4px rgba(255, 255, 255, 0.2);
    transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.character-tile:hover {
    transform: translateY(-4px) scale(1.05);
    border-color: #06b6d4;
    box-shadow: 0 8px 20px rgba(6, 182, 212, 0.45);
}

.tile-char {
    font-size: 28px;
    font-weight: 900;
    color: #ffffff;
    line-height: 1;
}

.tile-idx {
    font-size: 10px;
    color: #94a3b8;
    margin-top: 4px;
    font-family: monospace;
}

/* Stat Badges */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 9999px;
    font-weight: 700;
    font-size: 14px;
}

.stat-pill-lives {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    color: #f87171;
}

.stat-pill-score {
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: #fbbf24;
}

.stat-pill-streak {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34d399;
}

.stat-pill-timer {
    background: rgba(6, 182, 212, 0.15);
    border: 1px solid rgba(6, 182, 212, 0.4);
    color: #38bdf8;
}

/* Frequency Table */
.freq-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 8px;
    font-weight: bold;
    font-family: monospace;
    margin: 3px;
}
.freq-one {
    background: rgba(16, 185, 129, 0.25);
    border: 1px solid #10b981;
    color: #34d399;
}
.freq-multi {
    background: rgba(239, 68, 68, 0.2);
    border: 1px solid #ef4444;
    color: #fca5a5;
}

/* Streamlit button overrides */
div.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    font-size: 16px;
    padding: 10px 24px;
    transition: all 0.2s ease;
    border: 1px solid rgba(168, 85, 247, 0.5);
    background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%);
    color: white;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5);
    border-color: #06b6d4;
}

/* Option Buttons Grid */
.option-btn-container div.stButton > button {
    height: 64px;
    font-size: 22px;
    font-weight: 900;
    background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 100%);
    border: 2px solid #6366f1;
}

.option-btn-container div.stButton > button:hover {
    border-color: #22d3ee;
    background: linear-gradient(180deg, #312e81 0%, #1e1b4b 100%);
}
</style>
"""


def get_arcade_header_html(player_name: str, score: int, lives: int, streak: int, timer: Optional[float] = None) -> str:
    """Generates the top game HUD banner HTML."""
    lives_hearts = "❤️ " * lives + "🖤 " * max(0, 3 - lives)
    timer_html = ""
    if timer is not None:
        timer_html = f'<div class="stat-pill stat-pill-timer">⏱️ {int(timer)}s</div>'

    return f"""
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 20px; padding: 12px 20px; background: rgba(20, 15, 38, 0.7); border-radius: 16px; border: 1px solid rgba(168, 85, 247, 0.3);">
        <div style="font-weight: 800; font-size: 16px; color: #e2e8f0;">
            👾 <span style="color: #a855f7;">Player:</span> {player_name}
        </div>
        <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <div class="stat-pill stat-pill-score">🏆 {score} pts</div>
            <div class="stat-pill stat-pill-lives">{lives_hearts}</div>
            <div class="stat-pill stat-pill-streak">🔥 Streak: {streak}</div>
            {timer_html}
        </div>
    </div>
    """


def get_character_tiles_html(sequence: str) -> str:
    """Renders interactive sequence tiles with position indices."""
    tiles = []
    for idx, char in enumerate(sequence):
        disp_char = char if not char.isspace() else "␣"
        tiles.append(f"""
        <div class="character-tile">
            <span class="tile-char">{disp_char}</span>
            <span class="tile-idx">{idx}</span>
        </div>
        """)
    return f"""
    <div class="character-sequence-container">
        {"".join(tiles)}
    </div>
    """
