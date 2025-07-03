Launched via: python final_app.py

Features: Code editor, Run button, Tabs for Circuit, Statevector, Histogram, Bloch, Export buttons, Error logs and status messages

```
# Enhanced app.py for QuCPL Studio with all requested features

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os, json, re
from parser import parse_qucpl
from compiler import ast_to_ir
from simulation import simulate, build_qiskit_circuit
from visualize import visualize_circuit
from qiskit.quantum_info import Statevector, partial_trace
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import keyword

try:
    from qiskit_aer import AerSimulator
    from qiskit.visualization.timeline import draw as timeline_drawer
    from qiskit import transpile
except ImportError:
    AerSimulator = None
    timeline_drawer = None

QUCPL_KEYWORDS = ["h", "x", "cx", "ccx", "measure", "reset", "barrier", "if", "for", "module", "return", "let"]
QUCPL_SNIPPETS = {
    "if": "if condition {\n    // code\n}",
    "for": "for i in 0..N {\n    // code\n}",
    "module": "module name(args) {\n    // body\n}"
}

class QuCPLStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("QuCPL Studio – Quantum IDE")
        self.root.geometry("1400x900")
        self.save_dir = os.getcwd()
        self.ast = None
        self.ir = None
        self.code = ""
        self.ast_path = "ast.json"
        self.ir_path = "ir.json"
        self.create_widgets()

    def create_widgets(self):
        self.code_area = scrolledtext.ScrolledText(self.root, font=("Consolas", 12), wrap=tk.WORD, height=14, undo=True)
        self.code_area.pack(fill=tk.BOTH, expand=True)
        self.code_area.bind("<Tab>", self.on_tab_autocomplete)
        self.code_area.bind("<KeyRelease>", self.highlight_keywords)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X)
        for text, cmd in [
            ("Open", self.load_code),
            ("Save", self.save_code),
            ("Set Output Dir", self.set_save_dir),
            ("Parse", self.parse_code),
            ("Compile", self.compile_ir),
            ("Visualize", self.plot_visualization),
            ("Simulate", self.simulate_and_display),
            ("Statevector", self.show_statevector),
            ("Reset", self.reset_app),
            ("Export AST/IR", self.export_ast_ir)
        ]:
            tk.Button(btn_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=4, pady=4)

        # Main vertical split: Tabs + Logging Console
        main_pane = tk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # Tabs section
        paned = tk.PanedWindow(main_pane, orient=tk.VERTICAL)
        self.tabs = ttk.Notebook(paned)
        self.ast_view = scrolledtext.ScrolledText(self.tabs, font=("Courier", 11))
        self.ir_view = scrolledtext.ScrolledText(self.tabs, font=("Courier", 11))
        self.plot_frame = tk.Frame(self.tabs)
        self.sim_frame = tk.Frame(self.tabs)
        self.state_frame = tk.Frame(self.tabs)
        self.bloch_frame = tk.Frame(self.tabs)
        self.help_view = scrolledtext.ScrolledText(self.tabs, font=("Consolas", 11))

        for frame, label in [
            (self.ast_view, "AST"),
            (self.ir_view, "IR"),
            (self.plot_frame, "Visuals"),
            (self.sim_frame, "Simulation Output"),
            (self.state_frame, "Statevector"),
            (self.bloch_frame, "Bloch Spheres"),
            (self.help_view, "Help")
        ]:
            self.tabs.add(frame, text=label)
        paned.add(self.tabs)

        # Logging Console (Resizable)
        self.log_area = scrolledtext.ScrolledText(main_pane, height=6, bg="#111", fg="lime", font=("Courier", 10))

        main_pane.add(paned)
        main_pane.add(self.log_area)

        # Tutorial and View Controls
        ctrl_frame = tk.Frame(self.root)
        ctrl_frame.pack(fill=tk.X)
        tk.Label(ctrl_frame, text="Tutorial:").pack(side=tk.LEFT)
        self.tutorial_option = tk.StringVar(value="None")
        tutorials = ["None", "Bell", "GHZ", "Teleport"]
        tk.OptionMenu(ctrl_frame, self.tutorial_option, *tutorials, command=self.load_tutorial).pack(side=tk.LEFT)

        tk.Label(ctrl_frame, text="View:").pack(side=tk.LEFT)
        self.view_option = tk.StringVar(value="Circuit")
        views = ["Circuit", "Histogram", "Bloch", "Timeline", "Density", "Entanglement"]
        tk.OptionMenu(ctrl_frame, self.view_option, *views).pack(side=tk.LEFT)

        self.load_help_doc()

    def log(self, msg):
        print(msg)
        self.log_area.insert(tk.END, msg + "\n")
        self.log_area.see(tk.END)

    def load_help_doc(self):
        self.help_view.delete("1.0", tk.END)
        self.help_view.insert(tk.END, """
Welcome to QuCPL Studio!
=========================

Steps:
1. Write code or load a tutorial.
2. Click Parse to generate AST.
3. Click Compile to convert to IR.
4. Click Visualize or Simulate to view.
5. Use dropdowns for tutorials or views.

Keywords:
  - let, if, for, module, return
Gates:
  - h, x, cx, ccx, reset, barrier
Measurement:
  - measure q0 -> c0

Views:
  - Circuit: Standard diagram
  - Histogram: Output probabilities
  - Bloch: Visualize qubit states
  - Timeline: Gate scheduling
  - Density: Matrix visualization
  - Entanglement: Inter-qubit entanglement heatmap

Tutorials:
  Bell, GHZ, Quantum Teleportation
""")

    def load_tutorial(self, value):
        samples = {
            "Bell": "let q0, q1, c0, c1\nh q0\ncx q0 q1\nmeasure q0 -> c0\nmeasure q1 -> c1",
            "GHZ": "let q0, q1, q2, c0, c1, c2\nh q0\ncx q0 q1\ncx q1 q2\nmeasure q0 -> c0\nmeasure q1 -> c1\nmeasure q2 -> c2",
            "Teleport": "let q0, q1, q2, c0, c1\nh q1\ncx q1 q2\ncx q0 q1\nh q0\nmeasure q0 -> c0\nmeasure q1 -> c1\nif c0 == 1 { x q2 }\nif c1 == 1 { z q2 }"
        }
        if value in samples:
            self.code_area.delete("1.0", tk.END)
            self.code_area.insert(tk.END, samples[value])
            self.log(f"[📚 TUTORIAL LOADED] {value} example")

    def load_code(self):
        path = filedialog.askopenfilename()
        if path:
            with open(path) as f:
                self.code_area.delete("1.0", tk.END)
                self.code_area.insert(tk.END, f.read())
            self.log(f"[OPENED] {path}")

    def save_code(self):
        path = filedialog.asksaveasfilename(defaultextension=".qucpl")
        if path:
            with open(path, "w") as f:
                f.write(self.code_area.get("1.0", tk.END))
            self.log(f"[SAVED] {path}")

    def set_save_dir(self):
        dir_ = filedialog.askdirectory()
        if dir_:
            self.save_dir = dir_
            self.ast_path = os.path.join(dir_, "ast.json")
            self.ir_path = os.path.join(dir_, "ir.json")
            self.log(f"[DIR SET] Output: {dir_}")

    def parse_code(self):
        try:
            code = self.code_area.get("1.0", tk.END).strip()
            self.ast = parse_qucpl(code)
            with open(self.ast_path, "w") as f:
                json.dump(self.ast, f, indent=2)
            self.ast_view.delete("1.0", tk.END)
            self.ast_view.insert(tk.END, json.dumps(self.ast, indent=2))
            self.log("[✅ PARSED] AST generated")
        except Exception as e:
            self.log(f"[❌ PARSE ERROR] {e}")

    def compile_ir(self):
        try:
            if not self.ast:
                raise Exception("Parse first.")
            self.ir = ast_to_ir(self.ast)
            with open(self.ir_path, "w") as f:
                json.dump(self.ir, f, indent=2)
            self.ir_view.delete("1.0", tk.END)
            self.ir_view.insert(tk.END, json.dumps(self.ir, indent=2))
            self.log("[✅ COMPILED] IR generated")
        except Exception as e:
            self.log(f"[❌ COMPILE ERROR] {e}")

    def export_ast_ir(self):
        try:
            if self.ast:
                path = filedialog.asksaveasfilename(defaultextension=".json", initialfile="ast.json")
                if path:
                    with open(path, "w") as f:
                        json.dump(self.ast, f, indent=2)
                    self.log(f"[💾 AST SAVED] {path}")
            if self.ir:
                path = filedialog.asksaveasfilename(defaultextension=".json", initialfile="ir.json")
                if path:
                    with open(path, "w") as f:
                        json.dump(self.ir, f, indent=2)
                    self.log(f"[💾 IR SAVED] {path}")
        except Exception as e:
            self.log(f"[❌ EXPORT ERROR] {e}")

    def show_plot(self, fig, frame, save_name="circuit_output.png"):
        for w in frame.winfo_children():
            w.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        tk.Button(frame, text="Save Image", command=lambda: fig.savefig(save_name)).pack()
    

    def show_sim_plot(self, fig, frame, save_name="simulation_histogram.png"):
        for w in frame.winfo_children():
            w.destroy()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        tk.Button(frame, text="Save Image", command=lambda: fig.savefig(save_name)).pack()
            
    def simulate_and_display(self):
        try:
            if not self.ir:
                raise Exception("Compile first.")
            simulate(self.ir_path, title="Simulation")
            qc, _ = build_qiskit_circuit(self.ir)
            sim = AerSimulator()
            tqc = transpile(qc, sim)
            result = sim.run(tqc).result()
            counts = result.get_counts()
            fig = plot_histogram(counts)
            self.show_sim_plot(fig, self.sim_frame)
            self.log("[⚙️ SIMULATED] Histogram displayed")
        except Exception as e:
            self.log(f"[❌ SIM ERROR] {e}")


    def plot_visualization(self):
        try:
            if not self.ir:
                raise Exception("Compile first.")
            qc, _ = build_qiskit_circuit(self.ir)
            view = self.view_option.get()
            fig = None
            if view == "Circuit":
                fig = qc.draw(output="mpl")
            elif view == "Histogram" and AerSimulator:
                sim = AerSimulator()
                tqc = transpile(qc, sim)
                result = sim.run(tqc).result()
                counts = result.get_counts()
                fig = plot_histogram(counts)
            elif view == "Bloch":
                state = Statevector.from_instruction(qc)
                fig = plot_bloch_multivector(state)
            elif view == "Timeline" and timeline_drawer:
                fig = timeline_drawer(qc)
            elif view == "Density":
                from qiskit.quantum_info import DensityMatrix
                dm = DensityMatrix.from_instruction(qc)
                fig, ax = plt.subplots()
                ax.matshow(abs(dm.data), cmap='viridis')
                ax.set_title("Density Matrix")
            elif view == "Entanglement":
                import numpy as np
                state = Statevector.from_instruction(qc)
                n = state.num_qubits
                fig, ax = plt.subplots()
                ent = np.zeros((n, n))
                for i in range(n):
                    for j in range(n):
                        if i != j:
                            reduced = partial_trace(state, [k for k in range(n) if k != i and k != j])
                            ent[i, j] = np.linalg.norm(reduced.data.real)
                ax.imshow(ent, cmap='inferno')
                ax.set_title("Entanglement Heatmap")
            if fig:
                self.show_plot(fig, self.plot_frame)
                self.log(f"[🔍 VIEW] {view} shown")
        except Exception as e:
            self.log(f"[❌ VIS ERROR] {e}")

    def show_statevector(self):
        try:
            for w in self.state_frame.winfo_children():
                w.destroy()
            for w in self.bloch_frame.winfo_children():
                w.destroy()
            qc, _ = build_qiskit_circuit(self.ir)
            state = Statevector.from_instruction(qc)

            text = tk.Text(self.state_frame, font=("Courier", 12))
            text.pack(fill=tk.BOTH, expand=True)
            basis = [f"|{i:0{state.num_qubits}b}>" for i in range(len(state))]
            for i, amp in enumerate(state):
                text.insert(tk.END, f"{basis[i]}: {amp}\n")
            tk.Button(self.state_frame, text="Save Text", command=lambda: self.save_text_output(text, "statevector.txt")).pack()

            fig = plot_bloch_multivector(state)
            canvas = FigureCanvasTkAgg(fig, master=self.bloch_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            tk.Button(self.bloch_frame, text="Save Bloch Image", command=lambda: fig.savefig("bloch_sphere.png")).pack()

            self.log("[📊 STATEVECTOR & BLOCH] Displayed")
        except Exception as e:
            self.log(f"[❌ STATE ERROR] {e}")

    def save_text_output(self, widget, filename):
        content = widget.get("1.0", tk.END)
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=filename)
        if path:
            with open(path, "w") as f:
                f.write(content)
            self.log(f"[💾 TEXT SAVED] {path}")

    def reset_app(self):
        self.code_area.delete("1.0", tk.END)
        self.ast_view.delete("1.0", tk.END)
        self.ir_view.delete("1.0", tk.END)
        self.log_area.delete("1.0", tk.END)
        for f in [self.plot_frame, self.sim_frame, self.state_frame, self.bloch_frame]:
            for w in f.winfo_children():
                w.destroy()
        self.log("[🔄 RESET] App state cleared")

    def on_tab_autocomplete(self, event):
        pos = self.code_area.index(tk.INSERT)
        word = self.code_area.get("insert-1c wordstart", "insert")
        snippet = QUCPL_SNIPPETS.get(word.strip())
        if snippet:
            self.code_area.insert("insert", snippet[len(word):])
            return "break"

    def highlight_keywords(self, event=None):
        self.code_area.tag_remove("keyword", "1.0", tk.END)
        for kw in QUCPL_KEYWORDS:
            start = "1.0"
            while True:
                start = self.code_area.search(rf'\m{kw}\M', start, tk.END, regexp=True)
                if not start:
                    break
                end = f"{start}+{len(kw)}c"
                self.code_area.tag_add("keyword", start, end)
                start = end
        self.code_area.tag_config("keyword", foreground="blue", font=("Consolas", 12, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = QuCPLStudio(root)
    root.mainloop()

```