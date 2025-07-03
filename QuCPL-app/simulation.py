import json
from qiskit import transpile, QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

def build_qiskit_circuit(ir):
    qubits = ir["qubits"]
    instructions = ir["instructions"]
    classical_bits = sorted(set(c for instr in instructions if instr["op"] == "measure" for c in instr.get("classical", [])))

    qc = QuantumCircuit(len(qubits), len(classical_bits))
    qmap = {q: i for i, q in enumerate(qubits)}
    cmap = {c: i for i, c in enumerate(classical_bits)}

    for instr in instructions:
        op = instr["op"]
        try:
            if op == "h":
                qc.h(qmap[instr["args"][0]])
            elif op == "x":
                qc.x(qmap[instr["args"][0]])
            elif op == "y":
                qc.y(qmap[instr["args"][0]])
            elif op == "z":
                qc.z(qmap[instr["args"][0]])
            elif op == "cx":
                qc.cx(qmap[instr["args"][0]], qmap[instr["args"][1]])
            elif op == "cz":
                qc.cz(qmap[instr["args"][0]], qmap[instr["args"][1]])
            elif op == "cy":
                qc.cy(qmap[instr["args"][0]], qmap[instr["args"][1]])
            elif op == "ccx":
                qc.ccx(qmap[instr["args"][0]], qmap[instr["args"][1]], qmap[instr["args"][2]])
            elif op == "swap":
                qc.swap(qmap[instr["args"][0]], qmap[instr["args"][1]])
            elif op == "measure":
                for q, c in zip(instr["qubits"], instr["classical"]):
                    qc.measure(qmap[q], cmap[c])
        except KeyError as e:
            print(f"Runtime Error: Unknown bit '{e}' in {instr}")
        except Exception as e:
            print(f"Runtime Error: {e} in {instr}")

    return qc, classical_bits

def simulate(ir_path, title):
    with open(ir_path) as f:
        ir = json.load(f)

    qc, classical_bits = build_qiskit_circuit(ir)
    sim = Aer.get_backend('aer_simulator')
    job = sim.run(transpile(qc, sim), shots=1024)
    result = job.result()
    counts = result.get_counts()

    print(f"\n--- {title} Simulation Results ---")
    print("Counts:", counts)
    print("Backend:", sim.name)
    print("Total time taken:", result.time_taken, "seconds")

    plot_histogram(counts, title=title).show()

def get_simulation_figure(ir_path, title):
    with open(ir_path) as f:
        ir = json.load(f)
    qc, classical_bits = build_qiskit_circuit(ir)
    sim = Aer.get_backend('aer_simulator')
    job = sim.run(transpile(qc, sim), shots=1024)
    result = job.result()
    counts = result.get_counts()

    print(f"\n--- {title} Simulation Results ---")
    print("Counts:", counts)
    print("Backend:", sim.name)
    print("Total time taken:", result.time_taken, "seconds")
    
    return plot_histogram(counts, title=title)

if __name__ == "__main__":
    simulate("teleportation_ir.json", "Teleportation")
