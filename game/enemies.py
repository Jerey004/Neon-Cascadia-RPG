"""Enemy stats for combat encounters."""

ENEMIES = {
    # ========= LOW TIER =========
    "junkie": {
        "name": "Strung-out Junkie",
        "hp": 20, "damage": 6, "defense": 0,
        "credits": 10, "loot": ["smokes"], "loot_chance": 0.3,
        "desc": "Wired on stims, swinging wildly.",
    },
    "lowlife_thug": {
        "name": "Lowlife Thug",
        "hp": 35, "damage": 9, "defense": 1,
        "credits": 25, "loot": ["rusty_pipe", "ration_pack"], "loot_chance": 0.4,
        "desc": "Cheap muscle. Bad attitude. Worse hygiene.",
    },
    "pickpocket": {
        "name": "Market Pickpocket",
        "hp": 18, "damage": 5, "defense": 0,
        "credits": 40, "loot": ["smokes"], "loot_chance": 0.5,
        "desc": "Quick fingers, faster feet.",
    },
    "mugger": {
        "name": "Alley Mugger",
        "hp": 30, "damage": 11, "defense": 1,
        "credits": 35, "loot": ["leather_jacket"], "loot_chance": 0.3,
        "desc": "Knife out. Eyes hungry.",
    },
    "feral_dog": {
        "name": "Feral Cyber-Dog",
        "hp": 25, "damage": 10, "defense": 2,
        "credits": 0, "loot": [], "loot_chance": 0,
        "desc": "Half flesh, half chrome. All teeth.",
    },

    # ========= MID TIER =========
    "alley_ganger": {
        "name": "Crimson Fang Ganger",
        "hp": 50, "damage": 13, "defense": 3,
        "credits": 60, "loot": ["cheap_pistol", "stim_pack"], "loot_chance": 0.5,
        "desc": "Red bandana. Cheap pistol. Loyal to the gang.",
    },
    "rail_ganger": {
        "name": "Rail Rat Enforcer",
        "hp": 55, "damage": 14, "defense": 3,
        "credits": 75, "loot": ["stun_baton", "stim_pack"], "loot_chance": 0.4,
        "desc": "Lives in the tunnels. Smells like grease.",
    },
    "scavenger": {
        "name": "Sewer Scavenger",
        "hp": 40, "damage": 11, "defense": 2,
        "credits": 30, "loot": ["transit_card", "ration_pack"], "loot_chance": 0.6,
        "desc": "Hauls scrap for credits. Cornered animals are dangerous.",
    },
    "mutant_rat": {
        "name": "Toxic Rat",
        "hp": 35, "damage": 12, "defense": 1,
        "credits": 0, "loot": [], "loot_chance": 0,
        "desc": "Dog-sized. Three eyes. Drools acid.",
    },
    "broken_servitor": {
        "name": "Broken Servitor Bot",
        "hp": 60, "damage": 12, "defense": 5,
        "credits": 0, "loot": ["data_shard"], "loot_chance": 0.3,
        "desc": "Old factory robot. Logic loop has it killing everything.",
    },
    "rogue_drone": {
        "name": "Rogue Security Drone",
        "hp": 45, "damage": 15, "defense": 4,
        "credits": 0, "loot": [], "loot_chance": 0,
        "desc": "Hovering. Red laser sight. Trigger-happy.",
    },

    # ========= HIGH TIER =========
    "corpo_security": {
        "name": "OmniCorp Security",
        "hp": 80, "damage": 18, "defense": 6,
        "credits": 150, "loot": ["kevlar_vest", "stim_pack"], "loot_chance": 0.5,
        "desc": "Trained. Armed. Body cam recording everything.",
    },
    "security_drone": {
        "name": "OmniCorp Patrol Drone",
        "hp": 70, "damage": 20, "defense": 7,
        "credits": 0, "loot": ["data_shard"], "loot_chance": 0.4,
        "desc": "Black chassis. OmniCorp logo. Lethal force authorized.",
    },
    "war_machine": {
        "name": "Decommissioned War-Mech",
        "hp": 120, "damage": 25, "defense": 10,
        "credits": 0, "loot": ["smartgun", "combat_armor"], "loot_chance": 0.7,
        "desc": "Eight feet tall. Should not be online. Is.",
    },
    "elite_guard": {
        "name": "Elite Tower Guard",
        "hp": 100, "damage": 22, "defense": 8,
        "credits": 250, "loot": ["combat_armor", "trauma_kit"], "loot_chance": 0.6,
        "desc": "Black armor. Smartlinked rifle. Calm eyes.",
    },
    "sewer_horror": {
        "name": "Sewer Horror",
        "hp": 110, "damage": 24, "defense": 5,
        "credits": 0, "loot": ["monoblade"], "loot_chance": 0.5,
        "desc": "Once human. Now mostly tentacles. The water birthed it.",
    },
}


def get_enemy(enemy_id: str) -> dict:
    """Return a fresh copy of enemy stats."""
    if enemy_id not in ENEMIES:
        return None
    return dict(ENEMIES[enemy_id])
