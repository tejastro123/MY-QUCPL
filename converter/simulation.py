from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def simulate_ir(ir):
    num_qubits = len(ir["binary"])
    qc = QuantumCircuit(num_qubits)

    for instr in ir["instructions"]:
        if instr["gate"] == "x":
            qc.x(instr["target"])

    state = Statevector.from_instruction(qc)
    return qc, state
