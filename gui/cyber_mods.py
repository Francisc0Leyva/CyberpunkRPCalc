import tkinter as tk
from tkinter import ttk
from data.constants import CYBERMODS  # Option C schema

class CyberModsPanel(ttk.LabelFrame):
    """
    Cyber Mods selector with hover + selection description updates.

    Behavior:
      - Hovering a combobox shows "System — Mod: desc [ (Tier X) if OS ]" in the DescriptionBox.
      - Selecting a mod updates the DescriptionBox as well.
      - Leaving the widget clears the DescriptionBox, even if a mod is selected.
      - OS tier spinbox: hovering it shows the currently selected OS mod + Tier (if any).
    """
    def __init__(self, master, set_description=None, clear_description=None):
        super().__init__(master, text="Cyber Mods")
        # description callbacks (same pattern as TagsPanel)
        self.set_description = set_description or (lambda text: None)
        self.clear_description = clear_description or (lambda: None)

        self.system_boxes = {}         # system -> [Combobox,...]
        self.system_vars  = {}         # system -> [StringVar,...]
        self.os_tier_var  = tk.StringVar(value="")
        self._build_all()

    # ---------- PUBLIC API ----------
    def get_selected_mod_ids(self) -> dict:
        """
        Returns a dict of {system_key: [mod_id, ...]}, plus an OS tier token 'tier:X' if chosen.
        """
        out = {}
        for system, boxes in self.system_boxes.items():
            ids = []
            mods = CYBERMODS[system]["mods"]
            name_to_id = {m["name"]: m["id"] for m in mods}
            for i, cb in enumerate(boxes):
                if str(cb["state"]) != "readonly":
                    continue
                name = self.system_vars[system][i].get()
                if name and name != "None":
                    ids.append(name_to_id.get(name, name))
            if ids:
                out[self._syskey(system)] = ids

        if "Operating System" in self.system_boxes:
            tier = self.os_tier_var.get().strip()
            if tier:
                out.setdefault(self._syskey("Operating System"), [])
                out[self._syskey("Operating System")].append(f"tier:{tier}")
        return out

    # ---------- INTERNAL BUILD ----------
    def _build_all(self):
        order = [
            "Frontal Cortex", "Ocular System", "Circulatory System", "Immune System",
            "Integumentary System", "Operating System", "Skeleton", "Hands", "Arms", "Legs"
        ]
        for system in [s for s in order if s in CYBERMODS]:
            self._build_system(system)

    def _build_system(self, system: str):
        data = CYBERMODS[system]
        mods = data["mods"]
        names = ["None"] + [m["name"] for m in mods]

        ttk.Label(self, text=system).pack(anchor="w", pady=(6, 0))

        slots = data.get("slots", 1)
        self.system_boxes[system] = []
        self.system_vars[system]  = []

        for i in range(slots):
            var = tk.StringVar(value="None")
            cb = ttk.Combobox(self, values=names, state=("readonly" if i == 0 else "disabled"),
                              textvariable=var)
            cb.pack(anchor="w")

            # Selection -> update desc
            cb.bind("<<ComboboxSelected>>",
                    lambda e, sys=system, idx=i: self._on_slot_change(sys, idx))

            # Hover in -> show desc of current selection (if any)
            cb.bind("<Enter>",
                    lambda e, sys=system, idx=i: self._hover_show(sys, idx))
            # Hover out -> clear
            cb.bind("<Leave>", lambda e: self.clear_description())

            # (optional) focus in -> also show
            cb.bind("<FocusIn>",
                    lambda e, sys=system, idx=i: self._hover_show(sys, idx))

            self.system_boxes[system].append(cb)
            self.system_vars[system].append(var)

        # Hands: extra slot enabled by Pretty Tattoo (locked by default)
        if system == "Hands":
            var = tk.StringVar(value="None")
            extra = ttk.Combobox(self, values=names, state="disabled", textvariable=var)
            extra.pack(anchor="w")

            extra_idx = len(self.system_boxes[system])  # index for this extra box

            # Selection -> update desc
            extra.bind("<<ComboboxSelected>>",
                       lambda e, sys=system, idx=extra_idx: self._on_slot_change(sys, idx))

            # Hover in/out -> show/clear
            extra.bind("<Enter>", lambda e, sys=system, idx=extra_idx: self._hover_show(sys, idx))
            extra.bind("<Leave>", lambda e: self.clear_description())
            # focus nicety
            extra.bind("<FocusIn>", lambda e, sys=system, idx=extra_idx: self._hover_show(sys, idx))

            self.system_boxes[system].append(extra)
            self.system_vars[system].append(var)

        # OS: spinbox for tiers, with hover handlers
        if system == "Operating System":
            self._build_os_tiers_row()

    def _build_os_tiers_row(self):
        row = ttk.Frame(self)
        row.pack(anchor="w", pady=(2, 0))
        ttk.Label(row, text="Tier:").pack(side=tk.LEFT)
        self.os_tier_spin = ttk.Spinbox(
            row,
            values=("1", "2", "3", "4", "5", "5A", "5B"),
            state="disabled",
            textvariable=self.os_tier_var,
            width=5,
            wrap=True
        )
        self.os_tier_spin.pack(side=tk.LEFT, padx=(6, 0))

        # Hover in on tier spin -> show current OS selection + tier
        self.os_tier_spin.bind("<Enter>", lambda e: self._hover_show_os_tier())
        # Hover out -> clear
        self.os_tier_spin.bind("<Leave>", lambda e: self.clear_description())

        # If tier changes while hovered/focused, refresh description
        # (ttk.Spinbox doesn't emit a virtual event by default; use <FocusIn> & <KeyRelease> as a light proxy)
        self.os_tier_spin.bind("<FocusIn>", lambda e: self._hover_show_os_tier())
        self.os_tier_spin.bind("<KeyRelease>", lambda e: self._hover_show_os_tier())

    # ---------- EVENTS ----------
    def _on_slot_change(self, system: str, idx: int):
        boxes = self.system_boxes[system]
        vars_ = self.system_vars[system]

        chosen_name = vars_[idx].get()
        # show description immediately on selection
        self._show_desc(system, chosen_name)

        # 1) cascade enable/disable
        enable_next = (chosen_name != "None")
        if idx + 1 < len(boxes):
            if enable_next:
                boxes[idx + 1].config(state="readonly")
            else:
                for j in range(idx + 1, len(boxes)):
                    vars_[j].set("None")
                    boxes[j].config(state="disabled")

        # 2) Hands: Pretty Tattoo unlocks extra slot
        if system == "Hands":
            names_per_slot = [v.get() for v in vars_]
            pretty_present = any(n == "Pretty Tattoo" for n in names_per_slot)
            extra_idx = len(boxes) - 1
            if pretty_present:
                boxes[extra_idx].config(state="readonly")
            else:
                if vars_[extra_idx].get() == "None":
                    boxes[extra_idx].config(state="disabled")

        # 3) no duplicates
        self._enforce_no_duplicates(system)

        # 4) OS tier toggle
        if system == "Operating System":
            selected = vars_[0].get()
            has_selection = (selected and selected != "None")
            self.os_tier_spin.config(state=("readonly" if has_selection else "disabled"))
            if not has_selection:
                self.os_tier_var.set("")

    def _enforce_no_duplicates(self, system: str):
        boxes = self.system_boxes[system]
        vars_ = self.system_vars[system]
        names_all = ["None"] + [m["name"] for m in CYBERMODS[system]["mods"]]

        chosen = {v.get() for v in vars_ if v.get() != "None"}
        for j, cb in enumerate(boxes):
            current = vars_[j].get()
            allowed = ["None"] + [n for n in names_all[1:] if n not in (chosen - {current})]
            cb["values"] = allowed
            if current not in allowed:
                vars_[j].set("None")
                cb.config(state="disabled" if j > 0 else "readonly")

    # ---------- DESCRIPTION LOOKUP ----------
    def _hover_show(self, system: str, idx: int):
        """Show description for the current selection in this combobox."""
        name = self.system_vars[system][idx].get()
        self._show_desc(system, name)

    def _hover_show_os_tier(self):
        """Show OS selection + tier when hovering the tier spinbox."""
        system = "Operating System"
        if system not in self.system_vars or not self.system_vars[system]:
            self.clear_description()
            return
        current_name = self.system_vars[system][0].get()
        self._show_desc(system, current_name)

    def _show_desc(self, system: str, mod_name: str):
        """Push a friendly description line to the description box."""
        if not mod_name or mod_name == "None":
            self.clear_description()
            return
        mod = self._find_mod(system, mod_name)
        if not mod:
            self.clear_description()
            return

        # Build a friendly line: "System — Mod: description [tier hint if OS]"
        line = f"{mod['name']}: {mod.get('desc','')}".strip()
        if system == "Operating System":
            tier = self.os_tier_var.get().strip()
            if tier:
                line += f" (Tier {tier})"
        self.set_description(line)

    def _find_mod(self, system: str, mod_name: str):
        for m in CYBERMODS[system]["mods"]:
            if m["name"] == mod_name:
                return m
        return None

    # ---------- HELPERS ----------
    def _syskey(self, system: str) -> str:
        return system.lower().replace(" ", "_")
    