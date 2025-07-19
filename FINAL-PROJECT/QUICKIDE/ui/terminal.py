import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import sys

class TerminalOutput(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.output = ScrolledText(self, height=10, wrap=tk.WORD, state='disabled')
        self.output.pack(fill=tk.BOTH, expand=True)

        self._redirect_stdout()
        self._redirect_stderr()

    def _redirect_stdout(self):
        sys.stdout = self.TextRedirector(self.output, "stdout")

    def _redirect_stderr(self):
        sys.stderr = self.TextRedirector(self.output, "stderr")

    def clear(self):
        self.output.config(state='normal')
        self.output.delete("1.0", tk.END)
        self.output.config(state='disabled')

    def log(self, message):
        self.output.config(state='normal')
        self.output.insert(tk.END, message + '\n')
        self.output.see(tk.END)
        self.output.config(state='disabled')

    class TextRedirector:
        def __init__(self, widget, tag):
            self.widget = widget
            self.tag = tag

        def write(self, message):
            self.widget.config(state='normal')
            self.widget.insert(tk.END, message)
            self.widget.see(tk.END)
            self.widget.config(state='disabled')

        def flush(self):
            pass
