
bell.qucpl :
```
qubit q0, q1;
H q0;
CX q0, q1;
measure q0 -> c0;
measure q1 -> c1;
```

ghz.qucpl:
```
qubit q0, q1, q2;
H q0;
CX q0, q1;
CX q0, q2;
measure q0 -> c0;
measure q1 -> c1;
measure q2 -> c2;
```

teleportation.qucpl:
```
qubit q0, q1, q2;
qop h q1;
qop cx q1, q2;
qop cx q0, q1;
qop h q0;
measure q0, q1 -> c0, c1;
if (c1 == 1) {
  qop x q2;
}
if (c0 == 1) {
  qop z q2;
}
print q2;
```