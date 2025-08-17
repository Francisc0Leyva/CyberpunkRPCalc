import tkinter as tk
from tkinter import ttk
from tkinter import BooleanVar
from data.constants import TAG_DESCRIPTIONS  

class TagsPanel(ttk.LabelFrame):
    def __init__(self, master, set_description=None, clear_description=None):
        super().__init__(master, text="Character Tags")
        self.tags = {}
        self.set_description = set_description or (lambda text: None)
        self.clear_description = clear_description or (lambda: None)
        self._build_tags()

    def _build_tags(self):
        for tag, desc in TAG_DESCRIPTIONS.items():
            var = BooleanVar()
            chk = ttk.Checkbutton(self, text=tag, variable=var)
            chk.pack(anchor='w')
            chk.bind("<Enter>", lambda e, t=tag, d=desc: self.set_description(f"{t}: {d}"))
            chk.bind("<Leave>", lambda e: self.clear_description())
            self.tags[tag] = var

    def get_selected_tags(self):
        """Return a dict of tag names and whether they are selected (True/False)."""
        return {tag: var.get() for tag, var in self.tags.items()}
