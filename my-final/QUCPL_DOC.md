# 🧠 QuCPL — Quantum Computing Programming Language

QuCPL is a Python-based quantum programming language designed to make learning and exploring quantum computing intuitive and visual. It features a custom syntax, parser, compiler to IR, full simulator, and a visual GUI for programming and debugging.

---

## ❓ What is QuCPL?

QuCPL stands for **Quantum Computing Programming Language**, a high-level educational language designed to simplify the process of writing, visualizing, and simulating quantum programs.

It provides:
- A **custom domain-specific syntax**
- Compiler from source to **JSON-based intermediate representation (IR)**
- Integrated **quantum simulator** based on Qiskit
- **Tkinter-based GUI** with plotting, exporting, and live debugging features

---

## 🚀 Key Features

- 📜 **Custom QuCPL Syntax**  
  Write intuitive code like:
  ```qucpl
  qubit q0, q1;
  H q0;
  CX q0, q1;
  measure q0 -> c0;
  measure q1 -> c1;
  ```

- 🔤 **Grammar and Parser**  
  PEG-based syntax parsing using **Lark**

- ⚙️ **Compiler to JSON IR**  
  AST → IR conversion for structured simulation

- 🧮 **Quantum Simulator**  
  Based on Qiskit's AerSimulator with histogram, statevector, Bloch support

- 🎛️ **Graphical User Interface (GUI)**  
  Complete GUI for writing, simulating, visualizing, and exporting programs

- 🖼️ **Visualizations**  
  - Quantum circuit diagrams
  - Bloch spheres
  - Simulation results
  - Exportable .png and .json files

---

## 🧰 Installation

1. Clone the repository:
```bash
git clone https://github.com/tejastro123/qucpl.git
cd qucpl
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate        # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the GUI:
```bash
python final_app.py
```

---

## 📂 Example Programs

- `examples/bell.qucpl` — Bell state
- `examples/ghz.qucpl` — GHZ circuit
- `examples/teleport.qucpl` — Quantum teleportation

You can load these files via the GUI and press **Run** to simulate and visualize them.

---

## 🖼️ Demo Screenshots

_(Add your screenshots in the `assets/` folder and update the links below)_

| Circuit Diagram | Simulation Results | Bloch Spheres |
|------------------|--------------------|----------------|
| ![](assets/circuit.png) | ![](assets/histogram.png) | ![](assets/bloch.png) |

---

## 🤝 Contributor Guidelines

We welcome contributions from the community!

- Fork the repo and clone it
- Make your changes on a feature branch
- Write clear commit messages and add documentation
- Submit a pull request with a description of your changes

### 📌 Suggestions for Contribution:
- Add more built-in QuCPL examples
- Improve parser/IR engine
- Add OpenQASM import/export support
- Enhance the GUI with more interactive tools
- Extend documentation and tutorial site

---

## 📝 License

MIT License © 2025 Tejas Mellimpudi
This is an academic project under BITS Pilani.

---

## 📧 Contact

📩 tejas.mellimpudi@alumni.bits-pilani.ac.in  
🌐 [GitHub: @tejastro123](https://github.com/tejastro123)
