"""
main.py - Entry Point for Quantum Heist: Break the Entanglement Vault
Author: B.Tech CSE Hackathon Team (Qiskit Fall Fest 2026, Track 1)

Provides both an interactive Terminal CLI playthrough and a quick launcher
for the Streamlit graphical web application.
"""

import sys
import subprocess

# Ensure UTF-8 output encoding on Windows consoles with fallback error handling
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from quantum_circuits import (
    build_level1_circuit,
    evaluate_level1_result,
    build_level2_circuit,
    evaluate_level2_result,
    build_level3_circuit,
    evaluate_level3_result,
    run_circuit_simulation,
    MAX_MOVES,
    LEVEL_HINTS,
    AER_AVAILABLE
)


def print_banner():
    print("=" * 72)
    print("      💎 QUANTUM HEIST: BREAK THE ENTANGLEMENT VAULT (Track 1) 💎")
    print("              Qiskit Fall Fest 2026 -- IIIT Kottayam")
    print("=" * 72)
    print("Welcome, Infiltrator! Infiltrate the high-security quantum vault.")
    print("Construct genuine Qiskit quantum circuits to bypass 3 security layers.")
    backend_name = "Qiskit AerSimulator" if AER_AVAILABLE else "Qiskit StatevectorSampler"
    print(f"[Simulation Engine: {backend_name}]\n")


def play_cli_level1():
    print("\n--- [DOOR 1: SECURITY LASER GRID] ---")
    print(f"Objective: Transform qubit from |0> to target state |1>.")
    print(f"Security Constraint: Max {MAX_MOVES[1]} moves allowed!")
    print("Available gates: X (Bit-flip), Z (Phase-flip), H (Hadamard)")
    print("Options: Enter gate sequence (e.g. 'X') or type 'hint' for intel.")

    user_input = input("Enter gates or 'hint': ").strip()
    if user_input.lower() == "hint":
        print(f"\n{LEVEL_HINTS[1]}")
        user_input = input("Enter gates (e.g. 'X'): ").strip()

    gates = [g.upper() for g in user_input.split() if g.strip()] if user_input else []
    moves_used = len(gates)

    qc = build_level1_circuit(gates)
    print("\nGenerated Qiskit Circuit Diagram:")
    print(qc.draw(output="text"))

    shots = 200
    print(f"\nExecuting circuit on quantum simulator ({shots} shots)...")
    counts = run_circuit_simulation(qc, shots=shots)
    print(f"Measurement Counts: {counts}")

    result = evaluate_level1_result(counts, moves_used=moves_used, total_shots=shots)
    print(f"\n{result['message']}")
    return result["success"], result["score_earned"]


def play_cli_level2():
    print("\n--- [DOOR 2: THE QUANTUM DUAL-SENSOR] ---")
    print("Objective: Create balanced superposition (|0> + |1>)/sqrt(2).")
    print(f"Security Constraint: Max {MAX_MOVES[2]} moves allowed!")
    print("Available gates: H (Hadamard), X (Bit-flip), Z (Phase-flip)")
    print("Options: Enter gate sequence (e.g. 'H') or type 'hint' for intel.")

    user_input = input("Enter gates or 'hint': ").strip()
    if user_input.lower() == "hint":
        print(f"\n{LEVEL_HINTS[2]}")
        user_input = input("Enter gates (e.g. 'H'): ").strip()

    gates = [g.upper() for g in user_input.split() if g.strip()] if user_input else []
    moves_used = len(gates)

    qc = build_level2_circuit(gates)
    print("\nGenerated Qiskit Circuit Diagram:")
    print(qc.draw(output="text"))

    shots = 200
    print(f"\nExecuting circuit on quantum simulator ({shots} shots)...")
    counts = run_circuit_simulation(qc, shots=shots)
    print(f"Measurement Counts: {counts}")

    result = evaluate_level2_result(counts, moves_used=moves_used, total_shots=shots)
    print(f"\n{result['message']}")
    return result["success"], result["score_earned"]


def play_cli_level3():
    print("\n--- [DOOR 3: THE ENTANGLED MASTER VAULT] ---")
    print("Objective: Entangle Lock A (q0) and Lock B (q1) into Bell state (|00> + |11>)/sqrt(2).")
    print(f"Security Constraint: Max {MAX_MOVES[3]} operations allowed! 0% mismatch tolerated.")
    print("Format: comma-separated operations, e.g. 'H 0, CNOT 0 1' or type 'hint'.")

    user_input = input("Enter operations or 'hint': ").strip()
    if user_input.lower() == "hint":
        print(f"\n{LEVEL_HINTS[3]}")
        user_input = input("Enter operations (e.g. 'H 0, CNOT 0 1'): ").strip()

    ops = []
    if user_input:
        raw_ops = [op.strip() for op in user_input.split(",") if op.strip()]
        for item in raw_ops:
            parts = item.split()
            name = parts[0].upper()
            if name in ["H", "X", "Z"] and len(parts) >= 2:
                ops.append((name, int(parts[1])))
            elif name in ["CNOT", "CX"] and len(parts) >= 3:
                ops.append(("CNOT", int(parts[1]), int(parts[2])))

    moves_used = len(ops)
    qc = build_level3_circuit(ops)
    print("\nGenerated Qiskit Circuit Diagram:")
    print(qc.draw(output="text"))

    shots = 200
    print(f"\nExecuting circuit on quantum simulator ({shots} shots)...")
    counts = run_circuit_simulation(qc, shots=shots)
    print(f"Measurement Counts: {counts}")

    result = evaluate_level3_result(counts, moves_used=moves_used, total_shots=shots)
    print(f"\n{result['message']}")
    return result["success"], result["score_earned"]


def run_cli_game():
    print_banner()
    total_score = 0

    # Door 1
    s1, pts1 = play_cli_level1()
    total_score += pts1
    if s1:
        print(f"[+] Door 1 Bypassed! Current Bounty: {total_score} PTS")
    else:
        print("[-] Alarm triggered on Door 1. Retrying may be needed!")

    # Door 2
    s2, pts2 = play_cli_level2()
    total_score += pts2
    if s2:
        print(f"[+] Door 2 Deactivated! Current Bounty: {total_score} PTS")
    else:
        print("[-] Alarm triggered on Door 2.")

    # Door 3
    s3, pts3 = play_cli_level3()
    total_score += pts3
    if s3:
        print(f"[+] Master Vault Cracked! Final Bounty: {total_score} PTS")
        if s1 and s2 and s3:
            print("\n" + "=" * 72)
            print("  🎉🎉🎉 HEIST ACCOMPLISHED: THE QUANTUM VAULT IS BROKEN! 🎉🎉🎉")
            print(f"  Master Quantum Infiltrator Score: {total_score} PTS")
            print("=" * 72)
    else:
        print("[-] Desynchronization breach triggered lock down!")


def launch_streamlit():
    print("\n[*] Launching Streamlit Quantum Web App...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/app.py"])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_cli_game()
    elif len(sys.argv) > 1 and sys.argv[1] == "--web":
        launch_streamlit()
    else:
        print_banner()
        print("Select Mode:")
        print("1. Play interactive CLI game in Terminal")
        print("2. Launch Streamlit Quantum Web Application (Recommended)")
        choice = input("Enter choice (1 or 2, default is 2): ").strip()
        if choice == "1":
            run_cli_game()
        else:
            launch_streamlit()
