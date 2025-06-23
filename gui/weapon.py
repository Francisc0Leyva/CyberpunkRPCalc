import tkinter as tk
from tkinter import ttk

class WeaponPanel(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Weapon")
        self.weapon_type = None
        self.weapon_damage = None
        self.smart_weapon = tk.BooleanVar()
        self.uses_arrows = tk.BooleanVar()
        self.always_crit = tk.BooleanVar()
        self.returned_attack = tk.BooleanVar()
        self.attacking_first = tk.BooleanVar()
        self._build()

    def _build(self):
        # Weapon Type
        ttk.Label(self, text="Weapon Type:").pack(anchor='w')
        self.weapon_type = ttk.Combobox(
            self,
            values=[
                "Unarmed Melee", "Blunt Weapon Melee", "Sharp Weapon Melee",
                "Ranged Attack", "Kick", "Grappling"
            ],
            state="readonly"
        )
        self.weapon_type.current(0)
        self.weapon_type.pack(anchor='w')
        self.weapon_type.bind("<<ComboboxSelected>>", self.toggle_weapon_damage)

        # Weapon Damage
        ttk.Label(self, text="Weapon Damage:").pack(anchor='w')
        self.weapon_damage = tk.Spinbox(self, from_=0, to=1000, width=20)
        self.weapon_damage.pack(anchor='w')

        # Weapon Flags
        ttk.Checkbutton(self, text="Smart Weapon", variable=self.smart_weapon).pack(anchor='w')
        ttk.Checkbutton(self, text="Uses Arrows", variable=self.uses_arrows).pack(anchor='w')
        ttk.Checkbutton(self, text="Always Crit", variable=self.always_crit).pack(anchor='w')
        ttk.Checkbutton(self, text="Returned Attack", variable=self.returned_attack).pack(anchor='w')
        ttk.Checkbutton(self, text="Attacking First", variable=self.attacking_first).pack(anchor='w')

    def toggle_weapon_damage(self, event=None):
        if self.weapon_type.get() == "Unarmed Melee":
            self.weapon_damage.delete(0, tk.END)
            self.weapon_damage.insert(0, '0')
            self.weapon_damage.config(state='disabled')
        else:
            self.weapon_damage.config(state='normal')

    def get_weapon_data(self):
        return {
            "type": self.weapon_type.get(),
            "damage": int(self.weapon_damage.get()) if self.weapon_damage['state'] == 'normal' else 0,
            "smart": self.smart_weapon.get(),
            "arrows": self.uses_arrows.get(),
            "always_crit": self.always_crit.get(),
            "returned": self.returned_attack.get(),
            "first": self.attacking_first.get(),
        }
