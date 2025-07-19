import json
import numpy as np
import matplotlib.pyplot as plt
from qutip import Bloch, Qobj, ket2dm, ptrace
import os

# Define gates
GATES = {
    "h": (1, (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])),
    "x": (1, np.array([[0, 1], [1, 0]])),
    "cx": (2, np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1], 
        [0, 0, 1, 0]
    ])),
}

def apply_gate(state, gate, targets, total_qubits):
    targets = list(targets)
    if len(targets) == 1:
        full_op = 1
        for i in range(total_qubits):
            full_op = np.kron(full_op, gate if i == targets[0] else np.eye(2))
        return full_op @ state
    elif len(targets) == 2:
        q1, q2 = targets
        if q1 == q2:
            raise ValueError("Control and target qubits must differ")
        remaining = [i for i in range(total_qubits) if i != q1 and i != q2]
        perm = remaining + [q1, q2]
        inv_perm = np.argsort(perm)
        state_tensor = state.reshape([2] * total_qubits)
        state_tensor = np.transpose(state_tensor, perm)
        reshaped = state_tensor.reshape(-1, 4)
        new_tensor = reshaped @ gate.T
        new_tensor = new_tensor.reshape([2] * total_qubits)
        new_tensor = np.transpose(new_tensor, inv_perm)
        return new_tensor.reshape(2 ** total_qubits)
    else:
        raise ValueError("Only 1- or 2-qubit gates are supported.")

def apply_measure(state, qubits, cregs_out, total_qubits):
    probs = np.abs(state) ** 2
    collapsed_index = np.random.choice(len(state), p=probs)
    bin_str = format(collapsed_index, f'0{total_qubits}b')
    outcome = [int(bin_str[total_qubits - 1 - q]) for q in qubits]
    new_state = np.zeros_like(state)
    new_state[collapsed_index] = 1.0
    return new_state, outcome, collapsed_index

def plot_histogram(state, num_qubits):
    probs = np.abs(state) ** 2
    labels = [format(i, f'0{num_qubits}b') for i in range(len(probs))]
    plt.figure(figsize=(8, 4))
    plt.bar(labels, probs, color='skyblue')
    plt.ylabel("Probability")
    plt.xlabel("Basis State")
    plt.title("Final State Histogram")
    plt.tight_layout()
    plt.savefig("final_histogram.png")
    plt.show()

def visualize_bloch_spheres(state, num_qubits, save_dir="bloch_spheres"):
    """Visualize and save Bloch spheres for individual qubits."""
    print("\n🧭 Generating Bloch spheres...")

    os.makedirs(save_dir, exist_ok=True)

    dim = 2 ** num_qubits
    state_qobj = Qobj(state.reshape((dim, 1)), dims=[[2]*num_qubits, [1]*num_qubits])
    rho = ket2dm(state_qobj)

    for i in range(num_qubits):
        bloch = Bloch()
        qubit_rho = ptrace(rho, i)
        bloch.add_states(qubit_rho)
        bloch.title = f"Bloch Sphere for Qubit {i}"
        bloch.render()  # prepare the figure
        filepath = os.path.join(save_dir, f"bloch_qubit_{i}.png")
        bloch.fig.savefig(filepath, dpi=300)
        print(f"✅ Saved: {filepath}")

def simulate(ir_path="ir.json"):
    with open(ir_path) as f:
        ir = json.load(f)

    num_qubits = ir["qubits"]
    num_cregs = ir["cregs"]
    ops = ir["oper"]

    state = np.zeros(2 ** num_qubits, dtype=complex)
    state[0] = 1.0
    cregs = [0 for _ in range(num_cregs)]

    def resolve_creg(arg):
        return int(arg[1:]) if isinstance(arg, str) and arg.startswith("c") else int(arg)

    def execute_block(block):
        nonlocal state, cregs
        for op in block:
            if "op" in op and op["op"] == "convert":
                print(f"[i] Skipping convert operation with value {op['value']}")
                continue

            gate = op.get("gate")

            if gate in GATES:
                _, mat = GATES[gate]
                state = apply_gate(state, mat, op["qubits"], num_qubits)

            elif gate == "measure":
                state, measured_vals, _ = apply_measure(state, op["qubits"], op["cregs"], num_qubits)
                for q, c, val in zip(op["qubits"], op["cregs"], measured_vals):
                    cregs[c] = val
                    print(f"[m] Measured q{q} → c{c} = {val}")

            elif gate == "barrier":
                print(f"[b] Barrier on qubits: {op['qubits']}")

            elif gate == "print":
                out = [cregs[resolve_creg(arg)] for arg in op["args"]]
                print(f"[p] Print → {out}")

            elif gate == "if":
                cond = cregs[op["creg"]] == op["val"]
                print(f"[if] Condition c{op['creg']} == {op['val']} → {'✅' if cond else '❌'}")
                if cond:
                    execute_block(op["body"])
                elif "else" in op:
                    execute_block(op["else"])
            else:
                raise ValueError(f"Unknown operation: {op}")

    print("🚀 Starting QuCPL Simulation...\n")
    execute_block(ops)

    print("\n✅ Simulation finished.")
    print("🧠 Final classical registers:")
    for i, val in enumerate(cregs):
        print(f"  c{i} = {val}")

    print("\n🔬 Non-zero quantum amplitudes:")
    for i, amp in enumerate(state):
        if abs(amp) > 1e-6:
            print(f"  |{format(i, f'0{num_qubits}b')}⟩: {amp.real:.4f} + {amp.imag:.4f}j")

    # 🎯 Visualizations
    plot_histogram(state, num_qubits)
    visualize_bloch_spheres(state, num_qubits)

if __name__ == "__main__":
    simulate()
