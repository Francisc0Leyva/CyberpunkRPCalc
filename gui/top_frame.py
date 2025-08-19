import tkinter as tk
from tkinter import ttk
from utils.tooltip import ToolTip

class TopFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.build()
    def build(self):


        ttk.Label(self, text="Name:").pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(self, width=20)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        button_info = {
            "1": "Character Equipped, States, Cybermods, and Combat Stats",
            "2": "Character Origins, Trait Stats and Civil Attributes and Traits",
            "3": "???",
            "4": "Eurodollars, Inventory"
        }
        for num, info in button_info.items():
            btn = ttk.Button(self, text=num)
            btn.pack(side=tk.LEFT, padx=2)
            ToolTip(btn, info)