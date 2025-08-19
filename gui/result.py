import tkinter as tk
from tkinter import ttk

class ResultPanel(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Result")
        self.text = tk.Text(self, height=15, relief=tk.SOLID, borderwidth=1)
        self.text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.text.tag_configure("bold", foreground="red", font=("TkDefaultFont", 10, "bold"))
        self.text.tag_configure("italic", font=("TkDefaultFont", 10, "italic"))
        self.text.config(state="disabled")

    def clear(self):
        self.text.config(state="normal")
        self.text.delete(1.0, tk.END)
        self.text.config(state="disabled")

    def insert(self, content, style=None):
        self.text.config(state="normal")
        if style:
            self.text.insert(tk.END, content, style)
        else:
            self.text.insert(tk.END, content)
        self.text.config(state="disabled")
