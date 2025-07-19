from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit import transpile
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.visualization import plot_bloch_vector
import numpy as np
from qiskit.quantum_info import state_fidelity

# Step 1: Create a 3-qubit circuit (qubit 0: |ψ⟩, qubit 1: entangled with 2)
qc = QuantumCircuit(3, 2)

# Define custom state |ψ⟩ = 1/√3 |0⟩ + √(2/3) |1⟩ on qubit 0
alpha = 1/np.sqrt(3)
beta = np.sqrt(2/3)
qc.initialize([alpha, beta], 0)
fig = plot_bloch_vector([alpha, beta, 0], title="Initial State on Alice's Qubit")
fig.savefig('initial_state_alice.png')

# Step 2: Create Bell pair between qubits 1 (Alice) and 2 (Bob)
qc.h(1)
qc.cx(1, 2)

# Step 3: Alice performs Bell measurement on qubits 0 and 1
qc.cx(0, 1)
qc.h(0)
qc.measure([0, 1], [0, 1])

# Step 4: Bob applies conditional operations based on Alice’s result
qc.cx(1, 2)     # Apply X if classical bit 1 is 1
qc.cz(0, 2)     # Apply Z if classical bit 0 is 1

# Draw the full circuit
qc.draw('mpl', scale=0.7, filename='teleportation_circuit.png')

# Simulate with the Aer simulator
simulator = Aer.get_backend('aer_simulator')

# Save final state for fidelity calculation
qc.save_statevector()

# Execute the circuit
job = simulator.run(transpile(qc, simulator))
result = job.result()
output_state = result.get_statevector()

fig = plot_bloch_vector(output_state, title="Final State on Bob's Qubit")
fig.savefig('final_state_bob.png')

# Extract Bob's qubit (qubit 2) from the final state
reduced_bob = partial_trace(output_state, [0, 1])

# Display result
print("Teleported state on Bob’s qubit:")
print(reduced_bob)

# Compare fidelity
original_state = Statevector([alpha, beta])
fidelity = state_fidelity(original_state, reduced_bob)
print(f"Fidelity between original and teleported state: {fidelity:.4f}")

