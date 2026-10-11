"""
quantum_circuits.py - Core Quantum Engine for "Quantum Heist: Break the Entanglement Vault"
Author: Qiskit Fall Fest 2026 Hackathon Team (Track 1)

This module handles:
1. Genuine Qiskit QuantumCircuit construction for all 3 heist vault levels with diverse, solvable puzzle variants.
2. Authentic quantum circuit execution using Qiskit AerSimulator (or StatevectorSampler).
3. Exact theoretical Statevector analysis (amplitudes, phases & probabilities) alongside empirical shots.
4. Strategic evaluation: target states, limited move allowances, measurement evaluation, and scoring.
5. Dynamic puzzle generation avoiding recently shown variants in the same session.
"""

import random
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

# Try importing Qiskit AerSimulator, otherwise fall back to StatevectorSampler
try:
    from qiskit_aer import AerSimulator
    AER_AVAILABLE = True
except ImportError:
    AER_AVAILABLE = False

from qiskit.primitives import StatevectorSampler

# Maximum allowed moves/operations per door
MAX_MOVES = {
    1: 2,  # Door 1: Single-qubit state challenges
    2: 2,  # Door 2: Superposition & interference challenges
    3: 3   # Door 3: Two-qubit Bell state entanglement challenges
}

# 12 diverse, mathematically verified puzzle variants (4 per door)
PUZZLE_DESCRIPTIONS = {
    # ----------------- DOOR 1: SINGLE-QUBIT STATE ENGINEERING -----------------
    (1, 1): {
        "title": "Laser Grid Protocol Alpha (Bit-Flip)",
        "difficulty": "Easy",
        "initial": "|0⟩",
        "target": "|1⟩",
        "objective": "Transform ground state |0⟩ into excited state |1⟩ with 100% deterministic certainty.",
        "hint": "Apply a Pauli-X gate to perform a quantum bit-flip, rotating |0⟩ into |1⟩."
    },
    (1, 2): {
        "title": "Laser Grid Protocol Beta (Polarity Neutralizer)",
        "difficulty": "Easy",
        "initial": "|1⟩ (Excited Base)",
        "target": "|0⟩",
        "objective": "The laser security base is primed to |1⟩. Invert the excited qubit back into ground state |0⟩.",
        "hint": "The qubit begins in |1⟩. Applying a Pauli-X gate inverts |1⟩ directly back to |0⟩."
    },
    (1, 3): {
        "title": "Laser Grid Protocol Gamma (Phase & Bit Inversion)",
        "difficulty": "Medium",
        "initial": "|0⟩",
        "target": "-|1⟩",
        "objective": "The optical sensor requires an excited eigenstate with inverted phase -|1⟩ (flip bit, then flip phase).",
        "hint": "Apply Pauli-X to reach |1⟩, then Pauli-Z to apply relative negative phase: Z(X|0⟩) = -|1⟩."
    },
    (1, 4): {
        "title": "Laser Grid Protocol Delta (Unitarity Loop)",
        "difficulty": "Medium",
        "initial": "|0⟩",
        "target": "|0⟩ (2-Gate Loop)",
        "objective": "Prove gate self-inversion (U·U = I). Apply exactly 2 operations that return deterministically to |0⟩.",
        "hint": "Pauli-X and Hadamard are Hermitian and unitary: X·X = I and H·H = I. Apply two identical gates!"
    },

    # ----------------- DOOR 2: SUPERPOSITION & INTERFERENCE -----------------
    (2, 1): {
        "title": "Dual-Sensor Phase Alpha (Symmetric Superposition)",
        "difficulty": "Medium",
        "initial": "|0⟩",
        "target": "(|0⟩ + |1⟩)/√2",
        "objective": "Create balanced quantum superposition from ground state |0⟩ so measurements split ~50/50.",
        "hint": "Apply a single Hadamard (H) gate to split |0⟩ into equal superposition (|0⟩ + |1⟩)/√2."
    },
    (2, 2): {
        "title": "Dual-Sensor Phase Beta (Negative Superposition)",
        "difficulty": "Medium",
        "initial": "|1⟩ (Excited Base)",
        "target": "(|0⟩ - |1⟩)/√2",
        "objective": "The sensor base begins in |1⟩. Apply Hadamard to create the phase superposition |−⟩ (measuring ~50/50).",
        "hint": "Applying H to excited state |1⟩ produces the phase superposition state |−⟩ = (|0⟩ − |1⟩)/√2."
    },
    (2, 3): {
        "title": "Dual-Sensor Phase Gamma (Interference Collapse)",
        "difficulty": "Hard",
        "initial": "|+⟩ (Superposition Base)",
        "target": "|0⟩",
        "objective": "The sensor is stuck in superposition |+⟩. Use destructive interference to collapse the beam entirely into |0⟩.",
        "hint": "Applying Hadamard to |+⟩ causes destructive interference for |1⟩, returning 100% of shots to |0⟩ (H·H = I)!"
    },
    (2, 4): {
        "title": "Dual-Sensor Phase Delta (Phase Superposition Synthesis)",
        "difficulty": "Hard",
        "initial": "|0⟩",
        "target": "(|0⟩ - |1⟩)/√2",
        "objective": "Synthesize negative-phase superposition |−⟩ from ground state |0⟩ using 2 gates.",
        "hint": "Flip to |1⟩ with X, then apply H (X then H), or create |+⟩ with H and invert phase with Z (H then Z)!"
    },

    # ----------------- DOOR 3: TWO-QUBIT BELL ENTANGLEMENT -----------------
    (3, 1): {
        "title": "Master Vault: Synchronized Bell Lock (|Φ+⟩)",
        "difficulty": "Hard",
        "initial": "|00⟩",
        "target": "Bell State |Φ+⟩ = (|00⟩ + |11⟩)/√2",
        "objective": "Entangle Lock A (q0) and Lock B (q1) into Bell state |Φ+⟩ so outcomes synchronize ('00' or '11') with 0% mismatch.",
        "hint": "Apply H on Qubit 0, followed by CNOT(0 → 1). This entangles q0 and q1 into |Φ+⟩."
    },
    (3, 2): {
        "title": "Master Vault: Reverse Control Lock (|Φ+⟩)",
        "difficulty": "Hard",
        "initial": "|00⟩",
        "target": "Bell State |Φ+⟩ = (|00⟩ + |11⟩)/√2",
        "objective": "Security rerouted the primary bus to Lock B (q1). Entangle by applying H to Qubit 1 and CNOT(1 → 0)!",
        "hint": "Apply H on Qubit 1, followed by CNOT(1 → 0). This also prepares the synchronized Bell state |Φ+⟩!"
    },
    (3, 3): {
        "title": "Master Vault: Anti-Correlated Bell Lock (|Ψ+⟩)",
        "difficulty": "Master",
        "initial": "|00⟩",
        "target": "Bell State |Ψ+⟩ = (|01⟩ + |10⟩)/√2",
        "objective": "The vault switched to anti-synchronous locks! Entangle so outcomes alternate (only '01' or '10', 0% '00'/'11').",
        "hint": "Flip Qubit 1 with an X gate, then apply H(q0) and CNOT(0 → 1). This creates the anti-correlated Bell state |Ψ+⟩!"
    },
    (3, 4): {
        "title": "Master Vault: Phase-Inverted Bell Lock (|Φ-⟩)",
        "difficulty": "Master",
        "initial": "|00⟩",
        "target": "Bell State |Φ-⟩ = (|00⟩ - |11⟩)/√2",
        "objective": "The master lock requires phase-inverted Bell state |Φ-⟩. Prepare correlated readouts ('00' and '11') with π phase.",
        "hint": "Apply H(q0), then Z(q0) to flip phase, then CNOT(0 → 1). This prepares the phase-inverted Bell state |Φ-⟩!"
    }
}

# Backward compatibility alias for level hints
LEVEL_HINTS = {
    1: PUZZLE_DESCRIPTIONS[(1, 1)]["hint"],
    2: PUZZLE_DESCRIPTIONS[(2, 1)]["hint"],
    3: PUZZLE_DESCRIPTIONS[(3, 1)]["hint"]
}


def get_next_puzzle_variant(door: int, current_variant: int, seen_history: list = None) -> int:
    """
    Selects a different valid puzzle variant for the given door.
    Avoids repeating the current variant and recently seen variants in the session.
    """
    available = [1, 2, 3, 4]
    candidates = [v for v in available if v != current_variant]

    if seen_history:
        # Prefer candidates not in recently seen history
        unseen = [v for v in candidates if v not in seen_history]
        if unseen:
            return random.choice(unseen)

    return random.choice(candidates)


def generate_new_game_puzzles() -> dict:
    """
    Generates a fresh puzzle sequence across all three doors for a new game.
    """
    return {
        1: random.choice([1, 2, 3, 4]),
        2: random.choice([1, 2, 3, 4]),
        3: random.choice([1, 2, 3, 4])
    }


def run_circuit_simulation(circuit: QuantumCircuit, shots: int = 200) -> dict:
    """
    Executes a Qiskit QuantumCircuit on a quantum simulator and returns measurement counts.
    Never uses pseudo-random numbers.
    """
    if AER_AVAILABLE:
        simulator = AerSimulator()
        job = simulator.run(circuit, shots=shots)
        result = job.result()
        return result.get_counts()
    else:
        sampler = StatevectorSampler()
        job = sampler.run([circuit], shots=shots)
        pub_result = job.result()[0]
        data_dict = pub_result.data
        for reg_name in data_dict:
            reg_data = getattr(data_dict, reg_name)
            if hasattr(reg_data, "get_counts"):
                return reg_data.get_counts()
        return {"0": shots}


def get_theoretical_state_info(circuit: QuantumCircuit) -> dict:
    """
    Computes exact theoretical statevector and state probabilities prior to measurement.
    """
    try:
        qc_pure = circuit.copy()
        qc_pure.remove_final_measurements(inplace=True)
        sv = Statevector.from_instruction(qc_pure)
        probs_raw = sv.probabilities_dict()

        probs = {}
        for bitstr, p in probs_raw.items():
            p_float = float(p)
            if p_float > 1e-5:
                probs[str(bitstr)] = round(p_float, 4)

        is_entangled = False
        if circuit.num_qubits == 2:
            has_00 = probs.get("00", 0) > 0.3
            has_11 = probs.get("11", 0) > 0.3
            has_01 = probs.get("01", 0) > 0.3
            has_10 = probs.get("10", 0) > 0.3
            if (has_00 and has_11 and probs.get("01", 0) < 0.05 and probs.get("10", 0) < 0.05) or \
               (has_01 and has_10 and probs.get("00", 0) < 0.05 and probs.get("11", 0) < 0.05):
                is_entangled = True

        return {
            "probabilities": probs,
            "is_entangled": is_entangled,
            "num_qubits": circuit.num_qubits,
            "statevector": sv
        }
    except Exception:
        return {"probabilities": {}, "is_entangled": False, "num_qubits": circuit.num_qubits, "statevector": None}


# ==============================================================================
# LEVEL 1: Security Laser Grid
# ==============================================================================

def build_level1_circuit(gate_sequence: list, variant: int = 1) -> QuantumCircuit:
    """
    Constructs 1-qubit circuit for Door 1 based on active variant.
    """
    circuit = QuantumCircuit(1, 1)

    if variant == 2:
        # Primed to |1>
        circuit.x(0)
        circuit.barrier(label="Sensor Base |1⟩")

    for gate in gate_sequence:
        g = gate.strip().upper()
        if g == "X":
            circuit.x(0)
        elif g == "Z":
            circuit.z(0)
        elif g == "H":
            circuit.h(0)

    circuit.measure(0, 0)
    return circuit


def evaluate_level1_result(counts: dict, moves_used: int, variant: int = 1, total_shots: int = 200, qc: QuantumCircuit = None) -> dict:
    """
    Evaluates Door 1.
    """
    total_shots = sum(counts.values()) if (counts and sum(counts.values()) > 0) else total_shots
    count_0 = counts.get("0", 0)
    count_1 = counts.get("1", 0)

    exceeded_moves = moves_used > MAX_MOVES[1]

    if variant == 1:
        # Target |1>
        is_success = (count_1 == total_shots) and not exceeded_moves
        target_bit = "1"
        other_bit = "0"
        status_title = "Door 1 Bypassed Successfully" if is_success else "Access Denied — Incorrect State"
        explanation = (
            f"All {total_shots} measurement shots collapsed deterministically to target state |1⟩ within {moves_used}/{MAX_MOVES[1]} moves."
            if is_success else
            "Measurements collapsed to |0⟩ or superposition. Apply Pauli-X to rotate basis state into |1⟩."
        )

    elif variant == 2:
        # Target |0>
        is_success = (count_0 == total_shots) and not exceeded_moves
        target_bit = "0"
        other_bit = "1"
        status_title = "Laser Sensor Neutralized" if is_success else "Access Denied — Incorrect State"
        explanation = (
            f"All {total_shots} measurement shots collapsed to ground state |0⟩ within {moves_used}/{MAX_MOVES[1]} moves."
            if is_success else
            "Sensor remained in excited state |1⟩. Apply Pauli-X to invert the primed basis state back to |0⟩."
        )

    elif variant == 3:
        # Target -|1> (Phase & Bit Inversion)
        has_phase = False
        if qc is not None:
            th = get_theoretical_state_info(qc)
            if th.get("statevector") is not None:
                val = th["statevector"].data[1]
                has_phase = (val.real < -0.9)
        else:
            has_phase = (count_1 == total_shots)

        is_success = (count_1 == total_shots) and has_phase and not exceeded_moves
        target_bit = "1"
        other_bit = "0"
        status_title = "Phase & Bit Inversion Complete" if is_success else "Access Denied — Phase/State Mismatch"
        explanation = (
            f"Successfully flipped the bit to |1⟩ and inverted relative phase to -|1⟩ using X and Z within {moves_used}/{MAX_MOVES[1]} moves."
            if is_success else
            "Sensor requires both bit-flip to |1⟩ and negative phase via Pauli-Z (e.g. sequence: X then Z)."
        )

    elif variant == 4:
        # Unitarity loop: Target |0> with exactly 2 moves
        correct_depth = (moves_used == 2)
        is_success = (count_0 == total_shots) and correct_depth
        target_bit = "0"
        other_bit = "1"
        status_title = "Unitarity Loop Verified" if is_success else "Access Denied — Unitarity Incomplete"
        explanation = (
            f"Unitarity loop confirmed: applied 2 self-inverting gates returning |0⟩ deterministically to |0⟩."
            if is_success else
            f"Requires exactly 2 operations demonstrating gate self-inversion (U·U=I, e.g. X then X, or H then H) returning to |0⟩."
        )

    if is_success:
        bonus = 50 if moves_used <= 1 else 20
        earned_score = 100 + bonus
    else:
        earned_score = 0
        if exceeded_moves:
            status_title = "Alarm Triggered — Move Limit Exceeded"
            explanation = f"Security detected excessive operations ({moves_used}/{MAX_MOVES[1]})."

    pct_target = (counts.get(target_bit, 0) / total_shots) * 100

    return {
        "success": is_success,
        "percentage_target": pct_target,
        "counts": counts,
        "score_earned": earned_score,
        "moves_used": moves_used,
        "max_moves": MAX_MOVES[1],
        "status_title": status_title,
        "explanation": explanation,
        "message": f"{status_title}: {explanation}"
    }


# ==============================================================================
# LEVEL 2: The Quantum Dual-Sensor (Superposition & Interference)
# ==============================================================================

def build_level2_circuit(gate_sequence: list, variant: int = 1) -> QuantumCircuit:
    """
    Constructs 1-qubit circuit for Door 2 based on active variant.
    """
    circuit = QuantumCircuit(1, 1)

    if variant == 2:
        circuit.x(0)
        circuit.barrier(label="Sensor Base |1⟩")
    elif variant == 3:
        circuit.h(0)
        circuit.barrier(label="Superposition Base |+⟩")

    for gate in gate_sequence:
        g = gate.strip().upper()
        if g == "H":
            circuit.h(0)
        elif g == "X":
            circuit.x(0)
        elif g == "Z":
            circuit.z(0)

    circuit.measure(0, 0)
    return circuit


def evaluate_level2_result(counts: dict, moves_used: int, variant: int = 1, total_shots: int = 200, qc: QuantumCircuit = None) -> dict:
    """
    Evaluates Door 2.
    """
    total_shots = sum(counts.values()) if (counts and sum(counts.values()) > 0) else total_shots
    count_0 = counts.get("0", 0)
    count_1 = counts.get("1", 0)
    pct_0 = (count_0 / total_shots) * 100
    pct_1 = (count_1 / total_shots) * 100

    exceeded_moves = moves_used > MAX_MOVES[2]

    if variant in [1, 2]:
        # Balanced superposition: both outcomes >= 35%
        is_success = (pct_0 >= 35.0 and pct_1 >= 35.0) and not exceeded_moves
        status_title = "Door 2 Sensor Deactivated" if is_success else "Access Denied"
        explanation = (
            f"Balanced superposition established (|0⟩: {pct_0:.1f}%, |1⟩: {pct_1:.1f}%) within {moves_used}/{MAX_MOVES[2]} moves."
            if is_success else
            "Failed balance criteria. Apply a single Hadamard (H) gate to create equal amplitudes."
        )

    elif variant == 3:
        # Destructive interference from |+> back to |0>
        is_success = (count_0 == total_shots) and not exceeded_moves
        status_title = "Destructive Interference Achieved" if is_success else "Access Denied — Superposition Persists"
        explanation = (
            f"Destructive interference cancelled excitation; 100% collapsed to ground state |0⟩."
            if is_success else
            "Sensor remained in superposition. Apply Hadamard (H) to destructively cancel state |1⟩ (H·|+⟩ = |0⟩)."
        )

    elif variant == 4:
        # Phase superposition synthesis |-> from |0>
        has_neg_phase = False
        if qc is not None:
            th = get_theoretical_state_info(qc)
            if th.get("statevector") is not None:
                val1 = th["statevector"].data[1]
                has_neg_phase = (val1.real < -0.5)
        else:
            has_neg_phase = True

        is_success = (pct_0 >= 35.0 and pct_1 >= 35.0) and has_neg_phase and not exceeded_moves
        status_title = "Phase Superposition Synthesized" if is_success else "Access Denied — Phase/Balance Incorrect"
        explanation = (
            f"Synthesized negative-phase superposition |−⟩ (|0⟩: {pct_0:.1f}%, |1⟩: {pct_1:.1f}%) within {moves_used}/{MAX_MOVES[2]} moves."
            if is_success else
            "Requires state |−⟩ = (|0⟩ - |1⟩)/√2. Apply X then H, or H then Z to synthesize relative negative phase."
        )

    if is_success:
        bonus = 50 if moves_used == 1 else 25
        earned_score = 150 + bonus
    else:
        earned_score = 0
        if exceeded_moves:
            status_title = "Alarm Triggered — Move Limit Exceeded"
            explanation = f"Applied {moves_used} operations, exceeding Door 2 limit of {MAX_MOVES[2]}."

    return {
        "success": is_success,
        "pct_0": pct_0,
        "pct_1": pct_1,
        "counts": counts,
        "score_earned": earned_score,
        "moves_used": moves_used,
        "max_moves": MAX_MOVES[2],
        "status_title": status_title,
        "explanation": explanation,
        "message": f"{status_title}: {explanation}"
    }


# ==============================================================================
# LEVEL 3: The Entangled Master Vault (Bell States)
# ==============================================================================

def build_level3_circuit(operations: list, variant: int = 1) -> QuantumCircuit:
    """
    Constructs 2-qubit circuit for Door 3 based on active variant.
    """
    circuit = QuantumCircuit(2, 2)

    for op in operations:
        name = op[0].upper()
        if name == "H":
            circuit.h(op[1])
        elif name == "X":
            circuit.x(op[1])
        elif name == "Z":
            circuit.z(op[1])
        elif name in ["CNOT", "CX"]:
            circuit.cx(op[1], op[2])

    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit


def evaluate_level3_result(counts: dict, moves_used: int, variant: int = 1, total_shots: int = 200, qc: QuantumCircuit = None) -> dict:
    """
    Evaluates Door 3 based on active variant.
    """
    total_shots = sum(counts.values()) if (counts and sum(counts.values()) > 0) else total_shots
    count_00 = counts.get("00", 0)
    count_11 = counts.get("11", 0)
    count_01 = counts.get("01", 0)
    count_10 = counts.get("10", 0)

    pct_00 = (count_00 / total_shots) * 100
    pct_11 = (count_11 / total_shots) * 100
    pct_01 = (count_01 / total_shots) * 100
    pct_10 = (count_10 / total_shots) * 100

    exceeded_moves = moves_used > MAX_MOVES[3]

    if variant in [1, 2]:
        # Synchronized Bell State |Phi+>: correlated '00' and '11' with 0% mismatch
        mismatch_shots = count_01 + count_10
        pct_mismatch = (mismatch_shots / total_shots) * 100
        is_success = (mismatch_shots == 0 and pct_00 >= 30.0 and pct_11 >= 30.0) and not exceeded_moves
        target_name = "Bell State |Φ+⟩"
        status_title = "Master Vault Breached" if is_success else "Desynchronization Detected"
        explanation = (
            f"Lock A and Lock B are maximally entangled in {target_name}. Exactly 0.0% forbidden mismatches across {total_shots} shots."
            if is_success else
            f"Observed {mismatch_shots} mismatch readouts ({pct_mismatch:.1f}%). Requires genuine entanglement via H and CNOT."
        )

    elif variant == 3:
        # Anti-Correlated Bell State |Psi+>: only '01' and '10' with 0% mismatch
        mismatch_shots = count_00 + count_11
        pct_mismatch = (mismatch_shots / total_shots) * 100
        is_success = (mismatch_shots == 0 and pct_01 >= 30.0 and pct_10 >= 30.0) and not exceeded_moves
        target_name = "Anti-Correlated Bell State |Ψ+⟩"
        status_title = "Anti-Correlated Vault Breached" if is_success else "Correlation Mismatch"
        explanation = (
            f"Lock A and Lock B are entangled in {target_name}. Exactly 0.0% forbidden '00'/'11' readouts across {total_shots} shots."
            if is_success else
            f"Observed {mismatch_shots} forbidden readouts ({pct_mismatch:.1f}%). Apply X on q1, then H(q0) and CNOT(0→1)."
        )

    elif variant == 4:
        # Phase-Inverted Bell State |Phi->: correlated '00' and '11' with negative relative phase
        mismatch_shots = count_01 + count_10
        pct_mismatch = (mismatch_shots / total_shots) * 100
        has_neg_phase = False
        if qc is not None:
            th = get_theoretical_state_info(qc)
            if th.get("statevector") is not None:
                val11 = th["statevector"].data[3]
                has_neg_phase = (val11.real < -0.4)
        else:
            has_neg_phase = True

        is_success = (mismatch_shots == 0 and pct_00 >= 30.0 and pct_11 >= 30.0 and has_neg_phase) and not exceeded_moves
        target_name = "Phase-Inverted Bell State |Φ-⟩"
        status_title = "Phase-Inverted Bell Vault Breached" if is_success else "Phase/Correlation Mismatch"
        explanation = (
            f"Lock A and Lock B are entangled in {target_name} with relative π phase. 0.0% forbidden readouts across {total_shots} shots."
            if is_success else
            f"Requires Bell state |Φ-⟩ = (|00⟩ - |11⟩)/√2. Apply H(q0), Z(q0), and CNOT(0→1)."
        )

    if is_success:
        bonus = 50 if moves_used <= 2 else 20
        earned_score = 250 + bonus
    else:
        earned_score = 0
        if exceeded_moves:
            status_title = "Alarm Triggered — Move Limit Exceeded"
            explanation = f"Circuit complexity exceeded threshold ({moves_used}/{MAX_MOVES[3]} operations)."

    return {
        "success": is_success,
        "pct_00": pct_00,
        "pct_11": pct_11,
        "pct_01": pct_01,
        "pct_10": pct_10,
        "pct_mismatch": pct_mismatch,
        "counts": counts,
        "score_earned": earned_score,
        "moves_used": moves_used,
        "max_moves": MAX_MOVES[3],
        "status_title": status_title,
        "explanation": explanation,
        "message": f"{status_title}: {explanation}"
    }
