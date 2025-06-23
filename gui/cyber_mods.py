import tkinter as tk
from tkinter import ttk

class CyberModsPanel(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Cyber Mods")
        self.mods = {}
        self._build_hands_mods()

    def _build_hands_mods(self):
        # Primary hand mod
        ttk.Label(self, text="Hands").pack(anchor='w')
        self.cyber_mod = ttk.Combobox(self, values=[
            "None", "Ballistic Coprocessor", "Smart Link", "Scratchers",
            "Rippers", "Wolvers", "Big Knucks", "Slice N' Dice",
            "Heatsaw Hands", "Carbon Knuckles", "Pretty Tattoo"
        ], state="readonly")
        self.cyber_mod.current(0)
        self.cyber_mod.pack(anchor='w')
        self.cyber_mod.bind("<<ComboboxSelected>>", self._check_hand_tattoo)

        # Secondary hand mod (initially disabled)
        self.cyber_mod_1 = ttk.Combobox(self, values=[
            "None", "Ballistic Coprocessor", "Smart Link", "Scratchers",
            "Rippers", "Wolvers", "Big Knucks", "Slice N' Dice",
            "Heatsaw Hands", "Carbon Knuckles"
        ], state="readonly")
        self.cyber_mod_1.current(0)
        self.cyber_mod_1.pack(anchor='w', pady=(5, 0))
        self.cyber_mod_1.config(state="disabled")

    def _check_hand_tattoo(self, event):
        selected = self.cyber_mod.get()
        if selected == "Pretty Tattoo":
            self.cyber_mod_1.config(state="readonly")
        else:
            self.cyber_mod_1.config(state="disabled")

    def get_hand_mods(self):
        return self.cyber_mod.get(), self.cyber_mod_1.get()
