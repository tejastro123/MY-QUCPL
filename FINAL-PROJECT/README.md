
# QUCPL: Quantum Circuit Programming Language

## Overview

**QUCPL** is a domain-specific language (DSL) for defining and analyzing quantum circuits with classical control and state preparation features. This project implements the core syntax, grammar, parser, and Abstract Syntax Tree (AST) generator for QUCPL.

This phase covers:

- **Week 2:** Language syntax design, grammar specification (using Lark), parser implementation, and AST generation.
- **Week 3:** Extensions for multi-qubit gates (`CNOT`, `TOFFOLI`), the `CONVERT` statement, and classical control flow via `IF` statements and `MEASURE` operations.

---

## ✨ Features

- Qubit declarations and quantum gates (`H`, `CNOT`, `TOFFOLI`, etc.)
- Classical control via `IF` conditions and measurement results
- AST generation using a custom Lark-based parser
- Support for multi-qubit gates and state initialization
- `CONVERT` statements for binary encoding into qubit registers

---

## 📘 Week 2: Syntax, Grammar, and Parser

### 🔤 Language Syntax

Example: **Bell State Program**

```qucpl
qubit q0, q1;
H(q0);
CNOT(q0, q1);
MEASURE(q0, q1 -> c0, c1);
PRINT(c0, c1);
````

- `qubit`: Declare one or more qubits
- Gate calls like `H(q0)` and `CNOT(q0, q1)`
- `MEASURE` maps quantum results to classical bits
- `PRINT` outputs classical bit values

---

### 📐 Grammar Specification (PEG/EBNF-style)

```ebnf
start: stmt*
stmt: qubit_decl | qop_stmt | measure_stmt | print_stmt | convert_stmt | if_stmt

qubit_decl: "qubit" id_list ";"
qop_stmt: GATE_NAME "(" id_list ")" ";"
measure_stmt: "MEASURE" "(" id_list "->" id_list ")" ";"
print_stmt: "PRINT" "(" id_list ")" ";"
convert_stmt: "CONVERT" "(" INT ")" ";"
if_stmt: "IF" "(" condition ")" "{" stmt* "}" ("ELSE" "{" stmt* "}")?
condition: CNAME "==" INT
id_list: CNAME ("," CNAME)*
```

---

### 🛠️ Parser Implementation (`parser.py`)

Key Components:

- Uses **Lark** for grammar parsing (`LALR` parser)
- Implements an `ASTBuilder` transformer to walk the parse tree
- Generates structured JSON AST

Main Functions:

```python
def parse_qucpl(source_code):
    tree = parser.parse(source_code)
    return ASTBuilder().transform(tree)
```

---

### 🌳 AST Dump Example: Bell Program

QUCPL Code:

```qucpl
qubit q0, q1;
H(q0);
CNOT(q0, q1);
MEASURE(q0, q1 -> c0, c1);
PRINT(c0, c1);
```

AST Output:

```json
{
  "type": "Program",
  "body": [
    {
      "type": "QubitDecl",
      "qubits": [["q0", "q1"]]
    },
    {
      "type": "QuantumOp",
      "gate": "h",
      "qubits": ["q0"]
    },
    {
      "type": "QuantumOp",
      "gate": "cx",
      "qubits": ["q0", "q1"]
    },
    {
      "type": "Measure",
      "qubits": [["q0", "q1"]],
      "classical": [["c0", "c1"]]
    },
    {
      "type": "Print",
      "args": [["c0", "c1"]]
    }
  ]
}
```

---

## 🚀 Week 3: Multi-Qubit Gates & Classical Control

### 🧩 Multi-Qubit Gates Support

Grammar and parser were extended to support:

- `CNOT(q0, q1)`
- `TOFFOLI(q0, q1, q2)`
- Arbitrary gate names parsed via `GATE_NAME`

Example:

```qucpl
CNOT(q0, q1);
TOFFOLI(q0, q1, q2);
```

---

### 🔁 `CONVERT` Statement

Allows converting an integer into binary and assigning bits to qubits (e.g., initializing states):

```qucpl
CONVERT(5);  // Converts to binary 101 and maps to qubit states
```

AST Node Example:

```json
{ "type": "Convert", "value": 5 }
```

---

### 🧠 Classical Control: IF-ELSE and Measurement

Control quantum flow based on classical bits:

```qucpl
IF (c0 == 1) {
  PRINT(c0);
} ELSE {
  PRINT(c1);
}
```

AST Representation:

```json
{
  "type": "If",
  "condition": { "type": "Condition", "var": "c0", "value": 1 },
  "then": { "type": "Print", "args": [["c0"]] },
  "else": { "type": "Print", "args": [["c1"]] }
}
```

---

### ⚛️ GHZ State Program Example

```qucpl
qubit q0, q1, q2;
H(q0);
CNOT(q0, q1);
CNOT(q1, q2);
MEASURE(q0, q1, q2 -> c0, c1, c2);
IF (c0 == 1) {
  PRINT(c0);
} ELSE {
  PRINT(c1);
}
```

AST Output:

```json
{
  "type": "Program",
  "body": [
    { "type": "QubitDecl", "qubits": [["q0", "q1", "q2"]] },
    { "type": "QuantumOp", "gate": "h", "qubits": ["q0"] },
    { "type": "QuantumOp", "gate": "cx", "qubits": ["q0", "q1"] },
    { "type": "QuantumOp", "gate": "cx", "qubits": ["q1", "q2"] },
    { "type": "Measure", "qubits": [["q0", "q1", "q2"]], "classical": [["c0", "c1", "c2"]] },
    {
      "type": "If",
      "condition": { "type": "Condition", "var": "c0", "value": 1 },
      "then": { "type": "Print", "args": [["c0"]] },
      "else": { "type": "Print", "args": [["c1"]] }
    }
  ]
}
```

---

## 🧪 Usage Instructions

### 📦 Prerequisites

Install [Lark parser](https://github.com/lark-parser/lark):

```bash
pip install lark
```

### ▶️ Run the Parser

```bash
python parser.py
```

When prompted:

```qucpl
qubit q0, q1;
H(q0);
CNOT(q0, q1);
MEASURE(q0, q1 -> c0, c1);
PRINT(c0, c1);
```

### 📤 Output

- JSON AST is saved to `bell_ast.json` or similar
- Console message: `AST saved to bell_ast.json`

---

## 🔭 Future Work

- Semantic analysis and type checking
- Quantum circuit visualization
- Intermediate representation (IR) for simulators
- Backend support for Qiskit or Cirq
- Optimizations and gate simplification
- Integrated development environment (IDE) with syntax highlighting

---

## 📁 Project Structure

```bash
├── parser.py         # Main parser script using Lark
├── grammar.lark      # Formal grammar specification
├── bell.qucpl        # Bell program source
├── ghz.qucpl         # GHZ program source
├── bell_ast.json     # Generated AST for Bell
├── ghz_ast.json      # Generated AST for GHZ
```

---

## 📄 License

MIT License © Tejas Mellimpudi, 2025

---

```text

Let me know if you'd like this as a downloadable file, or want to include badges, a logo, or auto-generation instructions from `.qucpl` files.
```
