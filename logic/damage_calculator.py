
"""
    {
        "type": "Unarmed Melee" | "Blunt" | "Sharp" | "Ranged" | "Whip" | "Slice" | "Blast" | "Kick",
        "base_damage": float|int,   # optional; if omitted, base formula will rely mostly on stats
        "smart": bool,              # optional, for Smart Link
        "tags": set([...])          # optional weapon tags ("arrow","bladed","blunt","smart", etc.)
    }
- status: dict of contextual flags the UI may set, such as:
    {
        "is_first_turn": bool,
        "attacking_first": bool,
        "hp_percent": float,   # 0-100
        "berserk_active": bool # for OS Berserk manual trigger
    }

This implementation focuses on attacker-side effects for MVP. Defender-side mitigation (Rangeguard, Proxishield, etc.)
is not applied unless defender mods are later provided to this function.

Notes:
- Rounding follows the PDF: "round up to the nearest decimal point" -> ceil to 0.1.
- Randomness is used to determine hit/crit and a few status procs; repeated calls will vary.

"""
from __future__ import annotations

import math
import random
from typing import Dict, Any, Tuple, Optional
from data.constants import CYBERMODS 

def ceil1(x: float) -> float:
    """Ceil to one decimal place."""
    return math.ceil(x * 10.0) / 10.0

def clamp01(x: float) -> float:
    return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)

def tilde(a: float, b: float, cap: float = 2.0) -> float:
    """
    a ~ b  -> a / b, capped to [0, cap]
    Keeps growth controlled; many formulas multiply by 0.01 near this.
    """
    if b == 0:
        return cap
    val = a / float(b)
    if val < 0:
        val = 0.0
    if val > cap:
        val = cap
    return val

def syskey(name: str) -> str:
    """Canonicalize a system key (e.g., 'Operating System' -> 'operating_system')."""
    return name.strip().lower().replace(" ", "_")

def lookup_mod(system_key: str, mod_id_or_name: str) -> Optional[Dict[str, Any]]:
    """Find a mod dict by id (preferred) or by visible name."""
    systems = []
    if system_key in CYBERMODS:
        systems.append(system_key)
    else:
        systems = list(CYBERMODS.keys())

    for sysk in systems:
        for m in CYBERMODS[sysk]["mods"]:
            if m.get("id") == mod_id_or_name or m.get("name") == mod_id_or_name:
                return m
    return None

def parse_os_tier(os_values: list) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract selected OS id and its tier token from the operating_system selection list.
    Returns (os_id, tier_str or None)
    """
    os_id = None
    tier = None
    for v in os_values:
        if isinstance(v, str) and v.startswith("tier:"):
            tier = v.split(":", 1)[1]
        else:
            os_id = v  
    return os_id, tier



def base_hit_chance(attack_type: str, technical: float, skill: float) -> float:
    """
    Ranged default per doc: ((((Tech)/2 + (Skill)/2) × 0.01) + 0.47)
    Melee: assume contact unless dodge/graze system exists externally -> use 1.0 here.
    """
    if attack_type == "ranged":
        return clamp01((((technical / 2.0) + (skill / 2.0)) * 0.01) + 0.47)
    return 1.0

def base_crit_chance(skill: float) -> float:
    """Default crit chance path for both melee and ranged before modifiers."""
    return clamp01((skill * 0.01) + 0.03)

def melee_crit_multiplier(skill: float) -> float:
    """On crit: +20% + [Skill]% -> multiplier."""
    return 1.0 + 0.20 + (skill / 100.0)

def ranged_crit_multiplier(technical: float) -> float:
    """On crit: +35% + [Technical Ability]% -> multiplier."""
    return 1.0 + 0.35 + (technical / 100.0)

def detect_attack_category(weapon: Dict[str, Any]) -> Tuple[str, str]:
    """
    Decide attack category & subtype.

    Returns (attack_type, subtype)
      attack_type in {"melee","ranged"}
      subtype in {"unarmed","blunt","sharp","kick","whip","slice","blast","ranged"}
    """
    wtype_raw = weapon.get("type", "Unarmed Melee")
    wtype = str(wtype_raw).strip().lower()
    mapping = {
        "unarmed melee": ("melee","unarmed"),
        "unarmed": ("melee","unarmed"),
        "kick": ("melee","kick"),
        "grappling": ("melee","unarmed"),  
        "blunt": ("melee","blunt"),
        "blunt weapon melee": ("melee","blunt"),
        "sharp": ("melee","sharp"),
        "sharp weapon melee": ("melee","sharp"),
        "blade": ("melee","sharp"),
        "bladed": ("melee","sharp"),
        "whip": ("melee","whip"),
        "slice": ("melee","slice"),
        "blast": ("ranged","blast"),
        "ranged": ("ranged","ranged"),
        "ranged attack": ("ranged","ranged"),
    }
    return mapping.get(wtype, ("ranged","ranged"))


def base_damage_formula(subtype: str,
                        attrs: Dict[str, float],
                        weapon: Dict[str, Any],
                        tags: Dict[str, Any]) -> float:
    """
    Implements base damage baselines (pre-crit, pre-cybermods).
    Schema follows the design doc approximations for MVP.

    subtype: 'unarmed'|'kick'|'blunt'|'sharp'|'whip'|'slice'|'blast'|'ranged'
    """
    body = float(attrs.get("Body", 10))
    cool = float(attrs.get("Cool", 10))
    intel = float(attrs.get("Intelligence", 10))
    reflex = float(attrs.get("Reflexes", 10))
    skill = float(attrs.get("Skill", 10))
    technical = float(attrs.get("Technical Ability", 10))
    willpower = float(attrs.get("Willpower", 10))

    wbase = float(weapon.get("base_damage", weapon.get("damage", 0.0)))

    if tags.get("Boxing") and subtype in ("unarmed","kick"):
        body += 10
    if tags.get("Brawling") and subtype in ("unarmed","kick"):
        reflex += 10

    # Helper frequently used
    skill_tilde = tilde(skill, (cool + 50.0))

    if subtype == "unarmed":
        base = (body / 10.0) + (cool / 5.0) + (reflex * (0.01 * skill_tilde)) + 0.75
        return base

    if subtype == "kick":
        # "Kick doubles unarmed"
        base = (body / 10.0) + (cool / 5.0) + (reflex * (0.01 * skill_tilde)) + 0.75
        return 2.0 * base

    if subtype == "blunt":
        base = (body / 8.0) + ((wbase * 0.01) * skill_tilde)
        return base

    if subtype == "sharp":
        base = (body / 10.0) + (cool / 4.0)
        base *= (wbase * 0.01) if wbase > 0 else 1.0
        return base

    if subtype == "whip":
        # Monowire: swap Body->Intelligence; ×1.5
        base = (intel / 10.0) + (cool / 5.0) + (reflex * (0.01 * skill_tilde)) + 0.75
        return 1.5 * base

    if subtype == "slice":
        # Mantis Blades: heavier Cool; ×1.5
        base = (body / 10.0) + (cool / 3.0)
        base *= (wbase * 0.01) if wbase > 0 else 1.0
        return 1.5 * base

    if subtype == "blast":
        # PLS: ranged using Technical Ability; ×1.5
        base = (technical / 2.0) + (reflex / 10.0) + ((wbase * 0.01) * skill_tilde)
        return 1.5 * base

    # generic ranged
    base = (intel / 2.0) + (reflex / 10.0) + ((wbase * 0.01) * skill_tilde)
    return base



def collect_os_effects(os_values: list) -> Dict[str, Any]:
    """
    Merge OS base_effects + tier effects (if any) into a plain dict of effects.
    """
    os_id, tier = parse_os_tier(os_values)
    if not os_id:
        return {}
    mod = lookup_mod(syskey("Operating System"), os_id)
    if not mod:
        return {}
    effects = {}
    effects.update(mod.get("base_effects", {}))
    tiers = mod.get("tiers", {})
    # tier keys in constants can be ints or strings
    if tier in tiers:
        effects.update(tiers[tier])
    else:
        try:
            tkey = int(tier) if tier is not None else None
            if tkey in tiers:
                effects.update(tiers[tkey])
        except Exception:
            pass
    return effects

def apply_cybermods_to_numbers(dmg: float,
                               hit_chance: float,
                               crit_chance: float,
                               crit_mult: float,
                               attack_type: str,
                               subtype: str,
                               attrs: Dict[str, float],
                               status: Dict[str, Any],
                               cybermods: Dict[str, list],
                               tags: Dict[str, Any]) -> Tuple[float,float,float,float,Dict[str,Any],list]:
    """
    Adjusts damage & crit stats based on cybermods and combat tags.
    Returns updated (dmg, hit_chance, crit_chance, crit_mult, flags, procs_log)
    flags: dict of booleans (e.g., {"force_crit":True, "disable_crit":True, "force_max_roll":True})
    """
    flags = {"force_crit": False, "disable_crit": False, "force_max_roll": False}
    # Honor forced crit from weapon/UI
    if status.get("_force_crit"):
        flags["force_crit"] = True
    procs = []

    # Precompute some context
    is_first_turn = bool(status.get("is_first_turn", False))
    attacking_first = bool(status.get("attacking_first", False))
    hp_percent = float(status.get("hp_percent", 100.0))
    smart_weapon = bool(status.get("_weapon_smart", status.get("weapon_is_smart", False)))

    # Add OS merged effects (if present)
    os_key = syskey("Operating System")
    if os_key in cybermods:
        os_effects = collect_os_effects(cybermods[os_key])
    else:
        os_effects = {}

    # Iterate over all selected mods
    for raw_system, ids in (cybermods or {}).items():
        system = raw_system if raw_system in CYBERMODS else syskey(raw_system)
        if system == os_key:
            # OS handled via os_effects already
            effects_list = [os_effects] if os_effects else []
        else:
            effects_list = []
            for mod_id in ids:
                if isinstance(mod_id, str) and mod_id.startswith("tier:"):
                    continue
                mod = lookup_mod(system, mod_id)
                if not mod:
                    continue
                effects_list.append(mod.get("effects", {}))

        for effects in effects_list:
            # --- Accuracy / hit chance ---
            if attack_type == "ranged" and "ranged_accuracy_add" in effects:
                hit_chance += effects["ranged_accuracy_add"] / 100.0
            if "accuracy_set" in effects:
                hit_chance = effects["accuracy_set"] / 100.0
            if "attack_chance" in effects:
                hit_chance = max(hit_chance, effects["attack_chance"] / 100.0)

            # Smart Link support (requires weapon be marked smart)
            if effects.get("condition") == "smart_weapon" and smart_weapon:
                if "accuracy_set" in effects:
                    hit_chance = effects["accuracy_set"] / 100.0
                if "crit_rate_set" in effects:
                    crit_chance = effects["crit_rate_set"] / 100.0

            # --- Damage bonuses ---
            if attack_type == "melee":
                dmg *= 1.0 + (effects.get("melee_damage_add", 0) / 100.0)
            if attack_type == "ranged":
                dmg *= 1.0 + (effects.get("ranged_damage_add", 0) / 100.0)
            if subtype in ("unarmed","kick"):
                dmg *= 1.0 + (effects.get("unarmed_damage_add", 0) / 100.0)

            # Lynx Paws / Stalker / Callus Coalescer style conditions
            cond = effects.get("condition")
            if cond == "first_strike" and is_first_turn and attacking_first:
                dmg *= 1.0 + (effects.get("damage_add_percent", 0) / 100.0)
            if cond in ("hp_below_50", "hp_below_50%") and hp_percent < 50.0 and attack_type == "melee":
                dmg *= 1.0 + (effects.get("melee_damage_add", 0) / 100.0)
            if cond == "burn_inflicted" and status.get("has_burn", False) and attack_type == "melee":
                dmg *= 1.0 + (effects.get("melee_damage_add", 0) / 100.0)

            # Berserk manual trigger (status flag from UI)
            if status.get("berserk_active", False):
                # tier damage added lives in os_effects if OS is Berserk
                dmg *= 1.0 + (effects.get("damage_add_percent", 0) / 100.0)
                if effects.get("crit_reroll_once_per_battle", 0):
                    flags["force_crit"] = True

            # --- Crit chance / crit damage ---
            crit_chance += effects.get("crit_rate_add", 0) / 100.0
            if subtype in ("unarmed","kick"):
                crit_chance += effects.get("unarmed_crit_rate_add", 0) / 100.0
                if "unarmed_crit_rate_set" in effects:
                    crit_chance = effects["unarmed_crit_rate_set"] / 100.0
                crit_mult *= 1.0 + (effects.get("unarmed_crit_damage_add", 0) / 100.0)

            # Stabber: sharp weapons +10% crit
            if effects.get("condition") == "sharp_weapon" and subtype in ("sharp","slice"):
                crit_chance += effects.get("crit_chance_add", 0) / 100.0

            # Disable/force crits
            if effects.get("unarmed_disable_crit", 0) and subtype in ("unarmed","kick"):
                flags["disable_crit"] = True
            if effects.get("crit_auto_on_low_hp", 0) and hp_percent <= 20.0:
                flags["force_crit"] = True

            # Force to max roll (Big Knucks semantics: always scale to ceiling)
            if effects.get("unarmed_scale_to_ceiling", 0) and subtype in ("unarmed","kick"):
                flags["force_max_roll"] = True

            # Feedback Circuit heal on crit: we'll record the proc if crit happens later
            if effects.get("health_points_on_crit"):
                procs.append({"on_crit_heal": effects["health_points_on_crit"]})

    # Tag-driven global modifiers
    # Melee Training: +5% crit for all melee
    # Fencing: +15% crit for bladed weapons
    # Aikido: +25% unarmed damage
    # Archery: +15% hit/crit if using arrows (requires weapon tag)
    # Thai Kick Boxing: +50% kick damage (and lore note about cyberwear ignored for MVP)
    if tags:
        if attack_type == "melee" and tags.get("Melee Training"):
            crit_chance += 0.05
        if tags.get("Fencing") and subtype in ("sharp","slice"):
            crit_chance += 0.15
        if tags.get("Aikido") and subtype in ("unarmed","kick"):
            dmg *= 1.25
        if tags.get("Archery") and attack_type == "ranged" and status.get("_weapon_arrows", False):
            hit_chance += 0.15
            crit_chance += 0.15
        
        if tags.get("Thai Kick Boxing") and subtype == "kick":
            dmg *= 1.50

    # Clamp probabilities
    hit_chance = clamp01(hit_chance)
    crit_chance = 0.0 if flags["disable_crit"] else clamp01(crit_chance)

    return dmg, hit_chance, crit_chance, crit_mult, flags, procs


# ----------------------------- Public API -----------------------------

def compute_damage(attributes: Dict[str, Any],
                   tags: Dict[str, Any],
                   cybermods: Dict[str, list],
                   weapon: Dict[str, Any],
                   status: Dict[str, Any]) -> str:
    """
    Calculate a single attack result string, suitable for UI display.
    """
    attack_type, subtype = detect_attack_category(weapon)

    if "smart" in weapon and "_weapon_smart" not in status:
        status["_weapon_smart"] = bool(weapon["smart"])
    if "arrows" in weapon and "_weapon_arrows" not in status:
        status["_weapon_arrows"] = bool(weapon.get("arrows"))
    if weapon.get("first"):
        status["attacking_first"] = True
        status["is_first_turn"] = True
    if weapon.get("always_crit"):
        status["_force_crit"] = True
    if weapon.get("returned"):
        status["_returned_attack"] = True


    technical = float(attributes.get("Technical Ability", attributes.get("Technical", 10)))
    skill = float(attributes.get("Skill", 10))
    base_hit = base_hit_chance(attack_type, technical, skill)
    base_crit = base_crit_chance(skill)
    crit_mult = melee_crit_multiplier(skill) if attack_type == "melee" else ranged_crit_multiplier(technical)

    base_dmg = base_damage_formula(subtype, attributes, weapon, tags)
    base_dmg = ceil1(base_dmg)  

    dmg, hit_chance, crit_chance, crit_mult, flags, procs = apply_cybermods_to_numbers(
        dmg=base_dmg,
        hit_chance=base_hit,
        crit_chance=base_crit,
        crit_mult=crit_mult,
        attack_type=attack_type,
        subtype=subtype,
        attrs=attributes,
        status=status,
        cybermods=cybermods or {},
        tags=tags or {}
    )
    roll_hit = random.random() <= hit_chance
    did_crit = False
    if roll_hit:
        if flags.get("force_crit", False):
            did_crit = True
        else:
            did_crit = (random.random() <= crit_chance) and not flags.get("disable_crit", False)
    final_dmg = dmg
    if not roll_hit:
        final_dmg = 0.0
    else:
        if flags.get("force_max_roll", False):
            final_dmg = math.ceil(final_dmg)
        if did_crit:
            final_dmg = final_dmg * crit_mult

    final_dmg = ceil1(final_dmg)

    lines = []
    lines.append(f"Attack: {subtype.upper()} ({attack_type})")
    lines.append(f"Base Damage: {base_dmg}")
    lines.append(f"Hit Chance: {int(hit_chance*100)}%  |  Crit Chance: {int(crit_chance*100)}%  |  Crit Mult: x{crit_mult:.2f}")

    if not roll_hit:
        lines.append("Result: MISS")
    else:
        if did_crit:
            lines.append(f"Result: CRITICAL HIT — Damage {final_dmg}")
        else:
            lines.append(f"Result: HIT — Damage {final_dmg}")

    if roll_hit and did_crit:
        for p in procs:
            if "on_crit_heal" in p:
                lines.append(f"Proc: Feedback Circuit — Heal +{p['on_crit_heal']} HP")

    return "\n".join(lines)