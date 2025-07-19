import tkinter as tk
from tkinter import ttk, messagebox
import json

from parser import parse_code
from compiler import compile_ast_to_ir
from simulation import simulate_ir
from visualization import generate_plots

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

app = tk.Tk()
app.title("Decimal to Quantum Converter")
app.geometry("1200x900")

# -------------------- UI Layout -----------------------
frame = ttk.Frame(app, padding=10)
frame.pack(side="top", fill="x")

ttk.Label(frame, text="Enter Decimal Number:").pack(side="left")
entry = ttk.Entry(frame, width=20)
entry.pack(side="left", padx=5)

binary_str = tk.StringVar()
ttk.Label(frame, textvariable=binary_str, font=("Courier", 12)).pack(side="left", padx=10)

# --------- Output Area for Circuit + Plots ----------
output_frame = ttk.Frame(app)
output_frame.pack(fill="both", expand=True)

# Statevector label
state_output = tk.StringVar()
ttk.Label(output_frame, text="Final Qubit Statevector:", font=("Arial", 11, "bold")).pack()
state_label = ttk.Label(output_frame, textvariable=state_output, font=("Courier", 10), wraplength=1000)
state_label.pack(pady=10)

# Canvas areas for visualizations
plot_frame_circuit = ttk.LabelFrame(output_frame, text="Quantum Circuit")
plot_frame_circuit.pack(side="left", expand=True, fill="both", padx=10, pady=10)
plot_frame_circuit.configure(height=300)

plot_frame_bloch = ttk.LabelFrame(output_frame, text="Bloch Sphere Plot")
plot_frame_bloch.pack(side="right", expand=True, fill="both", padx=10, pady=10)
plot_frame_bloch.configure(height=300)

# AST + IR frame (with scrollbars)
text_frame = ttk.Frame(app)
text_frame.pack(fill="both", expand=True, padx=10, pady=10)

# AST frame
ast_frame = ttk.LabelFrame(text_frame, text="AST")
ast_frame.pack(side="left", expand=True, fill="both", padx=5)

ast_scrollbar = tk.Scrollbar(ast_frame)
ast_scrollbar.pack(side="right", fill="y")

ast_text = tk.Text(ast_frame, wrap="word", height=15, yscrollcommand=ast_scrollbar.set)
ast_text.pack(fill="both", expand=True)
ast_scrollbar.config(command=ast_text.yview)

# IR frame
ir_frame = ttk.LabelFrame(text_frame, text="IR")
ir_frame.pack(side="right", expand=True, fill="both", padx=5)

ir_scrollbar = tk.Scrollbar(ir_frame)
ir_scrollbar.pack(side="right", fill="y")

ir_text = tk.Text(ir_frame, wrap="word", height=15, yscrollcommand=ir_scrollbar.set)
ir_text.pack(fill="both", expand=True)
ir_scrollbar.config(command=ir_text.yview)

# Embed matplotlib figure into Tkinter
def display_plot(fig, container):
    for widget in container.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# Reset all fields
def reset_all():
    entry.delete(0, tk.END)
    binary_str.set("")
    state_output.set("")
    ast_text.delete("1.0", tk.END)
    ir_text.delete("1.0", tk.END)

    for frame in [plot_frame_circuit, plot_frame_bloch]:
        for widget in frame.winfo_children():
            widget.destroy()

# Run button logic
def run_converter():
    try:
        command = f"convert {entry.get()}"
        ast = parse_code(command)
        ir = compile_ast_to_ir(ast)
        qc, state = simulate_ir(ir)

        # Display binary and statevector
        binary_str.set(f"Binary: {ir['binary']}")
        # Format statevector nicely
        formatted = []
        for i, amp in enumerate(state.data):
            binary = format(i, f'0{len(ir["binary"])}b')
            if abs(amp) > 1e-6:  # Show only non-zero entries
                formatted.append(f"|{binary}⟩: {amp}")
        if not formatted:
            formatted.append("All amplitudes are 0.")
        state_output.set("\n".join(formatted))

        # AST and IR JSON
        ast_text.delete("1.0", tk.END)
        ir_text.delete("1.0", tk.END)
        ast_text.insert(tk.END, json.dumps(ast, indent=2))
        ir_text.insert(tk.END, json.dumps(ir, indent=2))

        # Display circuit and bloch
        fig_circuit, fig_bloch = generate_plots(qc, state)
        display_plot(fig_circuit, plot_frame_circuit)
        display_plot(fig_bloch, plot_frame_bloch)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Buttons
ttk.Button(frame, text="Convert to Quantum State", command=run_converter).pack(side="right", padx=10)
ttk.Button(frame, text="Reset", command=reset_all).pack(side="right", padx=5)

app.mainloop()
