# Glossary

This glossary compiles key terms and concepts encountered and applied throughout the 7-week development of QuCPL, a domain-specific language for quantum computing. It includes definitions from quantum mechanics, language design, compiler theory, and software development, providing context for both the theoretical foundations and the practical tools used.

## Quantum Computing Terms

• Qubit: The fundamental unit of quantum information. Unlike a classical bit, a qubit can exist in a superposition of 0 and 1, enabling parallel computation.

• Superposition: A quantum property that allows qubits to exist in multiple states simultaneously until measured. Practiced using the Hadamard gate in Week 1.

• Entanglement: A phenomenon where two or more qubits become linked, such that measuring one affects the state of the other. Implemented in Bell and GHZ circuits (Weeks 2–3).

• Quantum Gate: A unitary operation that changes the state of one or more qubits. Gates like Hadamard (H), CNOT, and X were used across all quantum programs.

• Hadamard Gate (H): A single-qubit gate that places a qubit into an equal superposition of |0⟩ and |1⟩.

• CNOT Gate: A two-qubit gate that flips the target qubit if the control qubit is |1⟩. Key to creating entanglement.

• Measurement: The act of observing a qubit, collapsing it to a classical state (0 or 1). Used in all simulations and circuit terminations.

• Bell State: A maximally entangled two-qubit state, generated in Week 2 to test QuCPL’s basic gate functionality.

• Quantum Circuit: A structured sequence of quantum gates applied to qubits. Represented textually in QuCPL and visually using IR-based tools (Weeks 4–5).

## Quantum Software and Tools

• Qiskit: IBM’s open-source quantum computing framework used to simulate and execute QuCPL-generated circuits. Integrated in Weeks 1, 2, 5, and 6.

• Aer Simulator: Qiskit’s high-performance simulator backend used to test circuits virtually before running them on real hardware.

• QuEDX: An interactive quantum learning platform used during Weeks 1 and 2 for visualizing gate operations and enhancing conceptual understanding.

## Language Design and Compiler Terms

• Domain-Specific Language (DSL): A programming language tailored for a specific domain. QuCPL was designed as a DSL for quantum circuit expression and simulation.

• Grammar: A formal set of syntax rules defining valid program structure. Written in PEG using the Lark parser during Weeks 2–3.

• Parsing: The process of analyzing and converting source code into a structured format. Implemented using Lark in Week 3.

• Lark Parser: A Python parsing library supporting both LALR and Earley algorithms. Used to build QuCPL’s grammar and AST transformation pipeline.

• Abstract Syntax Tree (AST): A tree-based data structure representing the hierarchical syntax of a program. Generated in JSON during Week 3.

• Intermediate Representation (IR): A backend-neutral JSON format capturing the logic of a quantum program. Designed in Week 4 for simulation and visualization.

• Transformer: A component that walks through the parse tree and outputs a cleaner AST. Used extensively in the parser module of QuCPL.

• JSON (JavaScript Object Notation): A lightweight data format used to serialize ASTs and IRs for backend integration and visualization across Weeks 3–5.

## General Computing and Project Terms

• Simulator: A software tool that emulates a quantum processor, allowing programs to be tested without quantum hardware. Qiskit’s Aer was used throughout the internship.

• Backend: The layer responsible for circuit execution. In Qiskit, it refers to the simulation engine or quantum hardware. The IR-to-Qiskit backend integration was completed in Week 5.

• Comment: Non-executable text in code used for annotations. In QuCPL, comments begin with // and were added to improve readability and documentation.

• Control Flow: Constructs that affect the sequence of execution (e.g., if, loop, while). Basic IF and MEASURE support was implemented in Week 3, with future expansion planned.
