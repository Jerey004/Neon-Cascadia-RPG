"""Tiered item database - now with class affinities and detailed gear stats.

Tiers (1=junk, 6=legendary). All gear has detailed stats:

WEAPONS:        damage, accuracy_mod, crit_mod, weight, ranged
ARMOR:          defense, agility_mod, perception_mod, weight, slot
CYBERWARE:      stat (which stat), bonus, slot (which body part)
CONSUMABLES:    heal, duration, stat_buffs

Each item can have:
- skill_mods:     {skill: bonus}      # active when equipped/installed
- class_affinity: [class_id, ...]    # which classes can use it best
- requires_skill: {skill: min_level} # prereq to use
"""

ITEMS = {

    # ==========================================================
    # TIER 1 - JUNK
    # ==========================================================

    # --- WEAPONS T1 ---
    "rusty_pipe": {
        "type": "weapon", "tier": 1, "value": 15,
        "damage": 8, "accuracy_mod": 0, "crit_mod": 0, "weight": 3,
        "desc": "A length of rebar. Crude but it'll cave a skull.",
    },
    "broken_bottle": {
        "type": "weapon", "tier": 1, "value": 5,
        "damage": 5, "accuracy_mod": -1, "crit_mod": 1, "weight": 1,
        "desc": "Jagged glass. Sharp edge, fragile.",
    },
    "wrench": {
        "type": "weapon", "tier": 1, "value": 12,
        "damage": 7, "accuracy_mod": 0, "crit_mod": 0, "weight": 2,
        "desc": "Standard mechanic's wrench. Heavy, blunt.",
        "skill_mods": {"tech_repair": 1},
        "class_affinity": ["tech"],
    },
    "scalpel": {
        "type": "weapon", "tier": 1, "value": 18,
        "damage": 6, "accuracy_mod": 2, "crit_mod": 2, "weight": 0,
        "desc": "Surgical steel. Tiny but precise.",
        "skill_mods": {"first_aid": 1},
        "class_affinity": ["medic"],
    },
    "old_revolver": {
        "type": "weapon", "tier": 1, "value": 35, "ranged": True,
        "damage": 12, "accuracy_mod": -2, "crit_mod": 1, "weight": 2,
        "desc": "Six shots, rusted barrel. Might explode.",
    },

    # --- ARMOR T1 ---
    "rags": {
        "type": "armor", "tier": 1, "value": 5, "slot": "body",
        "defense": 1, "agility_mod": 0, "perception_mod": 0, "weight": 1,
        "desc": "Layered cloth. Better than nothing. Barely.",
    },
    "hoodie": {
        "type": "armor", "tier": 1, "value": 15, "slot": "body",
        "defense": 2, "agility_mod": 0, "perception_mod": 0, "weight": 1,
        "desc": "A hood hides your face. Civilian wear.",
        "skill_mods": {"stealth": 1},
    },
    "work_gloves": {
        "type": "armor", "tier": 1, "value": 10, "slot": "hands",
        "defense": 1, "agility_mod": 0, "weight": 0,
        "desc": "Old leather work gloves.",
        "skill_mods": {"tech_repair": 1},
        "class_affinity": ["tech"],
    },

    # --- CONSUMABLES T1 ---
    "ration_pack": {
        "type": "consumable", "tier": 1, "value": 8,
        "heal": 15, "duration": 0,
        "desc": "Synth-protein bar. Tastes like wet cardboard.",
    },
    "synth_coffee": {
        "type": "consumable", "tier": 1, "value": 4,
        "heal": 5, "duration": 0,
        "desc": "Hot. Bitter. Caffeine kicks like a mule.",
    },
    "cheap_painkillers": {
        "type": "consumable", "tier": 1, "value": 6,
        "heal": 10, "duration": 0,
        "desc": "Generic synth-opioids. Take with food.",
    },

    # --- MISC T1 ---
    "scrap_metal": {
        "type": "misc", "tier": 1, "value": 8,
        "desc": "Salvageable scrap. Sells to scavengers.",
    },
    "smokes": {
        "type": "misc", "tier": 1, "value": 12,
        "desc": "Pack of synth-cigarettes. Useful for trading.",
    },
    "data_chip_corrupted": {
        "type": "misc", "tier": 1, "value": 10,
        "desc": "Damaged data shard. Hackers might want it.",
    },


    # ==========================================================
    # TIER 2 - COMMON
    # ==========================================================

    # --- WEAPONS T2 (combat-focused) ---
    "crowbar": {
        "type": "weapon", "tier": 2, "value": 30,
        "damage": 12, "accuracy_mod": 0, "crit_mod": 1, "weight": 4,
        "desc": "Heavy steel. Doubles for breaking and entering.",
        "skill_mods": {"engineering": 1},
    },
    "switchblade": {
        "type": "weapon", "tier": 2, "value": 25,
        "damage": 10, "accuracy_mod": 1, "crit_mod": 2, "weight": 0,
        "desc": "Quick. Quiet. Concealable.",
        "skill_mods": {"stealth": 1},
    },
    "cheap_pistol": {
        "type": "weapon", "tier": 2, "value": 80, "ranged": True,
        "damage": 18, "accuracy_mod": 0, "crit_mod": 1, "weight": 1,
        "desc": "Plastic-frame 9mm. Untraceable. Probably.",
    },
    "shock_baton": {
        "type": "weapon", "tier": 2, "value": 95,
        "damage": 13, "accuracy_mod": 0, "crit_mod": 0, "weight": 2,
        "desc": "Low-amp stun rod. Police academy issue.",
        "skill_mods": {"intimidation": 1},
    },

    # --- WEAPONS T2 (class-specific) ---
    "pocket_jammer": {
        "type": "weapon", "tier": 2, "value": 75,
        "damage": 6, "accuracy_mod": 0, "crit_mod": 0, "weight": 1,
        "desc": "Disrupts cyberware on hit. Useless against unmodded.",
        "skill_mods": {"hacking": 2},
        "class_affinity": ["netrunner", "tech"],
    },
    "med_injector": {
        "type": "weapon", "tier": 2, "value": 65,
        "damage": 8, "accuracy_mod": 1, "crit_mod": 0, "weight": 1,
        "desc": "Combat injector. Can fire stims OR poison.",
        "skill_mods": {"first_aid": 2, "biology": 1},
        "class_affinity": ["medic"],
    },
    "negotiator_revolver": {
        "type": "weapon", "tier": 2, "value": 110, "ranged": True,
        "damage": 16, "accuracy_mod": 1, "crit_mod": 2, "weight": 2,
        "desc": "Engraved. Beautiful. People respect it.",
        "skill_mods": {"intimidation": 2, "persuasion": 1},
        "class_affinity": ["fixer"],
    },

    # --- ARMOR T2 ---
    "leather_jacket": {
        "type": "armor", "tier": 2, "value": 40, "slot": "body",
        "defense": 3, "agility_mod": 0, "perception_mod": 0, "weight": 2,
        "desc": "Worn synth-leather. Stops a knife. Maybe.",
        "skill_mods": {"intimidation": 1},
    },
    "padded_vest": {
        "type": "armor", "tier": 2, "value": 60, "slot": "body",
        "defense": 4, "agility_mod": -1, "perception_mod": 0, "weight": 3,
        "desc": "Cheap kevlar substitute. Bulky.",
    },
    "running_boots": {
        "type": "armor", "tier": 2, "value": 35, "slot": "feet",
        "defense": 1, "agility_mod": 1, "weight": 1,
        "desc": "Light, grippy. Made for moving.",
        "skill_mods": {"stealth": 1},
    },
    "tactical_gloves": {
        "type": "armor", "tier": 2, "value": 30, "slot": "hands",
        "defense": 1, "agility_mod": 0, "weight": 0,
        "desc": "Reinforced knuckles. Subtle.",
        "skill_mods": {"combat": 1},
    },
    "doctor_coat": {
        "type": "armor", "tier": 2, "value": 50, "slot": "body",
        "defense": 2, "agility_mod": 0, "weight": 1,
        "desc": "White medical coat. Many pockets.",
        "skill_mods": {"first_aid": 2},
        "class_affinity": ["medic"],
    },
    "hacker_visor": {
        "type": "armor", "tier": 2, "value": 80, "slot": "head",
        "defense": 1, "perception_mod": 1, "weight": 0,
        "desc": "AR visor. Shows data streams.",
        "skill_mods": {"hacking": 2, "perception": 1},
        "class_affinity": ["netrunner"],
    },

    # --- CONSUMABLES T2 ---
    "stim_pack": {
        "type": "consumable", "tier": 2, "value": 35,
        "heal": 40, "duration": 0,
        "desc": "Combat med-stim. Burns going in.",
    },
    "adrenaline_shot": {
        "type": "consumable", "tier": 2, "value": 50,
        "heal": 25, "duration": 3, "stat_buffs": {"agility": 2},
        "desc": "Pure adrenaline. Speeds you up for 3 turns.",
    },
    "mem_booster": {
        "type": "consumable", "tier": 2, "value": 45,
        "heal": 0, "duration": 5, "stat_buffs": {"tech": 2},
        "desc": "Cognitive enhancer. Sharpens the mind for a while.",
    },

    # --- CYBERWARE T2 ---
    "neural_jack": {
        "type": "cyberware", "tier": 2, "value": 250, "slot": "head",
        "stat": "tech", "bonus": 2, "weight": 0,
        "desc": "Standard data port. Plug into the net.",
        "skill_mods": {"hacking": 2},
    },
    "muscle_grafts": {
        "type": "cyberware", "tier": 2, "value": 200, "slot": "arms",
        "stat": "strength", "bonus": 2, "weight": 0,
        "desc": "Synthetic muscle weave. Strong but slow.",
        "skill_mods": {"combat": 1, "intimidation": 1},
    },
    "low_light_lenses": {
        "type": "cyberware", "tier": 2, "value": 220, "slot": "eyes",
        "stat": "perception", "bonus": 2, "weight": 0,
        "desc": "Night vision implant.",
        "skill_mods": {"stealth": 1, "perception": 1},
    },

    # --- MISC T2 ---
    "transit_card": {
        "type": "misc", "tier": 2, "value": 25,
        "desc": "Magrail transit pass.",
    },
    "credstick": {
        "type": "misc", "tier": 2, "value": 100,
        "desc": "Anonymous credit chip.",
    },


    # ==========================================================
    # TIER 3 - UNCOMMON
    # ==========================================================

    # --- WEAPONS T3 ---
    "stun_baton": {
        "type": "weapon", "tier": 3, "value": 120,
        "damage": 15, "accuracy_mod": 0, "crit_mod": 1, "weight": 2, "stun": True,
        "desc": "OmniCorp issue. Disables cyberware on hit.",
        "skill_mods": {"intimidation": 2},
    },
    "tactical_smg": {
        "type": "weapon", "tier": 3, "value": 180, "ranged": True,
        "damage": 22, "accuracy_mod": 1, "crit_mod": 1, "weight": 3,
        "desc": "Compact submachine gun. Reliable spray.",
        "skill_mods": {"combat": 1},
    },
    "combat_shotgun": {
        "type": "weapon", "tier": 3, "value": 220, "ranged": True,
        "damage": 30, "accuracy_mod": -2, "crit_mod": 2, "weight": 5,
        "desc": "Pump-action. Up close, devastating.",
        "skill_mods": {"combat": 1, "intimidation": 2},
    },
    "ice_pick": {
        "type": "weapon", "tier": 3, "value": 175,
        "damage": 18, "accuracy_mod": 2, "crit_mod": 3, "weight": 1,
        "desc": "Mono-edged. Slips between ribs.",
        "skill_mods": {"stealth": 2, "combat": 1},
    },

    # --- WEAPONS T3 class-specific ---
    "ripper_blade": {
        "type": "weapon", "tier": 3, "value": 195,
        "damage": 24, "accuracy_mod": 1, "crit_mod": 2, "weight": 2,
        "desc": "Surgical steel. Made for the operating table. Or the throat.",
        "skill_mods": {"combat": 2, "first_aid": 1},
        "class_affinity": ["medic", "street_samurai"],
    },
    "ice_breaker_rig": {
        "type": "weapon", "tier": 3, "value": 240,
        "damage": 12, "accuracy_mod": 2, "crit_mod": 0, "weight": 1, "ranged": True,
        "desc": "Portable ICE breaker. Fries cyberware AND people.",
        "skill_mods": {"hacking": 3, "tech_repair": 1},
        "class_affinity": ["netrunner", "tech"],
    },
    "deal_maker_glock": {
        "type": "weapon", "tier": 3, "value": 250, "ranged": True,
        "damage": 25, "accuracy_mod": 1, "crit_mod": 1, "weight": 1,
        "desc": "Gold-plated. Fixer's signature.",
        "skill_mods": {"intimidation": 3, "combat": 1, "persuasion": 1},
        "class_affinity": ["fixer"],
    },

    # --- ARMOR T3 ---
    "kevlar_vest": {
        "type": "armor", "tier": 3, "value": 200, "slot": "body",
        "defense": 8, "agility_mod": -1, "perception_mod": 0, "weight": 4,
        "desc": "Police surplus. Stops most pistol rounds.",
    },
    "tactical_visor": {
        "type": "armor", "tier": 3, "value": 150, "slot": "head",
        "defense": 2, "perception_mod": 2, "weight": 1,
        "desc": "HUD overlay. Threat highlighting.",
        "skill_mods": {"perception": 2, "combat": 1},
    },
    "stealth_suit": {
        "type": "armor", "tier": 3, "value": 280, "slot": "body",
        "defense": 4, "agility_mod": 2, "weight": 1,
        "desc": "Light-bending fabric. Whispers when you move.",
        "skill_mods": {"stealth": 3},
        "class_affinity": ["netrunner", "fixer"],
    },
    "med_apron": {
        "type": "armor", "tier": 3, "value": 175, "slot": "body",
        "defense": 5, "agility_mod": 0, "weight": 2,
        "desc": "Reinforced surgical apron. Pockets for vials.",
        "skill_mods": {"first_aid": 3, "biology": 1},
        "class_affinity": ["medic"],
    },
    "combat_boots": {
        "type": "armor", "tier": 3, "value": 120, "slot": "feet",
        "defense": 3, "agility_mod": 0, "weight": 2,
        "desc": "Steel-toed. Mil-spec. Solid.",
        "skill_mods": {"combat": 1, "intimidation": 1},
    },
    "armored_gloves": {
        "type": "armor", "tier": 3, "value": 110, "slot": "hands",
        "defense": 2, "agility_mod": 0, "weight": 1,
        "desc": "Plated knuckle guards. Punches HURT.",
        "skill_mods": {"combat": 2},
    },

    # --- CONSUMABLES T3 ---
    "trauma_kit": {
        "type": "consumable", "tier": 3, "value": 120,
        "heal": 80, "duration": 0,
        "desc": "Full-spectrum medical. Saves lives.",
    },
    "combat_stim": {
        "type": "consumable", "tier": 3, "value": 95,
        "heal": 30, "duration": 4, "stat_buffs": {"strength": 2, "agility": 1},
        "desc": "Battlefield cocktail. Side effects: aggression.",
    },
    "neural_clarifier": {
        "type": "consumable", "tier": 3, "value": 110,
        "heal": 0, "duration": 6, "stat_buffs": {"tech": 3, "perception": 2},
        "desc": "Hacker's drug of choice. The wires SING.",
        "class_affinity": ["netrunner", "tech"],
    },

    # --- CYBERWARE T3 ---
    "cyber_eye": {
        "type": "cyberware", "tier": 3, "value": 400, "slot": "eyes",
        "stat": "perception", "bonus": 3, "weight": 0,
        "desc": "Zoom, IR, threat detection.",
        "skill_mods": {"perception": 3, "combat": 1},
    },
    "smartlink": {
        "type": "cyberware", "tier": 3, "value": 450, "slot": "arms",
        "stat": "agility", "bonus": 2, "weight": 0,
        "desc": "Targeting computer wired to your hands. Aim assist.",
        "skill_mods": {"combat": 3},
        "class_affinity": ["street_samurai"],
    },
    "biomonitor": {
        "type": "cyberware", "tier": 3, "value": 380, "slot": "body",
        "stat": "tech", "bonus": 1, "weight": 0,
        "desc": "Real-time vitals scanner. Reads enemies and allies.",
        "skill_mods": {"first_aid": 3, "biology": 2},
        "class_affinity": ["medic"],
    },
    "social_chip": {
        "type": "cyberware", "tier": 3, "value": 420, "slot": "head",
        "stat": "charisma", "bonus": 3, "weight": 0,
        "desc": "Reads micro-expressions. You see the lies.",
        "skill_mods": {"persuasion": 3, "perception": 1},
        "class_affinity": ["fixer", "ex_corpo"],
    },

    # --- QUEST T3 ---
    "data_shard": {
        "type": "quest", "tier": 3, "value": 0,
        "desc": "Encrypted data crystal. Someone wants this badly.",
    },
    "virus_chip": {
        "type": "consumable", "tier": 3, "value": 80,
        "heal": 0, "hack": True,
        "desc": "One-shot ICE breaker. Single-use.",
    },


    # ==========================================================
    # TIER 4 - RARE
    # ==========================================================

    # --- WEAPONS T4 ---
    "monoblade": {
        "type": "weapon", "tier": 4, "value": 350,
        "damage": 28, "accuracy_mod": 2, "crit_mod": 3, "weight": 1,
        "desc": "Mono-molecular edge. Cuts chrome like butter.",
        "skill_mods": {"combat": 2},
        "class_affinity": ["street_samurai"],
    },
    "smartgun": {
        "type": "weapon", "tier": 4, "value": 800, "ranged": True,
        "damage": 35, "accuracy_mod": 4, "crit_mod": 1, "weight": 3,
        "desc": "Auto-targeting. Links to your neural jack.",
        "skill_mods": {"combat": 3, "perception": 1},
        "requires_skill": {"combat": 3},
    },
    "assault_rifle": {
        "type": "weapon", "tier": 4, "value": 650, "ranged": True,
        "damage": 32, "accuracy_mod": 1, "crit_mod": 1, "weight": 5,
        "desc": "Mil-grade. Heavy. Deals serious damage.",
        "skill_mods": {"combat": 2},
    },
    "scalpel_blade": {
        "type": "weapon", "tier": 4, "value": 380,
        "damage": 22, "accuracy_mod": 3, "crit_mod": 4, "weight": 0,
        "desc": "Anatomical precision. Hits vital organs.",
        "skill_mods": {"first_aid": 3, "biology": 3, "combat": 1},
        "class_affinity": ["medic"],
    },
    "neural_disruptor": {
        "type": "weapon", "tier": 4, "value": 580, "ranged": True,
        "damage": 18, "accuracy_mod": 2, "crit_mod": 0, "weight": 1, "stun": True,
        "desc": "Fries cyberware. Bypasses armor entirely.",
        "skill_mods": {"hacking": 4, "tech_repair": 2},
        "class_affinity": ["netrunner", "tech"],
    },

    # --- ARMOR T4 ---
    "combat_armor": {
        "type": "armor", "tier": 4, "value": 600, "slot": "body",
        "defense": 15, "agility_mod": -2, "perception_mod": 0, "weight": 6,
        "desc": "Mil-spec ablative plates.",
        "skill_mods": {"combat": 1, "intimidation": 2},
    },
    "ghost_cloak": {
        "type": "armor", "tier": 4, "value": 750, "slot": "body",
        "defense": 6, "agility_mod": 3, "weight": 1,
        "desc": "Active camouflage weave. You blur and shimmer.",
        "skill_mods": {"stealth": 4, "perception": -1},
        "class_affinity": ["netrunner", "fixer"],
    },
    "executive_suit": {
        "type": "armor", "tier": 4, "value": 700, "slot": "body",
        "defense": 8, "agility_mod": 0, "weight": 2,
        "desc": "Tailored armor woven into pinstripes. You belong anywhere.",
        "skill_mods": {"persuasion": 3, "intimidation": 2, "corporate_lore": 2},
        "class_affinity": ["ex_corpo", "fixer"],
    },
    "doc_carapace": {
        "type": "armor", "tier": 4, "value": 620, "slot": "body",
        "defense": 9, "agility_mod": 0, "weight": 3,
        "desc": "Trauma-rated medical armor. Self-sealing punctures.",
        "skill_mods": {"first_aid": 4, "biology": 2},
        "class_affinity": ["medic"],
    },
    "smart_helmet": {
        "type": "armor", "tier": 4, "value": 480, "slot": "head",
        "defense": 6, "perception_mod": 3, "weight": 2,
        "desc": "Full-face HUD. Threat tracking, comms, biofeedback.",
        "skill_mods": {"perception": 3, "combat": 2},
    },

    # --- CONSUMABLES T4 ---
    "elite_med_kit": {
        "type": "consumable", "tier": 4, "value": 250,
        "heal": 150, "duration": 0,
        "desc": "Corpo executive grade. Heals near anything.",
    },
    "berserker_dose": {
        "type": "consumable", "tier": 4, "value": 200,
        "heal": 50, "duration": 5, "stat_buffs": {"strength": 4, "agility": 2},
        "desc": "Combat enhancement cocktail. You feel invincible. You're not.",
    },

    # --- CYBERWARE T4 ---
    "reflex_booster": {
        "type": "cyberware", "tier": 4, "value": 500, "slot": "spine",
        "stat": "agility", "bonus": 3, "weight": 0,
        "desc": "Wired reflexes. Time slows in combat.",
        "skill_mods": {"combat": 2, "stealth": 2},
    },
    "subdermal_armor": {
        "type": "cyberware", "tier": 4, "value": 700, "slot": "body",
        "stat": "defense", "bonus": 4, "weight": 0,
        "desc": "Ballistic mesh under the skin. Permanent.",
    },
    "pain_editor": {
        "type": "cyberware", "tier": 4, "value": 650, "slot": "spine",
        "stat": "strength", "bonus": 2, "weight": 0,
        "desc": "Disables pain response. You don't flinch.",
        "skill_mods": {"combat": 3, "intimidation": 2},
        "class_affinity": ["street_samurai"],
    },
    "med_implant": {
        "type": "cyberware", "tier": 4, "value": 720, "slot": "body",
        "stat": "perception", "bonus": 2, "weight": 0,
        "desc": "Auto-injector with stim reservoir. Heals when crit.",
        "skill_mods": {"first_aid": 4},
        "class_affinity": ["medic"],
    },


    # ==========================================================
    # TIER 5 - EPIC
    # ==========================================================

    # --- WEAPONS T5 ---
    "plasma_blade": {
        "type": "weapon", "tier": 5, "value": 1500,
        "damage": 45, "accuracy_mod": 2, "crit_mod": 3, "weight": 2,
        "desc": "Coherent plasma edge. Ignores most armor.",
        "skill_mods": {"combat": 3, "intimidation": 2},
        "requires_skill": {"combat": 5},
    },
    "rail_pistol": {
        "type": "weapon", "tier": 5, "value": 1800, "ranged": True,
        "damage": 50, "accuracy_mod": 3, "crit_mod": 2, "weight": 2,
        "desc": "Magnetically accelerated tungsten. Punches through walls.",
        "skill_mods": {"combat": 4},
        "requires_skill": {"combat": 5},
    },
    "soulrender": {
        "type": "weapon", "tier": 5, "value": 2200,
        "damage": 48, "accuracy_mod": 3, "crit_mod": 5, "weight": 2,
        "desc": "Mythic mono-katana. Forged in a Kazumi temple.",
        "skill_mods": {"combat": 5, "intimidation": 3, "stealth": 1},
        "class_affinity": ["street_samurai"],
        "requires_skill": {"combat": 6},
    },
    "hacker_rig": {
        "type": "weapon", "tier": 5, "value": 1900,
        "damage": 30, "accuracy_mod": 3, "crit_mod": 2, "weight": 1, "ranged": True,
        "desc": "Custom-built. Routes electricity through ICE chains.",
        "skill_mods": {"hacking": 5, "tech_repair": 3},
        "class_affinity": ["netrunner"],
        "requires_skill": {"hacking": 6},
    },
    "diplomat_pistol": {
        "type": "weapon", "tier": 5, "value": 2000, "ranged": True,
        "damage": 38, "accuracy_mod": 4, "crit_mod": 3, "weight": 1,
        "desc": "Designed by the corpo arms division. Disturbingly elegant.",
        "skill_mods": {"persuasion": 3, "intimidation": 4, "combat": 2},
        "class_affinity": ["fixer", "ex_corpo"],
    },

    # --- ARMOR T5 ---
    "powered_armor": {
        "type": "armor", "tier": 5, "value": 2000, "slot": "body",
        "defense": 25, "agility_mod": -1, "weight": 8,
        "desc": "Servo-assisted. You feel ten feet tall.",
        "skill_mods": {"combat": 2, "intimidation": 4, "strength": 2},
    },
    "ghost_suit": {
        "type": "armor", "tier": 5, "value": 1900, "slot": "body",
        "defense": 12, "agility_mod": 4, "weight": 1,
        "desc": "Adaptive metamaterial. You disappear at will.",
        "skill_mods": {"stealth": 5, "perception": 1},
        "class_affinity": ["netrunner", "fixer"],
    },
    "doctor_exoskeleton": {
        "type": "armor", "tier": 5, "value": 1850, "slot": "body",
        "defense": 14, "agility_mod": 1, "weight": 4,
        "desc": "Surgical exoskeleton. Auto-applies trauma kits.",
        "skill_mods": {"first_aid": 6, "biology": 3, "perception": 2},
        "class_affinity": ["medic"],
    },

    # --- CYBERWARE T5 ---
    "ghost_overlay": {
        "type": "cyberware", "tier": 5, "value": 1500, "slot": "head",
        "stat": "tech", "bonus": 4, "weight": 0,
        "desc": "Ice-breaker firmware in your brain.",
        "skill_mods": {"hacking": 5, "stealth": 2},
        "class_affinity": ["netrunner"],
    },
    "berserker_chip": {
        "type": "cyberware", "tier": 5, "value": 1300, "slot": "spine",
        "stat": "strength", "bonus": 4, "weight": 0,
        "desc": "Combat reflexes. Side effects: rage.",
        "skill_mods": {"combat": 4, "intimidation": 2},
        "class_affinity": ["street_samurai"],
    },
    "executive_implants": {
        "type": "cyberware", "tier": 5, "value": 1700, "slot": "head",
        "stat": "charisma", "bonus": 4, "weight": 0,
        "desc": "Voice modulation. Pheromone control. People listen.",
        "skill_mods": {"persuasion": 5, "intimidation": 3, "corporate_lore": 2},
        "class_affinity": ["fixer", "ex_corpo"],
    },
    "med_drone_swarm": {
        "type": "cyberware", "tier": 5, "value": 1600, "slot": "body",
        "stat": "perception", "bonus": 3, "weight": 0,
        "desc": "Micro-drones live in your bloodstream. Self-repairing.",
        "skill_mods": {"first_aid": 5, "biology": 4},
        "class_affinity": ["medic"],
    },


    # ==========================================================
    # TIER 6 - LEGENDARY
    # ==========================================================

    "katana_of_neo_kazumi": {
        "type": "weapon", "tier": 6, "value": 5000,
        "damage": 60, "accuracy_mod": 4, "crit_mod": 5, "weight": 1,
        "desc": "Folded by master Kazumi himself. Sings in your hand.",
        "skill_mods": {"combat": 6, "intimidation": 3, "stealth": 2},
        "class_affinity": ["street_samurai"],
        "requires_skill": {"combat": 8},
    },
    "ai_companion_drone": {
        "type": "cyberware", "tier": 6, "value": 4000, "slot": "head",
        "stat": "perception", "bonus": 5, "weight": 0,
        "desc": "Sentient micro-drone. Watches your back.",
        "skill_mods": {"perception": 5, "hacking": 3, "combat": 2},
    },
    "deus_machina": {
        "type": "armor", "tier": 6, "value": 6500, "slot": "body",
        "defense": 35, "agility_mod": 1, "weight": 5,
        "desc": "Prototype. Combat exoframe. The pinnacle.",
        "skill_mods": {"combat": 5, "intimidation": 5, "strength": 3},
    },
    "blackwire_antidote": {
        "type": "quest", "tier": 6, "value": 0,
        "desc": "The cure to BLACKWIRE. Worth more than your life.",
    },
    "ishikawa_keycard": {
        "type": "quest", "tier": 6, "value": 0,
        "desc": "CEO Ishikawa's executive override key. Opens any door in OmniCorp.",
    },

    # ==========================================================
    # ADDITIONAL STREET SAMURAI ITEMS (T2-T5)
    # ==========================================================

    "combat_knife": {
        "type": "weapon", "tier": 2, "value": 45,
        "damage": 11, "accuracy_mod": 1, "crit_mod": 3, "weight": 0,
        "desc": "Military-spec. Balanced for throwing.",
        "skill_mods": {"combat": 1, "stealth": 1},
        "class_affinity": ["street_samurai"],
    },
    "chain_whip": {
        "type": "weapon", "tier": 3, "value": 160,
        "damage": 19, "accuracy_mod": 0, "crit_mod": 2, "weight": 2,
        "desc": "Chrome chain. Intimidating reach.",
        "skill_mods": {"combat": 2, "intimidation": 2},
        "class_affinity": ["street_samurai"],
    },
    "blade_arm": {
        "type": "cyberware", "tier": 4, "value": 850, "slot": "arms",
        "stat": "strength", "bonus": 3, "weight": 0,
        "desc": "Retractable mono-blade grafted to forearm.",
        "skill_mods": {"combat": 4, "intimidation": 3},
        "class_affinity": ["street_samurai"],
    },
    "battle_visor": {
        "type": "armor", "tier": 3, "value": 200, "slot": "head",
        "defense": 4, "perception_mod": 2, "weight": 1,
        "desc": "Red-lens combat optics. Rage mode.",
        "skill_mods": {"combat": 3, "intimidation": 1},
        "class_affinity": ["street_samurai"],
    },
    "samurai_duster": {
        "type": "armor", "tier": 4, "value": 580, "slot": "body",
        "defense": 11, "agility_mod": 0, "weight": 3,
        "desc": "Reinforced armored coat. Long. Heavy.",
        "skill_mods": {"combat": 2, "intimidation": 3},
        "class_affinity": ["street_samurai"],
    },
    "bone_lacing": {
        "type": "cyberware", "tier": 3, "value": 480, "slot": "body",
        "stat": "strength", "bonus": 2, "weight": 0,
        "desc": "Ceramic weave into the skeleton. You hit harder.",
        "skill_mods": {"combat": 2, "intimidation": 1},
        "class_affinity": ["street_samurai"],
    },

    # ==========================================================
    # ADDITIONAL TECH ITEMS (T2-T5)
    # ==========================================================

    "tool_belt": {
        "type": "armor", "tier": 2, "value": 55, "slot": "body",
        "defense": 2, "agility_mod": 0, "weight": 1,
        "desc": "Heavy canvas with tool loops. Always ready.",
        "skill_mods": {"tech_repair": 2, "engineering": 1},
        "class_affinity": ["tech"],
    },
    "drone_kit": {
        "type": "weapon", "tier": 3, "value": 250, "ranged": True,
        "damage": 16, "accuracy_mod": 3, "crit_mod": 1, "weight": 2,
        "desc": "Recon drone with impact charge payload.",
        "skill_mods": {"tech_repair": 3, "perception": 2, "engineering": 2},
        "class_affinity": ["tech"],
    },
    "exo_gauntlet": {
        "type": "armor", "tier": 3, "value": 220, "slot": "hands",
        "defense": 4, "agility_mod": 0, "weight": 2,
        "desc": "Powered arm rig. Crushes metal.",
        "skill_mods": {"tech_repair": 2, "combat": 2, "engineering": 2},
        "class_affinity": ["tech"],
    },
    "field_fabricator": {
        "type": "weapon", "tier": 4, "value": 620,
        "damage": 20, "accuracy_mod": 1, "crit_mod": 0, "weight": 3,
        "desc": "Constructs traps and barricades mid-combat.",
        "skill_mods": {"engineering": 5, "tech_repair": 3},
        "class_affinity": ["tech"],
    },
    "overclock_chip": {
        "type": "cyberware", "tier": 4, "value": 780, "slot": "head",
        "stat": "tech", "bonus": 3, "weight": 0,
        "desc": "Overclocks your neural processor. Everything faster.",
        "skill_mods": {"tech_repair": 4, "hacking": 2, "engineering": 3},
        "class_affinity": ["tech"],
    },
    "hardened_chassis": {
        "type": "cyberware", "tier": 3, "value": 420, "slot": "body",
        "stat": "defense", "bonus": 3, "weight": 0,
        "desc": "Subdermal plating. Industrial grade.",
        "skill_mods": {"tech_repair": 1, "engineering": 1},
        "class_affinity": ["tech"],
    },
    "nanite_welder": {
        "type": "cyberware", "tier": 5, "value": 1400, "slot": "arms",
        "stat": "tech", "bonus": 4, "weight": 0,
        "desc": "Nanite injectors in the palms. Repair anything you touch.",
        "skill_mods": {"tech_repair": 6, "engineering": 4, "first_aid": 2},
        "class_affinity": ["tech"],
    },

    # ==========================================================
    # ADDITIONAL EX-CORPO ITEMS (T2-T5)
    # ==========================================================

    "corpo_id_card": {
        "type": "misc", "tier": 2, "value": 150,
        "desc": "Fake OmniCorp ID. Gets you past most checkpoints.",
        "skill_mods": {"corporate_lore": 1, "persuasion": 1},
        "class_affinity": ["ex_corpo"],
    },
    "briefcase_pistol": {
        "type": "weapon", "tier": 3, "value": 300, "ranged": True,
        "damage": 20, "accuracy_mod": 2, "crit_mod": 2, "weight": 1,
        "desc": "Pistol hidden inside a synth-leather briefcase.",
        "skill_mods": {"persuasion": 2, "intimidation": 2, "stealth": 2},
        "class_affinity": ["ex_corpo", "fixer"],
    },
    "insider_dossier": {
        "type": "misc", "tier": 3, "value": 500,
        "desc": "Blackmail files. Three OmniCorp mid-managers.",
        "skill_mods": {"corporate_lore": 3, "persuasion": 2},
        "class_affinity": ["ex_corpo"],
    },
    "boardroom_armor": {
        "type": "armor", "tier": 4, "value": 750, "slot": "body",
        "defense": 10, "agility_mod": 0, "weight": 2,
        "desc": "Armored suit. Reads as business casual.",
        "skill_mods": {"persuasion": 4, "corporate_lore": 3, "intimidation": 2},
        "class_affinity": ["ex_corpo"],
    },
    "corpo_override_chip": {
        "type": "cyberware", "tier": 4, "value": 900, "slot": "head",
        "stat": "tech", "bonus": 2, "weight": 0,
        "desc": "OmniCorp authentication firmware. Bypasses their own security.",
        "skill_mods": {"corporate_lore": 4, "hacking": 3},
        "class_affinity": ["ex_corpo"],
    },
    "shadow_network": {
        "type": "cyberware", "tier": 5, "value": 1800, "slot": "head",
        "stat": "charisma", "bonus": 3, "weight": 0,
        "desc": "Personal dark web. Your contacts are everywhere.",
        "skill_mods": {"corporate_lore": 5, "persuasion": 4, "streetwise": 3},
        "class_affinity": ["ex_corpo", "fixer"],
    },
    "corpo_sidearm": {
        "type": "weapon", "tier": 4, "value": 700, "ranged": True,
        "damage": 30, "accuracy_mod": 3, "crit_mod": 2, "weight": 1,
        "desc": "OmniCorp executive issue. Silenced.",
        "skill_mods": {"corporate_lore": 2, "combat": 2, "stealth": 2},
        "class_affinity": ["ex_corpo"],
    },

    # ==========================================================
    # ADDITIONAL GENERAL ITEMS (scattered world loot)
    # ==========================================================

    "sewer_map": {
        "type": "misc", "tier": 2, "value": 80,
        "desc": "Hand-drawn tunnels. Someone mapped the underground.",
        "skill_mods": {"streetwise": 1},
    },
    "blackwire_sample": {
        "type": "quest", "tier": 3, "value": 0,
        "desc": "Sample of the BLACKWIRE compound. Smells wrong.",
    },
    "gang_tattoo_kit": {
        "type": "misc", "tier": 1, "value": 20,
        "desc": "Crimson Fang gang ink. Wear it and you're one of them. Or a target.",
    },
    "encrypted_drive": {
        "type": "quest", "tier": 4, "value": 0,
        "desc": "Encrypted hard drive. Heavy. Whatever's on it - people died for it.",
    },
    "military_rations": {
        "type": "consumable", "tier": 2, "value": 18,
        "heal": 25, "duration": 0,
        "desc": "Military grade. Dense. Actually edible.",
    },
    "nano_bandages": {
        "type": "consumable", "tier": 3, "value": 85,
        "heal": 60, "duration": 0,
        "desc": "Smart-fabric wound closure. No scar.",
    },
    "surge_capsule": {
        "type": "consumable", "tier": 4, "value": 180,
        "heal": 120, "duration": 3, "stat_buffs": {"strength": 3},
        "desc": "Combat surge. Limited time. Full effect.",
    },
    "emp_grenade": {
        "type": "weapon", "tier": 3, "value": 200, "ranged": True,
        "damage": 25, "accuracy_mod": 0, "crit_mod": 0, "weight": 1, "stun": True,
        "desc": "Fries all electronics in a radius. Not picky.",
        "skill_mods": {"engineering": 2},
    },
    "sawn_off": {
        "type": "weapon", "tier": 2, "value": 90, "ranged": True,
        "damage": 22, "accuracy_mod": -3, "crit_mod": 3, "weight": 2,
        "desc": "Cut down shotgun. Deadly up close. Useless far.",
        "skill_mods": {"intimidation": 2},
    },
    "voice_modulator": {
        "type": "cyberware", "tier": 3, "value": 350, "slot": "head",
        "stat": "charisma", "bonus": 2, "weight": 0,
        "desc": "Synthesizes any voice. Useful.",
        "skill_mods": {"persuasion": 2, "intimidation": 2, "stealth": 1},
    },
    "encrypted_comms": {
        "type": "cyberware", "tier": 2, "value": 280, "slot": "head",
        "stat": "perception", "bonus": 1, "weight": 0,
        "desc": "Scrambled comms chip. No one taps this.",
        "skill_mods": {"streetwise": 2, "hacking": 1},
    },
}


# ============================================================
# TIER METADATA
# ============================================================
TIER_NAMES = {
    1: "JUNK",
    2: "COMMON",
    3: "UNCOMMON",
    4: "RARE",
    5: "EPIC",
    6: "LEGENDARY",
}

TIER_COLORS = {
    1: "dim white",
    2: "white",
    3: "green",
    4: "cyan",
    5: "magenta",
    6: "bold yellow",
}


# ============================================================
# LOOKUP HELPERS
# ============================================================

def get_item(name: str) -> dict:
    return ITEMS.get(name.lower().replace(" ", "_"))


def item_display_name(name: str) -> str:
    return name.replace("_", " ").title()


def get_items_by_tier(tier: int) -> list:
    return [k for k, v in ITEMS.items() if v.get("tier", 1) == tier]


def get_items_for_class(class_id: str, tier: int = None) -> list:
    """Get items affiliated with a class. Optionally filter by tier."""
    out = []
    for item_id, item in ITEMS.items():
        if class_id in item.get("class_affinity", []):
            if tier is None or item.get("tier") == tier:
                out.append(item_id)
    return out


def get_items_for_enemy_level(enemy_level: int) -> list:
    """Tier weights for loot drops based on enemy level."""
    if enemy_level <= 2:
        return [(1, 75), (2, 25)]
    elif enemy_level <= 4:
        return [(1, 40), (2, 45), (3, 15)]
    elif enemy_level <= 6:
        return [(2, 40), (3, 45), (4, 15)]
    elif enemy_level <= 9:
        return [(3, 40), (4, 45), (5, 15)]
    elif enemy_level <= 12:
        return [(4, 40), (5, 45), (6, 15)]
    else:
        return [(5, 40), (6, 60)]


def roll_loot(enemy_level: int, count: int = 1, prefer_class: str = None) -> list:
    """Roll random loot. If prefer_class is given, weight class-affinity items higher."""
    import random
    tier_weights = get_items_for_enemy_level(enemy_level)
    items = []
    for _ in range(count):
        tiers, weights = zip(*tier_weights)
        chosen_tier = random.choices(tiers, weights=weights, k=1)[0]
        candidates = get_items_by_tier(chosen_tier)
        candidates = [c for c in candidates if ITEMS[c]["type"] != "quest"]
        if not candidates:
            continue

        # Weight class-affinity items 3x if prefer_class given
        if prefer_class:
            weights = [3 if prefer_class in ITEMS[c].get("class_affinity", []) else 1
                       for c in candidates]
            items.append(random.choices(candidates, weights=weights, k=1)[0])
        else:
            items.append(random.choice(candidates))
    return items


def tier_label(tier: int) -> str:
    name = TIER_NAMES.get(tier, "?")
    color = TIER_COLORS.get(tier, "white")
    return "[" + color + "]T" + str(tier) + " " + name + "[/" + color + "]"


def get_skill_mods_summary(player) -> dict:
    """Sum all skill modifiers from equipped + cyberware."""
    mods = {}
    for slot in ("weapon", "armor"):
        item_id = player.equipped.get(slot)
        if not item_id:
            continue
        item = get_item(item_id)
        if item and "skill_mods" in item:
            for skill, bonus in item["skill_mods"].items():
                mods[skill] = mods.get(skill, 0) + bonus

    for cyber_id in player.cyberware:
        item = get_item(cyber_id)
        if item and "skill_mods" in item:
            for skill, bonus in item["skill_mods"].items():
                mods[skill] = mods.get(skill, 0) + bonus

    return mods


def can_equip(player, item_id: str) -> tuple:
    """Check if player meets requirements. Returns (bool, reason_str)."""
    item = get_item(item_id)
    if not item:
        return False, "Unknown item."
    reqs = item.get("requires_skill", {})
    for skill, min_level in reqs.items():
        if player.skills.get(skill, 0) < min_level:
            return False, "Requires " + skill + " " + str(min_level)
    return True, ""
