
Keywords:
qubit, measure, H, X, Y, Z, CX, CCX, reset

Includes:

List of supported gate operations

Basic QuCPL syntax with examples

Comment style

Clean, simple syntax like:
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