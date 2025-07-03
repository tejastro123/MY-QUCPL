
## IR Examples 

QuCPL's **Intermediate Representation (IR)** is a JSON format designed to bridge the parsed AST and quantum execution. It is backend-agnostic and can be interpreted by Qiskit or other simulators.

### `bell_ir.json`

```json
{
  "type": "Program",
  "qubits": ["q0", "q1"],
  "instructions": [
    {"op": "h", "args": ["q0"]},
    {"op": "cx", "args": ["q0", "q1"]},
    {
      "op": "measure",
      "qubits": ["q0", "q1"],
      "classical": ["c0", "c1"]
    }
  ],
  "control_flow": []
}
```

### `ghz_ir.json`

```json
{
  "type": "Program",
  "qubits": ["q0", "q1", "q2"],
  "instructions": [
    {"op": "h", "args": ["q0"]},
    {"op": "cx", "args": ["q0", "q1"]},
    {"op": "cx", "args": ["q0", "q2"]},
    {
      "op": "measure",
      "qubits": ["q0", "q1", "q2"],
      "classical": ["c0", "c1", "c2"]
    }
  ],
  "control_flow": []
}
```

### `teleportation_ir.json`

```json
{
  "type": "Program",
  "qubits": ["q0", "q1", "q2"],
  "instructions": [
    {"op": "h", "args": ["q1"]},
    {"op": "cx", "args": ["q1", "q2"]},
    {"op": "cx", "args": ["q0", "q1"]},
    {"op": "h", "args": ["q0"]},
    {
      "op": "measure",
      "qubits": ["q0", "q1"],
      "classical": ["c0", "c1"]
    }
  ],
  "control_flow": []
}
```

Each IR JSON includes:

* `type`: Always `"Program"`
* `qubits`: List of named qubit registers
* `instructions`: Gate applications and measurements
* `control_flow`: Optional structures like `if`, `while`

These `.json` files are used by the simulator to build and execute circuits.
