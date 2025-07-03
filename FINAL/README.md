# 🧠 QuCPL Studio — Quantum Programming IDE & Compiler

QuCPL (Quantum Computing Programming Language) is a beginner-friendly, Python-based quantum programming language with a custom syntax, a compiler to intermediate representation (IR), a circuit simulator, and a full-featured GUI IDE. QuCPL Studio enables intuitive learning and exploration of quantum computing concepts — including Bell states, GHZ states, teleportation, Bloch spheres, and more — with built-in visualizations and debugging support.

---

## 🌟 Features

- 🧾 **Custom QuCPL Syntax** — Simple syntax for quantum algorithms (Bell, GHZ, Teleportation)
- ⚙️ **Compiler & Intermediate Representation** — Converts to structured JSON IR for simulation and visualization
- 🧠 **Quantum Simulator** — Simulates state vectors, measurements, and circuits
- 🎛️ **GUI Studio App** — Write, simulate, and visualize programs interactively
- 📈 **In-GUI Plots** — Circuit diagrams, simulation histograms, Bloch spheres
- 📤 **Exportable Results** — Save circuit images, simulation results, IR/AST files
- 💡 **Tutorials & Examples** — Built-in code snippets for rapid learning
- 🔍 **Syntax Highlighting & Autocomplete** (in progress)

---

## 🧠 Required Knowledge

To effectively use QuCPL, you should have:
- Basic understanding of **quantum computing concepts**: qubits, gates, measurement, entanglement
- Familiarity with **Python**
- No prior knowledge of Qiskit/OpenQASM required (but helpful)

---

## 🧠 Quantum Computing Concepts (Quick Primer)

QuCPL is designed for learners and developers interested in exploring quantum computing. Here's a short primer on the foundational concepts you should understand:

### 🔹 Qubit (Quantum Bit)

A **qubit** is the basic unit of quantum information. Unlike a classical bit (which can be either 0 or 1), a qubit can be in a **superposition** of both 0 and 1 at the same time.

Mathematically, a qubit state is written as:

```
|ψ⟩ = α|0⟩ + β|1⟩
```

Where:
- `|0⟩` and `|1⟩` are basis states
- `α` and `β` are complex numbers (probability amplitudes)
- |α|² + |β|² = 1 (normalization)

### 🔹 Superposition

**Superposition** allows a qubit to be in multiple states simultaneously. For example, applying a **Hadamard (H)** gate to `|0⟩` puts it into:

```
|ψ⟩ = (|0⟩ + |1⟩)/√2
```

This means a 50% chance of measuring 0 or 1.

### 🔹 Entanglement

**Entanglement** is a uniquely quantum phenomenon where qubits become correlated in such a way that the state of one depends on the state of another — even across large distances.

For example, the **Bell state**:

```
|Φ+⟩ = (|00⟩ + |11⟩)/√2
```

This state means if one qubit is measured as 0, the other is also 0 — and vice versa.

### 🔹 Measurement

**Measuring** a qubit collapses its state into either `|0⟩` or `|1⟩`, based on its amplitudes. Probabilities are calculated as:

```
P(0) = |α|²
P(1) = |β|²
```

After measurement, the qubit no longer holds its previous superposition.

### 🔹 Common Quantum Gates

| Gate | Symbol | Description |
|------|--------|-------------|
| X    | NOT    | Flips `|0⟩` ↔ `|1⟩` |
| H    | Hadamard | Creates superposition |
| Z    | Pauli-Z  | Phase flip |
| CX   | CNOT     | Entangles two qubits |
| MEASURE | ⟶ c | Measures qubit into classical bit |

### 🔹 Circuit Model

Quantum algorithms are implemented using **quantum circuits**, where qubits pass through gates (like wires through logic gates in classical computing). The circuit specifies the sequence of operations applied to qubits.

---

## 🔧 What is Qiskit?

**Qiskit** is an open-source quantum computing framework developed by IBM. It provides tools to design quantum circuits, simulate quantum algorithms, and interface with real quantum devices.

### 🧱 Qiskit Components

- `qiskit.terra`: Circuit construction
- `qiskit.visualization`: Plotting and diagramming
- `qiskit.aer`: Simulators
- `qiskit.ibm_provider`: IBM Quantum integration

### 🧮 How QuCPL Uses Qiskit

- Parses QuCPL code to IR
- Converts IR to Qiskit circuits
- Uses `AerSimulator` for accurate simulations
- Plots circuits, statevectors, histograms, Bloch spheres

### 📘 Example: Bell State

```python
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
qc.draw('mpl')
```

Equivalent QuCPL:

```qucpl
qubit q0, q1;
H q0;
CX q0, q1;
measure q0 -> c0;
measure q1 -> c1;
```

---

🔗 Learn More About Qiskit : [text](https://quantum.cloud.ibm.com/docs/en/guides)
🌐 Official Qiskit Website : [text](https://www.ibm.com/quantum/qiskit)

📘 Qiskit Textbook : [text](https://github.com/Qiskit/textbook/tree/main/notebooks/ch-demos#)

📦 Install via pip:

pip install qiskit
Qiskit provides the reliable quantum simulation layer for QuCPL and is a great next step if you wish to deepen your understanding or transition to real quantum hardware.

With QuCPL, you can create and run circuits using simple syntax and see the effects of these principles through simulation and visualization.

---

## 🧰 Installation & Requirements

QuCPL is a Python-based project that runs on most systems with Python 3.7 or later.

### ✅ Prerequisites

Ensure the following are installed:
- Python 3.7+
- `pip` (Python package installer)
- Git (for cloning the repository)
- Optional: `venv` or `conda` for virtual environments

### 🔗 Clone the Repository

```bash
git clone https://github.com/tejastro123/qucpl.git
cd qucpl
```

### 📦 Install Dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate       # On macOS/Linux
venv\Scripts\activate        # On Windows
```

Install required packages:

```bash
pip install -r requirements.txt
```

Main dependencies:
- `qiskit`
- `matplotlib`
- `numpy`
- `Pillow`
- `tkinter` (comes with Python)
- `lark` (for parsing)
- `Pygments` (for syntax highlighting)

---

## 🚀 How to Run

### 🖥️ Launch QuCPL Studio GUI

```bash
python final_app.py
```

### 📁 Project Structure

```
qucpl/
│
├── parser.py           # Parses QuCPL syntax to AST
├── compiler.py         # Converts AST to JSON IR
├── simulation.py       # Runs quantum simulations from IR
├── visualize.py        # Circuit & Bloch visualization
├── final_app.py        # Full GUI application
├── examples/           # Sample .qucpl programs
├── docs/               # Documentation site content (MkDocs)
├── assets/             # Icons and static images
├── qucpl_logo.png
└── requirements.txt
```

---

## 💻 Usage Guide (GUI App)

### 📝 Writing Code
- Write your QuCPL program in the code editor (e.g., Bell state):
  ```qucpl
  qubit q0, q1;
  H q0;
  CX q0, q1;
  measure q0 -> c0;
  measure q1 -> c1;
  ```
- Press `Run` to:
  - Parse & compile the code
  - Simulate the circuit
  - View circuit diagram, statevector, measurement results, Bloch spheres

### 🧪 Simulation Output
- Circuit Diagram: Visualize gates and operations
- Statevector: Final quantum state of all qubits
- Measurement Histogram: Probability distribution of results
- Bloch Spheres: Single and multi-qubit visualizations

### 📤 Export Options
- Export circuit as `.png`
- Save IR/AST as `.json`
- Save plots and simulation results

### 📂 Load / Save Files
- Open `.qucpl` program files
- Save current program to disk

---

## 🎥 Demo Instructions

You can follow along with our [Loom Tutorial Videos](#) (add link) or:

1. Launch `final_app.py`
2. Try loading a program from the `examples/` folder
3. Press `Run`
4. Explore:
   - IR and AST outputs
   - Circuit diagram
   - Simulation results
   - Export/save features

---

## 📚 Learn More

- 📘 QuCPL Language Reference: `docs/language.md`
- 🧪 Sample Programs: `examples/`
- 🌐 Documentation Site: [Coming Soon]
- 🎓 Quantum Primer: `docs/quantum_basics.md`

---

## 🧑‍💻 Contributing

Want to contribute?
- Report bugs via GitHub Issues
- Submit pull requests for enhancements
- Suggest new features (e.g., OpenQASM support, Language Server)

---

## 📝 License

MIT License © 2025 Tejas Mellimpudi  
This is an academic project under BITS Pilani.

---

## 📧 Contact

Have feedback, questions, or ideas?  
📩 Email: tejas.mellimpudi@alumni.bits-pilani.ac.in  
🌐 GitHub: [@tejastro123](https://github.com/tejastro123)
