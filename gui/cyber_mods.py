import tkinter as tk
from tkinter import ttk

class CyberModsPanel(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Cyber Mods")
        self.mods = {}
        self._build_hands_mods()
        self._build_arms_mods()
        self._build_legs_mods()
        self._build_skeleton_mods()
        self._build_nervous_system_mods()
        self._build_immune_system_mods()
        self._build_frontal_cortex_mods()
        self._build_circulatory_system_mods()
        self._build_integumentary_system_mods()
        self._build_ocular_system_mods()
        self._build_operating_system_mods()

    def _build_hands_mods(self):
        # Primary hand mod
        ttk.Label(self, text="Hands").pack(anchor='w')
        self.cyber_mod = ttk.Combobox(self, values=[
            "None", "Ballistic Coprocessor", "Smart Link", "Scratchers",
            "Rippers", "Wolvers", "Big Knucks", "Slice N' Dice",
            "Heatsaw Hands", "Carbon Knuckles", "Pretty Tattoo"
        ], state="readonly")
        self.cyber_mod.current(0)
        self.cyber_mod.pack(anchor='sw')
        self.cyber_mod.bind("<<ComboboxSelected>>", self._check_hand_tattoo)

        # Secondary hand mod (initially disabled)
        self.cyber_mod_1 = ttk.Combobox(self, values=[
            "None", "Ballistic Coprocessor", "Smart Link", "Scratchers",
            "Rippers", "Wolvers", "Big Knucks", "Slice N' Dice",
            "Heatsaw Hands", "Carbon Knuckles"
        ], state="readonly")
        self.cyber_mod_1.current(0)
        self.cyber_mod_1.pack(anchor='w', pady=(5))
        self.cyber_mod_1.config(state="disabled")

    def _build_arms_mods(self):
        ttk.Label(self, text="Arms").pack(anchor='w')
        self.cyber_mod_arms = ttk.Combobox(self, values=["None", "Mantis Blades", "Monowire", "Proctile Launcher", "Gorilla Arms"], state = "readonly")
        self.cyber_mod_arms.current(0)
        self.cyber_mod_arms.pack(anchor='w')

    def _build_legs_mods(self):
        ttk.Label(self, text="Legs").pack(anchor='w')
        self.cyber_mod_legs = ttk.Combobox(self, values=["None", "Double Jump Module", "Fortified Ankles", "Lynx Paws", "Reinforced Tendons", "Hidden Compartment", "Razor Ankles", "Sprint Booster", "Jump Booster", "Stabilizer"], state = "readonly")
        self.cyber_mod_legs.current(0)
        self.cyber_mod_legs.pack(anchor='w')

        
    def _build_skeleton_mods(self):
        # Primary Skeleton mod
        ttk.Label(self, text="Skeleton").pack(anchor='w')
        self.cyber_mod_skeleton = ttk.Combobox(self, values=["None", "Bionic Joints", "Bionic Frame", "Synaptic Accelerators", "Reinforced Bones", "Tech-Frame", "Strength Weave", "Carbon Fiber Bones", "RAM Kinetics", "Reaction Optimizer", "Gorilla Grip"], state = "readonly")
        self.cyber_mod_skeleton.current(0)
        self.cyber_mod_skeleton.pack(anchor='w')

        # Secondary hand mod (initially disabled)
        self.cyber_mod_skeleton_1 = ttk.Combobox(self, values=["None", "Bionic Joints", "Bionic Frame", "Synaptic Accelerators", "Reinforced Bones", "Tech-Frame", "Strength Weave", "Carbon Fiber Bones", "RAM Kinetics", "Reaction Optimizer", "Gorilla Grip"], state = "readonly")
        self.cyber_mod_skeleton_1.current(0)
        self.cyber_mod_skeleton_1.pack(anchor='w')
        self.cyber_mod_skeleton_1.config(state="disabled")
        self.cyber_mod_skeleton.bind("<<ComboboxSelected>>", lambda e: self.change_dropdown_state(self.cyber_mod_skeleton, self.cyber_mod_skeleton_1))


    def _build_nervous_system_mods(self):
        ttk.Label(self, text="Nervous System").pack(anchor='w')
        self.cyber_mod_nervous_system = ttk.Combobox(self, values=["None", "Mantis Blades", "Monowires", "Gernade Launcher", "Gorilla Arms"], state = "readonly")
        self.cyber_mod_nervous_system.current(0)
        self.cyber_mod_nervous_system.pack(anchor='w')

    def _build_immune_system_mods(self):
        ttk.Label(self, text="Arms").pack(anchor='w')
        self.cyber_mod_arms = ttk.Combobox(self, values=["None", "Mantis Blades", "Monowires", "Gernade Launcher", "Gorilla Arms"], state = "readonly")
        self.cyber_mod_arms.current(0)
        self.cyber_mod_arms.pack(anchor='w')

    def _build_frontal_cortex_mods(self):
        ttk.Label(self, text="Arms").pack(anchor='w')
        self.cyber_mod_arms = ttk.Combobox(self, values=["None", "Mantis Blades", "Monowires", "Gernade Launcher", "Gorilla Arms"], state = "readonly")
        self.cyber_mod_arms.current(0)
        self.cyber_mod_arms.pack(anchor='w')

    def _build_circulatory_system_mods(self):
        ttk.Label(self, text="Arms").pack(anchor='w')
        self.cyber_mod_arms = ttk.Combobox(self, values=["None", "Mantis Blades", "Monowires", "Gernade Launcher", "Gorilla Arms"], state = "readonly")
        self.cyber_mod_arms.current(0)
        self.cyber_mod_arms.pack(anchor='w')

    def _build_integumentary_system_mods(self):
        ttk.Label(self, text="Arms").pack(anchor='w')
        self.cyber_mod_arms = ttk.Combobox(self, values=["None", "Mantis Blades", "Monowires", "Gernade Launcher", "Gorilla Arms"], state = "readonly")
        self.cyber_mod_arms.current(0)
        self.cyber_mod_arms.pack(anchor='w')

    def _build_ocular_system_mods(self):
        ttk.Label(self, text="Arms").pack(anchor='w')
        self.cyber_mod_arms = ttk.Combobox(self, values=["None", "Mantis Blades", "Monowires", "Gernade Launcher", "Gorilla Arms"], state = "readonly")
        self.cyber_mod_arms.current(0)
        self.cyber_mod_arms.pack(anchor='w')

    def _build_operating_system_mods(self):
        ttk.Label(self, text="Arms").pack(anchor='w')
        self.cyber_mod_arms = ttk.Combobox(self, values=["None", "Mantis Blades", "Monowires", "Gernade Launcher", "Gorilla Arms"], state = "readonly")
        self.cyber_mod_arms.current(0)
        self.cyber_mod_arms.pack(anchor='w')

    def _check_hand_tattoo(self, event):
        selected = self.cyber_mod.get()
        if selected == "Pretty Tattoo":
            self.cyber_mod_1.config(state="readonly")
        else:
            self.cyber_mod_1.set("None")
            self.cyber_mod_1.config(state="disabled")


    def change_dropdown_state(self, current_mod_list, next_mod_list):
        selected = current_mod_list.get()

        if selected != "None":
            next_mod_list.config(state="readonly")

            full_values = list(current_mod_list.cget("values"))

            new_values = [v for v in full_values if v != selected]

            next_mod_list['values'] = new_values
            next_mod_list.current(0)  

        else:
            next_mod_list.set("None")
            next_mod_list.config(state="disabled")

        



    def get_hand_mods(self):
        return self.cyber_mod.get(), self.cyber_mod_1.get()
