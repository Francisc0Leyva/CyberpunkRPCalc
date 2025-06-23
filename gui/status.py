import tkinter as tk
from tkinter import ttk, BooleanVar
from data.constants import STATUS_EFFECTS  

class StatusPanel(ttk.LabelFrame):
    def __init__(self, master, set_description=None, clear_description=None):
        super().__init__(master, text="Status Effects")
        self.effects = {}
        self.set_description = set_description or (lambda text: None)
        self.clear_description = clear_description or (lambda: None)
        self._build_effects()

    def _build_effects(self):
        for effect in STATUS_EFFECTS:
            var = BooleanVar()
            chk = ttk.Checkbutton(self, text=effect, variable=var)
            chk.pack(anchor='w')
            chk.bind("<Enter>", lambda e, eff=effect: self.set_description(f"Status Effect: {eff}"))
            chk.bind("<Leave>", lambda e: self.clear_description())
            self.effects[effect] = var

    def get_active_effects(self):
        """Return dict of active status effects and their states."""
        return {effect: var.get() for effect, var in self.effects.items()}
