import random
# TODO: Add support for Arms, Skeleton, and other body mod slots

def compute_damage(attributes, tags, hand_mods, weapon, status):
    result_lines = []
    primary_mod, secondary_mod = hand_mods

    # Extract inputs
    body = attributes["Body"]
    willpower = attributes["Willpower"]
    cool = attributes["Cool"]
    intelligence = attributes["Intelligence"]
    reflexes = attributes["Reflexes"]
    skill = attributes["Skill"]
    technical = attributes["Technical Ability"]

    weapon_type = weapon["type"]
    weapon_damage = weapon["damage"]
    smart_weapon = weapon["smart"]
    uses_arrows = weapon["arrows"]
    always_crit = weapon["always_crit"]
    returned = weapon["returned"]
    first = weapon["first"]

    # Handle status effects
    if status.get("Slow"):
        reflexes = max(10, reflexes // 2)
    if status.get("Drenched"):
        cool = max(10, cool - 5)

    # Pretty Tattoo mod bonus
    if primary_mod == "Pretty Tattoo":
        cool += 3

    # Tag-based stat boosts
    if tags.get("Brawling") and weapon_type == "Unarmed Melee":
        reflexes += 10
    if tags.get("Boxing") and weapon_type == "Unarmed Melee":
        body += 10

    # Bonuses
    crit_bonus = 0
    hit_bonus = 0
    damage_multiplier = 1.0
    crit_multiplier = 0.0
    inflicts_bleed = False
    inflicts_burn = False
    inflicts_stun = False

    # Cyber Mod logic
    if primary_mod == "Ballistic Coprocessor":
        hit_bonus += 0.15
        crit_bonus += 0.05
    elif primary_mod == "Smart Link" and smart_weapon:
        hit_bonus = 1.0
    elif primary_mod == "Scratchers" and weapon_type == "Unarmed Melee":
        damage_multiplier += 0.10
        crit_bonus += 0.10
    elif primary_mod == "Rippers" and weapon_type == "Unarmed Melee":
        damage_multiplier += 0.20
        crit_bonus += 0.20
    elif primary_mod == "Wolvers" and weapon_type == "Unarmed Melee":
        crit_bonus += 0.20
        crit_multiplier += 0.20
    elif primary_mod == "Big Knucks" and weapon_type == "Unarmed Melee":
        crit_bonus = 0.0
        damage_multiplier = 1.0
    elif primary_mod == "Slice N' Dice" and weapon_type == "Unarmed Melee":
        damage_multiplier += 0.25
        inflicts_bleed = True
    elif primary_mod == "Heatsaw Hands" and weapon_type == "Unarmed Melee":
        damage_multiplier += 0.25
        inflicts_burn = True
    elif primary_mod == "Carbon Knuckles" and weapon_type == "Unarmed Melee":
        damage_multiplier += 0.25
        crit_bonus = 1.0

    # Tag logic
    if tags.get("Archery") and uses_arrows:
        hit_bonus += 0.15
        crit_bonus += 0.15
    if tags.get("Melee Training") and weapon_type in ["Unarmed Melee", "Blunt Weapon Melee", "Sharp Weapon Melee"]:
        crit_bonus += 0.05
    if tags.get("Aikido") and weapon_type == "Unarmed Melee":
        damage_multiplier += 0.25
    if tags.get("Fencing") and weapon_type == "Sharp Weapon Melee":
        crit_bonus += 0.15
    if tags.get("Karate") and returned:
        hit_bonus += 0.20
    if tags.get("Tae Kwon Do") and first:
        hit_bonus += 0.50

    # Roll and calculate base damage
    skill_rand = random.randint(skill, cool + 50)

    if weapon_type == "Unarmed Melee":
        base = (body / 10 + cool / 5 + reflexes * (0.01 * skill_rand) + 0.75)
    elif weapon_type == "Blunt Weapon Melee":
        base = (body / 8 + cool / 5 + reflexes * (0.01 * skill_rand) + 0.75) * (weapon_damage * 0.01)
    elif weapon_type == "Sharp Weapon Melee":
        base = (body / 10 + cool / 4 + reflexes * (0.01 * skill_rand) + 0.75) * (weapon_damage * 0.01)
    elif weapon_type == "Ranged Attack":
        base = intelligence / 2 + reflexes / 10 + (weapon_damage * 0.01 * (skill_rand / 100))
    elif weapon_type == "Kick":
        if not tags.get("Thai Kick Boxing"):
            return "*Invalid: Kick requires Thai Kick Boxing*\n"
        base = (body / 10 + cool / 5 + reflexes * (0.01 * skill_rand) + 0.75) * 1.5
    elif weapon_type == "Grappling":
        if not tags.get("Wrestling"):
            return "*Invalid: Grappling requires Wrestling*\n"
        if random.random() > 0.75:
            return "*Grapple failed! You are stunned.*\n"
        base = (body / 10 + cool / 5 + reflexes * (0.01 * skill_rand) + 0.75) * 1.5
        inflicts_stun = True
    else:
        return "*Invalid weapon type selected*\n"

    base *= damage_multiplier

    # Focus reroll
    if status.get("Focus"):
        alt_skill_rand = random.randint(skill, cool + 50)
        reroll = base  # placeholder
        if weapon_type == "Unarmed Melee":
            reroll = (body / 10 + cool / 5 + reflexes * (0.01 * alt_skill_rand) + 0.75)
        elif weapon_type == "Blunt Weapon Melee":
            reroll = (body / 8 + cool / 5 + reflexes * (0.01 * alt_skill_rand) + 0.75) * (weapon_damage * 0.01)
        elif weapon_type == "Sharp Weapon Melee":
            reroll = (body / 10 + cool / 4 + reflexes * (0.01 * alt_skill_rand) + 0.75) * (weapon_damage * 0.01)
        elif weapon_type == "Ranged Attack":
            reroll = intelligence / 2 + reflexes / 10 + (weapon_damage * 0.01 * (alt_skill_rand / 100))

        reroll *= damage_multiplier
        if reroll > base:
            result_lines.append(f"Focus Reroll Activated!\nOld Damage: {round(base, 2)}\nNew Damage: {round(reroll, 2)}\n")
            base = reroll

    hit_chance = 1.0 if weapon_type != "Ranged Attack" else min(1.0, ((technical / 2 + skill / 2) * 0.01) + 0.47 + hit_bonus)
    crit_chance = 1.0 if always_crit else min(1.0, skill * 0.01 + 0.03 + crit_bonus)

    is_hit = weapon_type != "Ranged Attack" or random.random() < hit_chance
    is_crit = always_crit or random.random() < crit_chance

    if not is_hit:
        return "*Missed Attack*\n"

    if is_crit:
        if weapon_type == "Unarmed Melee" and primary_mod == "Big Knucks":
            pass
        elif weapon_type == "Ranged Attack":
            base *= (1 + 0.35 + technical * 0.01 + crit_multiplier)
        else:
            base *= (1 + 0.20 + skill * 0.01 + crit_multiplier)

    final_damage = int(base)
    status_lines = []

    if tags.get("Tae Kwon Do") and weapon_type == "Unarmed Melee":
        result_lines.append(f"Surprise Result: {final_damage} (Formula used with bonus)\n")
    else:
        if tags.get("Choi Li Fut") and weapon_type == "Unarmed Melee":
            result_lines.append(f"{final_damage} Pure damage\n")
        else:
            result_lines.append(f"{final_damage}{' (CRIT)' if is_crit else ''}\n")

        if tags.get("Animal Kung Fu") and weapon_type == "Unarmed Melee" and random.random() < 0.15:
            status_lines.append("Status Effect: Stun")
        if tags.get("Capoeria") and weapon_type == "Unarmed Melee" and random.random() < 0.20:
            status_lines.append("Status Effect: Confuse")
        if tags.get("Judo") and weapon_type == "Unarmed Melee" and random.random() < 0.25:
            status_lines.append("Status Effect: Taunt")
        if inflicts_bleed:
            status_lines.append("Status Effect: Bleed")
        if inflicts_burn:
            status_lines.append("Status Effect: Burn")
        if inflicts_stun:
            status_lines.append("Status Effect: Stun")

    return "\n".join(result_lines + status_lines)
