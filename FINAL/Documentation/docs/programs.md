A valid QuCPL program contains:
Qubit declarations,
Gate operations,
Measurement operations,

Example: Bell State
```
qubit q0, q1;
H q0;
CX q0, q1;
measure q0 -> c0;
measure q1 -> c1;
```
Example: GHZ State:
```
qubit q0, q1, q2;
H q0;
CX q0, q1;
CX q0, q2;
measure q0 -> c0;
measure q1 -> c1;
measure q2 -> c2;
```