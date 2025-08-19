from utils.dice_roller import roll as dice_roll, DiceRollError
import tkinter as tk
from tkinter import ttk
from gui.top_frame import TopFrame
from gui.attributes import AttributesPanel
from gui.cyber_mods import CyberModsPanel
from gui.tags import TagsPanel
from gui.status import StatusPanel
from gui.weapon import WeaponPanel
from gui.description import DescriptionBox
from gui.result import ResultPanel
from logic.damage_calculator import compute_damage


class CyberpunkAttackGuide(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cyberpunk D&D Attack Guide")
        self.geometry("1100x750")


        self.top_frame = TopFrame(self)
        self.top_frame.pack(fill=tk.X, padx=10, pady=5)


        self.attributes_panel = AttributesPanel(self)
        self.attributes_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        
        self.cyber_mods_panel = CyberModsPanel(self, self.set_description, self.clear_description)
        self.cyber_mods_panel.pack(side=tk.LEFT, padx=10, pady=5)


        self.tags_panel = TagsPanel(self, self.set_description, self.clear_description)
        self.tags_panel.pack(side=tk.LEFT,  padx=10, pady=5)
        self.status_panel = StatusPanel(self, self.set_description, self.clear_description)
        self.status_panel.pack(side=tk.LEFT,  padx=10, pady=5)
        
        self.weapon_panel = WeaponPanel(self)
        self.weapon_panel.pack(side=tk.LEFT,  padx=10, pady=5)
        
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)


        self.description_box = DescriptionBox(self.bottom_frame)
        self.description_box.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(self.bottom_frame, text="Calculate", command=self.calculate).pack(pady=5)
        dice_row = ttk.Frame(self.bottom_frame)
        dice_row.pack(fill=tk.X, padx=5, pady=(0, 6))

        ttk.Label(dice_row, text="Dice:").pack(side=tk.LEFT)
        self.dice_entry = ttk.Entry(dice_row, width=12)
        self.dice_entry.insert(0, "1d20")   # default
        self.dice_entry.pack(side=tk.LEFT, padx=(6, 8))
        ttk.Button(dice_row, text="Roll", command=self.roll_dice).pack(side=tk.LEFT)
        self.dice_entry.bind("<Return>", lambda _e: self.roll_dice())
        self.result_panel = ResultPanel(self.bottom_frame)
        self.result_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        
    def set_description(self, text):
        self.description_box.set_description(text)

    def clear_description(self):
        self.description_box.clear_description()

    def calculate(self):
        attributes = self.attributes_panel.get_values()
        tags = self.tags_panel.get_selected_tags()
        cybermods = self.cyber_mods_panel.get_selected_mod_ids()     
        weapon = self.weapon_panel.get_weapon_data()
        status = self.status_panel.get_active_effects()

        result = compute_damage(attributes, tags, cybermods, weapon, status)
        self.result_panel.clear()
        self.result_panel.insert(result, style="bold" if "CRIT" in result else None)
   
    def roll_dice(self):
        expr = (self.dice_entry.get() or "1d20").strip()
        try:
            res = dice_roll(expr)
            self.result_panel.clear()
            self.result_panel.insert(
                f"Dice Roll — {res['expr']}\n{res['detail']}\nTotal: {res['total']}"
            )
        except DiceRollError as e:
            self.result_panel.clear()
            self.result_panel.insert(f"Dice Roll Error: {e}")
