### QuCPL Intermediate Representation (IR) – JSON Schema Documentation


# Overview

The **QuCPL JSON IR** is an intermediate representation used to bridge the abstract syntax tree (AST) and execution or simulation (Qiskit/OpenQASM). It encodes quantum programs in a structured and backend-friendly format.


# 🧱 Root Structure

```json
{
  "type": "Program",
  "qubits": [ "q0", "q1", "q2" ],
  "instructions": [ ... ],
  "control_flow": [ ... ]
}
```

| Field          | Type     | Description                                     |
| -------------- | -------- | ----------------------------------------------- |
| `type`         | `string` | Always `"Program"`                              |
| `qubits`       | `array`  | List of declared quantum registers              |
| `instructions` | `array`  | Sequence of gate, measure, print operations     |
| `control_flow` | `array`  | High-level control structures (e.g., if, while) |


## Instructions Block

# 🎯 Gate Operation

```json
{
  "op": "h",
  "args": ["q0"]
}
```

```json
{
  "op": "cx",
  "args": ["q0", "q1"]
}
```

| Field  | Description                              |
| ------ | ---------------------------------------- |
| `op`   | Gate name: `h`, `cx`, `x`, `z`, etc.     |
| `args` | List of target qubit IDs (order matters) |


# Measurement Operation

```json
{
  "op": "measure",
  "qubits": ["q0", "q1"],
  "classical": ["c0", "c1"]
}
```

| Field       | Description                         |
| ----------- | ----------------------------------- |
| `op`        | Always `"measure"`                  |
| `qubits`    | Qubit list to be measured           |
| `classical` | Classical bit list to store results |


# Print Operation

```json
{
  "op": "print",
  "args": ["c0", "c1"]
}
```

| Field  | Description                                   |
| ------ | --------------------------------------------- |
| `op`   | Always `"print"`                              |
| `args` | Variables to print (typically classical bits) |


## Control Flow Block

# If Statement

```json
{
  "type": "if",
  "condition": {
    "type": "Condition",
    "var": "c0",
    "value": 1
  },
  "then": [
    { "op": "print", "args": ["c0"] }
  ],
  "else": [
    { "op": "print", "args": ["c1"] }
  ]
}
```

| Field       | Description                                       |
| ----------- | ------------------------------------------------- |
| `type`      | `"if"`                                            |
| `condition` | See [Condition Structure](#condition-structure)   |
| `then`      | Instruction list if condition is true             |
| `else`      | (Optional) Instruction list if condition is false |

---

# While Statement

```json
{
  "type": "while",
  "condition": {
    "type": "Condition",
    "var": "c1",
    "value": 0
  },
  "body": [
    { "op": "h", "args": ["q0"] }
  ]
}
```

| Field       | Description                                     |
| ----------- | ----------------------------------------------- |
| `type`      | `"while"`                                       |
| `condition` | See [Condition Structure](#condition-structure) |
| `body`      | Instruction list to repeat                      |

---

## Condition Structure

```json
{
  "type": "Condition",
  "var": "c0",
  "value": 1
}
```

| Field   | Description                      |
| ------- | -------------------------------- |
| `type`  | `"Condition"`                    |
| `var`   | Classical bit or variable        |
| `value` | Integer value to compare against |


## Full Example

```json
{
  "type": "Program",
  "qubits": ["q0", "q1"],
  "instructions": [
    { "op": "h", "args": ["q0"] },
    { "op": "cx", "args": ["q0", "q1"] },
    {
      "op": "measure",
      "qubits": ["q0", "q1"],
      "classical": ["c0", "c1"]
    },
    {
      "op": "print",
      "args": ["c0", "c1"]
    }
  ],
  "control_flow": [
    {
      "type": "if",
      "condition": { "type": "Condition", "var": "c0", "value": 1 },
      "then": [ { "op": "print", "args": ["c0"] } ],
      "else": [ { "op": "print", "args": ["c1"] } ]
    }
  ]
}
```


## Notes & Design Considerations

* IR is **backend-agnostic** and easily convertible to Qiskit, OpenQASM, or a custom simulator.
* Fields like `args`, `qubits`, and `classical` are **flattened arrays** (not nested lists).
* **Control flow** is kept separate from gate-level instructions for modular execution.
* JSON structure supports **easy debugging**, **visualization**, and **export**.
