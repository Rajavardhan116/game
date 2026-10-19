"""
Unique Character Quest - Main Streamlit Application
---------------------------------------------------
A colorful, arcade-style educational web game centered on the
First Non-Repeating Character algorithm with real-time multiplayer,
scoring, lives, persistent SQLite leaderboards, and educational tools.
"""

import time
import os
import streamlit as st

# Configure Streamlit page layout and title
st.set_page_config(
    page_title="Unique Character Quest",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import internal modules
from frontend.styles import ARCADE_CSS, get_arcade_header_html, get_character_tiles_html
from frontend.components import (
    play_audio_synth,
    render_explanation_box,
    render_leaderboard_table,
    render_achievements_display
)
from frontend.api_client import api_client
from frontend.websocket_client import render_browser_websocket_bridge
from backend.game.algorithms import (
    first_non_repeating_frequency,
    first_non_repeating_nested,
    explain_first_non_repeating
)
from backend.game.questions import generate_question, DIFFICULTY_CONFIGS
from backend.game.scoring import evaluate_answer_submission
from backend.game.validation import validate_player_name, validate_room_code
from backend.database import init_db, SessionLocal, save_match_result, get_leaderboard, get_player_achievements_list, get_player_history
from backend.multiplayer.rooms import room_manager

# Ensure SQLite schema is prepared
try:
    init_db()
except Exception:
    pass

# Inject custom CSS
st.markdown(ARCADE_CSS, unsafe_allow_html=True)


# -------------------------------------------------------------
# Session State Initialization
# -------------------------------------------------------------
def init_session_state():
    defaults = {
        "screen": "home",  # home, tutorial, profile, mode_select, settings, gameplay, game_over, results, leaderboard, achievements, history, multiplayer_lobby, multiplayer_game, algorithm_lab
        "player_name": "Player1",
        "sound_enabled": True,
        "mode": "classic",
        "difficulty": "easy",
        "score": 0,
        "lives": 3,
        "streak": 0,
        "hints_used": 0,
        "current_question_index": 1,
        "total_questions": 5,
        "current_question": None,
        "question_start_time": time.time(),
        "last_answer_result": None,
        "show_feedback": False,
        "history": [],
        "room_code": "",
        "is_host": False,
        "multiplayer_active": False,
        "seed": 42
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session_state()


# Sound trigger helper
def trigger_sound(sound_name: str):
    if st.session_state.get("sound_enabled", True):
        play_audio_synth(sound_name)


# -------------------------------------------------------------
# Navigation Sidebar
# -------------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="arcade-title" style="font-size: 16px;">🧩 QUEST NAV</div>', unsafe_allow_html=True)
    st.markdown(f"**👤 Current Player:** `{st.session_state.player_name}`")
    st.markdown("---")

    nav_options = [
        ("🏠 Home & Play", "home"),
        ("🎮 Game Modes", "mode_select"),
        ("⚔️ Online Multiplayer", "multiplayer_lobby"),
        ("🧪 Algorithm Lab", "algorithm_lab"),
        ("📖 Tutorial & Rules", "tutorial"),
        ("🏆 Leaderboard", "leaderboard"),
        ("🎖️ Achievements", "achievements"),
        ("📜 Match History", "history"),
        ("⚙️ Settings", "settings")
    ]

    for label, target_screen in nav_options:
        if st.button(label, use_container_width=True):
            st.session_state.screen = target_screen
            st.rerun()

    st.markdown("---")
    sound_toggle = st.checkbox("🔊 Sound Effects", value=st.session_state.sound_enabled)
    if sound_toggle != st.session_state.sound_enabled:
        st.session_state.sound_enabled = sound_toggle
        st.rerun()

    st.markdown("---")
    st.caption("Capstone Project: *Unique Character Quest*\nAlgorithm: First Non-Repeating Character\nStack: Python, FastAPI, WebSockets, Streamlit, SQLite.")


# -------------------------------------------------------------
# SCREEN 1: Home Screen
# -------------------------------------------------------------
if st.session_state.screen == "home":
    st.markdown('<h1 class="arcade-title">UNIQUE CHARACTER QUEST</h1>', unsafe_allow_html=True)
    st.markdown('<div class="arcade-subtitle">The Arcade Puzzle Game of Sequences and Singletons</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        <div class="arcade-card">
            <h3>⚡ Welcome, Code Detective!</h3>
            <p>Every character sequence hides a mystery. Your quest is simple yet profound:
            <strong>find the very first character that appears exactly once</strong> from left to right!</p>
            <p>Explore classic puzzles, test your reflexes in the Speed Challenge, unravel trick edge-cases,
            or battle your friends in real-time online multiplayer.</p>
        </div>
        """, unsafe_allow_html=True)

        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("🚀 Start Playing Now", use_container_width=True):
                st.session_state.screen = "mode_select"
                st.rerun()
        with btn_c2:
            if st.button("⚔️ Multiplayer Battle", use_container_width=True):
                st.session_state.screen = "multiplayer_lobby"
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🧪 Enter Algorithm Laboratory", use_container_width=True):
            st.session_state.screen = "algorithm_lab"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="arcade-card">
            <h3>👤 Player Identity</h3>
            <p>Set your player handle to track personal high scores, unlock achievements, and join rooms:</p>
        </div>
        """, unsafe_allow_html=True)

        new_name = st.text_input("Enter Display Name:", value=st.session_state.player_name, max_chars=20)
        if st.button("Save Player Handle", use_container_width=True):
            val_ok, sanitized = validate_player_name(new_name)
            if val_ok:
                st.session_state.player_name = sanitized
                # Try creating/fetching player on backend/DB
                db = SessionLocal()
                try:
                    from backend.database import get_or_create_player
                    get_or_create_player(db, sanitized)
                finally:
                    db.close()
                st.success(f"Player handle saved as '{sanitized}'!")
                trigger_sound("click")
            else:
                st.error(sanitized)


# -------------------------------------------------------------
# SCREEN 2: Tutorial & Instructions
# -------------------------------------------------------------
elif st.session_state.screen == "tutorial":
    st.markdown('<h1 class="arcade-title">📖 HOW TO PLAY & RULES</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="arcade-card">
        <h3>🎯 The Core Objective</h3>
        <p>In every puzzle, you are presented with a character sequence. Your job is to identify the <strong>first non-repeating character</strong>.</p>
        <ul>
            <li><strong>Order Matters:</strong> We scan characters strictly from left to right.</li>
            <li><strong>Singleton Only:</strong> A qualifying character must have a total occurrence count of exactly <strong>1</strong>.</li>
            <li><strong>Multiple Uniques:</strong> If several characters appear only once (e.g., in <code>"aabbcd"</code>, both <code>'c'</code> and <code>'d'</code> are unique), the correct answer is the <em>earliest</em> one (<code>'c'</code>).</li>
            <li><strong>The "None" Edge Case:</strong> If every character repeats (e.g., in <code>"aabb"</code> or <code>"swiss"</code> with all repeats), select the special option <strong>"None"</strong>!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="arcade-card">
            <h4>🏆 Scoring & Multipliers</h4>
            <ul>
                <li><strong>Correct Answer:</strong> +100 to +300 points based on difficulty.</li>
                <li><strong>Speed Bonus:</strong> Up to +50% extra points for quick responses.</li>
                <li><strong>Streak Multiplier:</strong> Consecutive correct answers add +20 bonus per streak level.</li>
                <li><strong>Lives:</strong> Start with 3 lives. An incorrect answer or timeout deducts 1 life.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="arcade-card">
            <h4>⏱️ Game Modes</h4>
            <ul>
                <li><strong>Classic Challenge:</strong> 5 progressive levels from introductory to expert.</li>
                <li><strong>Speed Challenge:</strong> High-octane round countdown with accelerated scoring.</li>
                <li><strong>Puzzle Challenge:</strong> Tricky algorithmic edge cases, palindromes, and "None" sequences.</li>
                <li><strong>Online Multiplayer:</strong> Synchronized room-based competition across devices.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    if st.button("⬅️ Back to Menu", use_container_width=True):
        st.session_state.screen = "home"
        st.rerun()


# -------------------------------------------------------------
# SCREEN 4: Game Mode Selection
# -------------------------------------------------------------
elif st.session_state.screen == "mode_select":
    st.markdown('<h1 class="arcade-title">🎮 SELECT GAME MODE</h1>', unsafe_allow_html=True)
    st.markdown('<div class="arcade-subtitle">Choose your challenge type and difficulty tier</div>', unsafe_allow_html=True)

    diff = st.select_slider(
        "Select Difficulty Level:",
        options=["easy", "medium", "hard", "expert"],
        value=st.session_state.difficulty,
        format_func=lambda x: x.upper()
    )
    st.session_state.difficulty = diff

    cfg = DIFFICULTY_CONFIGS[diff]
    st.info(f"📊 **{diff.upper()} Difficulty Settings:** Time Limit: {cfg['time_limit']}s | Base Reward: {cfg['base_points']} pts | Sequence Length: {cfg['min_len']}-{cfg['max_len']} chars")

    m_col1, m_col2, m_col3 = st.columns(3)

    def start_single_player_session(selected_mode: str):
        st.session_state.mode = selected_mode
        st.session_state.score = 0
        st.session_state.lives = 2 if selected_mode == "speed" else 3
        st.session_state.streak = 0
        st.session_state.hints_used = 0
        st.session_state.current_question_index = 1
        st.session_state.total_questions = 8 if selected_mode == "speed" else (6 if selected_mode == "puzzle" else 5)
        st.session_state.history = []
        st.session_state.show_feedback = False
        st.session_state.last_answer_result = None

        # Generate 1st question
        q = generate_question(
            difficulty=st.session_state.difficulty,
            seed=None,
            question_index=1,
            force_curated=(selected_mode == "puzzle")
        )
        st.session_state.current_question = q
        st.session_state.question_start_time = time.time()
        st.session_state.screen = "gameplay"
        trigger_sound("click")
        st.rerun()

    with m_col1:
        st.markdown("""
        <div class="arcade-card">
            <h3>🌟 Classic Quest</h3>
            <p>Balanced puzzle progression with 5 questions ramping from easy to expert. Perfect for sharpening your pattern recognition.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Play Classic", use_container_width=True):
            start_single_player_session("classic")

    with m_col2:
        st.markdown("""
        <div class="arcade-card">
            <h3>⚡ Speed Challenge</h3>
            <p>Race against the countdown timer! Earn massive speed bonuses for quick single-pass mental evaluations.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Play Speed", use_container_width=True):
            start_single_player_session("speed")

    with m_col3:
        st.markdown("""
        <div class="arcade-card">
            <h3>🧩 Puzzle Challenge</h3>
            <p>Hand-crafted tricky sequences with multiple unique candidates, all-repeating strings, and edge-cases.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Play Puzzle", use_container_width=True):
            start_single_player_session("puzzle")


# -------------------------------------------------------------
# SCREEN 6 & MULTIPLAYER LOBBY
# -------------------------------------------------------------
elif st.session_state.screen == "multiplayer_lobby":
    st.markdown('<h1 class="arcade-title">⚔️ ONLINE MULTIPLAYER</h1>', unsafe_allow_html=True)
    st.markdown('<div class="arcade-subtitle">Real-time synchronized multiplayer across separate devices</div>', unsafe_allow_html=True)

    tab_create, tab_join = st.tabs(["Create Match Room", "Join Existing Room"])

    with tab_create:
        st.markdown("### Host a New Room")
        c_diff = st.selectbox("Match Difficulty", ["easy", "medium", "hard", "expert"], index=1)
        c_rounds = st.slider("Rounds to Play", min_value=3, max_value=10, value=5)
        c_time = st.slider("Seconds Per Round", min_value=8, max_value=30, value=15)

        if st.button("Create Room & Generate Code", use_container_width=True):
            room = room_manager.create_room(
                host_name=st.session_state.player_name,
                difficulty=c_diff,
                total_rounds=c_rounds,
                round_duration=c_time
            )
            st.session_state.room_code = room.room_code
            st.session_state.is_host = True
            st.session_state.screen = "multiplayer_game"
            trigger_sound("level_up")
            st.rerun()

    with tab_join:
        st.markdown("### Join a Friend's Room")
        join_code_in = st.text_input("Enter 6-Character Room Code:", max_chars=8).upper().strip()
        if st.button("Join Room", use_container_width=True):
            val_ok, clean_code = validate_room_code(join_code_in)
            if not val_ok:
                st.error(clean_code)
            else:
                room = room_manager.get_room(clean_code)
                if not room:
                    st.error("Room code not found! Check code and try again.")
                else:
                    ok, msg = room.add_player(st.session_state.player_name)
                    if ok:
                        st.session_state.room_code = clean_code
                        st.session_state.is_host = False
                        st.session_state.screen = "multiplayer_game"
                        trigger_sound("click")
                        st.rerun()
                    else:
                        st.error(msg)


# -------------------------------------------------------------
# MULTIPLAYER MATCH SCREEN
# -------------------------------------------------------------
elif st.session_state.screen == "multiplayer_game":
    room_code = st.session_state.room_code
    room = room_manager.get_room(room_code)

    if not room:
        st.error(f"Room '{room_code}' is no longer active.")
        if st.button("Back to Lobby"):
            st.session_state.screen = "multiplayer_lobby"
            st.rerun()
    else:
        # Check deadline update
        room.check_deadline_and_resolve()
        
        # Render real WebSocket bridge
        render_browser_websocket_bridge(room_code, st.session_state.player_name)

        st.markdown(f'<div class="arcade-card"><h2>Room: <span style="color:#06b6d4;">{room_code}</span> | Host: {room.host_name}</h2></div>', unsafe_allow_html=True)

        # STATE 1: Waiting Lobby
        if room.status == "waiting":
            st.info("🕒 Waiting for players to join... Share your Room Code!")
            st.markdown(f"### Share this Room Code: `{room_code}`")

            st.markdown("#### 👥 Players in Room:")
            for p in room.players.values():
                host_badge = " (Host)" if p.is_host else ""
                st.markdown(f"- **{p.player_name}**{host_badge}")

            c1, c2 = st.columns(2)
            with c1:
                if st.session_state.is_host:
                    if st.button("🚀 Start Match Now", use_container_width=True):
                        room.start_match()
                        trigger_sound("level_up")
                        st.rerun()
                else:
                    st.caption("Waiting for host to start the game...")
            with c2:
                if st.button("🔄 Refresh Lobby", use_container_width=True):
                    st.rerun()

        # STATE 2: In Round
        elif room.status == "in_round":
            rem_secs = room.get_seconds_remaining()
            q = room.current_question

            st.markdown(f"### Round {room.current_round} of {room.total_rounds} | ⏱️ Time: **{rem_secs:.1f}s**")
            st.progress(max(0.0, min(1.0, rem_secs / room.round_duration)))

            if q:
                st.markdown(get_character_tiles_html(q.sequence), unsafe_allow_html=True)

                player = room.players.get(st.session_state.player_name)
                has_submitted = player.has_submitted if player else False

                if has_submitted:
                    st.success(f"✅ Your answer '{player.submitted_answer}' has been registered! Waiting for other players...")
                else:
                    st.markdown("#### Choose the first non-repeating character:")
                    cols = st.columns(len(q.options))
                    for idx, opt in enumerate(q.options):
                        with cols[idx]:
                            if st.button(f"{opt}", key=f"mp_opt_{idx}", use_container_width=True):
                                room.submit_answer(st.session_state.player_name, opt)
                                trigger_sound("click")
                                st.rerun()

            # Poll/refresh button
            time.sleep(1)
            st.rerun()

        # STATE 3: Round Recap
        elif room.status == "round_recap":
            st.markdown(f"### 📋 Round {room.current_round} Summary")
            recap = room.latest_recap
            if recap:
                st.success(f"**Correct Answer:** `{recap.correct_answer}`")
                st.info(recap.explanation)

                st.markdown("#### Round Results:")
                for p_name, ans_info in recap.player_answers.items():
                    status_icon = "✅" if ans_info["is_correct"] else "❌"
                    st.markdown(f"- {status_icon} **{p_name}**: answered `{ans_info['answer']}` ({ans_info['time_taken']}s) → +{ans_info['points_earned']} pts")

            if st.session_state.is_host:
                if st.button("➡️ Next Round", use_container_width=True):
                    room.next_round()
                    if room.status == "match_finished":
                        # Persist multiplayer results
                        from backend.multiplayer.websocket import persist_multiplayer_records
                        persist_multiplayer_records(room)
                    st.rerun()
            else:
                st.caption("Waiting for host to continue...")
                if st.button("🔄 Refresh"):
                    st.rerun()

        # STATE 4: Match Finished
        elif room.status == "match_finished":
            st.markdown(f'<h2 style="color: #10b981;">🎉 MATCH COMPLETE!</h2>', unsafe_allow_html=True)
            st.balloons()
            trigger_sound("achievement")

            st.markdown(f"### 👑 Winner: **{room.winner}**")

            st.markdown("#### 🏆 Final Standings:")
            sorted_players = sorted(room.players.values(), key=lambda x: x.score, reverse=True)
            for rank, p in enumerate(sorted_players, start=1):
                st.markdown(f"**#{rank} {p.player_name}** — Score: `{p.score}` pts | Remaining Lives: `{p.lives}`")

            if st.button("Return to Lobby", use_container_width=True):
                st.session_state.screen = "multiplayer_lobby"
                st.rerun()


# -------------------------------------------------------------
# SCREEN 7: Single-Player Main Gameplay
# -------------------------------------------------------------
elif st.session_state.screen == "gameplay":
    q = st.session_state.current_question
    if not q:
        st.session_state.screen = "mode_select"
        st.rerun()

    # Time tracking
    elapsed = time.time() - st.session_state.question_start_time
    remaining = max(0.0, q.time_limit_seconds - elapsed)

    # Render HUD
    st.markdown(
        get_arcade_header_html(
            player_name=st.session_state.player_name,
            score=st.session_state.score,
            lives=st.session_state.lives,
            streak=st.session_state.streak,
            timer=remaining
        ),
        unsafe_allow_html=True
    )

    st.markdown(f"**Round {st.session_state.current_question_index} of {st.session_state.total_questions}** | *Difficulty: {q.difficulty.upper()}*")
    st.progress(max(0.0, min(1.0, remaining / q.time_limit_seconds)))

    # Render Arcade Character Sequence Tiles
    st.markdown(get_character_tiles_html(q.sequence), unsafe_allow_html=True)

    # Feedback Box if answered
    if st.session_state.show_feedback and st.session_state.last_answer_result:
        res = st.session_state.last_answer_result
        if res.is_correct:
            st.success(f"🎉 {res.explanation}")
        else:
            st.error(f"💥 {res.explanation}")

        # Render algorithmic breakdown
        freqs = explain_first_non_repeating(q.sequence)["frequencies"]
        render_explanation_box(q.explanation or "", freqs, q.correct_answer)

        if st.button("➡️ Continue Next Question", use_container_width=True):
            st.session_state.show_feedback = False
            st.session_state.last_answer_result = None

            # Advance or end
            if st.session_state.lives <= 0:
                st.session_state.screen = "game_over"
                trigger_sound("game_over")
            elif st.session_state.current_question_index >= st.session_state.total_questions:
                st.session_state.screen = "results"
                trigger_sound("level_up")
            else:
                st.session_state.current_question_index += 1
                next_diff = st.session_state.difficulty
                if st.session_state.mode == "classic":
                    prog = ["easy", "easy", "medium", "hard", "expert"]
                    next_diff = prog[min(len(prog)-1, st.session_state.current_question_index-1)]

                st.session_state.current_question = generate_question(
                    difficulty=next_diff,
                    question_index=st.session_state.current_question_index,
                    force_curated=(st.session_state.mode == "puzzle")
                )
                st.session_state.question_start_time = time.time()

            st.rerun()

    else:
        # Answering controls
        st.markdown("#### Select the First Non-Repeating Character:")
        cols = st.columns(len(q.options))
        
        for idx, option in enumerate(q.options):
            with cols[idx]:
                if st.button(f"{option}", key=f"btn_opt_{idx}", use_container_width=True):
                    time_taken = time.time() - st.session_state.question_start_time
                    eval_res = evaluate_answer_submission(
                        submitted_answer=option,
                        correct_answer=q.correct_answer,
                        time_taken=time_taken,
                        time_limit=q.time_limit_seconds,
                        current_lives=st.session_state.lives,
                        current_streak=st.session_state.streak,
                        base_points=q.base_points,
                        hint_used=False
                    )

                    # Update session
                    st.session_state.score += eval_res.total_delta
                    st.session_state.lives = eval_res.lives_remaining
                    st.session_state.streak = eval_res.new_streak
                    st.session_state.last_answer_result = eval_res
                    st.session_state.show_feedback = True

                    st.session_state.history.append({
                        "sequence": q.sequence,
                        "answer": option,
                        "correct": q.correct_answer,
                        "is_correct": eval_res.is_correct,
                        "points": eval_res.total_delta
                    })

                    trigger_sound("correct" if eval_res.is_correct else "incorrect")
                    st.rerun()

        # Hint expander
        with st.expander("💡 Need a Hint?"):
            st.info(f"Hint: {q.hint}")


# -------------------------------------------------------------
# SCREEN 10 & 11: Game Over and Final Results
# -------------------------------------------------------------
elif st.session_state.screen in ["game_over", "results"]:
    is_win = (st.session_state.screen == "results")
    
    if is_win:
        st.markdown('<h1 class="arcade-title" style="color: #10b981;">🎉 QUEST COMPLETED!</h1>', unsafe_allow_html=True)
        st.markdown('<div class="arcade-subtitle">Outstanding work, Master of Singletons!</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown('<h1 class="arcade-title" style="color: #ef4444;">💀 GAME OVER</h1>', unsafe_allow_html=True)
        st.markdown('<div class="arcade-subtitle">You ran out of lives, but every sequence teaches a lesson!</div>', unsafe_allow_html=True)

    # Tally metrics
    total_q = len(st.session_state.history)
    correct_q = sum(1 for h in st.session_state.history if h["is_correct"])
    accuracy = (correct_q / total_q * 100) if total_q > 0 else 0.0

    # Auto-save match to database
    db = SessionLocal()
    try:
        match_record = save_match_result(
            db=db,
            player_name=st.session_state.player_name,
            mode=st.session_state.mode,
            difficulty=st.session_state.difficulty,
            score=st.session_state.score,
            accuracy=accuracy,
            questions_answered=total_q,
            correct_answers=correct_q,
            levels_completed=total_q if is_win else max(0, total_q - 1),
            match_result="WON" if is_win else "GAME_OVER",
            duration_seconds=60.0,
            hints_used=st.session_state.hints_used
        )
    finally:
        db.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Final Score", f"{st.session_state.score:,} pts")
    col2.metric("Accuracy", f"{accuracy:.1f}%")
    col3.metric("Correct Answers", f"{correct_q}/{total_q}")

    st.markdown("### 📜 Round Summary:")
    for idx, item in enumerate(st.session_state.history, start=1):
        status_icon = "✅" if item["is_correct"] else "❌"
        st.markdown(f"- {status_icon} **Round {idx}:** `{item['sequence']}` | Answer: `{item['answer']}` | Correct: `{item['correct']}` (+{item['points']} pts)")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("🔄 Play Again", use_container_width=True):
            st.session_state.screen = "mode_select"
            st.rerun()
    with b2:
        if st.button("🏆 View Leaderboard", use_container_width=True):
            st.session_state.screen = "leaderboard"
            st.rerun()


# -------------------------------------------------------------
# SCREEN 12: Leaderboard
# -------------------------------------------------------------
elif st.session_state.screen == "leaderboard":
    st.markdown('<h1 class="arcade-title">🏆 PERSISTENT LEADERBOARD</h1>', unsafe_allow_html=True)
    st.markdown('<div class="arcade-subtitle">Server-Authoritative High Scores from SQLite Database</div>', unsafe_allow_html=True)

    db = SessionLocal()
    try:
        board_data = get_leaderboard(db, limit=25)
    finally:
        db.close()

    render_leaderboard_table(board_data)

    if st.button("⬅️ Back to Menu", use_container_width=True):
        st.session_state.screen = "home"
        st.rerun()


# -------------------------------------------------------------
# SCREEN 13: Achievements
# -------------------------------------------------------------
elif st.session_state.screen == "achievements":
    st.markdown('<h1 class="arcade-title">🎖️ ACHIEVEMENTS GALLERY</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="arcade-subtitle">Player: {st.session_state.player_name}</div>', unsafe_allow_html=True)

    db = SessionLocal()
    try:
        ach_data = get_player_achievements_list(db, st.session_state.player_name)
    finally:
        db.close()

    render_achievements_display(ach_data)

    if st.button("⬅️ Back to Menu", use_container_width=True):
        st.session_state.screen = "home"
        st.rerun()


# -------------------------------------------------------------
# SCREEN 14: Match History
# -------------------------------------------------------------
elif st.session_state.screen == "history":
    st.markdown('<h1 class="arcade-title">📜 PERSONAL MATCH HISTORY</h1>', unsafe_allow_html=True)
    st.markdown(f'<div class="arcade-subtitle">Career Log for: {st.session_state.player_name}</div>', unsafe_allow_html=True)

    db = SessionLocal()
    try:
        hist_data = get_player_history(db, st.session_state.player_name, limit=20)
    finally:
        db.close()

    if hist_data:
        st.table(hist_data)
    else:
        st.info("No recorded matches yet. Play a game to record your first match!")

    if st.button("⬅️ Back to Menu", use_container_width=True):
        st.session_state.screen = "home"
        st.rerun()


# -------------------------------------------------------------
# SCREEN 15: Educational Algorithm Laboratory
# -------------------------------------------------------------
elif st.session_state.screen == "algorithm_lab":
    st.markdown('<h1 class="arcade-title">🧪 ALGORITHM LABORATORY</h1>', unsafe_allow_html=True)
    st.markdown('<div class="arcade-subtitle">Interactive Dual-Algorithm Sandbox: O(n) Frequency Dictionary vs O(n²) Nested Loop</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="arcade-card">
        <h3>Academic Demonstration & Complexity Comparison</h3>
        <p>Type any custom string or character sequence below to visualize how both algorithms
        process the data, compare operations, and verify theoretical time & space complexity.</p>
    </div>
    """, unsafe_allow_html=True)

    test_seq = st.text_input("Enter any sequence to analyze:", value="aabbccdef")
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        case_sens = st.checkbox("Case-Sensitive Matching ('A' != 'a')", value=True)
    with col_opt2:
        ign_spaces = st.checkbox("Ignore Whitespace Characters", value=True)

    if test_seq:
        analysis = explain_first_non_repeating(test_seq, case_sens, ign_spaces)
        nested_res = first_non_repeating_nested(test_seq, case_sens, ign_spaces)

        st.markdown(get_character_tiles_html(analysis["normalized_sequence"]), unsafe_allow_html=True)

        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.markdown(f"""
            <div class="arcade-card" style="border-color: #10b981;">
                <h4>⚡ Method 1: Frequency Dictionary</h4>
                <p><strong>Result:</strong> <code>{analysis['result']}</code></p>
                <p><strong>Time Complexity:</strong> <code>O(n)</code> (2 linear passes)</p>
                <p><strong>Space Complexity:</strong> <code>{analysis['frequency_method_space_complexity']}</code></p>
            </div>
            """, unsafe_allow_html=True)

        with res_col2:
            st.markdown(f"""
            <div class="arcade-card" style="border-color: #f59e0b;">
                <h4>🐢 Method 2: Nested Loops</h4>
                <p><strong>Result:</strong> <code>{nested_res}</code></p>
                <p><strong>Time Complexity:</strong> <code>O(n²)</code> worst-case</p>
                <p><strong>Space Complexity:</strong> <code>O(1)</code> auxiliary space</p>
            </div>
            """, unsafe_allow_html=True)

        # Verification check
        if analysis["result"] == nested_res:
            st.success("✅ **Algorithm Consistency Verified:** Both methods yield the exact identical result!")
        else:
            st.error("❌ Discrepancy detected!")

        # Step by step trace table
        st.markdown("#### 🔍 Step-by-Step Character Inspection:")
        st.table([
            {
                "Index": s["index"],
                "Character": s["character"],
                "Total Frequency": s["frequency"],
                "Is Unique?": "YES" if s["is_unique"] else "NO",
                "Is First Unique?": "★ FIRST UNIQUE" if s["is_first_unique"] else ""
            }
            for s in analysis["steps"]
        ])

        render_explanation_box(analysis["explanation"], analysis["frequencies"], analysis["result"] or "")

    if st.button("⬅️ Back to Menu", use_container_width=True):
        st.session_state.screen = "home"
        st.rerun()


# -------------------------------------------------------------
# SCREEN 5: Settings
# -------------------------------------------------------------
elif st.session_state.screen == "settings":
    st.markdown('<h1 class="arcade-title">⚙️ GAME SETTINGS</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="arcade-card">
        <h3>Game Preferences</h3>
    </div>
    """, unsafe_allow_html=True)

    snd = st.toggle("Enable Arcade Sound Effects", value=st.session_state.sound_enabled)
    st.session_state.sound_enabled = snd

    def_diff = st.selectbox("Default Difficulty Level", ["easy", "medium", "hard", "expert"], index=0)
    st.session_state.difficulty = def_diff

    if st.button("Save Settings", use_container_width=True):
        trigger_sound("click")
        st.success("Preferences updated!")

    if st.button("⬅️ Back to Menu", use_container_width=True):
        st.session_state.screen = "home"
        st.rerun()
