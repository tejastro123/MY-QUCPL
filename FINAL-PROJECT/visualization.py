import json
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Define display names and custom gate colors
GATE_DISPLAY = {
    "h": "H",
    "x": "X",
    "y": "Y",
    "z": "Z",
    "cx": "CX",
    "cz": "CZ",
    "ccx": "CCX",
    "swap": "SWAP",
    "cy": "CY",
    "measure": "M"
}

GATE_COLORS = {
    "h": "#1f77b4",      # Blue
    "x": "#2ca02c",      # Green
    "y": "#ff7f0e",      # Orange
    "z": "#d62728",      # Red
    "cx": "#9467bd",     # Purple
    "cz": "#8c564b",     # Brown
    "ccx": "#17becf",    # Cyan
    "swap": "#e377c2",   # Pink
    "cy": "#7f7f7f",     # Gray
    "measure": "#ffbb78" # Light orange
}

def draw_circuit(ir, save_path=None):
    qubits = ir.get("qubits", [])
    instructions = ir.get("instructions", [])

    num_qubits = len(qubits)
    qubit_idx = {q: i for i, q in enumerate(qubits)}

    fig, ax = plt.subplots(figsize=(max(12, len(instructions) * 1.2), num_qubits * 1.2))

    # Style settings
    font_size = 14
    gate_box_size = 0.6
    gate_col = 1

    # Draw horizontal lines for qubits
    for i, q in enumerate(qubits):
        ax.hlines(i, 0, len(instructions)+1, color='black', linewidth=1.2)
        ax.text(-0.6, i, f"{q}", fontsize=font_size + 2, va='center', ha='right', fontweight='bold')

    # Process each instruction
    for instr in instructions:
        op = instr["op"]
        args = instr.get("args", [])
        classical = instr.get("classical", [])
        qubit_targets = instr.get("qubits", [])

        color = GATE_COLORS.get(op, "#333333")  # Default dark gray if undefined
        label = GATE_DISPLAY.get(op, op.upper())

        if op == "measure":
            for q, c in zip(qubit_targets, classical):
                y = qubit_idx[q]
                ax.add_patch(Rectangle((gate_col - gate_box_size/2, y - gate_box_size/2),
                                       gate_box_size, gate_box_size,
                                       color=color, edgecolor='black', linewidth=1.5, zorder=2))
                ax.text(gate_col, y, label, color='black', ha='center', va='center',
                        fontsize=font_size, fontweight='bold')
                ax.annotate(f"→ {c}", (gate_col + 0.5, y + 0.3),
                            fontsize=font_size - 2, color='purple',
                            arrowprops=dict(arrowstyle='->', lw=1.5, color='gray'))
        elif op == "print":
            ax.text(gate_col, -1.2, f"print({', '.join(args)})", fontsize=font_size, color='gray')
        elif op == "cx" and len(args) == 2:
            ctrl, tgt = args
            y1, y2 = qubit_idx[ctrl], qubit_idx[tgt]
            ax.plot(gate_col, y1, 'ko', markersize=6)
            ax.add_patch(Rectangle((gate_col - gate_box_size/2, y2 - gate_box_size/2),
                                   gate_box_size, gate_box_size,
                                   color=color, edgecolor='black', linewidth=1.5))
            ax.text(gate_col, y2, "X", color='white', ha='center', va='center',
                    fontsize=font_size, fontweight='bold')
            ax.vlines(gate_col, min(y1, y2), max(y1, y2), color='black', linestyle='-')
        elif op == "ccx" and len(args) == 3:
            ctrl1, ctrl2, tgt = args
            y1, y2, y3 = qubit_idx[ctrl1], qubit_idx[ctrl2], qubit_idx[tgt]
            ax.plot(gate_col, y1, 'ko', markersize=6)
            ax.plot(gate_col, y2, 'ko', markersize=6)
            ax.add_patch(Rectangle((gate_col - gate_box_size/2, y3 - gate_box_size/2),
                                   gate_box_size, gate_box_size,
                                   color=color, edgecolor='black', linewidth=1.5))
            ax.text(gate_col, y3, "X", color='white', ha='center', va='center',
                    fontsize=font_size, fontweight='bold')
            ax.vlines(gate_col, min(y1, y3), max(y2, y3), color='black', linestyle='-')
        else:
            for q in args:
                y = qubit_idx[q]
                ax.add_patch(Rectangle((gate_col - gate_box_size/2, y - gate_box_size/2),
                                       gate_box_size, gate_box_size,
                                       color=color, edgecolor='black', linewidth=1.5))
                ax.text(gate_col, y, label, color='white', ha='center', va='center',
                        fontsize=font_size, fontweight='bold')

        gate_col += 1

    # Draw border around circuit
    x0, x1 = -0.8, gate_col
    y0, y1 = -0.8, num_qubits - 0.5 + 1
    ax.add_patch(Rectangle((x0, y0), x1 - x0 + 0.2, y1 - y0, edgecolor='black',
                           facecolor='none', linewidth=2.0, linestyle='--', zorder=1))

    ax.set_ylim(-1.5, num_qubits + 0.5)
    ax.set_xlim(-1, gate_col + 1)
    ax.axis('off')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"✅ Circuit image saved to: {save_path}")

    plt.show()

if __name__ == "__main__":
    with open("bell_ir.json") as f:
        ir = json.load(f)

    draw_circuit(ir, save_path="bell_circuit.png")
