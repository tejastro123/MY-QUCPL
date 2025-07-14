import json
import matplotlib.pyplot as plt
from qiskit import transpile, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector
def simulate_convert(value: int):
    print(f"\n--- Convert Command ---")
    binary_str = bin(value)[2:]
    num_bits = len(binary_str)
    print(f"Decimal {value} → Binary {binary_str}")
    qr = QuantumRegister(num_bits, 'q')
    cr = ClassicalRegister(num_bits, 'c')
    cqc = QuantumCircuit(qr, cr)
    for i, bit in enumerate(reversed(binary_str)):
        if bit == '1':
            cqc.x(qr[i])
            print(f"Initializing q[{i}] to |1⟩")
        else:
            print(f"Initializing q[{i}] to |0⟩")
    sv = Statevector.from_instruction(cqc)
    print("\n[STATEVECTOR]")
    print(sv)
    try:
        plot_bloch_multivector(sv)
        plt.title("Bloch Spheres of Converted State")
        plt.show()
    except Exception as e:
        print(f"[BLOCH ERROR] {e}")
    return
def build_qiskit_circuit(ir):
    qubits = ir.get("qubits", [])
    instructions = ir.get("instructions", [])
    if instructions and instructions[0].get("op") == "convert":
        simulate_convert(instructions[0]["value"])
        return None, []
    classical_bits = set()
    for instr in instructions:
        if instr.get("op") == "measure":
            classical_bits.update(instr.get("classical", []))
        elif instr.get("type") == "if":
            classical_bits.add(instr["condition"]["var"])
    classical_bits = sorted(classical_bits)
    qmap = {q: i for i, q in enumerate(qubits)}
    cmap = {c: i for i, c in enumerate(classical_bits)}
    qc = QuantumCircuit(len(qubits), len(classical_bits))
    gate_counts = {}
    def apply_instruction(instr):
        if "op" in instr:
            op = instr["op"]
            args = instr.get("args", [])
            try:
                if op in {"h", "x", "y", "z"}:
                    qc.__getattribute__(op)(qmap[args[0]])
                elif op in {"cx", "cy", "cz", "swap"}:
                    qc.__getattribute__(op)(qmap[args[0]], qmap[args[1]])
                elif op == "ccx":
                    qc.ccx(qmap[args[0]], qmap[args[1]], qmap[args[2]])
                elif op == "barrier":
                    qc.barrier(*[qmap[q] for q in args])
                elif op == "measure":
                    for q, c in zip(instr["qubits"], instr["classical"]):
                        qc.measure(qmap[q], cmap[c])
                elif op == "print":
                    print(f"[PRINT] {', '.join(args)}")
                elif op == "convert":
                    simulate_convert(instr["value"])
                gate_counts[op] = gate_counts.get(op, 0) + 1
            except Exception as e:
                print(f"[ERROR] Failed to apply {instr}: {e}")
        elif instr.get("type") == "if":
            cond = instr["condition"]
            var = cond["var"]
            val = cond["value"]
            c_idx = cmap[var]
            for sub in instr.get("then", []):
                op = sub.get("op")
                args = sub.get("args", [])
                try:
                    if op == "x":
                        with qc.if_test((c_idx, val)):
                            qc.x(qmap[args[0]])
                    elif op == "z":
                        with qc.if_test((c_idx, val)):
                            qc.z(qmap[args[0]])
                    else:
                        print(f"[WARNING] Unsupported conditional gate '{op}'")
                    gate_counts[op] = gate_counts.get(op, 0) + 1
                except Exception as e:
                    print(f"[ERROR in conditional]: {e}")
    for instr in instructions:
        apply_instruction(instr)
    print("\n[GATE COUNTS]")
    for g, count in gate_counts.items():
        print(f"{g}: {count}")
    return qc, classical_bits
def simulate(ir, title):
    result = build_qiskit_circuit(ir)
    if result is None or result[0] is None:
        print("[INFO] No circuit to simulate (likely 'convert' instruction handled).")
        return
    qc, classical_bits = result
    sim = Aer.get_backend('aer_simulator')
    try:
        job = sim.run(transpile(qc, sim), shots=1024)
        result = job.result()
        counts = result.get_counts()
        print(f"\n--- {title} Simulation Results ---")
        print("Counts:", counts)
        print("Backend:", sim.name)
        print("Total time taken:", result.time_taken, "seconds")
        plot_histogram(counts, title=title)
        plt.show()
    except Exception as e:
        print(f"[SIMULATION ERROR] {e}")
        
if __name__ == "__main__":
    try:
        with open("tele_ir.json") as f:
            ir = json.load(f)
        simulate(ir, "Quantum Teleportation")
    except FileNotFoundError:
        print("[FILE ERROR] IR file 'ir.json' not found.")
