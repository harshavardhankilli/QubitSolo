# Qiskit Fall Fest 2026 — Project Submission Template
**IIIT Kottayam Quantum Hackathon (24-Hour Sprint)**

---

# Quantum Heist: Break the Entanglement Vault

## Project Metadata

* **Project Title:** `Quantum Heist: Break the Entanglement Vault`
* **Team Name:** `QubitSolo`
* **Chosen Track:** `Track 1: Quantum Games & Interactive Puzzles`
* **Video Presentation Link:** `[Insert YouTube Unlisted / Google Drive / Loom URL here]`
  *(⚠️ Crucial: Ensure link access is set to "Anyone with the link can view" on Google Drive or "Unlisted / Public" on YouTube. Locked/inaccessible links cannot be scored!)*
* **Live Demo Timestamp in Video:** `[MM:SS — To be specified upon uploading; mark the exact second where working gameplay begins after the introductory presentation]` *(Total video duration: 09:00)*

### Team Members (Max 4 members)
| Name | Email | GitHub Username |
| :--- | :--- | :--- |
| `K. Harshavardhan` | `harshavardhankilli1122@gmail.com` | `[@harshavardhankilli](https://github.com/harshavardhankilli)` |

---

## 1. Project Overview & Motivation

* **Summary (3–4 sentences):**  
  **Quantum Heist: Break the Entanglement Vault** is a mission-based, strategic quantum puzzle game where players assume the role of an elite quantum infiltrator bypassing three security layers of the high-security Entanglement Vault. Players must construct genuine Qiskit circuits under move-allowance constraints: Door 1 requires inverting ground state $|0\rangle$ to target state $|1\rangle$, Door 2 requires balancing a dual-sensor in equal superposition without triggering self-interference, and Door 3 requires synchronizing dual locks via Bell state entanglement ($H + CNOT$) with 0% mismatch. All puzzle resolutions, scores, and alarms are driven strictly by authentic simulated Qiskit quantum measurements.

* **Why this problem / game?**  
  Quantum phenomena like state transitions, wave superposition, and non-local entanglement are often perceived as abstract mathematics. By framing them as a high-stakes heist with clear objectives, limited moves, actionable physics hints, efficiency scoring, and a celebratory victory screen, *Quantum Heist* transforms quantum mechanics into a tactile, intuitive problem-solving game that reinforces physical understanding.

---

## 2. Quantum Architecture & Mechanics

* **Core Quantum Principles Used:**  
  - **Single-Qubit State Manipulation ($X, Z, H$ gates):** Rotating basis states on the Bloch sphere from $|0\rangle$ to $|1\rangle$.
  - **Superposition & Measurement Collapse ($H$ gate & Born Rule):** Generating balanced state $|\psi\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$ and exploring quantum self-interference ($H \cdot H = I$).
  - **Quantum Entanglement ($CNOT$ & Bell State $|\Phi^+\rangle$):** Creating non-local correlation between Lock A ($q_0$) and Lock B ($q_1$) such that measurement collapses yield 100% agreement with 0% mismatch.

* **How the Quantum Circuit is Integrated:**  
  Player operations dynamically construct a Qiskit `QuantumCircuit`. When the hack attempt is executed, the circuit is simulated for 200 shots using Qiskit Aer (`AerSimulator`) or Qiskit's `StatevectorSampler`. Move counters enforce strict security limits, and the returned measurement count dictionary directly dictates whether the vault door opens or alarms trigger.

* **Circuit Details:**  
  * **Number of Qubits:** 1 qubit for Doors 1 & 2; 2 qubits for Door 3.
  * **Key Gates Used:** $X$ (Pauli-X), $Z$ (Pauli-Z), $H$ (Hadamard), $CNOT$ ($CX$), and Measurement operators.
  * **Primitives Used:** Qiskit Aer Simulator (`AerSimulator`) with automatic fallback to Qiskit 1.x `StatevectorSampler`.
  * **Other Technologies Used:** Python, Streamlit (cyber-heist UI with glassmorphic cards and live charts), Matplotlib.

```python
# Representative snippet: Door 3 Bell State Entanglement in Qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)
# Step 1: Create superposition on Lock A (Qubit 0)
qc.h(0)
# Step 2: Entangle Lock A and Lock B (Qubit 1) via CNOT
qc.cx(0, 1)
# Step 3: Measure both locks simultaneously
qc.measure([0, 1], [0, 1])

simulator = AerSimulator()
counts = simulator.run(qc, shots=200).result().get_counts()
# Yields Bell State |Phi+>: only '00' and '11', with 0% mismatches!
```

---

## 3. Repository Structure & How to Run

### Project Structure
```text
├── README.md               # Hackathon submission documentation (this file)
├── CODE_EXPLANATION.md     # Code explanation, mathematical concepts & judge presentation guide
├── JUDGE_QA.md             # Likely judge questions & winning, concise answers
├── requirements.txt        # Python dependencies (Qiskit, Qiskit-Aer, Streamlit, Matplotlib)
├── src/                    # Source code
│   ├── quantum_circuits.py # Pure Qiskit circuit builders, move limits & evaluation logic
│   ├── app.py              # Streamlit interactive cyber-heist web application
│   ├── leaderboard.py      # Local leaderboard persistence engine
│   └── main.py             # Dual CLI runner & Streamlit app launcher
├── notebooks/              # Jupyter notebooks containing experiments
│   └── solution.ipynb      # Main runnable notebook with pre-executed outputs and plots
└── references/             # Hackathon reference guides (Track 1 & Track 2)
```

### Installation & Execution Instructions

> 💡 **Environment Recommendation:** To avoid package conflicts, use a fresh virtual environment:
> ```bash
> python -m venv venv
> source venv/bin/activate    # On Windows: venv\Scripts\activate
> pip install -r requirements.txt
> ```

1. **Clone the repository:**
   ```bash
   git clone https://github.com/harshavardhankilli/QubitSolo.git
   cd QubitSolo
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the project / demo:**
   ```bash
   # Option A: Launch the Streamlit Web Application (Recommended for Demo Video):
   streamlit run src/app.py

   # Option B: Run via terminal CLI:
   python src/main.py --cli
   python src/main.py --web

   # Option C: Open the pre-executed Jupyter Notebook:
   jupyter notebook notebooks/solution.ipynb
   ```

---

## 4. Implementation Walkthrough & Live Demo

* **Walkthrough of Gameplay / Optimization Pipeline:**  
  1. **Door 1 (Security Laser Grid):** The player starts with Qubit 0 in ground state $|0\rangle$ (max 2 moves). Applying Pauli-$X$ in 1 move flips the qubit to target state $|1\rangle$. Executing 200 shots yields 100% ones, bypassing Door 1 and awarding a speed bonus (+150 PTS).
  2. **Door 2 (Quantum Dual-Sensor):** Requires balanced superposition (max 2 moves). Applying a single $H$ gate splits $|0\rangle$ into $\frac{|0\rangle + |1\rangle}{\sqrt{2}}$, yielding ~50% `0` and ~50% `1`. If the player mistakenly applies two $H$ gates, $H \cdot H = I$ resets the state to $|0\rangle$, triggering the alarm. Bypassing Door 2 awards +200 PTS.
  3. **Door 3 (The Entangled Master Vault):** Locks A ($q_0$) and B ($q_1$) must synchronize with 0% mismatch (max 3 operations). Applying $H(q_0)$ and $CNOT(q_0 \to q_1)$ creates $|\Phi^+\rangle$. Measurement shows zero occurrences of `01` or `10`, cracking the master vault (+300 PTS) and triggering the celebratory **Final Victory Screen**.

* **Key Screenshots / Terminal Output:**  
  ```text
  Door 1 Circuit Diagram:
       ┌───┐┌─┐
    q: ┤ X ├┤M├
       └───┘└╥┘
  c: 1/══════╩═
             0 
  Door 1 Measurement Counts (200 shots): {'1': 200}
  VAULT DOOR 1 BYPASSED! Target state |1> achieved with 100% certainty. Used 1/2 moves (+150 PTS)!

  Door 3 Bell State Circuit Diagram:
       ┌───┐     ┌─┐   
  q_0: ┤ H ├──■──┤M├───
       └───┘┌─┴─┐└╥┘┌─┐
  q_1: ─────┤ X ├─╫─┤M├
            └───┘ ║ └╥┘
  c: 2/═══════════╩══╩═
                  0  1 
  Door 3 Measurement Counts (200 shots): {'00': 101, '11': 99}
  Mismatches ('01' or '10'): 0.0%
  MASTER VAULT CRACKED! Locks A & B are maximally entangled in Bell State |Phi+>! Used 2/3 operations (+300 PTS)!
  ```

---

## 5. Classical vs. Quantum Comparison

* **Educational Context & Model Assumptions:**  
  This comparison serves as an interactive pedagogical model to illustrate quantum correlation, not a demonstration of quantum computational advantage.

* **Comparative Analysis (Uncorrelated Baseline vs. Entangled Locks):**  
  - **Uncorrelated Classical Baseline:** Consider two separate security sensors that independently and uniformly generate binary outcomes ($P(0) = 0.5, P(1) = 0.5$) without a shared key or communication link. Under this specific uncoordinated model:
    $$P(00) = 0.25, \quad P(11) = 0.25, \quad P(01) = 0.25, \quad P(10) = 0.25$$
    The desynchronization rate (mismatched readouts $01$ or $10$) is **50%**.  
    *(Note: Classical systems can easily achieve 100% correlation if connected by a physical wire, a shared deterministic seed, or pre-shared keys. The 50% mismatch rate applies strictly to independent, uncorrelated binary generators.)*
  - **Quantum Entanglement Strategy:** In an ideal noiseless quantum circuit, applying a Hadamard gate to qubit 0 followed by a CNOT gate from qubit 0 to qubit 1 prepares the maximally entangled Bell state:
    $$|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$
    Measuring this state in the computational basis yields correlated outcomes $00$ and $11$ (with ~50% probability each), while the probability of observing mismatched outcomes ($01$ or $10$) is mathematically **0.0%** in an ideal noiseless simulation. In the game's narrative, this perfect correlation allows the dual locks to open without triggering the desynchronization alarm.
  - **Important Clarification:** Entanglement produces non-local correlations that violate Bell inequalities, but entanglement alone does not imply computational speedup. Both the classical baseline and the 2-qubit quantum circuit are fully and trivially simulatable on classical computers.

---

## 6. Performance, Results & Limitations

* **Key Results & Observations:**  
  - **Simulation Latency:** 200 shots simulated on Qiskit Aer execute in ~1.8 ms on local hardware (benchmarked across repeated runs), providing responsive real-time feedback within the Streamlit workbench.
  - **Statistical Agreement:** Measured distributions across 200 shots closely match theoretical probabilities ($|\Phi^+\rangle \to \approx 50\% \text{ '00'}, \approx 50\% \text{ '11'}$) within expected statistical shot noise.
  - **Ideal Correlation:** Ideal simulation of Bell states consistently yields 0.0% forbidden mismatch counts across all verification runs.

* **Critical Reflection on Limitations:**  
  - **Educational Simulation vs. Quantum Advantage:** This project is an educational puzzle game designed for Track 1, demonstrating foundational quantum mechanics. It does not claim or demonstrate quantum computational advantage. Quantum computational advantage is problem-dependent and requires complex circuits, high entanglement scaling, and system sizes that exceed classical simulation capabilities—far beyond a 2-qubit didactic game.
  - **Ideal Simulation vs. Physical NISQ Hardware:** All circuits are executed on ideal local simulators (`AerSimulator` / `StatevectorSampler`). Physical noisy intermediate-scale quantum (NISQ) processors experience environmental decoherence (energy relaxation $T_1$ and dephasing $T_2$), measurement readout errors, and two-qubit gate infidelities ($CX$ error rates typically 0.5%–1.5%). On physical hardware, a small percentage of spurious mismatch counts ($01$ or $10$) would occur even for an entangled Bell pair without quantum error mitigation.

---

## 7. References & Acknowledgments

* **IBM Qiskit Documentation:** [Qiskit Circuit & Primitives Guides](https://docs.quantum.ibm.com/guides)
* **Qiskit Aer Simulator:** [Qiskit Aer Documentation](https://github.com/Qiskit/qiskit-aer)
* **Educational Concepts:** David A. Meyer, *"Quantum Strategies"* (Phys. Rev. Lett., 1999); Allan Goff, *"Quantum Tic-Tac-Toe"* (quant-ph/0202151).
* **AI Assistance Disclosure:** In compliance with official hackathon integrity guidelines, AI coding assistance (Antigravity) was used during the sprint for user interface CSS styling, terminal banner formatting, dynamic puzzle variation structuring, and automated test scripting. All underlying educational concepts, quantum circuit architectures, move constraints, gameplay progression rules, and technical documentation were formulated, reviewed, and finalized by the participant.
