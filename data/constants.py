TAG_DESCRIPTIONS = {
    "Aikido": "+25% Unarmed damage.",
    "Animal Kung Fu": "15% chance to cause Stun (Unarmed).",
    "Archery": "+15% hit/crit if using arrows.",
    "Boxing": "+10 Body for Unarmed.",
    "Brawling": "+10 Reflexes for Unarmed.",
    "Capoeria": "20% chance to cause Confuse (Unarmed).",
    "Choi Li Fut": "Adds 'Pure damage' text (Unarmed).",
    "Fencing": "+15% crit for all bladed weapons.",
    "Judo": "25% chance to cause Taunt (Unarmed).",
    "Karate": "Special future-based modifier.",
    "Melee Training": "+5% crit for all melee.",
    "Tae Kwon Do": "Prefix 'Surprise'. Shows full formula.",
    "Thai Kick Boxing": "Enables kick damage type; +50% damage, doesn't use cyberwear.",
    "Wrestling": "Enables grappling damage type; may stun the enemy."
}

STATUS_EFFECTS = [
    "Blind",
    "Confuse",
    "Slow",
    "Focus",
    "Drenched"
]

CYBERMODS = {
    "Frontal Cortex": {
        "slots": 3,
        "mods": [
            {
            "id": "ex-disk",
            "name": "Ex-Disk",
            "desc": "+7 Intelligence.",
            "effects": {"int_add": 7},
            "on_roll": 2
        },
        {
            "id": "camillo-ram-manager",
            "name": "Camillo RAM Manager",
            "desc": "Reroll one failed quickhack per battle.",
            "effects": {"reroll_quickhack": 1},
            "on_roll": 1
        },
        {
            "id": "cerebral-coordinator",
            "name": "Cerebral Coordinator",
            "desc": "Instantly recharge a use of operating system, once per battle.",
            "effects": {"recharge_operating_system": 1, "uses_per_battle": 1},
            "on_roll": 3
        },
        {
            "id": "limbic-system-enchancement",
            "name": "Limbic System Enchancement",
            "desc": "Reroll a perfomance check, once per session, increase performance by 2.",
            "effects": {"reroll_performance": 1, "performance_add": 2, "uses_per_session": 1},
            "on_roll": 4
        },
        {
            "id" : "kerenzikov-boost-system",
            "name": "Kerenzikov Boost System",
            "desc": "Increases reflexes by 3. If Kerenzikov is on the player, additionally grant a 5% dodge chance",
            "effects": {"reflexes_add": 3, "dodge_add": 5},
            "on_roll": 5
        },
        {
            "id" : "bioconductor",
            "name": "Bioconductor",
            "desc": "Allows quickhacks to deal critical damage, with a default crit chance of 20%",
            "effects": {"quickhack_crit_yes": 1, "default_quickhack_crit": 20},
            "on_roll": 6
        },
        {
            "id": "ram-upgrade",
            "name": "RAM Upgrade",
            "desc": "Increases RAM by 1. Increases intelligence by 3.",
            "effects": {"ram_add": 1 ,"int_add": 3},
            "on_roll": 7  
        },
        {
            "id": "self-ice",
            "name": "Self-ICE",
            "desc": "Completely negates the first status effect inflicted on the player, once per battle",
            "effects": {"status_effect_negate": 1, "uses_per_battle": 1},
            "on_roll": 8
        },
        {
            "id": "visual-cortex-support",
            "name": "Visual Cortex Support",
            "desc": "Reroll a crafting and driving check, once per session",
            "effects": {"craft_reroll": 1, "drive_reroll":1, "uses per_session": 1},
            "on_roll": 9
        },
        {
            "id": "newton-model",
            "name": "Newton Model",
            "desc": "After defeating an enemy, regain 1 RAM",
            "effects": {"regain_ram": 1},
            "on_roll": 10
        }
        ]
    },
    "Ocular System":{
        "slots": 1,
        "mods": [
            {
            "id": "kiroshi-dazzle",
            "name": "Dazzle",
            "desc": "Immune to blind. Increased tolerance by 1.",
            "effects": {"blind_immune":1 ,"tolerance_add": 1},
            "on_roll": 5
        },
        {
            "id": "kiroshi-defunct",
            "name": "Defunct Kiroshi",
            "desc": "Ads constantly! Decreased cool by 2.",
            "effects": {"ads_constantly": 1, "cool_sub": 1},
            "on_roll": 10
        },
        {
            "id": "kiroshi-focus",
            "name": "Focus",
            "desc": "Increases performance by 1. Immune to confuse.",
            "effects": {"performance_add": 1, "confuse_immune": 1},
            "on_roll": 8
        },
        {
            "id": "kiroshi-glare",
            "name": "Glare Resistance",
            "desc": "Increase tolerance by 1. Immune to daze.",
            "effects": {"tolerance_add": 1, "daze_immune": 1},
            "on_roll": 6
        },
        {
            "id" : "kiroshi-icognito",
            "name": "Incognito",
            "desc": "Increase evasion by 1. Reroll an evasion check, once per session.",
            "effects": {"evasion_add": 1, "evasion_reroll": 1, "uses per session": 1},
            "on_roll": 7
        },
        {
            "id" : "kiroshi-kameleon",
            "name": "Kameleon",
            "desc": "Increase appeal by 1. Increase persuasion by 1",
            "effects": {"appeal_add": 1, "persuassion_add": 1},
            "on_roll": 3
        },
        {
            "id": "kiroshi-markdown",
            "name": "Markdown",
            "desc": "Grants trait [Gambler]. Increase luck by 1.",
            "effects": {"gambler_add": 1, "luck_add": 1},
            "on_roll": 9  
        },
        {
            "id": "seethru",
            "name": "SEETHRU_X3",
            "desc": "Increases perception by 1. Reroll a perception check, once per session",
            "effects": {"perception_add": 1, "perception_reroll": 1, "uses per session": 1},
            "on_roll": 2
        },
        {
            "id": "kiroshi-sentry",
            "name": "Sentry",
            "desc": "Increase crafting by 1. Increase driving by 1.",
            "effects": {"crafting_add": 1, "driving_add": 1},
            "on_roll": 1
        },
        {
            "id": "kiroshi-stalker",
            "name": "Stalker",
            "desc": "Increase intimidation by 1. If attacking first, deal 25% more damage on first attack.",
            "effects": {"intimidation_add": 1, "first_attack_add": 25},
            "on_roll": 4
        }
        ]
    },
    "Circulatory System": {
            "slots": 3,
            "mods": [
                {
                "id": "adrenaline-booster",
                "name": "Adrenaline Booster",
                "desc": "Increases the critical hit rate of melee attacks by 10%.",
                "effects": {"crit_rate_add": 10},
                "on_roll": 1
            },
            {
                "id": "clutch-padding",
                "name": "Clutch Padding",
                "desc": "Immune to Bleeding.",
                "effects": {"bleeding_immune": 1},
                "on_roll": 2
            },
            {
                "id": "biomonitor",
                "name": "Biomonitor",
                "desc": "When health is below half, convert RAM regenerated into health, with 1 RAM equalling 20 HP.",
                "effects": {"condition": "hp_below_50", "ram_to_health_rate": 20},
                "on_roll": 3
            },
            {
                "id": "heal-on-kill",
                "name": "Heal-On-Kill",
                "desc": "After defeating an enemy, regenerate 20% of HP.",
                "effects": {"health_on_kill_percentage": 20, "on_final_blow_health_regen_percent": 100},
                "on_roll": 4
            },
            {
                "id" : "blood-pump",
                "name": "Blood Pump",
                "desc": "Regenerate 5% HP per turn.",
                "effects": {"health_regen_rate": 5},
                "on_roll": 5
            },
            {
                "id" : "feedback-circuit",
                "name": "Feedback Circuit",
                "desc": "When dealing a critical hit,, regenerate 10 HP.",
                "effects": {"condition": "crit_landed", "health_points_on_crit": 10},
                "on_roll": 6
            },
            {
                "id": "microrotors",
                "name": "Microrotors",
                "desc": "Reroll one missed attack of choice, once per session",
                "effects": {"reroll_attack": 1, "uses per session": 1},
                "on_roll": 7  
            },
            {
                "id": "second-heart",
                "name": "Second Heart",
                "desc": "When dealt with a fatal blow, HP becomes 1, rather than defeat",
                "effects": {"condition": "attacked_fatal", "lifesaver": 1},
                "on_roll": 8
            },
            {
                "id": "syn-lungs",
                "name": "Syn-Lungs",
                "desc": "Increase body by 7. May outlast one swim check every session.",
                "effects": {"body_add": 7, "swim_check_bypass": 1},
                "on_roll": 9
            },
            {
                "id": "adrenochrome-surge",
                "name": "Adrenochrome Surge",
                "desc": "When health is below 20%, guarantee a critical hit, once per battle",
                "effects": {"condition": "health_below_20", "crit_auto_on_low_hp": 1, "uses_per_battle": 1},
                "on_roll": 10
            }
            ]
        },
    "Nervous System": {
            "slots": 2,
            "mods": [
                {
                "id": "tyrosine-injector",
                "name": "Tyrosine Injector",
                "desc": "Lading a critical hit increases your change to mitigate damage taken from an attack by 40%. This has a 50% chance to occur.",
                "effects": {"condition": "crit_landed", "mitigate_add": 40, "chance_to_occur": 50},
                "on_roll": 1
            },
            {
                "id": "atomic-sensors",
                "name": "Atomic Sensors",
                "desc": "If attacked first at the start of a battle, increases your chance to mitigate damage taken from an attack by 40%. This has a 40% chance to occur.",
                "effects": {"condition": "attacked_first", "mitigate_add": 40, "chance_to_occur": 40 },
                "on_roll": 2
            },
            {
                "id": "nanorelays",
                "name": "Nanorelays",
                "desc": "The first critical hit against you is converted into regular damage.",
                "effects": {"condition": "attacked_crit", "uses_per_battle": 1},
                "on_roll": 3
            },
            {
                "id": "neofiber",
                "name": "NeoFiber",
                "desc": "Grants a chance to mitigate damage taken from an attack by 40%. This has a 15% chance to occur.",
                "effects": {"mitigate_add": 40, "chance_to_occur": 15},
                "on_roll": 4
            },
            {
                "id" : "mood-regulator",
                "name": "Mood Regulator",
                "desc": "+7 cool.",
                "effects": {"cool_add": 7},
                "on_roll": 5
            },
            {
                "id" : "synaptic-accelerator",
                "name": "Synaptic Accelerator",
                "desc": "At the start of a battle, atacks are guaranteed to hit, with a bonus crit chance of 15%",
                "effects": {"condition": "start_of_battle", "attack_chance": 100, "crit_chance_add": 15},
                "on_roll": 6
            },
            {
                "id": "kerenzikov",
                "name": "Kerenzikov",
                "desc": "Gain a 10% chance to dodge attacks.",
                "effects": {"dodge_chance_add": 10},
                "on_roll": 7  
            },
            {
                "id": "stabber",
                "name": "Stabber",
                "desc": "Sharp weapons, including Mantis Blades, gain 10% crit chance.",
                "effects": {"condition": "sharp_weapon", "crit_chance_add": 10},
                "on_roll": 8
            },
            {
                "id": "nanosurgeons",
                "name": "Nanosurgeons",
                "desc": "For every 20% of HP missing, increases your chance to mitigate damage taken by 40%. This has a 4% chance to occur, for every 20% missing.",
                "effects": {"condition": "per_missing_20%_HP", "mitigate_add": 40, "chance_per_stack": 4},
                "on_roll": 9
            },
            {
                "id": "reflex-infusor",
                "name": "Reflex Infusor",
                "desc": "If you are defeated by a melee attack, return one final attack before being defeated. Cannot heal from this state. Once per battle.",
                "effects": {"condition": "defeated_by_melee", "return_final_attack": 1, "uses_per_battle": 1},
                "on_roll": 10
            }
            ]
        },
    "Integumentary System": {
        "slots": 3,
        "mods": [
            {
                "id": "fireproof-coating",
                "name": "Fireproof Coating",
                "desc": "Immune to Burn status effect.",
                "effects": {"burn_immune": 1},
                "on_roll": 1
            },
            {
                "id": "nano-plating",
                "name": "Nano Plating",
                "desc": "Ranged attacks have a 4% chance of deflecting back towards the attacker.",
                "effects": {"chance_to_deflect_ranged_attack": 4},
                "on_roll": 2
            },
            {
                "id": "heat-converter",
                "name": "Heat Converter",
                "desc": "When inflicted with burn, deal 25% more melee damage. Unarmed melee has a chance to inflict burn.",
                "effects": {"condition": "burn_inflicted", "melee_damage_add": 25, "unarmed_melee_burn_chance": 25},
                "on_roll": 3
            },
            {
                "id": "optical-camo",
                "name": "Optical Camo",
                "desc": "+2 evasion.",
                "effects": {"evasion_add": 2},
                "on_roll": 4
            },
            {
                "id": "subdermal-armor",
                "name": "Subdermal Armor",
                "desc": "Increases HP by 15% of Body.",
                "effects": {"hp_add_percentage_of_body": 15},
                "on_roll": 5
            },
            {
                "id": "cellular-adapter",
                "name": "Cellular Adapter",
                "desc": "When damage taken exceeds 100, guarantee the next attack to be critical. Resets after a critical is dealt.",
                "effects": {"condition": "damage_taken_over_100", "crit_auto_next": 1, "resets_after_crit": 1},
                "on_roll": 6
            },
            {
                "id": "em-resistant-coating",
                "name": "Electromagnetic Resistant Coating",
                "desc": "If a quickhack is used against this player, decrease its accuracy by 15%.",
                "effects": {"enemy_quickhack_accuracy_reduce": 15},
                "on_roll": 7
            },
            {
                "id": "pain-editor",
                "name": "Pain Editor",
                "desc": "Immune to Tolerance checks. Morale cannot be lowered through physical means. Immune to Stun. For every Tolerance point, add 5 HP.",
                "effects": {"tolerance_check_immune": 1, "morale_lower_physical_immune": 1, "stun_immune": 1, "hp_per_tolerance": 5},
                "on_roll": 8
            },
            {
                "id": "rangeguard",
                "name": "Rangeguard",
                "desc": "Ranged attacks deal 15% less damage.",
                "effects": {"ranged_damage_taken_reduce": 15},
                "on_roll": 9
            },
            {
                "id": "proxishield",
                "name": "Proxishield",
                "desc": "Melee attacks deal 15% less damage.",
                "effects": {"melee_damage_taken_reduce": 15},
                "on_roll": 10
            }
        ]
    },
    "Skeleton": {
        "slots": 2,
        "mods": [
            {
                "id": "callus-coalescer",
                "name": "Callus Coalescer",
                "desc": "When below 50% HP, melee attack damage is increased by 30%.",
                "effects": {"condition": "hp_below_50%", "melee_damage_add": 30},
                "on_roll": 1
            },
            {
                "id": "bionic-joints",
                "name": "Bionic Joints",
                "desc": "Reduces all damage taken by 10%.",
                "effects": {"damage_taken_reduce": 10},
                "on_roll": 2
            },
            {
                "id": "dense-marrow",
                "name": "Dense Marrow",
                "desc": "+15% Melee Damage.",
                "effects": {"melee_damage_add": 15},
                "on_roll": 3
            },
            {
                "id": "ram-kinetic-converter",
                "name": "RAM Kinetic Converter",
                "desc": "When taking 20% or more damage in a single attack, regenerate one RAM.",
                "effects": {"condition": "damage_taken_over_20%", "ram_regen": 1},
                "on_roll": 4
            },
            {
                "id": "epimorphic-skeleton",
                "name": "Epimorphic Skeleton",
                "desc": "Increase HP by 10%.",
                "effects": {"hp_add_percent": 10},
                "on_roll": 5
            },
            {
                "id": "mechanical-rotary-emulator",
                "name": "Mechanical Rotary Emulator",
                "desc": "+7 Technical Ability.",
                "effects": {"technical_ability_add": 7},
                "on_roll": 6
            },
            {
                "id": "titanium-bones",
                "name": "Titanium Bones",
                "desc": "+7 Strength.",
                "effects": {"strength_add": 7},
                "on_roll": 7
            },
            {
                "id": "feen-x",
                "name": "FEEN-X",
                "desc": "If RAM reaches 0, instantly regenerate one RAM.",
                "effects": {"condition": "ram_reaches_0", "ram_instant_regen": 1},
                "on_roll": 8
            },
            {
                "id": "ram-recoup",
                "name": "RAM Recoup",
                "desc": "On taking damage from an enemy attack, 50% chance to restore 1 extra RAM.",
                "effects": {"condition": "damage_taken", "ram_restore_chance": 50, "ram_restore_amount": 1},
                "on_roll": 9
            },
            {
                "id": "looped-circuitry",
                "name": "Looped Circuitry",
                "desc": "Increase Accuracy by 5% and Crit Rate by 2% for every landed ranged attack. Lasts for three rounds.",
                "effects": {"accuracy_add_per_ranged_hit": 5, "crit_rate_add_per_ranged_hit": 2, "duration_rounds": 3},
                "on_roll": 10
            }
        ]
    },
    "Hands": {
        "slots": 1,
        "mods": [
            {
                "id": "ballistic-coprocessor",
                "name": "Ballistic Coprocessor",
                "desc": "If a shot misses, 50% chance to reroll that shot. Says 'Ricochet hit' upon hit.",
                "effects": {"miss_reroll_chance": 50, "special_text": "Ricochet hit"},
                "on_roll": 1
            },
            {
                "id": "smart-link",
                "name": "Smart Link",
                "desc": "For Smart Ranged Weapons, accuracy defaults to 100% but crit rate drops to 0%.",
                "effects": {"condition": "smart_weapon", "accuracy_set": 100, "crit_rate_set": 0},
                "on_roll": 2
            },
            {
                "id": "pretty-tattoo",
                "name": "Pretty Tattoo",
                "desc": "Increase Intimidation by 1. Adds +1 Hands slot.",
                "effects": {"intimidation_add": 1, "hands_slots_add": 1},
                "on_roll": 3
            },
            {
                "id": "scratchers",
                "name": "Scratchers",
                "desc": "Unarmed damage is increased by 10%. Critical chance for unarmed damage increases by 10%.",
                "effects": {"unarmed_damage_add": 10, "unarmed_crit_rate_add": 10},
                "on_roll": 4
            },
            {
                "id": "rippers",
                "name": "Rippers",
                "desc": "Unarmed damage is increased by 15%. Critical chance for unarmed damage increases by 20%. Requires Gorilla Arms.",
                "effects": {"condition": "requires_gorilla_arms", "unarmed_damage_add": 15, "unarmed_crit_rate_add": 20},
                "on_roll": 5
            },
            {
                "id": "wolvers",
                "name": "Wolvers",
                "desc": "Critical chance for unarmed damage increases by 20%. Crit damage is boosted by 20%. Requires Gorilla Arms.",
                "effects": {"condition": "requires_gorilla_arms", "unarmed_crit_rate_add": 20, "unarmed_crit_damage_add": 20},
                "on_roll": 6
            },
            {
                "id": "big-knucks",
                "name": "Big Knucks",
                "desc": "Unarmed damage calculation is static, can no longer crit, and is always scaled to the attack’s damage ceiling. Requires Gorilla Arms.",
                "effects": {"condition": "requires_gorilla_arms", "unarmed_damage_static": 1, "unarmed_disable_crit": 1, "unarmed_scale_to_ceiling": 1},
                "on_roll": 7
            },
            {
                "id": "slice-n-dice",
                "name": "Slice N’ Dice",
                "desc": "Unarmed damage is increased by 25%. Critical hits for unarmed damage now cause Bleed.",
                "effects": {"unarmed_damage_add": 25, "unarmed_crit_inflict_bleed": 1},
                "on_roll": 8
            },
            {
                "id": "shock-absorber",
                "name": "Shock Absorber",
                "desc": "+10% Accuracy for Ranged attacks.",
                "effects": {"ranged_accuracy_add": 10},
                "on_roll": 9
            },
            {
                "id": "carbon-knuckles",
                "name": "Carbon Knuckles",
                "desc": "Unarmed damage is increased by 25%. Unarmed Critical chance is now 100%.",
                "effects": {"unarmed_damage_add": 25, "unarmed_crit_rate_set": 100},
                "on_roll": 10
            }
        ]
    },  
    "Arms": {
        "slots": 1,
        "mods": [
            {
                "id": "gorilla-arms",
                "name": "Gorilla Arms",
                "desc": "Allows for the use of more Hands cybermods. Increases unarmed damage by 20%. Counts as Unarmed damage.",
                "effects": {
                    "has_gorilla_arms": 1, "unarmed_damage_add": 20, "counts_as_unarmed": 1},
                "on_roll": 1
            },
            {
                "id": "mantis-blades",
                "name": "Mantis Blades",
                "desc": "Creates a new attack called 'Slice'. 'Slice' scales off of Cool more than regular attacks.",
                "effects": {
                    "grants_attack": {
                        "id": "slice",
                        "name": "Slice",
                        "type": "melee",
                        "scales_with": "cool"
                    }
                },
                "on_roll": 2
            },
            {
                "id": "monowire",
                "name": "Monowire",
                "desc": "Creates a new attack called 'Whip'. 'Whip' scales off of Intelligence rather than Body.",
                "effects": {
                    "grants_attack": {
                        "id": "whip",
                        "name": "Whip",
                        "type": "melee",
                        "scales_with": "intelligence"
                    }
                },
                "on_roll": 3
            },
            {
                "id": "projectile-launch-system",
                "name": "Projectile Launch System",
                "desc": "Creates a new attack called 'Blast'. 'Blast' is a ranged attack that deals damage based off Technical Ability.",
                "effects": {
                    "grants_attack": {
                        "id": "blast",
                        "name": "Blast",
                        "type": "ranged",
                        "scales_with": "technical_ability"
                    }
                },
                "on_roll": 4
            },
            {
                "id": "hidden-compartment-arms",
                "name": "Hidden Compartment",
                "desc": "Can be used to store special items.",
                "effects": {
                    "hidden_compartment": 1
                },
                "on_roll": 5
            }
        ]
    },
    "Legs": {
        "slots": 1,
        "mods": [
            {
                "id": "razor-ankles",
                "name": "Razor Ankles",
                "desc": "Grants the wearer the ability to 'Kick', doubling the damage of standard unarmed melee attacks.",
                "effects": {
                    "grants_attack": {
                        "id": "kick",
                        "name": "Kick",
                        "type": "melee",
                        "scales_with": "unarmed",
                        "damage_multiplier": 2
                    }
                },
                "on_roll": 1
            },
            {
                "id": "fortified-ankles",
                "name": "Fortified Ankles",
                "desc": "Increases Reflexes by 7 points.",
                "effects": {"reflex_add": 7},
                "on_roll": 2
            },
            {
                "id": "lynx-paws",
                "name": "Lynx Paws",
                "desc": "If attacking first in combat, damage increases by 50%.",
                "effects": {
                    "condition": "first_strike",
                    "damage_add_percent": 50
                },
                "on_roll": 3
            },
            {
                "id": "reinforced-tendons",
                "name": "Reinforced Tendons",
                "desc": "Increases Skill by 7 points.",
                "effects": {"skill_add": 7},
                "on_roll": 4
            },
            {
                "id": "hidden-compartment-legs",
                "name": "Hidden Compartment",
                "desc": "Can be used to store special items.",
                "effects": {"hidden_compartment": 1},
                "on_roll": 5
            }
        ]
},
#I FORGOT OPERATING SYSTEMS!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    "Operating System": {
        "slots": 1,
        "mods": [
            {
                "id": "chrome-compressor",
                "name": "Chrome Compressor",
                "desc": "Ignore up to three Cyberpsychosis checks. If the player has Cyberpsychosis, increase Willpower during checks.",
                "base_effects": {"ignore_psychosis_checks": 3},
                "tiers": {
                    1: {"willpower_add_on_psychosis": 25},
                    2: {"willpower_add_on_psychosis": 30},
                    3: {"willpower_add_on_psychosis": 35},
                    4: {"willpower_add_on_psychosis": 40},
                    5: {"psychosis_immunity": 1}
                },
                "on_roll": 1
            },
            {
                "id": "berserk",
                "name": "Berserk",
                "desc": "Once per battle, reroll an attack (even if it is missed) to be a critical hit. Adds bonus damage depending on tier.",
                "base_effects": {"crit_reroll_once_per_battle": 1},
                "tiers": {
                    1: {"damage_add_percent": 20},
                    2: {"damage_add_percent": 25},
                    3: {"damage_add_percent": 30},
                    4: {"damage_add_percent": 35},
                    5: {"damage_add_percent": 50}
                },
                "on_roll": 2
            },
            {
                "id": "cyberdeck",
                "name": "Cyberdeck",
                "desc": "Allows the user to manipulate technology and use Quickhacks. Higher tiers increase base RAM.",
                "base_effects": {"quickhack_enabled": 1},
                "tiers": {
                    1: {"ram_add": 2},
                    2: {"ram_add": 3},
                    3: {"ram_add": 4},
                    4: {"ram_add": 5},
                    5: {"ram_add": 6}
                },
                "on_roll": 3
            },
            {
                "id": "sandevistan",
                "name": "Sandevistan",
                "desc": "Time-dilation OS: allows multiple actions on a cooldown. Tiers adjust cooldown and number of actions.",
                "base_effects": {"time_dilation": 1},
                "tiers": {
                    1: {"actions_bonus": 2, "cooldown_turns": 7},
                    2: {"actions_bonus": 2, "cooldown_turns": 6},
                    3: {"actions_bonus": 2, "cooldown_turns": 5},
                    4: {"actions_bonus": 2, "cooldown_turns": 4},
                    "5A": {"actions_bonus": 3, "cooldown_turns": 4},
                    "5B": {"actions_bonus": 2, "cooldown_turns": 3}
                },
                "on_roll": 4
            }
        ]
    }

}