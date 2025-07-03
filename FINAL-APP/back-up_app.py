import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os, json, re
from parser import parse_qucpl
from compiler import ast_to_ir
from simulation import simulate, build_qiskit_circuit
from visualize import visualize_circuit
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

try:
    from qiskit_aer import AerSimulator
    from qiskit.visualization.timeline import draw as timeline_drawer
    from qiskit import transpile
except ImportError:
    AerSimulator = None
    timeline_drawer = None

QUCPL_KEYWORDS = ["h", "x", "cx", "ccx", "measure", "reset", "barrier", "if", "for", "module", "return", "let"]
QUCPL_SNIPPETS = {
    "if": "if (condition) {\n    // code\n}",
    "for": "for i in 0..N {\n    // code\n}",
    "module": "module name(args) {\n    // body\n}"
}

class QuCPLStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("QuCPL Studio – Quantum IDE")
        self.root.geometry("1300x900")
        self.save_dir = os.getcwd()
        self.ast = None
        self.ir = None
        self.ir_instr_index = 0
        self.code = ""
        self.ast_path = "ast.json"
        self.ir_path = "ir.json"
        self.create_widgets()

    def create_widgets(self):
        self.code_area = scrolledtext.ScrolledText(self.root, font=("Consolas", 12), wrap=tk.WORD, height=14, undo=True)
        self.code_area.pack(fill=tk.BOTH, expand=True)
        self.code_area.bind("<Tab>", self.on_tab_autocomplete)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X)
        for text, cmd in [
            ("Open", self.load_code),
            ("Save", self.save_code),
            ("Set Output Dir", self.set_save_dir),
            ("Parse", self.parse_code),
            ("Compile", self.compile_ir),
            ("Visualize", self.visualize),
            ("Simulate", self.simulate),
            ("Step ▶", self.step_debug),
            ("Statevector", self.show_statevector),
            ("Reset", self.reset_app)
        ]:
            tk.Button(btn_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=4, pady=4)

        self.tabs = ttk.Notebook(self.root)
        self.ast_view = tk.Text(self.tabs)
        self.ir_view = tk.Text(self.tabs)
        self.plot_frame = tk.Frame(self.tabs)
        self.state_frame = tk.Frame(self.tabs)
        self.tabs.add(self.ast_view, text="AST")
        self.tabs.add(self.ir_view, text="IR")
        self.tabs.add(self.plot_frame, text="Visuals")
        self.tabs.add(self.state_frame, text="Statevector")
        self.tabs.pack(fill=tk.BOTH, expand=True)

        viz_ctrl = tk.Frame(self.plot_frame)
        viz_ctrl.pack(anchor="nw")
        tk.Label(viz_ctrl, text="View:").pack(side=tk.LEFT)
        self.view_option = tk.StringVar(value="Circuit")
        options = ["Circuit", "Histogram", "Bloch", "Timeline", "Density", "Entanglement"]
        tk.OptionMenu(viz_ctrl, self.view_option, *options, command=self.plot_visualization).pack(side=tk.LEFT)

        self.log_area = scrolledtext.ScrolledText(self.root, height=6, bg="#111", fg="lime", font=("Courier", 10))
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

    def set_save_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_dir = directory
            self.ast_path = os.path.join(directory, "ast.json")
            self.ir_path = os.path.join(directory, "ir.json")
            self.log(f"[DIR SET] Output to {directory}")

    def parse_code(self):
        try:
            code = self.code_area.get("1.0", tk.END).strip()
            self.ast = parse_qucpl(code)
            with open(self.ast_path, "w") as f:
                json.dump(self.ast, f, indent=2)
            self.ast_view.delete("1.0", tk.END)
            self.ast_view.insert("end", json.dumps(self.ast, indent=2))
            self.log("[✅ PARSED] AST generated")
        except Exception as e:
            self.log(f"[❌ PARSE ERROR] {e}")

    def compile_ir(self):
        try:
            if not self.ast:
                raise Exception("Parse the code first.")
            self.ir = ast_to_ir(self.ast)
            self.ir_instr_index = 0
            with open(self.ir_path, "w") as f:
                json.dump(self.ir, f, indent=2)
            self.ir_view.delete("1.0", tk.END)
            self.ir_view.insert("end", json.dumps(self.ir, indent=2))
            self.log("[✅ COMPILED] IR generated")
        except Exception as e:
            self.log(f"[❌ COMPILE ERROR] {e}")

    def simulate(self):
        try:
            if not self.ir:
                raise Exception("Compile IR first.")
            simulate(self.ir_path, title="QuCPL Simulation")
            self.log("[⚙️ SIMULATED] Histogram displayed")
        except Exception as e:
            self.log(f"[❌ SIMULATION ERROR] {e}")

    def visualize(self):
        try:
            if not self.ir:
                raise Exception("Compile IR first.")
            visualize_circuit(self.ir, title="QuCPL Circuit")
            self.log("[👁️ CIRCUIT SHOWN]")
        except Exception as e:
            self.log(f"[❌ VISUALIZATION ERROR] {e}")

    def plot_visualization(self, *_):
        try:
            if not self.ir:
                raise Exception("Compile IR first.")
            qc, _ = build_qiskit_circuit(self.ir)
            option = self.view_option.get()
            fig = None

            if option == "Circuit":
                fig = qc.draw(output="mpl")
            elif option == "Histogram":
                if AerSimulator:
                    sim = AerSimulator()
                    tqc = transpile(qc, sim)
                    result = sim.run(tqc).result()
                    counts = result.get_counts()
                    fig = plot_histogram(counts)
            elif option == "Bloch":
                state = Statevector.from_instruction(qc)
                fig = plot_bloch_multivector(state)
            elif option == "Timeline" and timeline_drawer:
                fig = timeline_drawer(qc, show_idle=True, show_barriers=True)
            elif option == "Density":
                dm = DensityMatrix.from_instruction(qc)
                fig, ax = plt.subplots()
                ax.matshow(abs(dm.data), cmap='viridis')
                ax.set_title("Density Matrix |ρ|")
            elif option == "Entanglement":
                state = Statevector.from_instruction(qc)
                n = state.num_qubits
                import numpy as np
                fig, ax = plt.subplots()
                ent = np.zeros((n, n))
                for i in range(n):
                    for j in range(n):
                        if i != j:
                            reduced = partial_trace(state, [k for k in range(n) if k != i and k != j])
                            ent[i, j] = np.linalg.norm(reduced.data.real)
                ax.imshow(ent, cmap='inferno')
                ax.set_title("Entanglement Heatmap")
                ax.set_xlabel("Qubit")
                ax.set_ylabel("Qubit")
            if fig:
                self.show_plot(fig)
                self.log(f"[🔍 VIEW] {option} shown")
        except Exception as e:
            self.log(f"[❌ VISUALIZATION ERROR] {e}")

    def show_plot(self, fig):
        for widget in self.plot_frame.winfo_children():
            if isinstance(widget, tk.Frame): continue
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def step_debug(self):
        try:
            if not self.ir or "instructions" not in self.ir:
                raise Exception("Compile IR first.")
            instrs = self.ir["instructions"][:self.ir_instr_index + 1]
            partial_ir = {"qubits": self.ir["qubits"], "instructions": instrs}
            qc, _ = build_qiskit_circuit(partial_ir)
            state = Statevector.from_instruction(qc)
            fig = qc.draw(output="mpl")
            self.ir_instr_index += 1
            if self.ir_instr_index >= len(self.ir["instructions"]):
                self.ir_instr_index = 0
            self.show_plot(fig)
            self.log(f"[🐾 STEP] Executed {self.ir_instr_index} instructions.")
        except Exception as e:
            self.log(f"[❌ DEBUG ERROR] {e}")

    def show_statevector(self):
        try:
            qc, _ = build_qiskit_circuit(self.ir)
            state = Statevector.from_instruction(qc)
            for widget in self.state_frame.winfo_children():
                widget.destroy()
            text = tk.Text(self.state_frame)
            text.pack(fill=tk.BOTH, expand=True)
            for i, amp in enumerate(state):
                text.insert(tk.END, f"|{i:0{state.num_qubits}b}> : {amp.real:.3f} + {amp.imag:.3f}i\n")
            self.log("[📊 STATEVECTOR SHOWN]")
        except Exception as e:
            self.log(f"[❌ STATEVECTOR ERROR] {e}")

    def on_tab_autocomplete(self, event):
        pos = self.code_area.index(tk.INSERT)
        word_start = self.code_area.search(r"\w+", pos, backwards=True, regexp=True)
        word_end = self.code_area.index(f"{word_start} wordend")
        word = self.code_area.get(word_start, word_end)
        snippet = QUCPL_SNIPPETS.get(word.strip())
        if snippet:
            self.code_area.delete(word_start, word_end)
            self.code_area.insert(word_start, snippet)
            return "break"
        return None

    def reset_app(self):
        self.code_area.delete("1.0", tk.END)
        self.ast_view.delete("1.0", tk.END)
        self.ir_view.delete("1.0", tk.END)
        self.log_area.delete("1.0", tk.END)
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        for widget in self.state_frame.winfo_children():
            widget.destroy()
        self.ir_instr_index = 0
        self.log("[🔄 RESET] App cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuCPLStudio(root)
    root.mainloop()
    
