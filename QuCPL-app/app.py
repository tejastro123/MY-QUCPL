import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os, json
from visualize import get_circuit_figure
from simulation import simulate, get_simulation_figure, build_qiskit_circuit
from parser import parse_qucpl
from compiler import ast_to_ir
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_vector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class QuCPLStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("QuCPL Studio - Quantum Compiler GUI")
        self.root.geometry("1200x800")

        self.ast_file = "teleportation_ast.json"
        self.ir_file = "teleportation_ir.json"

        self.create_widgets()

    def create_widgets(self):
        # Code Area
        self.code_area = scrolledtext.ScrolledText(self.root, font=("Consolas", 12), wrap=tk.WORD, height=15)
        self.code_area.pack(fill=tk.BOTH, expand=True)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X)

        for text, cmd in [
            ("Open", self.load_code),
            ("Save", self.save_code),
            ("Parse", self.parse_code),
            ("Compile", self.compile_ir),
            ("Visualize", self.visualize_circuit),
            ("Simulate", self.simulate_circuit),
            ("Bloch Viewer", self.view_bloch),
            ("Export PNG", self.export_diagram),
            ("Reset", self.reset_app)
        ]:
            tk.Button(btn_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=4, pady=4)

        # Plot Viewer (resizable)
        self.plot_frame = tk.Frame(self.root, bg="black", height=300)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)

        # Log
        self.log_area = scrolledtext.ScrolledText(self.root, height=10, bg="black", fg="lime", font=("Courier", 10))
        self.log_area.pack(fill=tk.X)

    def log(self, msg):
        self.log_area.insert(tk.END, f"{msg}\n")
        self.log_area.see(tk.END)

    def load_code(self):
        path = filedialog.askopenfilename(filetypes=[("QuCPL Files", "*.qucpl"), ("All Files", "*.*")])
        if path:
            with open(path) as f:
                self.code_area.delete("1.0", tk.END)
                self.code_area.insert(tk.END, f.read())
            self.log(f"[OPENED] {path}")

    def save_code(self):
        path = filedialog.asksaveasfilename(defaultextension=".qucpl")
        if path:
            with open(path, "w") as f:
                f.write(self.code_area.get("1.0", tk.END).strip())
            self.log(f"[SAVED] {path}")

    def parse_code(self):
        code = self.code_area.get("1.0", tk.END).strip()
        try:
            ast = parse_qucpl(code)
            with open(self.ast_file, "w") as f:
                json.dump(ast, f, indent=2)
            self.log("[✅ PARSED] AST generated")
        except Exception as e:
            self.log(f"[❌ PARSE ERROR] {e}")

    def compile_ir(self):
        try:
            with open(self.ast_file) as f:
                ast = json.load(f)
            ir = ast_to_ir(ast)
            with open(self.ir_file, "w") as f:
                json.dump(ir, f, indent=2)
            self.log("[✅ COMPILED] IR generated")
        except Exception as e:
            self.log(f"[❌ COMPILE ERROR] {e}")

    def show_plot(self, fig):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def visualize_circuit(self):
        try:
            with open(self.ir_file) as f:
                ir = json.load(f)
            fig = get_circuit_figure(ir, "QuCPL Circuit")
            self.show_plot(fig)
            self.log("[👁️ CIRCUIT VISUALIZED]")
        except Exception as e:
            self.log(f"[❌ VISUALIZATION ERROR] {e}")

    def simulate_circuit(self):
        try:
            fig = get_simulation_figure(self.ir_file, "QuCPL Simulation")
            self.show_plot(fig)
            self.log("[⚙️ SIMULATED CIRCUIT]")
        except Exception as e:
            self.log(f"[❌ SIMULATION ERROR] {e}")

    def view_bloch(self):
        try:
            with open(self.ir_file) as f:
                ir = json.load(f)
            qc, _ = build_qiskit_circuit(ir)
            state = Statevector.from_instruction(qc)
            fig = plot_bloch_vector(state.data[:2], title="Bloch Sphere - Qubit 0")
            self.show_plot(fig)
            self.log("[🔵 BLOCH SPHERE SHOWN]")
        except Exception as e:
            self.log(f"[❌ BLOCH ERROR] {e}")

    def export_diagram(self):
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            try:
                with open(self.ir_file) as f:
                    ir = json.load(f)
                fig = get_circuit_figure(ir, "Exported Circuit")
                fig.savefig(path)
                self.log(f"[📤 EXPORTED IMAGE] {path}")
            except Exception as e:
                self.log(f"[❌ EXPORT ERROR] {e}")

    def reset_app(self):
        self.code_area.delete("1.0", tk.END)
        self.log_area.delete("1.0", tk.END)
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        self.log("[🔄 RESET] Cleared code, logs, and visualization")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuCPLStudio(root)
    root.mainloop()
