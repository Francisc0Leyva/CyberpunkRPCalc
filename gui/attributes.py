import tkinter as tk
from tkinter import ttk
from utils.tooltip import ToolTip

class AttributesPanel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.attributes = {}
        self.lock_stats = tk.BooleanVar()
        self.build()

    def build(self):
        ttk.Label(self, text="Attributes", font=("Arial", 10, "bold")).pack(anchor='w')

        for attr in ["Body", "Willpower", "Cool", "Intelligence", "Reflexes", "Skill", "Technical Ability"]:
            ttk.Label(self, text=f"{attr}:").pack(anchor='w')
            sb = tk.Spinbox(self, from_=10, to=50, width=5)
            sb.pack(anchor='w')
            ToolTip(sb, "Value must be between 10 and 50.")
            self.attributes[attr] = sb

        ttk.Checkbutton(
            self, text="Lock Stats",
            variable=self.lock_stats,
            command=self.toggle_stats_lock
        ).pack(anchor='w', pady=(10, 0))

    def toggle_stats_lock(self):
        state = "disabled" if self.lock_stats.get() else "normal"
        for sb in self.attributes.values():
            sb.config(state=state)

    def get_values(self):
        try:
            return {attr: int(sb.get()) for attr, sb in self.attributes.items()}
        except ValueError:
            return None
