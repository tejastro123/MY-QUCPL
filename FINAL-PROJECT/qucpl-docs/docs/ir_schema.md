
# QuCPL Intermediate Representation (IR) – JSON Schema Documentation

## Overview

The **QuCPL JSON IR** is an intermediate representation used to bridge the abstract syntax tree (AST) and execution or simulation (Qiskit/OpenQASM). It encodes quantum programs in a structured and backend-friendly format.

The IR schema was defined in a modular and backend-agnostic JSON format, described in detail in the documentation file ir_schema_docs.md. The core design principles focused on:

• Readability: JSON format allows easy inspection and debugging.

• Structure: Clearly separated fields for quantum instructions, declared qubits, and control flow.

• Extensibility: Support for future constructs like loops and conditionals.

• IR is backend-agnostic and easily convertible to Qiskit, OpenQASM, or a custom simulator.

• Fields like args, qubits, and classical are flattened arrays (not nested lists).

• Control flow is kept separate from gate-level instructions for modular execution.

• JSON structure supports easy debugging, visualization, and export.

## IR Schema Design

The Intermediate Representation (IR) is a JSON-based format that captures the essential operations of a quantum program in a structured and extensible way. It is designed to be readable, modular, and independent of any specific quantum backend.

The IR consists of the following main fields:

"qubits": An array listing all declared qubits in the program.

"classical": An array listing all declared classical bits.

"instructions": An array of objects, each representing a quantum gate, measurement, or print operation.

"control_flow": An optional field for handling control flow constructs like if statements.

Instruction Types

Each instruction in the "instructions" array is an object tailored to its operation type:

Gate Operations (e.g., Hadamard, CNOT):

"type": "gate"

"name": the gate name (e.g., "h", "cx")

"args": an array of qubit indices or names

Measurements:

"type": "measure"

"qubit": the qubit being measured

"target": the classical bit to store the measurement result

Print Statements:

"type": "print"

"args": an array of variables or literals to print

Control Flow

The "control_flow" field manages conditional logic, such as if statements, by nesting instructions within a block that executes based on a condition.

This design ensures that the IR can represent both simple quantum circuits and more complex programs with classical control flow.

## Root Structure

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

### Gate Operation

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

### Measurement Operation

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

### Print Operation

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

### If Statement

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

### While Statement

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

### Condition Structure

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
