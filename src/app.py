"""
Quantum Heist: Break the Entanglement Vault
===========================================
A Cinematic, Sequential-Mission Quantum Infiltration Game
Built for the Qiskit Fall Fest 2026 Hackathon (Track 1)
Organized by IIIT Kottayam. Powered by IBM Qiskit & Qiskit Aer.

Author: B.Tech CSE Hackathon Team
"""

import time
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
from quantum_circuits import (
    build_level1_circuit,
    evaluate_level1_result,
    build_level2_circuit,
    evaluate_level2_result,
    build_level3_circuit,
    evaluate_level3_result,
    run_circuit_simulation,
    get_theoretical_state_info,
    get_next_puzzle_variant,
    generate_new_game_puzzles,
    MAX_MOVES,
    PUZZLE_DESCRIPTIONS,
    AER_AVAILABLE
)
from leaderboard import load_leaderboard, add_leaderboard_entry

# ------------------------------------------------------------------------------
# 1. PAGE SETUP & SOPHISTICATED DARK VAULT THEME
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Quantum Heist: Break the Entanglement Vault",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom High-Contrast Dark CSS & Cinematic Heist Styling
st.markdown("""
<style>
    /* Global Background & Typography */
    .stApp {
        background-color: #070B14;
        color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    }

    /* ========================================================================== */
    /* EXHAUSTIVE HIGH-CONTRAST BUTTON SYSTEM (ELIMINATES WHITE BUTTONS)          */
    /* ========================================================================== */
    div.stButton > button,
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"],
    .stButton button {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    div.stButton > button:hover,
    button[kind="secondary"]:hover,
    button[data-testid="baseButton-secondary"]:hover {
        background-color: #28374F !important;
        color: #38BDF8 !important;
        border-color: #06B6D4 !important;
        box-shadow: 0 4px 14px rgba(6, 182, 212, 0.25) !important;
        transform: translateY(-1.5px) !important;
    }

    div.stButton > button:active,
    button[kind="secondary"]:active {
        background-color: #1E293B !important;
        transform: translateY(0px) !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }

    div.stButton > button:focus,
    div.stButton > button:focus-visible {
        outline: none !important;
        border-color: #06B6D4 !important;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.35) !important;
    }

    div.stButton > button:disabled,
    button:disabled {
        background-color: #0F172A !important;
        color: #475569 !important;
        border-color: #1E293B !important;
        cursor: not-allowed !important;
        opacity: 0.55 !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* Primary Action Buttons */
    button[kind="primary"],
    button[data-testid="baseButton-primary"],
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0891B2 0%, #06B6D4 100%) !important;
        color: #070B14 !important;
        font-weight: 750 !important;
        font-size: 0.95rem !important;
        border: 1px solid #22D3EE !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 16px rgba(6, 182, 212, 0.35) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #06B6D4 0%, #22D3EE 100%) !important;
        color: #070B14 !important;
        border-color: #67E8F9 !important;
        box-shadow: 0 6px 22px rgba(6, 182, 212, 0.5) !important;
        transform: translateY(-2px) !important;
    }

    /* ========================================================================== */
    /* CINEMATIC CARDS & CONTAINERS                                               */
    /* ========================================================================== */
    .hero-banner {
        position: relative;
        background: radial-gradient(circle at 50% 15%, rgba(6, 182, 212, 0.15) 0%, rgba(17, 26, 46, 0.9) 65%, #080D1A 100%);
        border: 1px solid rgba(6, 182, 212, 0.35);
        border-radius: 16px;
        padding: 40px 44px;
        max-width: 880px;
        margin: 20px auto;
        box-shadow: 0 16px 50px rgba(0, 0, 0, 0.75), 0 0 35px rgba(6, 182, 212, 0.18);
        overflow: hidden;
    }
    .hero-banner::before {
        content: "";
        position: absolute;
        top: -40%;
        left: -40%;
        width: 180%;
        height: 180%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.06) 0%, transparent 60%);
        animation: subtlePulse 8s ease-in-out infinite alternate;
        pointer-events: none;
    }
    @keyframes subtlePulse {
        0% { transform: scale(0.96); opacity: 0.6; }
        100% { transform: scale(1.04); opacity: 1; }
    }

    .start-card {
        background: linear-gradient(180deg, #111A2E 0%, #090E1A 100%);
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 36px 42px;
        max-width: 860px;
        margin: 20px auto;
        box-shadow: 0 16px 50px rgba(0, 0, 0, 0.65);
    }

    .transit-terminal {
        background: #090E17;
        border: 1px solid #06B6D4;
        border-radius: 12px;
        padding: 24px 30px;
        font-family: 'Courier New', Courier, monospace;
        color: #38BDF8;
        box-shadow: 0 0 25px rgba(6, 182, 212, 0.2);
        max-width: 860px;
        margin: 20px auto;
    }

    /* Tactical HUD */
    .tactical-hud {
        background: linear-gradient(180deg, #111A2E 0%, #0A0F1D 100%);
        border: 1px solid #1E293B;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    .hud-title {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: 0.6px;
        color: #F8FAFC;
        margin-bottom: 2px;
    }
    .hud-subtitle {
        font-size: 0.85rem;
        color: #94A3B8;
        margin-bottom: 12px;
    }

    /* Metric Cards */
    .metric-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 10px 14px;
        text-align: left;
    }
    .metric-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        margin-bottom: 2px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #38BDF8;
    }

    /* Airlock Tactical Deck */
    .level-card {
        background: #0F172A;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 16px;
        transition: transform 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease;
        height: 100%;
    }
    .level-card:hover {
        transform: translateY(-2px);
        border-color: #38BDF8;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
    }
    .level-card-active {
        background: #131E33;
        border: 1px solid #06B6D4;
        box-shadow: 0 0 16px rgba(6, 182, 212, 0.22);
    }
    .level-card-cleared {
        border-left: 4px solid #10B981;
    }
    .level-card-locked {
        opacity: 0.65;
        border-left: 4px solid #475569;
    }
    .level-title {
        font-size: 1.02rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 4px;
    }
    .level-desc {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-bottom: 10px;
        min-height: 36px;
    }

    /* Badges */
    .pill {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 2px 7px;
        border-radius: 4px;
        margin-right: 4px;
    }
    .pill-easy { background: rgba(16, 185, 129, 0.15); color: #34D399; }
    .pill-med { background: rgba(245, 158, 11, 0.15); color: #FBBF24; }
    .pill-hard { background: rgba(139, 92, 246, 0.15); color: #A78BFA; }
    .pill-master { background: rgba(239, 68, 68, 0.2); color: #F87171; border: 1px solid #EF4444; }
    .pill-cleared { background: rgba(16, 185, 129, 0.2); color: #10B981; }
    .pill-locked { background: rgba(100, 116, 139, 0.2); color: #94A3B8; }
    .pill-active { background: rgba(6, 182, 212, 0.2); color: #06B6D4; }

    /* Pipeline Chips */
    .pipeline-chip {
        display: inline-block;
        background: #1E293B;
        color: #38BDF8;
        border: 1px solid #334155;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 3px 8px;
        margin: 2px 3px;
    }

    /* ========================================================================== */
    /* CINEMATIC ANIMATIONS (VAULT DOORS & ALARMS)                                 */
    /* ========================================================================== */
    .vault-doors-container {
        position: relative;
        height: 84px;
        background: #060A12;
        border: 2px solid #10B981;
        border-radius: 8px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.35);
        margin: 14px 0;
    }
    .vault-door-half-left {
        position: absolute;
        left: 0;
        top: 0;
        width: 50%;
        height: 100%;
        background: linear-gradient(90deg, #1E293B 0%, #0F172A 100%);
        border-right: 2px solid #10B981;
        animation: blastDoorSlideLeft 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    .vault-door-half-right {
        position: absolute;
        right: 0;
        top: 0;
        width: 50%;
        height: 100%;
        background: linear-gradient(270deg, #1E293B 0%, #0F172A 100%);
        border-left: 2px solid #10B981;
        animation: blastDoorSlideRight 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes blastDoorSlideLeft {
        0% { transform: translateX(0); }
        100% { transform: translateX(-92%); }
    }
    @keyframes blastDoorSlideRight {
        0% { transform: translateX(0); }
        100% { transform: translateX(92%); }
    }

    .alarm-lockdown-container {
        background: rgba(239, 68, 68, 0.08);
        border: 2px solid #EF4444;
        border-radius: 8px;
        padding: 16px 20px;
        animation: emergencyStrobe 1.5s infinite alternate;
        margin: 14px 0;
    }
    @keyframes emergencyStrobe {
        0% { box-shadow: 0 0 10px rgba(239, 68, 68, 0.25); border-color: #EF4444; }
        100% { box-shadow: 0 0 25px rgba(239, 68, 68, 0.65); border-color: #F87171; }
    }

    .lockout-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 24px;
        text-align: center;
        margin-top: 20px;
    }

    @media (prefers-reduced-motion: reduce) {
        *, ::before, ::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 2. AUDIO FEEDBACK HELPER (SAFE BROWSER WEB AUDIO API SYNTHESIS)
# ------------------------------------------------------------------------------
def play_audio_feedback(kind: str = "success"):
    """
    Plays non-blocking, lightweight Web Audio synthesis in the browser.
    Zero external files or network requests required.
    """
    if kind == "success":
        js = """
        <script>
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const now = ctx.currentTime;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = 'sine';
            osc.frequency.setValueAtTime(523.25, now);       // C5
            osc.frequency.setValueAtTime(659.25, now + 0.1); // E5
            osc.frequency.setValueAtTime(783.99, now + 0.2); // G5
            gain.gain.setValueAtTime(0.12, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
            osc.start(now);
            osc.stop(now + 0.4);
        } catch(e) {}
        </script>
        """
    else:  # alarm / failure
        js = """
        <script>
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const now = ctx.currentTime;
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(320, now);
            osc.frequency.setValueAtTime(220, now + 0.15);
            gain.gain.setValueAtTime(0.14, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
            osc.start(now);
            osc.stop(now + 0.35);
        } catch(e) {}
        </script>
        """
    components.html(js, height=0)


# ------------------------------------------------------------------------------
# 3. SESSION STATE MANAGEMENT & DYNAMIC PUZZLE INITIALIZATION
# ------------------------------------------------------------------------------
if "game_state" not in st.session_state:
    st.session_state.game_state = "START"  # "START" -> "TRANSITION" -> "PLAYING" -> "VICTORY"
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "final_elapsed_seconds" not in st.session_state:
    st.session_state.final_elapsed_seconds = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "mistakes" not in st.session_state:
    st.session_state.mistakes = 0
if "cleared_doors" not in st.session_state:
    st.session_state.cleared_doors = []
if "active_door" not in st.session_state:
    st.session_state.active_door = 1

# Dynamic puzzle sequences: randomized at start and non-repeating across retries
if "puzzle_variants" not in st.session_state:
    st.session_state.puzzle_variants = generate_new_game_puzzles()
if "seen_puzzles" not in st.session_state:
    st.session_state.seen_puzzles = {
        1: [st.session_state.puzzle_variants[1]],
        2: [st.session_state.puzzle_variants[2]],
        3: [st.session_state.puzzle_variants[3]]
    }

if "l1_gates" not in st.session_state:
    st.session_state.l1_gates = []
if "l2_gates" not in st.session_state:
    st.session_state.l2_gates = []
if "l3_ops" not in st.session_state:
    st.session_state.l3_ops = []
if "last_results" not in st.session_state:
    st.session_state.last_results = {1: None, 2: None, 3: None}
if "show_hint" not in st.session_state:
    st.session_state.show_hint = {1: False, 2: False, 3: False}
if "leaderboard_rank" not in st.session_state:
    st.session_state.leaderboard_rank = None


def reset_to_new_game(clear_name: bool = False):
    """
    Completely resets the mission with a fresh puzzle sequence.
    Prevents stale answers, old measurement results, or cleared doors from carrying over.
    Preserves persistent local leaderboard.
    """
    st.session_state.game_state = "START"
    if clear_name:
        st.session_state.player_name = ""
    st.session_state.start_time = None
    st.session_state.final_elapsed_seconds = 0
    st.session_state.score = 0
    st.session_state.mistakes = 0
    st.session_state.cleared_doors = []
    st.session_state.active_door = 1
    # Generate fresh randomized puzzle sequence across all 3 doors
    fresh_puzzles = generate_new_game_puzzles()
    st.session_state.puzzle_variants = fresh_puzzles
    st.session_state.seen_puzzles = {
        1: [fresh_puzzles[1]],
        2: [fresh_puzzles[2]],
        3: [fresh_puzzles[3]]
    }
    st.session_state.l1_gates = []
    st.session_state.l2_gates = []
    st.session_state.l3_ops = []
    st.session_state.last_results = {1: None, 2: None, 3: None}
    st.session_state.show_hint = {1: False, 2: False, 3: False}
    st.session_state.leaderboard_rank = None


def format_elapsed_time(seconds: int) -> str:
    """Formats integer seconds into MM:SS."""
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m:02d}:{s:02d}"


# ------------------------------------------------------------------------------
# 4. HELPER: DARK-THEMED HISTOGRAM PLOTTER
# ------------------------------------------------------------------------------
def plot_measurement_distribution(counts: dict, theoretical_probs: dict, total_shots: int):
    """
    Renders high-contrast dark matplotlib histogram comparing empirical shots to theory.
    """
    keys = sorted(list(set(list(counts.keys()) + list(theoretical_probs.keys()))))
    empirical_pcts = [(counts.get(k, 0) / total_shots) * 100 for k in keys]
    theory_pcts = [theoretical_probs.get(k, 0.0) * 100 for k in keys]

    fig, ax = plt.subplots(figsize=(6.5, 3.0), facecolor="#0F172A")
    ax.set_facecolor("#0F172A")

    x = range(len(keys))
    width = 0.35

    bars_emp = ax.bar([i - width/2 for i in x], empirical_pcts, width=width,
                      label=f"Empirical Shots ({total_shots})", color="#06B6D4", edgecolor="#22D3EE", alpha=0.95)
    bars_th = ax.bar([i + width/2 for i in x], theory_pcts, width=width,
                     label="Theoretical Prob (%)", color="#6366F1", edgecolor="#818CF8", alpha=0.75)

    ax.set_xticks(list(x))
    ax.set_xticklabels([f"|{k}⟩" for k in keys], color="#F8FAFC", fontsize=11, fontweight="bold")
    ax.set_ylabel("Probability (%)", color="#94A3B8", fontsize=9.5)
    ax.set_ylim(0, 115)
    ax.tick_params(colors="#94A3B8")
    ax.grid(axis="y", color="#1E293B", linestyle="--", alpha=0.7)

    for spine in ax.spines.values():
        spine.set_color("#1E293B")

    for bar in bars_emp:
        h = bar.get_height()
        if h > 0:
            ax.annotate(f"{h:.1f}%",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", color="#E2E8F0", fontsize=9, fontweight="600")

    ax.legend(facecolor="#1E293B", edgecolor="#334155", labelcolor="#E2E8F0", fontsize=8.5, loc="upper right")
    plt.tight_layout()
    return fig


# ------------------------------------------------------------------------------
# 5. SIDEBAR: OPERATIVE QUICK PANEL
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚛️ Infiltrator Manual")
    st.caption("Qiskit Fall Fest 2026 — Track 1")

    engine_name = "AerSimulator" if AER_AVAILABLE else "StatevectorSampler"
    st.markdown(f"**Engine:** `{engine_name}`")
    st.markdown(f"**Qiskit:** `v2.5.2` (Verified)")

    if st.session_state.game_state not in ["START", "ENTRY"]:
        st.markdown(f"**Operative:** `{st.session_state.player_name}`")
        if st.session_state.start_time:
            if st.session_state.game_state == "PLAYING":
                current_elapsed = int(time.time() - st.session_state.start_time)
            else:
                current_elapsed = st.session_state.final_elapsed_seconds
            st.markdown(f"**Timer:** `{format_elapsed_time(current_elapsed)}`")

    st.markdown("---")
    st.markdown("#### Quantum Gate Reference")
    with st.expander("Pauli-X (Quantum NOT)", expanded=False):
        st.write("Bit-flip operator: $X|0\\rangle = |1\\rangle$ and $X|1\\rangle = |0\\rangle$.")
        st.caption("Matrix: [[0, 1], [1, 0]]")

    with st.expander("Pauli-Z (Phase Flip)", expanded=False):
        st.write("Leaves $|0\\rangle$ intact; inverts relative phase of $|1\\rangle$ to $-|1\\rangle$.")
        st.caption("Matrix: [[1, 0], [0, -1]]")

    with st.expander("Hadamard (H)", expanded=False):
        st.write("Creates equal superposition: $H|0\\rangle = \\frac{|0\\rangle + |1\\rangle}{\\sqrt{2}}$.")
        st.write("Self-inverting: $H \\cdot H = I$ (destructive interference cancels superposition).")

    with st.expander("CNOT / CX (Controlled-NOT)", expanded=False):
        st.write("Entangles two qubits: flips Target if Control is $|1\\rangle$.")
        st.write("Bell State: $H(q_0) + CNOT(q_0, q_1) \\to \\frac{|00\\rangle + |11\\rangle}{\\sqrt{2}}$.")

    st.markdown("---")
    if st.button("🔄 Try Again / Fresh Mission", use_container_width=True):
        reset_to_new_game(clear_name=False)
        st.rerun()


# ==============================================================================
# 6. SCENE A: CINEMATIC OPENING (START SCREEN)
# ==============================================================================
if st.session_state.game_state == "START":
    st.markdown("""
    <div class='hero-banner'>
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 12px;'>
            <span class='pill pill-hard'>Qiskit Fall Fest 2026</span>
            <span class='pill pill-active'>Track 1: Interactive Puzzles</span>
            <span class='pill pill-cleared'>IBM Qiskit v2.5.2</span>
        </div>
        <div style='font-size: 2.6rem; font-weight: 900; color: #F8FAFC; letter-spacing: 1px; line-height: 1.15; margin-bottom: 6px; text-shadow: 0 0 30px rgba(6, 182, 212, 0.4);'>
            QUANTUM HEIST
        </div>
        <div style='font-size: 1.25rem; font-weight: 700; color: #22D3EE; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 20px;'>
            BREAK THE ENTANGLEMENT VAULT
        </div>
        <div style='font-size: 1.05rem; color: #CBD5E1; margin-bottom: 26px; line-height: 1.7;'>
            Welcome, Operative. The Quantum Cryptographic Reserve has secured their prime master key 
            inside the impenetrable <b>Vault Sigma-9</b>. Three sequential quantum-encrypted containment airlocks stand between you and the core. 
            Each door dynamically recalibrates its quantum challenge, ensuring no two heists are identical. 
            You must engineer authentic IBM Qiskit circuits under move constraints to breach the defenses.
        </div>
        <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 28px;'>
            <div style='background: #090E17; border: 1px solid #1E293B; border-radius: 10px; padding: 14px;'>
                <div style='font-size: 0.75rem; color: #38BDF8; font-weight: 700; text-transform: uppercase;'>Airlock 1</div>
                <div style='font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin: 4px 0;'>Laser Grid</div>
                <div style='font-size: 0.8rem; color: #94A3B8;'>Single-qubit basis state rotations (X, Z, H).</div>
            </div>
            <div style='background: #090E17; border: 1px solid #1E293B; border-radius: 10px; padding: 14px;'>
                <div style='font-size: 0.75rem; color: #FBBF24; font-weight: 700; text-transform: uppercase;'>Airlock 2</div>
                <div style='font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin: 4px 0;'>Dual Sensor</div>
                <div style='font-size: 0.8rem; color: #94A3B8;'>Superposition balance & interference collapse.</div>
            </div>
            <div style='background: #090E17; border: 1px solid #1E293B; border-radius: 10px; padding: 14px;'>
                <div style='font-size: 0.75rem; color: #A78BFA; font-weight: 700; text-transform: uppercase;'>Airlock 3</div>
                <div style='font-size: 0.95rem; font-weight: 700; color: #F8FAFC; margin: 4px 0;'>Master Vault</div>
                <div style='font-size: 0.8rem; color: #94A3B8;'>Two-qubit non-local Bell state entanglement.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_in1, c_in2, c_in3 = st.columns([1, 2, 1])
    with c_in2:
        if st.button("🚀 START HEIST", key="btn_start_heist", type="primary", use_container_width=True):
            st.session_state.game_state = "ENTRY"
            st.rerun()


# ==============================================================================
# 7. SCENE B: PLAYER ENTRY & MISSION BRIEFING
# ==============================================================================
elif st.session_state.game_state == "ENTRY":
    # Get active variant for door 1 to preview
    d1_v = st.session_state.puzzle_variants[1]
    p_d1 = PUZZLE_DESCRIPTIONS.get((1, d1_v), PUZZLE_DESCRIPTIONS[(1, 1)])

    st.markdown(f"""
    <div class='transit-terminal'>
        <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;'>
            <span style='font-weight: 800; font-size: 1.15rem; color: #22D3EE;'>🛰️ OPERATIVE REGISTRATION & VAULT BRIEFING</span>
            <span class='pill pill-active'>UPLINK ACTIVE</span>
        </div>
        <div style='font-size: 0.92rem; line-height: 1.8; color: #CBD5E1;'>
            &gt; [0.1s] TARGET FACILITY: <b>Vault Sigma-9</b> (Quantum Cryptographic Reserve)<br>
            &gt; [0.3s] SIMULATOR ENGINE: <b>{engine_name}</b> (IBM Qiskit v2.5.2)<br>
            &gt; [0.5s] SECURITY LEVEL: <b>3 Sequential Containment Airlocks</b><br>
            &gt; [0.7s] INITIAL AIRLOCK PROTOCOL: <b>{p_d1['title']}</b> ({p_d1['difficulty']})<br>
            &gt; [0.9s] ALL SYSTEMS READY. ENTER CODENAME TO AUTHENTICATE AND COMMENCE BREACH.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c_tr1, c_tr2, c_tr3 = st.columns([1, 2, 1])
    with c_tr2:
        codename = st.text_input(
            "Operative Codename:",
            value=st.session_state.player_name,
            placeholder="e.g. CipherAgent",
            max_chars=24,
            key="input_player_codename"
        )

        if st.button("⚡ BEGIN MISSION", key="btn_begin_mission", type="primary", use_container_width=True):
            if not codename.strip():
                st.error("⚠️ Operative codename required to initialize vault credentials.")
            else:
                st.session_state.player_name = codename.strip()
                st.session_state.start_time = time.time()
                st.session_state.score = 0
                st.session_state.mistakes = 0
                st.session_state.cleared_doors = []
                st.session_state.active_door = 1
                st.session_state.game_state = "PLAYING"
                st.rerun()


# ==============================================================================
# 8. SCREEN 2: INFILTRATION MISSION WORKBENCH (GAMEPLAY)
# ==============================================================================
elif st.session_state.game_state == "PLAYING":
    elapsed_seconds = int(time.time() - st.session_state.start_time)

    # Top Tactical HUD
    st.markdown("""
    <div class='tactical-hud'>
        <div class='hud-title'>⚡ QUANTUM HEIST: BREAK THE ENTANGLEMENT VAULT</div>
        <div class='hud-subtitle'>
            Construct verified Qiskit quantum circuits to sequentially bypass the vault's containment airlocks.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Telemetry Badges
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    with m_col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Operative</div>
            <div class='metric-value' style='font-size: 1.02rem; color: #F8FAFC;'>{st.session_state.player_name}</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Mission Clock</div>
            <div class='metric-value' style='color: #FBBF24;'>{format_elapsed_time(elapsed_seconds)}</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Current Bounty</div>
            <div class='metric-value'>{st.session_state.score} PTS</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col4:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Alarms / Mistakes</div>
            <div class='metric-value' style='color: {"#EF4444" if st.session_state.mistakes > 0 else "#34D399"};'>{st.session_state.mistakes}</div>
        </div>
        """, unsafe_allow_html=True)
    with m_col5:
        doors_count = len(st.session_state.cleared_doors)
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Vault Security</div>
            <div class='metric-value'>{doors_count} / 3 Bypassed</div>
        </div>
        """, unsafe_allow_html=True)

    # Sequential Airlock Deck (3 Cards with dynamic difficulty badges)
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    l_col1, l_col2, l_col3 = st.columns(3)

    d1_unlocked = True
    d2_unlocked = 1 in st.session_state.cleared_doors
    d3_unlocked = (1 in st.session_state.cleared_doors) and (2 in st.session_state.cleared_doors)

    # Grab active puzzle info for each door
    p_info_d1 = PUZZLE_DESCRIPTIONS.get((1, st.session_state.puzzle_variants[1]), PUZZLE_DESCRIPTIONS[(1, 1)])
    p_info_d2 = PUZZLE_DESCRIPTIONS.get((2, st.session_state.puzzle_variants[2]), PUZZLE_DESCRIPTIONS[(2, 1)])
    p_info_d3 = PUZZLE_DESCRIPTIONS.get((3, st.session_state.puzzle_variants[3]), PUZZLE_DESCRIPTIONS[(3, 1)])

    # Card 1: Door 1
    with l_col1:
        is_active_1 = st.session_state.active_door == 1
        is_cleared_1 = 1 in st.session_state.cleared_doors
        active_cls_1 = "level-card-active" if is_active_1 else ""
        cleared_cls_1 = "level-card-cleared" if is_cleared_1 else ""

        st.markdown(f"""
        <div class='level-card {active_cls_1} {cleared_cls_1}'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                <span class='pill pill-easy'>{p_info_d1['difficulty']}</span>
                <span class='pill {"pill-cleared" if is_cleared_1 else "pill-active"}'>{"Bypassed" if is_cleared_1 else "Armed"}</span>
            </div>
            <div class='level-title'>Door 1: Laser Grid</div>
            <div class='level-desc'>{p_info_d1['title']}</div>
            <div style='font-size: 0.78rem; color: #64748B; margin-bottom: 10px;'>Max Moves: 2 | Reward: 150 PTS</div>
        </div>
        """, unsafe_allow_html=True)
        btn_label_1 = "Active Workbench" if is_active_1 else ("Revisit Door 1" if is_cleared_1 else "Select Door 1")
        if st.button(btn_label_1, key="nav_d1", use_container_width=True, disabled=is_active_1):
            st.session_state.active_door = 1
            st.rerun()

    # Card 2: Door 2
    with l_col2:
        is_active_2 = st.session_state.active_door == 2
        is_cleared_2 = 2 in st.session_state.cleared_doors
        active_cls_2 = "level-card-active" if is_active_2 else ""
        cleared_cls_2 = "level-card-cleared" if is_cleared_2 else ("level-card-locked" if not d2_unlocked else "")

        diff_class_2 = "pill-med" if p_info_d2['difficulty'] == "Medium" else "pill-hard"
        st.markdown(f"""
        <div class='level-card {active_cls_2} {cleared_cls_2}'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                <span class='pill {diff_class_2}'>{p_info_d2['difficulty']}</span>
                <span class='pill {"pill-cleared" if is_cleared_2 else ("pill-active" if d2_unlocked else "pill-locked")}'>
                    {"Bypassed" if is_cleared_2 else ("Armed" if d2_unlocked else "🔒 Locked")}
                </span>
            </div>
            <div class='level-title'>Door 2: Dual-Sensor</div>
            <div class='level-desc'>{p_info_d2['title']}</div>
            <div style='font-size: 0.78rem; color: #64748B; margin-bottom: 10px;'>Max Moves: 2 | Reward: 200 PTS</div>
        </div>
        """, unsafe_allow_html=True)
        btn_label_2 = "Active Workbench" if is_active_2 else ("Revisit Door 2" if is_cleared_2 else ("Select Door 2" if d2_unlocked else "🔒 Locked"))
        if st.button(btn_label_2, key="nav_d2", use_container_width=True, disabled=is_active_2 or not d2_unlocked):
            st.session_state.active_door = 2
            st.rerun()

    # Card 3: Door 3
    with l_col3:
        is_active_3 = st.session_state.active_door == 3
        is_cleared_3 = 3 in st.session_state.cleared_doors
        active_cls_3 = "level-card-active" if is_active_3 else ""
        cleared_cls_3 = "level-card-cleared" if is_cleared_3 else ("level-card-locked" if not d3_unlocked else "")

        diff_class_3 = "pill-hard" if p_info_d3['difficulty'] == "Hard" else "pill-master"
        st.markdown(f"""
        <div class='level-card {active_cls_3} {cleared_cls_3}'>
            <div style='display: flex; justify-content: space-between; margin-bottom: 8px;'>
                <span class='pill {diff_class_3}'>{p_info_d3['difficulty']}</span>
                <span class='pill {"pill-cleared" if is_cleared_3 else ("pill-active" if d3_unlocked else "pill-locked")}'>
                    {"Bypassed" if is_cleared_3 else ("Armed" if d3_unlocked else "🔒 Locked")}
                </span>
            </div>
            <div class='level-title'>Door 3: Master Vault</div>
            <div class='level-desc'>{p_info_d3['title']}</div>
            <div style='font-size: 0.78rem; color: #64748B; margin-bottom: 10px;'>Max Moves: 3 | Reward: 300 PTS</div>
        </div>
        """, unsafe_allow_html=True)
        btn_label_3 = "Active Workbench" if is_active_3 else ("Revisit Door 3" if is_cleared_3 else ("Select Door 3" if d3_unlocked else "🔒 Locked"))
        if st.button(btn_label_3, key="nav_d3", use_container_width=True, disabled=is_active_3 or not d3_unlocked):
            st.session_state.active_door = 3
            st.rerun()

    # WORKBENCH SECTION WITH GENUINE LOCKOUT ENFORCEMENT
    curr_door = st.session_state.active_door
    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)

    if curr_door == 2 and not d2_unlocked:
        st.markdown("""
        <div class='lockout-card'>
            <div style='font-size: 1.4rem; font-weight: 700; color: #EF4444; margin-bottom: 8px;'>
                🔒 SECURITY LOCKOUT: DOOR 2 IS SEALED
            </div>
            <div style='font-size: 0.95rem; color: #94A3B8; margin-bottom: 14px;'>
                You cannot access Tier 2 until Door 1 (Security Laser Grid) has been compromised.
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Return to Door 1 Workbench", key="lock_back_d1", type="primary"):
            st.session_state.active_door = 1
            st.rerun()

    elif curr_door == 3 and not d3_unlocked:
        st.markdown("""
        <div class='lockout-card'>
            <div style='font-size: 1.4rem; font-weight: 700; color: #EF4444; margin-bottom: 8px;'>
                🔒 SECURITY LOCKOUT: MASTER VAULT IS SEALED
            </div>
            <div style='font-size: 0.95rem; color: #94A3B8; margin-bottom: 14px;'>
                Master Vault authorization requires compromising Door 2 (Dual-Sensor) first.
            </div>
        </div>
        """, unsafe_allow_html=True)
        target_step = 2 if d2_unlocked else 1
        if st.button(f"Return to Door {target_step} Workbench", key="lock_back_d2", type="primary"):
            st.session_state.active_door = target_step
            st.rerun()

    else:
        # ACTIVE WORKBENCH RENDER
        v_idx = st.session_state.puzzle_variants[curr_door]
        p_info = PUZZLE_DESCRIPTIONS.get((curr_door, v_idx), PUZZLE_DESCRIPTIONS[(curr_door, 1)])

        # ----------------- DOOR 1 WORKBENCH -----------------
        if curr_door == 1:
            st.markdown(f"### 🛠️ Circuit Workbench — {p_info['title']} ({p_info['difficulty']})")
            wb_col1, wb_col2 = st.columns([2, 1])
            with wb_col1:
                st.write(f"**Protocol:** {p_info['objective']} Initial: `{p_info['initial']}`, Target: `{p_info['target']}`.")
            with wb_col2:
                m_used = len(st.session_state.l1_gates)
                m_max = MAX_MOVES[1]
                m_color = "#10B981" if m_used <= m_max else "#EF4444"
                st.markdown(f"""
                <div style='text-align: right;'>
                    <span class='pill' style='background: #1E293B; color: {m_color}; border: 1px solid {m_color};'>
                        Moves: {m_used} / {m_max} Max
                    </span>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("🔍 Quantum Intel & Physics Briefing (Door 1)", expanded=False):
                st.markdown(r"""
                **Single-Qubit State Space:**  
                A single qubit exists as $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$.
                - The **Pauli-X Gate** performs a $\pi$-radian rotation around the X-axis of the Bloch sphere, inverting basis states: $X|0\rangle = |1\rangle$ and $X|1\rangle = |0\rangle$.
                - The **Pauli-Z Gate** adjusts relative phase: $Z|0\rangle = |0\rangle$ and $Z|1\rangle = -|1\rangle$.
                - **Unitarity Property:** Applying $X \cdot X = I$ returns the qubit to its original state deterministically.
                """)

            st.markdown("##### Apply Quantum Operations to Qubit 0")
            g_col1, g_col2, g_col3, g_col4, g_col5, g_col6 = st.columns([1, 1, 1, 0.9, 0.9, 1.1])
            with g_col1:
                if st.button("X (Bit-Flip)", key="x_1", use_container_width=True):
                    st.session_state.l1_gates.append("X")
                    st.session_state.last_results[1] = None
                    st.rerun()
            with g_col2:
                if st.button("Z (Phase-Flip)", key="z_1", use_container_width=True):
                    st.session_state.l1_gates.append("Z")
                    st.session_state.last_results[1] = None
                    st.rerun()
            with g_col3:
                if st.button("H (Hadamard)", key="h_1", use_container_width=True):
                    st.session_state.l1_gates.append("H")
                    st.session_state.last_results[1] = None
                    st.rerun()
            with g_col4:
                undo_d1 = len(st.session_state.l1_gates) == 0
                if st.button("Undo", key="undo_1", use_container_width=True, disabled=undo_d1):
                    st.session_state.l1_gates.pop()
                    st.session_state.last_results[1] = None
                    st.rerun()
            with g_col5:
                if st.button("Clear", key="clr_1", use_container_width=True):
                    st.session_state.l1_gates = []
                    st.session_state.last_results[1] = None
                    st.rerun()
            with g_col6:
                h_label = "Hide Intel" if st.session_state.show_hint[1] else "Vault Intel"
                if st.button(h_label, key="hint_btn_1", use_container_width=True):
                    st.session_state.show_hint[1] = not st.session_state.show_hint[1]
                    st.rerun()

            if st.session_state.show_hint[1]:
                if st.session_state.last_results[1] is None:
                    st.info(f"🔒 **Classified Intel:** Execute your initial breach attempt to decrypt specific gate recommendations.\n\n**Mission Objective:** {p_info['objective']}")
                else:
                    st.info(f"💡 **Security Decryption Intel:** {p_info['hint']}")

            if st.session_state.l1_gates:
                chips = " ".join([f"<span class='pipeline-chip'>{g}</span>" for g in st.session_state.l1_gates])
                st.markdown(f"**Gate Pipeline:** `{p_info['initial']}` ──▶ {chips} ──▶ `[Measure]`", unsafe_allow_html=True)
            else:
                st.caption(f"Gate Pipeline: {p_info['initial']} ──▶ (No gates queued) ──▶ [Measure]")

            qc1 = build_level1_circuit(st.session_state.l1_gates, variant=v_idx)
            th_info_1 = get_theoretical_state_info(qc1)

            c_left, c_right = st.columns([1.1, 0.9])
            with c_left:
                st.markdown("##### Real Qiskit Circuit Diagram")
                try:
                    fig_qc1 = qc1.draw(output="mpl", style="iqp-dark")
                    st.pyplot(fig_qc1, use_container_width=False)
                    plt.close(fig_qc1)
                except Exception:
                    st.code(qc1.draw(output="text"), language="text")

            with c_right:
                st.markdown("##### Simulator Execution Controls")
                shots_1 = st.select_slider("Measurement Shots", options=[50, 100, 200, 500], value=200, key="shots_s1")
                st.caption(f"Theoretical Probabilities: `{th_info_1['probabilities']}`")

                if st.button("🚀 Execute Circuit on Simulator", key="exec_1", type="primary", use_container_width=True):
                    counts_1 = run_circuit_simulation(qc1, shots=shots_1)
                    eval_1 = evaluate_level1_result(counts_1, moves_used=len(st.session_state.l1_gates), variant=v_idx, total_shots=shots_1, qc=qc1)
                    st.session_state.last_results[1] = eval_1

                    if eval_1["success"]:
                        if 1 not in st.session_state.cleared_doors:
                            st.session_state.cleared_doors.append(1)
                            st.session_state.score += eval_1["score_earned"]
                    else:
                        st.session_state.mistakes += 1
                        st.session_state.score = max(0, st.session_state.score - 25)
                        # Rotate to fresh non-repeating variant for Door 1
                        next_v = get_next_puzzle_variant(1, v_idx, st.session_state.seen_puzzles.get(1, []))
                        st.session_state.puzzle_variants[1] = next_v
                        st.session_state.seen_puzzles[1].append(next_v)
                        st.session_state.l1_gates = []
                    st.rerun()

            if st.session_state.last_results[1]:
                res1 = st.session_state.last_results[1]
                st.markdown("---")
                if res1["success"]:
                    play_audio_feedback("success")
                    st.markdown(f"""
                    <div class='vault-doors-container'>
                        <div class='vault-door-half-left'></div>
                        <div class='vault-door-half-right'></div>
                        <div style='z-index: 2; font-size: 1.1rem; font-weight: 800; color: #10B981; letter-spacing: 0.6px;'>
                            🔓 AIRLOCK 1 BREACHED — ACCESS GRANTED (+{res1['score_earned']} PTS)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    play_audio_feedback("alarm")
                    next_variant_info = PUZZLE_DESCRIPTIONS.get((1, st.session_state.puzzle_variants[1]), {})
                    st.markdown(f"""
                    <div class='alarm-lockdown-container'>
                        <div style='font-size: 1.05rem; font-weight: 800; color: #EF4444; margin-bottom: 4px;'>
                            🚨 SECURITY ALERT: {res1['status_title'].upper()}
                        </div>
                        <div style='font-size: 0.88rem; color: #CBD5E1;'>
                            {res1['explanation']}
                        </div>
                        <div style='margin-top: 8px; font-size: 0.85rem; color: #38BDF8; font-style: italic;'>
                            💡 <b>Operative Intel:</b> Keep going! Security sensors have rotated to a fresh solvable puzzle (<b>{next_variant_info.get('title', 'Next Challenge')}</b>). Click 'Retry Puzzle' below to tackle the new configuration!
                        </div>
                        <div style='font-size: 0.8rem; font-weight: 600; color: #F87171; margin-top: 6px;'>
                            Penalty: -25 PTS applied. Total mistakes: {st.session_state.mistakes}.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("#### 📊 Measurement Outcome & Security Diagnosis")
                d_col1, d_col2 = st.columns([1.1, 0.9])
                with d_col1:
                    fig_h1 = plot_measurement_distribution(res1["counts"], th_info_1["probabilities"], shots_1)
                    st.pyplot(fig_h1, use_container_width=True)
                    plt.close(fig_h1)

                with d_col2:
                    if res1["success"] and 2 not in st.session_state.cleared_doors:
                        if st.button("🚪 PROCEED TO AIRLOCK 2 (DUAL-SENSOR) ➔", key="nxt_d2", type="primary", use_container_width=True):
                            st.session_state.active_door = 2
                            st.rerun()
                    elif not res1["success"]:
                        if st.button("🔄 RETRY PUZZLE (FRESH CONFIGURATION)", key="retry_d1", type="primary", use_container_width=True):
                            st.session_state.last_results[1] = None
                            st.session_state.l1_gates = []
                            st.rerun()

        # ----------------- DOOR 2 WORKBENCH -----------------
        elif curr_door == 2:
            st.markdown(f"### 🛠️ Circuit Workbench — {p_info['title']} ({p_info['difficulty']})")
            wb_col1, wb_col2 = st.columns([2, 1])
            with wb_col1:
                st.write(f"**Protocol:** {p_info['objective']} Initial: `{p_info['initial']}`, Target: `{p_info['target']}`.")
            with wb_col2:
                m_used = len(st.session_state.l2_gates)
                m_max = MAX_MOVES[2]
                m_color = "#10B981" if m_used <= m_max else "#EF4444"
                st.markdown(f"""
                <div style='text-align: right;'>
                    <span class='pill' style='background: #1E293B; color: {m_color}; border: 1px solid {m_color};'>
                        Moves: {m_used} / {m_max} Max
                    </span>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("🔍 Quantum Intel & Physics Briefing (Door 2)", expanded=False):
                st.markdown(r"""
                **Superposition & Finite-Shot Sampling:**  
                - Applying the **Hadamard (H)** gate rotates the basis state into equal superposition:
                  $$H|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$
                - Under Born's rule, measurement probabilities are $|\alpha|^2 = |1/\sqrt{2}|^2 = 0.50$ (50% each).
                - **Why finite shots matter:** A single measurement shot only returns `0` or `1`, which cannot verify a superposition. Executing 200 shots produces a binomial distribution centered at 50% (criteria: both $\ge 35\%$).
                - **Self-Interference Trap:** Applying two Hadamards in series cancels out ($H \cdot H = I$), returning the qubit deterministically to ground state $|0\rangle$!
                """)

            st.markdown("##### Apply Quantum Operations to Qubit 0")
            g_col1, g_col2, g_col3, g_col4, g_col5, g_col6 = st.columns([1, 1, 1, 0.9, 0.9, 1.1])
            with g_col1:
                if st.button("H (Hadamard)", key="h_2", use_container_width=True):
                    st.session_state.l2_gates.append("H")
                    st.session_state.last_results[2] = None
                    st.rerun()
            with g_col2:
                if st.button("X (Bit-Flip)", key="x_2", use_container_width=True):
                    st.session_state.l2_gates.append("X")
                    st.session_state.last_results[2] = None
                    st.rerun()
            with g_col3:
                if st.button("Z (Phase-Flip)", key="z_2", use_container_width=True):
                    st.session_state.l2_gates.append("Z")
                    st.session_state.last_results[2] = None
                    st.rerun()
            with g_col4:
                undo_d2 = len(st.session_state.l2_gates) == 0
                if st.button("Undo", key="undo_2", use_container_width=True, disabled=undo_d2):
                    st.session_state.l2_gates.pop()
                    st.session_state.last_results[2] = None
                    st.rerun()
            with g_col5:
                if st.button("Clear", key="clr_2", use_container_width=True):
                    st.session_state.l2_gates = []
                    st.session_state.last_results[2] = None
                    st.rerun()
            with g_col6:
                h_label = "Hide Intel" if st.session_state.show_hint[2] else "Vault Intel"
                if st.button(h_label, key="hint_btn_2", use_container_width=True):
                    st.session_state.show_hint[2] = not st.session_state.show_hint[2]
                    st.rerun()

            if st.session_state.show_hint[2]:
                if st.session_state.last_results[2] is None:
                    st.info(f"🔒 **Classified Intel:** Execute your initial breach attempt to decrypt specific gate recommendations.\n\n**Mission Objective:** {p_info['objective']}")
                else:
                    st.info(f"💡 **Security Decryption Intel:** {p_info['hint']}")

            if st.session_state.l2_gates:
                chips = " ".join([f"<span class='pipeline-chip'>{g}</span>" for g in st.session_state.l2_gates])
                st.markdown(f"**Gate Pipeline:** `{p_info['initial']}` ──▶ {chips} ──▶ `[Measure]`", unsafe_allow_html=True)
            else:
                st.caption(f"Gate Pipeline: {p_info['initial']} ──▶ (No gates queued) ──▶ [Measure]")

            qc2 = build_level2_circuit(st.session_state.l2_gates, variant=v_idx)
            th_info_2 = get_theoretical_state_info(qc2)

            c_left, c_right = st.columns([1.1, 0.9])
            with c_left:
                st.markdown("##### Real Qiskit Circuit Diagram")
                try:
                    fig_qc2 = qc2.draw(output="mpl", style="iqp-dark")
                    st.pyplot(fig_qc2, use_container_width=False)
                    plt.close(fig_qc2)
                except Exception:
                    st.code(qc2.draw(output="text"), language="text")

            with c_right:
                st.markdown("##### Simulator Execution Controls")
                shots_2 = st.select_slider("Measurement Shots", options=[50, 100, 200, 500], value=200, key="shots_s2")
                st.caption(f"Theoretical Probabilities: `{th_info_2['probabilities']}`")

                if st.button("🚀 Execute Circuit on Simulator", key="exec_2", type="primary", use_container_width=True):
                    counts_2 = run_circuit_simulation(qc2, shots=shots_2)
                    eval_2 = evaluate_level2_result(counts_2, moves_used=len(st.session_state.l2_gates), variant=v_idx, total_shots=shots_2, qc=qc2)
                    st.session_state.last_results[2] = eval_2

                    if eval_2["success"]:
                        if 2 not in st.session_state.cleared_doors:
                            st.session_state.cleared_doors.append(2)
                            st.session_state.score += eval_2["score_earned"]
                    else:
                        st.session_state.mistakes += 1
                        st.session_state.score = max(0, st.session_state.score - 25)
                        # Rotate to fresh non-repeating variant for Door 2
                        next_v = get_next_puzzle_variant(2, v_idx, st.session_state.seen_puzzles.get(2, []))
                        st.session_state.puzzle_variants[2] = next_v
                        st.session_state.seen_puzzles[2].append(next_v)
                        st.session_state.l2_gates = []
                    st.rerun()

            if st.session_state.last_results[2]:
                res2 = st.session_state.last_results[2]
                st.markdown("---")
                if res2["success"]:
                    play_audio_feedback("success")
                    st.markdown(f"""
                    <div class='vault-doors-container'>
                        <div class='vault-door-half-left'></div>
                        <div class='vault-door-half-right'></div>
                        <div style='z-index: 2; font-size: 1.1rem; font-weight: 800; color: #10B981; letter-spacing: 0.6px;'>
                            🔓 AIRLOCK 2 BREACHED — RESONANCE ACHIEVED (+{res2['score_earned']} PTS)
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    play_audio_feedback("alarm")
                    next_variant_info = PUZZLE_DESCRIPTIONS.get((2, st.session_state.puzzle_variants[2]), {})
                    st.markdown(f"""
                    <div class='alarm-lockdown-container'>
                        <div style='font-size: 1.05rem; font-weight: 800; color: #EF4444; margin-bottom: 4px;'>
                            🚨 SECURITY ALERT: {res2['status_title'].upper()}
                        </div>
                        <div style='font-size: 0.88rem; color: #CBD5E1;'>
                            {res2['explanation']}
                        </div>
                        <div style='margin-top: 8px; font-size: 0.85rem; color: #38BDF8; font-style: italic;'>
                            💡 <b>Operative Intel:</b> Keep going! Security sensors have rotated to a fresh solvable puzzle (<b>{next_variant_info.get('title', 'Next Challenge')}</b>). Click 'Retry Puzzle' below to tackle the new configuration!
                        </div>
                        <div style='font-size: 0.8rem; font-weight: 600; color: #F87171; margin-top: 6px;'>
                            Penalty: -25 PTS applied. Total mistakes: {st.session_state.mistakes}.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("#### 📊 Measurement Outcome & Security Diagnosis")
                d_col1, d_col2 = st.columns([1.1, 0.9])
                with d_col1:
                    fig_h2 = plot_measurement_distribution(res2["counts"], th_info_2["probabilities"], shots_2)
                    st.pyplot(fig_h2, use_container_width=True)
                    plt.close(fig_h2)

                with d_col2:
                    if res2["success"] and 3 not in st.session_state.cleared_doors:
                        if st.button("🚪 PROCEED TO AIRLOCK 3 (MASTER VAULT) ➔", key="nxt_d3", type="primary", use_container_width=True):
                            st.session_state.active_door = 3
                            st.rerun()
                    elif not res2["success"]:
                        if st.button("🔄 RETRY PUZZLE (FRESH CONFIGURATION)", key="retry_d2", type="primary", use_container_width=True):
                            st.session_state.last_results[2] = None
                            st.session_state.l2_gates = []
                            st.rerun()

        # ----------------- DOOR 3 WORKBENCH -----------------
        elif curr_door == 3:
            st.markdown(f"### 🛠️ Circuit Workbench — {p_info['title']} ({p_info['difficulty']})")
            wb_col1, wb_col2 = st.columns([2, 1])
            with wb_col1:
                st.write(f"**Protocol:** {p_info['objective']} Initial: `{p_info['initial']}`, Target: `{p_info['target']}`.")
            with wb_col2:
                m_used = len(st.session_state.l3_ops)
                m_max = MAX_MOVES[3]
                m_color = "#10B981" if m_used <= m_max else "#EF4444"
                st.markdown(f"""
                <div style='text-align: right;'>
                    <span class='pill' style='background: #1E293B; color: {m_color}; border: 1px solid {m_color};'>
                        Moves: {m_used} / {m_max} Max
                    </span>
                </div>
                """, unsafe_allow_html=True)

            with st.expander("🔍 Quantum Intel & Physics Briefing (Door 3)", expanded=False):
                st.markdown(r"""
                **Non-Local Entanglement & Bell States:**  
                - Entangling Lock A ($q_0$) and Lock B ($q_1$) creates non-separable two-qubit quantum correlations:
                  - **$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$:** Synchronized Bell pair (0% mismatch readouts: only `00` and `11`).
                  - **$|\Psi^+\rangle = \frac{|01\rangle + |10\rangle}{\sqrt{2}}$:** Anti-correlated Bell pair (0% agreement readouts: only `01` and `10`).
                  - **$|\Phi^-\rangle = \frac{|00\rangle - |11\rangle}{\sqrt{2}}$:** Phase-inverted Bell pair (correlated readouts with $\pi$ phase).
                - **Physical meaning of correlated outcomes:** Measuring either qubit collapses both instantaneously into the designated Bell state basis.
                """)

            st.markdown("##### Apply Quantum Operations to Qubits (q0: Lock A, q1: Lock B)")
            g1, g2, g3, g4, g5, g6, g7, g8, g9, g10 = st.columns([1, 1, 1, 1, 1, 1.15, 1.15, 0.85, 0.85, 1.05])
            with g1:
                if st.button("H(q0)", key="h_q0", use_container_width=True):
                    st.session_state.l3_ops.append(("H", 0))
                    st.session_state.last_results[3] = None
                    st.rerun()
            with g2:
                if st.button("H(q1)", key="h_q1", use_container_width=True):
                    st.session_state.l3_ops.append(("H", 1))
                    st.session_state.last_results[3] = None
                    st.rerun()
            with g3:
                if st.button("X(q0)", key="x_q0", use_container_width=True):
                    st.session_state.l3_ops.append(("X", 0))
                    st.session_state.last_results[3] = None
                    st.rerun()
            with g4:
                if st.button("X(q1)", key="x_q1", use_container_width=True):
                    st.session_state.l3_ops.append(("X", 1))
                    st.session_state.last_results[3] = None
                    st.rerun()
            with g5:
                if st.button("Z(q0)", key="z_q0", use_container_width=True):
                    st.session_state.l3_ops.append(("Z", 0))
                    st.session_state.last_results[3] = None
                    st.rerun()
            with g6:
                if st.button("CNOT(q0→q1)", key="cnot_01", use_container_width=True):
                    st.session_state.l3_ops.append(("CNOT", 0, 1))
                    st.session_state.last_results[3] = None
                    st.rerun()
            with g7:
                if st.button("CNOT(q1→q0)", key="cnot_10", use_container_width=True):
                    st.session_state.l3_ops.append(("CNOT", 1, 0))
                    st.session_state.last_results[3] = None
                    st.rerun()
            with g8:
                undo_d3 = len(st.session_state.l3_ops) == 0
                if st.button("Undo", key="undo_3", use_container_width=True, disabled=undo_d3):
                    st.session_state.l3_ops.pop()
                    st.session_state.last_results[3] = None
                    st.rerun()
            with g9:
                if st.button("Clear", key="clr_3", use_container_width=True):
                    st.session_state.l3_ops = []
                    st.session_state.last_results[3] = None
                    st.rerun()
            with g10:
                h_label = "Hide Intel" if st.session_state.show_hint[3] else "Vault Intel"
                if st.button(h_label, key="hint_btn_3", use_container_width=True):
                    st.session_state.show_hint[3] = not st.session_state.show_hint[3]
                    st.rerun()

            if st.session_state.show_hint[3]:
                if st.session_state.last_results[3] is None:
                    st.info(f"🔒 **Classified Intel:** Execute your initial breach attempt to decrypt specific gate recommendations.\n\n**Mission Objective:** {p_info['objective']}")
                else:
                    st.info(f"💡 **Security Decryption Intel:** {p_info['hint']}")

            if st.session_state.l3_ops:
                formatted_ops = []
                for op in st.session_state.l3_ops:
                    if op[0] == "CNOT":
                        formatted_ops.append(f"<span class='pipeline-chip'>CNOT(q{op[1]}→q{op[2]})</span>")
                    else:
                        formatted_ops.append(f"<span class='pipeline-chip'>{op[0]}(q{op[1]})</span>")
                st.markdown(f"**Dual-Qubit Pipeline:** `|00⟩` ──▶ {' '.join(formatted_ops)} ──▶ `[Measure Both]`", unsafe_allow_html=True)
            else:
                st.caption("Dual-Qubit Pipeline: |00⟩ ──▶ (No operations applied) ──▶ [Measure Both]")

            qc3 = build_level3_circuit(st.session_state.l3_ops, variant=v_idx)
            th_info_3 = get_theoretical_state_info(qc3)

            c_left, c_right = st.columns([1.1, 0.9])
            with c_left:
                st.markdown("##### Real Qiskit Circuit Diagram")
                try:
                    fig_qc3 = qc3.draw(output="mpl", style="iqp-dark")
                    st.pyplot(fig_qc3, use_container_width=False)
                    plt.close(fig_qc3)
                except Exception:
                    st.code(qc3.draw(output="text"), language="text")

            with c_right:
                st.markdown("##### Simulator Execution Controls")
                shots_3 = st.select_slider("Measurement Shots", options=[50, 100, 200, 500], value=200, key="shots_s3")
                is_ent = "YES (Non-separable)" if th_info_3["is_entangled"] else "NO (Separable)"
                st.caption(f"Theoretical Probabilities: `{th_info_3['probabilities']}` | Entangled: `{is_ent}`")

                if st.button("🚀 Execute Circuit on Simulator", key="exec_3", type="primary", use_container_width=True):
                    counts_3 = run_circuit_simulation(qc3, shots=shots_3)
                    eval_3 = evaluate_level3_result(counts_3, moves_used=len(st.session_state.l3_ops), variant=v_idx, total_shots=shots_3, qc=qc3)
                    st.session_state.last_results[3] = eval_3

                    if eval_3["success"]:
                        if 3 not in st.session_state.cleared_doors:
                            st.session_state.cleared_doors.append(3)
                            st.session_state.score += eval_3["score_earned"]
                            st.session_state.final_elapsed_seconds = int(time.time() - st.session_state.start_time)
                            st.session_state.game_state = "VICTORY"
                            rank = add_leaderboard_entry(
                                st.session_state.player_name,
                                st.session_state.score,
                                st.session_state.final_elapsed_seconds,
                                st.session_state.mistakes
                            )
                            st.session_state.leaderboard_rank = rank
                    else:
                        st.session_state.mistakes += 1
                        st.session_state.score = max(0, st.session_state.score - 25)
                        # Rotate to fresh non-repeating variant for Door 3
                        next_v = get_next_puzzle_variant(3, v_idx, st.session_state.seen_puzzles.get(3, []))
                        st.session_state.puzzle_variants[3] = next_v
                        st.session_state.seen_puzzles[3].append(next_v)
                        st.session_state.l3_ops = []
                    st.rerun()

            if st.session_state.last_results[3]:
                res3 = st.session_state.last_results[3]
                st.markdown("---")
                if not res3["success"]:
                    play_audio_feedback("alarm")
                    next_variant_info = PUZZLE_DESCRIPTIONS.get((3, st.session_state.puzzle_variants[3]), {})
                    st.markdown(f"""
                    <div class='alarm-lockdown-container'>
                        <div style='font-size: 1.05rem; font-weight: 800; color: #EF4444; margin-bottom: 4px;'>
                            🚨 SECURITY ALERT: {res3['status_title'].upper()}
                        </div>
                        <div style='font-size: 0.88rem; color: #CBD5E1;'>
                            {res3['explanation']}
                        </div>
                        <div style='margin-top: 8px; font-size: 0.85rem; color: #38BDF8; font-style: italic;'>
                            💡 <b>Operative Intel:</b> Keep going! Security sensors have rotated to a fresh solvable puzzle (<b>{next_variant_info.get('title', 'Next Challenge')}</b>). Click 'Retry Puzzle' below to tackle the new configuration!
                        </div>
                        <div style='font-size: 0.8rem; font-weight: 600; color: #F87171; margin-top: 6px;'>
                            Penalty: -25 PTS applied. Total mistakes: {st.session_state.mistakes}.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("#### 📊 Measurement Outcome & Security Diagnosis")
                d_col1, d_col2 = st.columns([1.1, 0.9])
                with d_col1:
                    fig_h3 = plot_measurement_distribution(res3["counts"], th_info_3["probabilities"], shots_3)
                    st.pyplot(fig_h3, use_container_width=True)
                    plt.close(fig_h3)

                with d_col2:
                    if not res3["success"]:
                        if st.button("🔄 RETRY PUZZLE (FRESH CONFIGURATION)", key="retry_d3", type="primary", use_container_width=True):
                            st.session_state.last_results[3] = None
                            st.session_state.l3_ops = []
                            st.rerun()


# ==============================================================================
# 9. SCREEN 3: CINEMATIC VICTORY SCREEN & PERSISTENT LEADERBOARD
# ==============================================================================
elif st.session_state.game_state == "VICTORY":
    st.balloons()
    play_audio_feedback("success")
    rank_display = f"#{st.session_state.leaderboard_rank}" if st.session_state.leaderboard_rank else "Top Tier"

    st.markdown(f"""
    <div class='start-card' style='border-color: #10B981; box-shadow: 0 0 35px rgba(16, 185, 129, 0.35);'>
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 8px;'>
            <span class='pill pill-cleared'>Mission Accomplished</span>
            <span class='pill pill-active'>Entanglement Vault Breached</span>
        </div>
        <div style='font-size: 2.2rem; font-weight: 850; color: #10B981; margin-bottom: 6px;'>
            HEIST COMPLETED: THE VAULT HAS FALLEN!
        </div>
        <div style='font-size: 1.05rem; color: #CBD5E1; margin-bottom: 24px; line-height: 1.6;'>
            Congratulations, Operative <b>{st.session_state.player_name}</b>. 
            All three quantum security airlocks have been dismantled using authentic Qiskit circuits. 
            The master entanglement key has been extracted. Your performance is permanently logged below.
        </div>
        <div style='display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 24px;'>
            <div class='metric-card'>
                <div class='metric-label'>Final Bounty</div>
                <div class='metric-value' style='color: #10B981;'>{st.session_state.score} PTS</div>
            </div>
            <div class='metric-card'>
                <div class='metric-label'>Elapsed Time</div>
                <div class='metric-value' style='color: #FBBF24;'>{format_elapsed_time(st.session_state.final_elapsed_seconds)}</div>
            </div>
            <div class='metric-card'>
                <div class='metric-label'>Airlocks Cleared</div>
                <div class='metric-value' style='color: #38BDF8;'>3 / 3 (100%)</div>
            </div>
            <div class='metric-card'>
                <div class='metric-label'>Alarms / Mistakes</div>
                <div class='metric-value' style='color: {"#EF4444" if st.session_state.mistakes > 0 else "#34D399"};'>{st.session_state.mistakes}</div>
            </div>
            <div class='metric-card'>
                <div class='metric-label'>Terminal Rank</div>
                <div class='metric-value' style='color: #A78BFA;'>{rank_display}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Local Leaderboard Display
    st.markdown("### 🏆 Local Terminal Leaderboard")
    st.caption("Records are persisted locally on this installation (leaderboard.json).")

    entries = load_leaderboard()
    if entries:
        table_rows = []
        for idx, e in enumerate(entries[:10], 1):
            is_current = (e.get("player_name") == st.session_state.player_name and e.get("score") == st.session_state.score)
            highlight = "style='color: #38BDF8; font-weight: 700; background: rgba(56, 189, 248, 0.08);'" if is_current else ""
            table_rows.append(
                f"<tr {highlight}>"
                f"<td style='padding: 8px 12px;'>#{idx}</td>"
                f"<td style='padding: 8px 12px;'>{e.get('player_name', 'Anon')}</td>"
                f"<td style='padding: 8px 12px;'>{e.get('score', 0)} PTS</td>"
                f"<td style='padding: 8px 12px;'>{format_elapsed_time(e.get('time_seconds', 0))}</td>"
                f"<td style='padding: 8px 12px;'>{e.get('mistakes', 0)}</td>"
                f"<td style='padding: 8px 12px;'>{e.get('rank_title', 'Operative')}</td>"
                f"<td style='padding: 8px 12px; color: #64748B;'>{e.get('timestamp', '')}</td>"
                f"</tr>"
            )

        html_table = f"""
        <div style='background: #0F172A; border: 1px solid #1E293B; border-radius: 8px; overflow-x: auto; margin-bottom: 24px;'>
            <table style='width: 100%; border-collapse: collapse; font-size: 0.88rem; text-align: left;'>
                <thead>
                    <tr style='border-bottom: 1px solid #334155; color: #94A3B8; font-size: 0.75rem; text-transform: uppercase;'>
                        <th style='padding: 10px 12px;'>Rank</th>
                        <th style='padding: 10px 12px;'>Operative</th>
                        <th style='padding: 10px 12px;'>Score</th>
                        <th style='padding: 10px 12px;'>Time</th>
                        <th style='padding: 10px 12px;'>Mistakes</th>
                        <th style='padding: 10px 12px;'>Title</th>
                        <th style='padding: 10px 12px;'>Date</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(table_rows)}
                </tbody>
            </table>
        </div>
        """
        st.markdown(html_table, unsafe_allow_html=True)

    c_btn1, c_btn2, c_btn3 = st.columns([1, 1.8, 1])
    with c_btn2:
        if st.button("🎮 PLAY AGAIN / NEW HEIST (FRESH PUZZLE SEQUENCE)", key="btn_new_game", type="primary", use_container_width=True):
            reset_to_new_game(clear_name=False)
            st.rerun()

    # Credits & Technical Specifications
    st.markdown("---")
    st.markdown("""
    <div style='background: #090E17; border: 1px solid #1E293B; border-radius: 8px; padding: 18px 22px; font-size: 0.85rem; color: #94A3B8; line-height: 1.6;'>
        <b>Credits & Technical Specifications (Qiskit Fall Fest 2026, IIIT Kottayam):</b><br>
        • <b>Quantum Core:</b> Built using genuine IBM Qiskit (v2.5.2) and Qiskit Aer simulator. Zero classical random-number substitutions.<br>
        • <b>Event Context:</b> Created as an educational quantum game for Track 1 of the Qiskit Fall Fest 2026 Hackathon organized by IIIT Kottayam.<br>
        • <b>Hardware Note:</b> Simulates ideal quantum execution locally. Does not claim quantum computational supremacy or execution on physical quantum hardware.
    </div>
    """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 10. FOOTER
# ------------------------------------------------------------------------------
st.markdown("---")
f_col1, f_col2 = st.columns([3, 1])
with f_col1:
    st.caption(
        "Quantum Heist: Break the Entanglement Vault | Built for Qiskit Fall Fest 2026 (Track 1) | "
        "Powered by IBM Qiskit. Real quantum circuits; no classical pseudo-random substitutions."
    )
with f_col2:
    st.caption("IIIT Kottayam Hackathon Sprint")
