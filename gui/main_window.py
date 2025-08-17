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
        
        self.cyber_mods_panel = CyberModsPanel(self)
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
        
        self.result_panel = ResultPanel(self.bottom_frame)
        self.result_panel.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        
    def set_description(self, text):
        self.description_box.set_description(text)

    def clear_description(self):
        self.description_box.clear_description()

    def calculate(self):
        attributes = self.attributes_panel.get_values()
        tags = self.tags_panel.get_selected_tags()
        primary_hand, secondary_hand = self.cyber_mods_panel.get_hand_mods()
        weapon = self.weapon_panel.get_weapon_data()
        status = self.status_panel.get_active_effects()

        result = compute_damage(attributes, tags, (primary_hand, secondary_hand), weapon, status)
        self.result_panel.clear()
        self.result_panel.insert(result, style="bold" if "CRIT" in result else None)
        