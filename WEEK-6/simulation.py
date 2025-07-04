import json
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Define single-qubit gates
GATES = {
    "h": 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]], dtype=complex),
    "x": np.array([[0, 1], [1, 0]], dtype=complex),
    "y": np.array([[0, -1j], [1j, 0]], dtype=complex),
    "z": np.array([[1, 0], [0, -1]], dtype=complex),
    "i": np.eye(2, dtype=complex)
}


def kron_n(*ops):
    result = np.array([[1]], dtype=complex)
    for op in ops:
        result = np.kron(result, op)
    return result


def apply_gate(state, gate, qubit, n):
    ops = [GATES["i"]] * n
    ops[qubit] = gate
    U = kron_n(*ops)
    return U @ state


def apply_controlled(state, control, target, n, gate_matrix):
    dim = 2 ** n
    new_state = np.copy(state)
    for i in range(dim):
        if ((i >> (n - 1 - control)) & 1) == 1:
            flipped = i ^ (1 << (n - 1 - target))
            new_state[flipped] += state[i]
            new_state[i] -= state[i]
    return new_state


def apply_cx(state, control, target, n):
    return apply_controlled(state, control, target, n, GATES["x"])


def apply_cz(state, control, target, n):
    return apply_controlled(state, control, target, n, GATES["z"])


def apply_cy(state, control, target, n):
    return apply_controlled(state, control, target, n, GATES["y"])


def apply_ccx(state, c1, c2, target, n):
    dim = 2 ** n
    new_state = np.copy(state)
    for i in range(dim):
        b = format(i, f'0{n}b')
        if b[n - 1 - c1] == '1' and b[n - 1 - c2] == '1':
            flipped = i ^ (1 << (n - 1 - target))
            new_state[flipped] += state[i]
            new_state[i] -= state[i]
    return new_state


def apply_swap(state, q1, q2, n):
    dim = 2 ** n
    new_state = np.zeros_like(state)
    for i in range(dim):
        b = list(format(i, f'0{n}b'))
        b[n - 1 - q1], b[n - 1 - q2] = b[n - 1 - q2], b[n - 1 - q1]
        j = int("".join(b), 2)
        new_state[j] = state[i]
    return new_state


def measure(state, n, measured_qubits):
    dim = 2 ** n
    probs = np.abs(state) ** 2
    outcomes = []
    for _ in range(1024):
        index = np.random.choice(dim, p=probs)
        b = format(index, f'0{n}b')
        outcome = ''.join(b[n - 1 - q] for q in measured_qubits)
        outcomes.append(outcome)
    return Counter(outcomes)


def display_bloch(qubit_state, qubit_name="q", show=True):
    alpha, beta = qubit_state[0], qubit_state[1]
    theta = 2 * np.arccos(np.abs(alpha))
    phi = np.angle(beta) - np.angle(alpha)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)

    fig = plt.figure(figsize=(5, 5))
    ax = fig.add_subplot(111, projection='3d')
    ax.quiver(0, 0, 0, x, y, z, color='red', linewidth=2)

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    X = np.outer(np.cos(u), np.sin(v))
    Y = np.outer(np.sin(u), np.sin(v))
    Z = np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(X, Y, Z, color='lightblue', alpha=0.1)

    ax.set_title(f"Bloch Sphere of {qubit_name}", fontsize=14)
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    if show:
        plt.show()


def show_all_bloch_spheres(state, qubits):
    n = len(qubits)
    for i, q in enumerate(qubits):
        reduced_state = np.zeros((2,), dtype=complex)
        for j in range(2 ** n):
            bin_str = format(j, f'0{n}b')
            if all(bin_str[k] == '0' for k in range(n) if k != i):
                reduced_state[int(bin_str[i])] = state[j]
        norm = np.linalg.norm(reduced_state)
        if norm > 0:
            reduced_state /= norm
            display_bloch(reduced_state, qubit_name=q)

def plot_statevector(state, qubit_labels):
    n = len(qubit_labels)
    dim = 2 ** n
    fig, ax = plt.subplots(figsize=(12, 4))
    real_vals = [state[i].real for i in range(dim)]
    imag_vals = [state[i].imag for i in range(dim)]
    indices = [format(i, f'0{n}b') for i in range(dim)]
    bar1 = ax.bar(np.arange(dim) - 0.15, real_vals, width=0.3, label="Real", color='green')
    bar2 = ax.bar(np.arange(dim) + 0.15, imag_vals, width=0.3, label="Imag", color='orange')
    ax.set_xticks(np.arange(dim))
    ax.set_xticklabels(indices)
    ax.set_ylabel("Amplitude")
    ax.set_title("Final Statevector")
    ax.legend()
    plt.savefig("statevector_plot.png")
    plt.show()

def simulate(ir, save_hist="histogram.png", log_file="runtime_log.txt"):
    logs = []
    state_history = []
    qubit_labels = ir["qubits"]
    n = len(qubit_labels)
    qubit_index = {q: i for i, q in enumerate(qubit_labels)}
    state = np.zeros((2 ** n,), dtype=complex)
    state[0] = 1.0
    logs.append(f"Initialized state |{'0' * n}>")
    state_history.append(state.copy())

    measured_qubits = []

    for instr in ir["instructions"]:
        op = instr["op"]

        if op in GATES:
            for q in instr["args"]:
                idx = qubit_index[q]
                state = apply_gate(state, GATES[op], idx, n)
                logs.append(f"Applied {op.upper()} to {q}")
                state_history.append(state.copy())
        elif op == "cx":
            c, t = instr["args"]
            state = apply_cx(state, qubit_index[c], qubit_index[t], n)
            logs.append(f"Applied CX to {c} → {t}")
            state_history.append(state.copy())
        elif op == "cz":
            c, t = instr["args"]
            state = apply_cz(state, qubit_index[c], qubit_index[t], n)
            logs.append(f"Applied CZ to {c} → {t}")
            state_history.append(state.copy())
        elif op == "cy":
            c, t = instr["args"]
            state = apply_cy(state, qubit_index[c], qubit_index[t], n)
            logs.append(f"Applied CY to {c} → {t}")
            state_history.append(state.copy())
        elif op == "ccx":
            c1, c2, t = instr["args"]
            state = apply_ccx(state, qubit_index[c1], qubit_index[c2], qubit_index[t], n)
            logs.append(f"Applied CCX to {c1}, {c2} → {t}")
            state_history.append(state.copy())
        elif op == "swap":
            q1, q2 = instr["args"]
            state = apply_swap(state, qubit_index[q1], qubit_index[q2], n)
            logs.append(f"Swapped {q1} and {q2}")
            state_history.append(state.copy())
        elif op == "measure":
            measured_qubits = [qubit_index[q] for q in instr["qubits"]]
            logs.append(f"Scheduled measurement on {instr['qubits']}")

    logs.append("Final Statevector:")
    for i, amp in enumerate(state):
        bin_label = format(i, f'0{n}b')
        logs.append(f"|{bin_label}> : {amp.real:.4f} + {amp.imag:.4f}j")

    # Bloch sphere and animation
    show_all_bloch_spheres(state, qubit_labels)
    # Plot the final statevector
    plot_statevector(state, qubit_labels)
    
    if measured_qubits:
        result_counts = measure(state, n, measured_qubits)
        logs.append("Performed 1024-shot measurement.")
    else:
        result_counts = Counter()
        logs.append("No measurement found. Skipping measurement step.")

    if result_counts:
        keys, values = zip(*sorted(result_counts.items()))
        plt.figure(figsize=(10, 4))
        bars = plt.bar(keys, values, color='skyblue')
        for bar, val in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width() / 2, val + 5, str(val),
                     ha='center', va='bottom', fontsize=10)
        plt.xlabel("Measurement Outcome", fontsize=12)
        plt.ylabel("Counts", fontsize=12)
        plt.title("Measurement Histogram (1024 shots)")
        plt.tight_layout()
        plt.savefig(save_hist)
        plt.show()
        logs.append(f"Histogram saved to {save_hist}")

    # Save logs to file
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(logs))
    print(f"✅ Runtime logs saved to {log_file}")

    return result_counts, logs


# Run on bell_ir.json if executed directly
if __name__ == "__main__":
    with open("teleportation_ir.json") as f:
        ir = json.load(f)
    simulate(ir)

