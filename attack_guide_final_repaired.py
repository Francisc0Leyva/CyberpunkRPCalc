import tkinter as tk
from tkinter import ttk
import random

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, background="#ffffe0",
            relief="solid", borderwidth=1,
            font=("tahoma", "8", "normal")
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

class CyberpunkAttackGuide(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cyberpunk D&D Attack Guide")
        self.geometry("1100x750")
        self.create_widgets()

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(top_frame, text="Name:").pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(top_frame, width=20)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        button_info = {
            "1": "Character Equipped, States, Cybermods, and Combat Stats",
            "2": "Character Origins, Trait Stats and Civil Attributes and Traits",
            "3": "???",
            "4": "Eurodollars, Inventory"
        }
        for num, info in button_info.items():
            btn = ttk.Button(top_frame, text=num)
            btn.pack(side=tk.LEFT, padx=2)
            ToolTip(btn, info)

        left_frame = ttk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        center_frame = ttk.Frame(self)
        center_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5)
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(left_frame, text="Statistics", font=("Arial", 10, "bold")).pack(anchor='w')
        self.attributes = {}
        for attr in ["Body", "Willpower", "Cool", "Intelligence", "Reflexes", "Skill", "Technical Ability"]:
            ttk.Label(left_frame, text=f"{attr}:").pack(anchor='w')
            sb = tk.Spinbox(left_frame, from_=10, to=50, width=5)
            sb.pack(anchor='w')
            ToolTip(sb, "Value must be between 10 and 50.")
            self.attributes[attr] = sb

        ttk.Label(center_frame, text="Character Tags", font=("Arial", 10, "bold")).pack(anchor='w')
        self.tags = {}
        tag_descriptions = {
            "Aikido": "+25% Unarmed damage.",
            "Animal Kung Fu": "15% chance to cause Stun (Unarmed).",
            "Archery": "+15% hit/crit if using arrows.",
            "Boxing": "+10 Body for Unarmed.",
            "Brawling": "+10 Reflexes for Unarmed.",
            "Capoeria": "20% chance to cause Confuse (Unarmed).",
            "Choi Li Fut": "Adds 'Pure damage' text (Unarmed).",
            "Fencing" : "+15% crit for all bladed weapons.",
            "Judo": "25% chance to cause Taunt (Unarmed).",
            "Karate": "Special future-based modifier.",
            "Melee Training": "+5% crit for all melee.",
            "Tae Kwon Do": "Prefix 'Surprise'. Shows full formula.",
            "Thai Kick Boxing": "Enables new damage type, kick, increases damage by 50%, doesn't use cyberwear",
            "Wrestling": "enables new damage type, grappling, may stun the enemy"
        }
        for tag, desc in tag_descriptions.items():
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(center_frame, text=tag, variable=var)
            chk.pack(anchor='w')
            chk.bind("<Enter>", lambda e, t=tag, d=desc: self.set_description(f"{t}: {d}"))
            chk.bind("<Leave>", lambda e: self.clear_description())
            self.tags[tag] = var

        ttk.Label(right_frame, text="Status Effects", font=("Arial", 10, "bold")).pack(anchor='w')
        self.status_effects = {}
        status_effect_list = ["Blind", "Confuse", "Slow", "Focus", "Drenched"]

        for effect in status_effect_list:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(right_frame, text=effect, variable=var)
            chk.pack(anchor='w')
            chk.bind("<Enter>", lambda e, eff=effect: self.set_description(f"Status Effect: {eff}"))
            chk.bind("<Leave>", lambda e: self.clear_description())
            self.status_effects[effect] = var

        ttk.Label(right_frame, text="Weapon", font=("Arial", 10, "bold")).pack(anchor='w', pady=(10, 0))
        ttk.Label(right_frame, text="Weapon Type:").pack(anchor='w')
        #TODO:banaid fix putting kick in the drop box for now, only works if the user has thai kickboxing
        # also wrestling grappling
        self.weapon_type = ttk.Combobox(right_frame, values=["Unarmed Melee", "Blunt Weapon Melee", "Sharp Weapon Melee", "Ranged Attack", "Kick", "Grappling"], state="readonly")
        self.weapon_type.current(0)
        self.weapon_type.pack(anchor='w')
        self.weapon_type.bind("<<ComboboxSelected>>", self.toggle_weapon_damage)

        ttk.Label(right_frame, text="Weapon Damage:").pack(anchor='w')
        self.weapon_damage = tk.Spinbox(right_frame, from_=0, to=1000, width=20)
        self.weapon_damage.pack(anchor='w')

        self.smart_weapon = tk.BooleanVar()
        ttk.Checkbutton(right_frame, text="Smart Weapon", variable=self.smart_weapon).pack(anchor='w')

        self.uses_arrows = tk.BooleanVar()
        ttk.Checkbutton(right_frame, text="Uses Arrows", variable=self.uses_arrows).pack(anchor='w')

        self.always_crit = tk.BooleanVar()
        ttk.Checkbutton(right_frame, text="Always Crit", variable=self.always_crit).pack(anchor='w')

        self.returnedAttack = tk.BooleanVar()
        ttk.Checkbutton(right_frame, text="Returned Attack", variable=self.always_crit).pack(anchor='w')

        self.attackingFirst = tk.BooleanVar()
        ttk.Checkbutton(right_frame, text="Attacking First", variable=self.always_crit).pack(anchor='w')

        self.lock_stats = tk.BooleanVar()
        ttk.Checkbutton(right_frame, text="Lock Stats", variable=self.lock_stats, command=self.toggle_stats_lock).pack(anchor='w')



        ttk.Label(left_frame, text="Cyber Mods", font=("Arial", 10, "bold")).pack(anchor='w', pady=(10, 0))
        ttk.Label(left_frame, text="Hands").pack(anchor='w')
        self.cyber_mod = ttk.Combobox(left_frame, values=[
            "None", "Ballistic Coprocessor", "Smart Link", "Scratchers",
            "Rippers", "Wolvers", "Big Knucks", "Slice N' Dice",
            "Heatsaw Hands", "Carbon Knuckles", "Pretty Tattoo"
        ], state = "readonly")
        self.cyber_mod.current(0)
        self.cyber_mod.pack(anchor='w')
        self.cyber_mod.bind("<<ComboboxSelected>>", self.check_hand_tattoo)

        #TODO: change the weapon calculation logic '
        ttk.Label(left_frame, text="Hands(1)").pack(anchor='w')
        self.cyber_mod_1 = ttk.Combobox(left_frame, values=[
            "None", "Ballistic Coprocessor", "Smart Link", "Scratchers",
            "Rippers", "Wolvers", "Big Knucks", "Slice N' Dice",
            "Heatsaw Hands", "Carbon Knuckles"
        ], state = "readonly")
        self.cyber_mod_1.current(0)
        self.cyber_mod_1.pack(anchor='w')
        self.cyber_mod_1.config(state="disabled")



        self.description_box = tk.Text(bottom_frame, height=5)
        self.description_box.pack(fill=tk.X, padx=5, pady=5)
        self.description_box.config(state="disabled")

        ttk.Button(bottom_frame, text="Calculate", command=self.calculate).pack(pady=5)

        self.result_text = tk.Text(bottom_frame, height=15, relief=tk.SOLID, borderwidth=1)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_text.config(state="disabled")

    def check_hand_tattoo(self, event):
        selected_mod = event.widget.get()
        if self.cyber_mod.get() == "Pretty Tattoo":
            self.cyber_mod_1.config(state="normal")
        else:
            self.cyber_mod_1.config(state="disabled")

    def toggle_stats_lock(self):
        state = "disabled" if self.lock_stats.get() else "normal"
        for spinbox in self.attributes.values():
            spinbox.config(state=state)

    def set_description(self, text):
        self.description_box.config(state="normal")
        self.description_box.delete(1.0, tk.END)
        self.description_box.insert(tk.END, text)
        self.description_box.config(state="disabled")

    def clear_description(self):
        self.description_box.config(state="normal")
        self.description_box.delete(1.0, tk.END)
        self.description_box.config(state="disabled")

    def toggle_weapon_damage(self, event=None):
        if self.weapon_type.get() == "Unarmed Melee":
            self.weapon_damage.delete(0, tk.END)
            self.weapon_damage.insert(0, '0')
            self.weapon_damage.config(state='disabled')
        else:
            self.weapon_damage.config(state='normal')  # <-- END OF METHOD

    def calculate(self):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        try:
            body = int(self.attributes["Body"].get())
            willpower = int(self.attributes["Willpower"].get())
            cool = int(self.attributes["Cool"].get())
            intelligence = int(self.attributes["Intelligence"].get())
            reflexes = int(self.attributes["Reflexes"].get())
            skill = int(self.attributes["Skill"].get())
            technical = int(self.attributes["Technical Ability"].get())
        except ValueError:  # Now properly aligned
            self.result_text.insert(tk.END, "Invalid attribute values!")
            return

        if self.status_effects["Slow"].get():
            reflexes = max(10, reflexes // 2)

        if self.status_effects["Drenched"].get():
            cool = max(10, cool - 5)

        if self.cyber_mod.get() == "Pretty Tattoo":
            cool += 3

        # Tags adjustments
        if self.tags["Brawling"].get() and self.weapon_type.get() == "Unarmed Melee":
            reflexes += 10
        if self.tags["Boxing"].get() and self.weapon_type.get() == "Unarmed Melee":
            body += 10

        # Weapon Damage
        weapon_damage = int(self.weapon_damage.get()) if self.weapon_damage['state'] == 'normal' else 0

        # Cyber Mod effects
        crit_bonus = 0
        hit_bonus = 0
        damage_multiplier = 1.0
        crit_multiplier = 1.0
        inflicts_bleed = False
        inflicts_burn = False
        inflicts_stun = False
        if self.cyber_mod.get() == "Ballistic Coprocessor":
            hit_bonus += 0.15
            crit_bonus += 0.05
        elif self.cyber_mod.get() == "Smart Link" and self.smart_weapon.get():
            hit_bonus = 1.0
            crit_bonus = 0.0
        elif self.cyber_mod.get() == "Scratchers" and self.weapon_type.get() == "Unarmed Melee":
            damage_multiplier += 0.10
            crit_bonus += 0.10
        elif self.cyber_mod.get() == "Rippers" and self.weapon_type.get() == "Unarmed Melee":
            damage_multiplier += 0.20
            crit_bonus += 0.20
        elif self.cyber_mod.get() == "Wolvers" and self.weapon_type.get() == "Unarmed Melee":
            crit_bonus += 0.20
            crit_multiplier += 0.20
        elif self.cyber_mod.get() == "Big Knucks" and self.weapon_type.get() == "Unarmed Melee":
            crit_bonus = 0.0
            damage_multiplier = 1.0  # Will set damage to max later
        elif self.cyber_mod.get() == "Slice N' Dice" and self.weapon_type.get() == "Unarmed Melee":
            damage_multiplier += 0.25
            inflicts_bleed = True
        elif self.cyber_mod.get() == "Heatsaw Hands" and self.weapon_type.get() == "Unarmed Melee":
            damage_multiplier += 0.25
            inflicts_burn = True
        elif self.cyber_mod.get() == "Carbon Knuckles" and self.weapon_type.get() == "Unarmed Melee":
            damage_multiplier += 0.25
            crit_bonus = 1.0

        # Tags adjustments
        if self.tags["Archery"].get() and self.uses_arrows.get():
            hit_bonus += 0.15
            crit_bonus += 0.15
        if self.tags["Melee Training"].get() and self.weapon_type.get() in ["Unarmed Melee", "Blunt Weapon Melee", "Sharp Weapon Melee"]:
            crit_bonus += 0.05
        if self.tags["Aikido"].get() and self.weapon_type.get() == "Unarmed Melee":
            damage_multiplier += 0.25
        if self.tags["Fencing"].get() and self.weapon_type.get() in ["Sharp Weapon Melee"]:
            crit_bonus += 0.15
        # placing the karate attack first bonus here for now
        if self.tags["Karate"].get() and self.returnedAttack.get():
            hit_bonus += 0.20
        if self.tags["Tae Kwon Do"].get() and self.attackingFirst.get():
            hit_bonus += 0.50

        # Calculate base damage
        #TODO check damage multiplier math
        skill_rand = random.randint(skill, cool + 50)
        if self.weapon_type.get() == "Unarmed Melee":
            body_divisor = 10
            base_damage = (body / body_divisor + cool / 5 + reflexes * (0.01 * skill_rand) + 0.75)
            base_damage *= damage_multiplier
            crit_chance = min(1.0, skill * 0.01 + 0.03 + crit_bonus)
            hit_chance = 1.0
        elif self.weapon_type.get() == "Blunt Weapon Melee":
            body_divisor = 8
            base_damage = (body / body_divisor + cool / 5 + reflexes * (0.01 * skill_rand) + 0.75) * (weapon_damage * 0.01)
            base_damage *= damage_multiplier
            crit_chance = min(1.0, skill * 0.01 + 0.03 + crit_bonus)
            hit_chance = 1.0
        elif self.weapon_type.get() == "Sharp Weapon Melee":
            body_divisor = 10
            base_damage = (body / body_divisor + cool / 4 + reflexes * (0.01 * skill_rand) + 0.75) * (weapon_damage * 0.01)
            base_damage *= damage_multiplier
            crit_chance = min(1.0, skill * 0.01 + 0.03 + crit_bonus)
            hit_chance = 1.0
        elif self.weapon_type.get() == "Ranged Attack":
            base_damage = intelligence / 2 + reflexes / 10 + (weapon_damage * 0.01 * (skill_rand / 100))
            hit_chance = min(1.0, ((technical / 2 + skill / 2) * 0.01) + 0.47 + hit_bonus)
            crit_chance = min(1.0, skill * 0.01 + 0.03 + crit_bonus)
            base_damage *= damage_multiplier
        elif self.weapon_type.get() == "Kick":
            if not self.tags["Thai Kick Boxing"].get():
                self.result_text.insert(tk.END, "Invalid weapon type selected.\n")
                self.result_text.config(state="disabled")
                return
            body_divisor = 10
            base_damage = (body / body_divisor + cool / 5 + reflexes * (0.01 * skill_rand) + 0.75)
            base_damage *= 1.50
            crit_chance = min(1.0, skill * 0.01 + 0.03 )
            hit_chance = 1.0
        elif self.weapon_type.get() == "Grappling":
            if not self.tags["Wrestling"].get():
                self.result_text.insert(tk.END, "Invalid weapon type selected.\n")
                self.result_text.config(state="disabled")
                return
            grapple_success = random.random() < 0.75
            if grapple_success:
                inflicts_stun = True
                body_divisor = 10
                base_damage = (body / body_divisor + cool / 5 + reflexes * (0.01 * skill_rand) + 0.75)
                base_damage *= 1.50
                crit_chance = min(1.0, skill * 0.01 + 0.03 + crit_bonus)
                hit_chance = 1.0
            else:
                self.result_text.insert(tk.END, "Grapple failed! You are stunned.\n")
                self.result_text.config(state="disabled")
                return
        else:
            self.result_text.insert(tk.END, "Invalid weapon type selected.\n")
            self.result_text.config(state="disabled")
            return
        # Apply Focus reroll if enabled
        if self.status_effects["Focus"].get():
            alt_skill_rand = random.randint(skill, cool + 50)
            original_damage = base_damage
            reroll_damage = base_damage  # default fallback
            if self.weapon_type.get() == "Unarmed Melee":
                reroll_damage = (body / body_divisor + cool / 5 + reflexes * (0.01 * alt_skill_rand) + 0.75)
            elif self.weapon_type.get() == "Blunt Weapon Melee":
                reroll_damage = (body / body_divisor + cool / 5 + reflexes * (0.01 * alt_skill_rand) + 0.75) * (weapon_damage * 0.01)
            elif self.weapon_type.get() == "Sharp Weapon Melee":
                reroll_damage = (body / body_divisor + cool / 4 + reflexes * (0.01 * alt_skill_rand) + 0.75) * (weapon_damage * 0.01)
            elif self.weapon_type.get() == "Ranged Attack":
                reroll_damage = intelligence / 2 + reflexes / 10 + (weapon_damage * 0.01 * (alt_skill_rand / 100))

            reroll_damage *= damage_multiplier
            if reroll_damage > original_damage:
                base_damage = reroll_damage
                self.result_text.insert(tk.END, f"Focus Reroll Activated!\nOld Damage: {round(original_damage, 2)}\nNew Damage: {round(reroll_damage, 2)}\n\n")

        # Determine hit and crit
        is_hit = self.weapon_type.get() != "Ranged Attack" or random.random() < hit_chance
        is_crit = self.always_crit.get() or random.random() < crit_chance

        if not is_hit:
            self.result_text.insert(tk.END, "*Missed Attack*\n", ("italic",))
            return

        if is_crit:
            if self.weapon_type.get() == "Unarmed Melee" and self.cyber_mod.get() == "Big Knucks":
                base_damage = base_damage  # already maxed
            else:
                if self.weapon_type.get() == "Ranged Attack":
                    base_damage *= (1 + 0.35 + technical * 0.01 + crit_multiplier)
                else:
                    base_damage *= (1 + 0.20 + skill * 0.01 + crit_multiplier)

        # Round and display damage
        # Pure damage cannot be reduced TODO: CHOI LI FUT weapon logic, ignores enemy damage reduction
        final_damage = int(base_damage)
        if self.tags["Tae Kwon Do"].get() and self.weapon_type.get() == "Unarmed Melee":
            self.result_text.insert(tk.END, f"Surprise Result: {final_damage} (Formula used with bonus)\n")
        else:
            damage_display = f"{final_damage}"
            if self.tags["Choi Li Fut"].get() and self.weapon_type.get() == "Unarmed Melee":
                damage_display += " Pure damage"
            if self.tags["Animal Kung Fu"].get() and self.weapon_type.get() == "Unarmed Melee" and random.random() < 0.15:
                self.result_text.insert(tk.END, "Status Effect: Stun\n")
            if self.tags["Capoeria"].get() and self.weapon_type.get() == "Unarmed Melee" and random.random() < 0.20:
                self.result_text.insert(tk.END, "Status Effect: Confuse\n")
            if self.tags["Judo"].get() and self.weapon_type.get() == "Unarmed Melee" and random.random() < 0.25:
                self.result_text.insert(tk.END, "Status Effect: Taunt\n")
            if inflicts_bleed:
                self.result_text.insert(tk.END, "Status Effect: Bleed\n")
            if inflicts_burn:
                self.result_text.insert(tk.END, "Status Effect: Burn\n")
            if inflicts_stun:
                self.result_text.insert(tk.END, "Status Effect: Stun\n")
            if is_crit:
                self.result_text.insert(tk.END, f"{damage_display} (CRIT)\n", ("bold",))
            else:
                self.result_text.insert(tk.END, f"{damage_display}\n")

        # Text formatting tags
        self.result_text.tag_configure("bold", foreground = "red", font=("TkDefaultFont", 10, "bold"))
        self.result_text.tag_configure("italic", font=("TkDefaultFont", 10, "italic"))
        self.result_text.config(state="disabled")

'''
      self.result_text.insert([
            f"Damage: {final_damage:.2f}",
           # f"Damage Range: {damage_range[0]:.2f} - {damage_range[1]:.2f}",
            f"Hit Chance: {hit_chance*100:.1f}%",
            f"Crit Chance: {crit_chance*100:.1f}%",
          #  f"Base Formula: {base:.2f}",
            f"Skill Rand: {skill_rand}"
        ])

        # Display results
'''

if __name__ == "__main__":
    app = CyberpunkAttackGuide()
    app.mainloop()
