# QuCPL Documentation

Welcome to the **QuCPL** Documentation — the official guide for using, understanding, and contributing to the Quantum Computing Programming Language.

QuCPL is a domain-specific language (DSL) built on Python, designed for educational and research purposes. It combines custom syntax, a parser/compiler system, quantum circuit simulation, and a GUI application for an intuitive and visual approach to quantum programming.

---

## 🔭 What is Quantum Computing?

Quantum computing is a transformative field of computing that leverages the principles of quantum mechanics to perform operations on data. Unlike classical computers, which use binary bits (`0` or `1`), quantum computers use **qubits** that can exist in superpositions of states, allowing them to process vast combinations of possibilities simultaneously.

Quantum computers can solve certain problems exponentially faster than classical ones — such as factoring large numbers (Shor’s algorithm), searching unsorted databases (Grover’s algorithm), and simulating quantum systems in physics, chemistry, and cryptography.

---

## 🧠 What is a Qubit?

A **qubit** (quantum bit) is the fundamental unit of quantum information. It can be in the state `|0⟩`, `|1⟩`, or any complex linear combination:

```
|ψ⟩ = α|0⟩ + β|1⟩
```

Where:

* `α` and `β` are complex probability amplitudes
* `|α|² + |β|² = 1`
* The state collapses to either `|0⟩` or `|1⟩` upon measurement

Qubits can also be **entangled**, meaning their states are correlated no matter the physical distance between them — a crucial property for quantum teleportation and quantum communication.

---

## 💻 Introducing QuCPL

**QuCPL** (Quantum Computing Programming Language) is an educational-friendly quantum language designed to simplify quantum programming. It features:

* A readable syntax inspired by C/Python
* A custom compiler that outputs an intermediate JSON representation
* A simulator built on Qiskit
* A GUI studio with tabs for writing, simulating, and visualizing circuits

QuCPL abstracts the complexity of backend circuit manipulation and allows users to focus on **algorithmic thinking and quantum logic**.

---

## 📦 What You'll Find in This Documentation

This site is structured to help you get started with QuCPL and dive deep into its components:

* 📘 **Language Reference**: Syntax, gates, measurement rules
* ✍️ **Writing QuCPL Programs**: Sample code and real examples
* 📐 **Grammar & Parser**: The PEG grammar used and parsing pipeline
* 🛠️ **Compiler**: AST to IR translation and IR schema
* 📊 **Visualization & Simulation**: How results are generated and displayed
* 🖥️ **GUI Application**: Interface features and usage
* 💾 **Outputs Explained**: All exportable files and formats
* 💡 **Developer Notes**: Internal architecture and contribution tips

Use the navigation bar to explore each section in depth. Whether you're a student, educator, or enthusiast, **QuCPL** is your gateway to practical quantum programming.

---

Happy coding, and welcome to the quantum era! ✨

run mkdocs: mkdocs serve