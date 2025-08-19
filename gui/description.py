import tkinter as tk
from tkinter import ttk

class DescriptionBox(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Info")
        self.text_widget = tk.Text(self, height=5)
        self.text_widget.pack(fill=tk.X, padx=5, pady=5)
        self.text_widget.config(state="disabled")

    def set_description(self, text):
        self.text_widget.config(state="normal")
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, text)
        self.text_widget.config(state="disabled")

    def clear_description(self):
        self.text_widget.config(state="normal")
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.config(state="disabled")
