
Keywords:
qubit, measure, H, X, Y, Z, CX, CCX, reset

Syntax Example:
```
qubit q0, q1;
H q0;
CX q0, q1;
measure q0 -> c0;
measure q1 -> c1;
```
Comments:
Use // for single-line comments.

Classical Registers:
Declare as needed: classical c0, c1;