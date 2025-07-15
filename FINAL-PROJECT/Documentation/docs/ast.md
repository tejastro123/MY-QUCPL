
## AST Examples 

The **Abstract Syntax Tree (AST)** is the structured representation generated after parsing a `.qucpl` file. This tree retains the syntactic structure of the source code and serves as the input to the QuCPL compiler.

Below are AST examples for three common quantum programs:

### `bell_ast.json`

```json
{
  "type": "Program",
  "body": [
    {"type": "QubitDeclaration", "qubits": ["q0", "q1"]},
    {"type": "GateOperation", "gate": "H", "args": ["q0"]},
    {"type": "GateOperation", "gate": "CX", "args": ["q0", "q1"]},
    {"type": "Measurement", "qubit": "q0", "target": "c0"},
    {"type": "Measurement", "qubit": "q1", "target": "c1"}
  ]
}
```

### `ghz_ast.json`

```json
{
  "type": "Program",
  "body": [
    {"type": "QubitDeclaration", "qubits": ["q0", "q1", "q2"]},
    {"type": "GateOperation", "gate": "H", "args": ["q0"]},
    {"type": "GateOperation", "gate": "CX", "args": ["q0", "q1"]},
    {"type": "GateOperation", "gate": "CX", "args": ["q0", "q2"]},
    {"type": "Measurement", "qubit": "q0", "target": "c0"},
    {"type": "Measurement", "qubit": "q1", "target": "c1"},
    {"type": "Measurement", "qubit": "q2", "target": "c2"}
  ]
}
```

### `teleportation_ast.json`

```json
{
  "type": "Program",
  "body": [
    {"type": "QubitDeclaration", "qubits": ["q0", "q1", "q2"]},
    {"type": "GateOperation", "gate": "H", "args": ["q1"]},
    {"type": "GateOperation", "gate": "CX", "args": ["q1", "q2"]},
    {"type": "GateOperation", "gate": "CX", "args": ["q0", "q1"]},
    {"type": "GateOperation", "gate": "H", "args": ["q0"]},
    {"type": "Measurement", "qubit": "q0", "target": "c0"},
    {"type": "Measurement", "qubit": "q1", "target": "c1"}
  ]
}
```

Each AST object contains:

* `QubitDeclaration`: Declares one or more quantum registers
* `GateOperation`: Describes a single- or multi-qubit gate
* `Measurement`: Maps quantum measurements to classical bits

These JSON structures are saved to `ast.json` by the parser and passed to the compiler for IR generation.
