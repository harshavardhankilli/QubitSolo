# 📘 Quantum Heist: Break the Entanglement Vault — Code & Concept Explanation
**Participant Presentation & Judge Walkthrough Guide (Qiskit Fall Fest 2026, Track 1)**

---

## 🌟 1. Project Overview & Architecture

**Quantum Heist: Break the Entanglement Vault** is an interactive, mission-based quantum puzzle game. Players assume the role of an elite quantum infiltrator tasked with bypassing three security layers of the high-security Entanglement Vault:
- **Door 1:** Laser Grid — Reach target state $|1\rangle$ using single-qubit gates within 2 moves.
- **Door 2:** Dual-Sensor — Create balanced superposition $\frac{|0\rangle + |1\rangle}{\sqrt{2}}$ using $H$ within 2 moves (avoiding $H \cdot H = I$ cancellation).
- **Door 3:** Master Vault — Entangle Lock A ($q_0$) and Lock B ($q_1$) into Bell State $|\Phi^+\rangle$ using $H$ and $CNOT$ with 0% mismatch within 3 operations.

```text
QubitSolo-main/
├── README.md               # Mandatory hackathon submission file (exact template headings preserved)
├── CODE_EXPLANATION.md     # Comprehensive code & concept guide
├── JUDGE_QA.md             # Likely judge questions & winning, concise answers
├── requirements.txt        # Qiskit, Qiskit-Aer, Streamlit, Matplotlib
├── src/
│   ├── quantum_circuits.py # Quantum core: Circuit builders, move limits, hints & scoring
│   ├── app.py              # Streamlit cyber-heist web application & victory dashboard
│   ├── leaderboard.py      # Local leaderboard persistence engine
│   └── main.py             # Dual CLI runner & Streamlit app launcher
└── notebooks/
    └── solution.ipynb      # Runnable Jupyter notebook with pre-executed outputs
```

---

## 🔬 2. Quantum Concepts Explained

### Concept 1: Qubit & Quantum State ($|0\rangle, |1\rangle$)
A classical bit can only be `0` or `1`. A qubit is a two-level quantum system represented as a state vector:
$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$$
where $\alpha, \beta \in \mathbb{C}$, $|\alpha|^2$ is the probability of measuring $0$, and $|\beta|^2$ is the probability of measuring $1$, with the normalization condition $|\alpha|^2 + |\beta|^2 = 1$. When measured in the computational $Z$-basis, the superposition collapses probabilistically to either $|0\rangle$ or $|1\rangle$.

---

### Concept 2: Pauli-X Gate (Bit-Flip / Quantum NOT)
The $X$ gate acts like a quantum NOT gate. It rotates the qubit state by $\pi$ radians around the X-axis of the Bloch sphere:
$$X|0\rangle = |1\rangle, \quad X|1\rangle = |0\rangle$$
Matrix representation:
$$X = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}$$
In Door 1, applying $X$ to ground state $|0\rangle$ yields excited state $|1\rangle$ with 100% deterministic certainty.

---

### Concept 3: Pauli-Z Gate (Phase-Flip)
The $Z$ gate leaves $|0\rangle$ unchanged and applies a relative negative phase to $|1\rangle$:
$$Z|0\rangle = |0\rangle, \quad Z|1\rangle = -|1\rangle$$
Matrix representation:
$$Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$
Pauli-$Z$ is critical in quantum interference and state engineering challenges requiring phase inversion.

---

### Concept 4: Hadamard ($H$) Gate & Superposition
The Hadamard gate transforms computational basis states into equal superposition states:
$$H|0\rangle = |+\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$
$$H|1\rangle = |-\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$$
When measured, $|+\rangle$ yields approximately 50% probability of $0$ and 50% probability of $1$.
**Self-Inversion / Unitarity:** Because $H$ is Hermitian and unitary ($H = H^\dagger = H^{-1}$):
$$H \cdot H = I$$
Applying $H$ twice causes destructive interference on $|1\rangle$ and constructive interference on $|0\rangle$, returning the state to $|0\rangle$. Door 2 uses this property to test the player's grasp of quantum interference.

---

### Concept 5: CNOT Gate & Quantum Entanglement (Bell States)
The Controlled-NOT ($CNOT$) gate operates on two qubits: it flips the target qubit if and only if the control qubit is in state $|1\rangle$.
When combined with a Hadamard gate on the control qubit:
$$|00\rangle \xrightarrow{H(0)} \frac{|00\rangle + |10\rangle}{\sqrt{2}} \xrightarrow{CNOT(0,1)} |\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$
This prepares the maximally entangled **Bell State** $|\Phi^+\rangle$. The joint wave function cannot be factored into two independent single-qubit states ($|\psi_A\rangle \otimes |\psi_B\rangle$).
When measured across 200 shots, the outcomes collapse into either `00` or `11` with ~50% probability each, while mismatched outcomes (`01` and `10`) have an exact theoretical probability of **0.0%**.

---

## 📂 3. Source File Breakdown & Line-by-Line Logic

### File 1: `src/quantum_circuits.py`
The pure quantum mechanics logic module:
- `MAX_MOVES`: Dictionary setting strict move allowances (`{1: 2, 2: 2, 3: 3}`).
- `PUZZLE_DESCRIPTIONS`: 12 mathematically verified, solvable puzzle variants (4 per door).
- `get_next_puzzle_variant(door, current, seen_history)`: Dynamically selects an alternate puzzle variant, avoiding immediate or session repeats.
- `generate_new_game_puzzles()`: Seeds a randomized sequence of valid puzzles for a fresh game.
- `run_circuit_simulation(circuit, shots)`: Executes circuits on `AerSimulator` (or `StatevectorSampler`) and returns measurement count dictionary.
- `get_theoretical_state_info(circuit)`: Uses Qiskit's `Statevector` to calculate exact mathematical basis state probabilities and phases prior to measurement.
- `build_level1_circuit(gate_sequence, variant)`: Constructs 1-qubit circuit with user gates and measurement.
- `evaluate_level1_result(counts, moves_used, variant, shots, qc)`: Evaluates target state certainty and relative phase.
- `build_level2_circuit(gate_sequence, variant)`: Constructs 1-qubit circuit for superposition/interference.
- `evaluate_level2_result(counts, moves_used, variant, shots, qc)`: Evaluates statistical balance ($\ge 35\%$) or destructive collapse.
- `build_level3_circuit(operations, variant)`: Constructs 2-qubit circuit with $H$ and $CNOT$.
- `evaluate_level3_result(counts, moves_used, variant, shots, qc)`: Evaluates 0% forbidden mismatch readouts for Bell states.

### File 2: `src/app.py`
The Streamlit cinematic cyber-heist web application:
- **Scene A (Cinematic Opening):** Hero banner with title, badges, story, and `START HEIST` button.
- **Scene B (Player Entry):** Input validation requiring a non-empty codename, terminal briefing, and `BEGIN MISSION` trigger.
- **Fair Mission Clock:** The infiltration timer begins strictly when the operative begins the mission.
- **Sequential Door Gating:** Door 2 is strictly locked until Door 1 is cleared; Door 3 is strictly locked until Door 2 is cleared.
- **Audio & Visual Feedback:** Non-blocking Web Audio API synthesis and CSS sliding blast door animations.
- **Dynamic Retry System:** Failed attempts trigger emergency strobe alarms, apply a -25 PTS penalty, and provide a `RETRY PUZZLE` button that loads a new solvable configuration.
- **Circuit Workbench:** High-contrast gate buttons, pipeline chips, undo/clear controls, and protected `Vault Intel` hints that decrypt after initial attempt.
- **Circuit Diagrams & Dual Histograms:** Native dark Qiskit Matplotlib rendering (`style='iqp-dark'`) and high-contrast empirical vs theoretical probability comparison charts.
- **Scene F (Results & Leaderboard):** Displays 5 telemetry cards, balloons, and appends records to `leaderboard.json`.
- **New Heist Reset:** `reset_to_new_game()` scrubs all stale state and regenerates fresh puzzles.

### File 3: `src/leaderboard.py`
Local leaderboard storage and retrieval:
- Persists operative run histories (player name, final score, time in seconds, mistakes, timestamp, and rank title) in `leaderboard.json`.
- Automatically sorts records by highest score, then lowest time, then lowest mistakes.

### File 4: `src/main.py`
Multi-mode CLI and launcher:
- Terminal gameplay (`python src/main.py --cli`) with move tracking, hints, and score.
- Streamlit web launcher (`python src/main.py --web`).
- UTF-8 console output configured to prevent Windows encoding issues.

### File 5: `notebooks/solution.ipynb`
Contains all pre-executed circuits, text diagrams, and simulation outputs for all 3 doors.

---

## 🎮 4. Dynamic Puzzle Variations & Solvability Matrix (12 Verified Variants)

| Door | Variant | Difficulty | Mission Challenge | Initial State | Target State | Solvable Move Sequence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Door 1** | **1.1 (Alpha)** | Easy | Bit-Flip Inversion | $\|0\rangle$ | $\|1\rangle$ | `['X']` |
| **Door 1** | **1.2 (Beta)** | Easy | Polarity Neutralizer | $\|1\rangle$ (Excited) | $\|0\rangle$ | `['X']` |
| **Door 1** | **1.3 (Gamma)** | Medium | Phase & Bit Inversion | $\|0\rangle$ | $-\|1\rangle$ | `['X', 'Z']` |
| **Door 1** | **1.4 (Delta)** | Medium | Unitarity 2-Gate Loop | $\|0\rangle$ | $\|0\rangle$ | `['X', 'X']` or `['H', 'H']` |
| **Door 2** | **2.1 (Alpha)** | Medium | Symmetric Superposition | $\|0\rangle$ | $\|+\rangle = \frac{\|0\rangle + \|1\rangle}{\sqrt{2}}$ | `['H']` |
| **Door 2** | **2.2 (Beta)** | Medium | Phase Superposition | $\|1\rangle$ (Excited) | $\|-\rangle = \frac{\|0\rangle - \|1\rangle}{\sqrt{2}}$ | `['H']` |
| **Door 2** | **2.3 (Gamma)** | Hard | Destructive Interference | $\|+\rangle$ (Superposition) | $\|0\rangle$ | `['H']` |
| **Door 2** | **2.4 (Delta)** | Hard | Phase Superposition Synth | $\|0\rangle$ | $\|-\rangle = \frac{\|0\rangle - \|1\rangle}{\sqrt{2}}$ | `['X', 'H']` or `['H', 'Z']` |
| **Door 3** | **3.1 (Alpha)** | Hard | Correlated Bell Lock $\|\Phi^+\rangle$ | $\|00\rangle$ | $\frac{\|00\rangle + \|11\rangle}{\sqrt{2}}$ | `[('H', 0), ('CNOT', 0, 1)]` |
| **Door 3** | **3.2 (Beta)** | Hard | Reverse Control Bell $\|\Phi^+\rangle$ | $\|00\rangle$ | $\frac{\|00\rangle + \|11\rangle}{\sqrt{2}}$ | `[('H', 1), ('CNOT', 1, 0)]` |
| **Door 3** | **3.3 (Gamma)** | Master | Anti-Correlated Bell $\|\Psi^+\rangle$ | $\|00\rangle$ | $\frac{\|01\rangle + \|10\rangle}{\sqrt{2}}$ | `[('X', 1), ('H', 0), ('CNOT', 0, 1)]` |
| **Door 3** | **3.4 (Delta)** | Master | Phase-Inverted Bell $\|\Phi^-\rangle$ | $\|00\rangle$ | $\frac{\|00\rangle - \|11\rangle}{\sqrt{2}}$ | `[('H', 0), ('Z', 0), ('CNOT', 0, 1)]` |

*Note: The dynamic selection engine avoids repeating recently shown puzzles in the same infiltration session, and 'New Game' or 'Try Again' generates fresh randomized sequences.*

---

## 🗣️ 5. Judge Elevator Pitch & Presentation Script

> *"Respected judges, our project is **Quantum Heist: Break the Entanglement Vault**, developed for Track 1 of the Qiskit Fall Fest 2026 Hackathon.*  
> *In this game, the player acts as a quantum infiltrator tasked with breaching three sequential security airlocks of Vault Sigma-9 within strict move allowances:*  
> *1. **Door 1 (Laser Grid):** The player engineers single-qubit basis state rotations using Pauli-X and Pauli-Z gates (Max 2 moves).*  
> *2. **Door 2 (Dual-Sensor):** The player balances a dual-sensor in quantum superposition using Hadamard gates, learning quantum phase and destructive self-interference ($H \cdot H = I$).*  
> *3. **Door 3 (Master Vault):** The player entangles Lock A and Lock B into a Bell State using H and CNOT gates, achieving 100% correlation agreement with 0% mismatch readouts.*  
> *Every puzzle outcome is computed in real time using genuine IBM Qiskit QuantumCircuit compilation and AerSimulator execution—with zero classical random-number substitutions. The game features an adaptive retry engine with 12 solvable puzzle variants, move tracking, fair mission clock, and persistent local leaderboard scoring."*
