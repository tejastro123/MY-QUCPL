import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import json

from backend.parser import parse_qucpl
from backend.visualize import visualize_circuit
from backend.compiler import ast_to_ir
from backend.simulator import simulate
from backend.utils import open_file, save_file, format_json

from ui.editor import CodeEditor
from ui.viewer import ViewerPanel
from ui.visualizer import CircuitVisualizer
from ui.terminal import TerminalOutput
from ui.tutorials import TutorialViewer


class QuickIDE(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QuickIDE - Quantum DSL GUI")
        self.geometry("1300x850")
        self._init_layout()

    def _init_layout(self):
        self._create_menu()
        self._create_toolbar()
        self._create_panels()

    def _create_menu(self):
        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open .qucpl", command=self.load_code)
        filemenu.add_command(label="Save .qucpl", command=self.save_code)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        runmenu = tk.Menu(menubar, tearoff=0)
        runmenu.add_command(label="Compile + Visualize", command=self.run_simulation)
        menubar.add_cascade(label="Run", menu=runmenu)

        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Clear Console", command=self.clear_console)
        menubar.add_cascade(label="View", menu=viewmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Open Tutorial", command=self.load_tutorial)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

    def _create_toolbar(self):
        toolbar = ttk.Frame(self, padding=5)
        ttk.Button(toolbar, text="Run", command=self.run_simulation).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Clear Console", command=self.clear_console).pack(side=tk.LEFT, padx=4)
        ttk.Button(toolbar, text="Open Tutorial", command=self.load_tutorial).pack(side=tk.LEFT, padx=4)
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def _create_panels(self):
        self.main_panes = ttk.Panedwindow(self, orient=tk.HORIZONTAL)

        # Left side: Editor
        editor_frame = ttk.Labelframe(self.main_panes, text="QuCPL Code Editor")
        self.editor = CodeEditor(editor_frame)
        self.editor.pack(fill=tk.BOTH, expand=True)
        self.main_panes.add(editor_frame, weight=3)

        # Right side: Output/Visuals
        right_pane = ttk.Panedwindow(self.main_panes, orient=tk.VERTICAL)

        viewer_frame = ttk.Labelframe(right_pane, text="AST / IR Viewer")
        self.viewer = ViewerPanel(viewer_frame)
        self.viewer.pack(fill=tk.BOTH, expand=True)
        right_pane.add(viewer_frame, weight=1)

        visualizer_frame = ttk.Labelframe(right_pane, text="Circuit Visualization")
        self.visualizer = CircuitVisualizer(visualizer_frame)
        self.visualizer.pack(fill=tk.BOTH, expand=True)
        right_pane.add(visualizer_frame, weight=1)

        docs_frame = ttk.Labelframe(right_pane, text="Tutorials")
        self.tutorial_viewer = TutorialViewer(docs_frame)
        self.tutorial_viewer.pack(fill=tk.BOTH, expand=True)
        right_pane.add(docs_frame, weight=1)

        self.main_panes.add(right_pane, weight=5)
        self.main_panes.pack(fill=tk.BOTH, expand=True)

        console_frame = ttk.Labelframe(self, text="Console Output")
        self.console = TerminalOutput(console_frame)
        self.console.pack(fill=tk.BOTH, expand=True)
        console_frame.pack(fill=tk.X)

    def load_code(self):
        content, path = open_file(filetypes=[("QuCPL Files", "*.qucpl")])
        if content:
            self.editor.set_code(content)
            self.log(f"[INFO] Loaded file: {path}\n")

    def save_code(self):
        code = self.editor.get_code()
        path = save_file(code, defaultextension=".qucpl", filetypes=[("QuCPL Files", "*.qucpl")])
        if path:
            self.log(f"[INFO] Saved file: {path}\n")

    def run_simulation(self):
        code = self.editor.get_code()
        if not code:
            messagebox.showwarning("No Input", "Editor is empty. Please enter some QuCPL code.")
            return
        try:
            ast = parse_qucpl(code)
            ir = ast_to_ir(ast)

            self.viewer.display_ast(ast)
            self.viewer.display_ir(ir)
            self.visualizer.display_circuit(ir, title="Compiled Circuit")
            visualize_circuit(ir, "Generated Circuit")
            simulate(ir, title="Simulation")
            self.log("[SUCCESS] Compilation and simulation completed.\n")
        except Exception as e:
            self.log(f"[ERROR] {e}\n")

    def clear_console(self):
        self.console.clear()

    def log(self, message):
        self.console.log(message)

    def load_tutorial(self):
        self.tutorial_viewer.load_tutorial()


if __name__ == "__main__":
    app = QuickIDE()
    app.mainloop()
