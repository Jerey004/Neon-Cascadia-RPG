"""Enemy stats for combat encounters - now with levels for tiered loot."""

ENEMIES = {
    # ========= LOW TIER (lvl 1-2) =========
    "junkie": {
        "name": "Strung-out Junkie", "level": 1,
        "hp": 20, "damage": 6, "defense": 0,
        "credits_min": 5, "credits_max": 20,
        "guaranteed_loot": [],  # always drops
        "loot_chance": 0.4,  # chance for tiered loot rolls
        "loot_rolls": 1,
        "desc": "Wired on stims, swinging wildly.",
    },
    "lowlife_thug": {
        "name": "Lowlife Thug", "level": 2,
        "hp": 35, "damage": 9, "defense": 1,
        "credits_min": 15, "credits_max": 40,
        "guaranteed_loot": [],
        "loot_chance": 0.6,
        "loot_rolls": 1,
        "desc": "Cheap muscle. Bad attitude. Worse hygiene.",
    },
    "pickpocket": {
        "name": "Market Pickpocket", "level": 1,
        "hp": 18, "damage": 5, "defense": 0,
        "credits_min": 25, "credits_max": 60,
        "guaranteed_loot": [],
        "loot_chance": 0.5,
        "loot_rolls": 1,
        "desc": "Quick fingers, faster feet.",
    },
    "mugger": {
        "name": "Alley Mugger", "level": 2,
        "hp": 30, "damage": 11, "defense": 1,
        "credits_min": 20, "credits_max": 50,
        "guaranteed_loot": [],
        "loot_chance": 0.5,
        "loot_rolls": 1,
        "desc": "Knife out. Eyes hungry.",
    },
    "feral_dog": {
        "name": "Feral Cyber-Dog", "level": 2,
        "hp": 25, "damage": 10, "defense": 2,
        "credits_min": 0, "credits_max": 0,
        "guaranteed_loot": ["scrap_metal"],
        "loot_chance": 0.2,
        "loot_rolls": 1,
        "desc": "Half flesh, half chrome. All teeth.",
    },

    # ========= MID TIER (lvl 3-5) =========
    "alley_ganger": {
        "name": "Crimson Fang Ganger", "level": 4,
        "hp": 50, "damage": 13, "defense": 3,
        "credits_min": 40, "credits_max": 100,
        "guaranteed_loot": [],
        "loot_chance": 0.7,
        "loot_rolls": 2,
        "desc": "Red bandana. Cheap pistol. Loyal to the gang.",
    },
    "rail_ganger": {
        "name": "Rail Rat Enforcer", "level": 4,
        "hp": 55, "damage": 14, "defense": 3,
        "credits_min": 50, "credits_max": 120,
        "guaranteed_loot": [],
        "loot_chance": 0.7,
        "loot_rolls": 2,
        "desc": "Lives in the tunnels. Smells like grease.",
    },
    "scavenger": {
        "name": "Sewer Scavenger", "level": 3,
        "hp": 40, "damage": 11, "defense": 2,
        "credits_min": 20, "credits_max": 60,
        "guaranteed_loot": ["scrap_metal"],
        "loot_chance": 0.6,
        "loot_rolls": 1,
        "desc": "Hauls scrap for credits. Cornered animals are dangerous.",
    },
    "mutant_rat": {
        "name": "Toxic Rat", "level": 3,
        "hp": 35, "damage": 12, "defense": 1,
        "credits_min": 0, "credits_max": 0,
        "guaranteed_loot": [],
        "loot_chance": 0.1,
        "loot_rolls": 1,
        "desc": "Dog-sized. Three eyes. Drools acid.",
    },
    "broken_servitor": {
        "name": "Broken Servitor Bot", "level": 5,
        "hp": 60, "damage": 12, "defense": 5,
        "credits_min": 0, "credits_max": 0,
        "guaranteed_loot": ["scrap_metal", "scrap_metal"],
        "loot_chance": 0.5,
        "loot_rolls": 2,
        "desc": "Old factory robot. Logic loop has it killing everything.",
    },
    "rogue_drone": {
        "name": "Rogue Security Drone", "level": 5,
        "hp": 45, "damage": 15, "defense": 4,
        "credits_min": 0, "credits_max": 0,
        "guaranteed_loot": [],
        "loot_chance": 0.6,
        "loot_rolls": 1,
        "desc": "Hovering. Red laser sight. Trigger-happy.",
    },

    # ========= HIGH TIER (lvl 7-10) =========
    "corpo_security": {
        "name": "OmniCorp Security", "level": 7,
        "hp": 80, "damage": 18, "defense": 6,
        "credits_min": 100, "credits_max": 250,
        "guaranteed_loot": [],
        "loot_chance": 0.8,
        "loot_rolls": 2,
        "desc": "Trained. Armed. Body cam recording everything.",
    },
    "security_drone": {
        "name": "OmniCorp Patrol Drone", "level": 7,
        "hp": 70, "damage": 20, "defense": 7,
        "credits_min": 0, "credits_max": 0,
        "guaranteed_loot": [],
        "loot_chance": 0.7,
        "loot_rolls": 2,
        "desc": "Black chassis. OmniCorp logo. Lethal force authorized.",
    },
    "war_machine": {
        "name": "Decommissioned War-Mech", "level": 10,
        "hp": 120, "damage": 25, "defense": 10,
        "credits_min": 0, "credits_max": 0,
        "guaranteed_loot": [],
        "loot_chance": 0.9,
        "loot_rolls": 3,
        "desc": "Eight feet tall. Should not be online. Is.",
    },
    "elite_guard": {
        "name": "Elite Tower Guard", "level": 9,
        "hp": 100, "damage": 22, "defense": 8,
        "credits_min": 200, "credits_max": 400,
        "guaranteed_loot": [],
        "loot_chance": 0.8,
        "loot_rolls": 3,
        "desc": "Black armor. Smartlinked rifle. Calm eyes.",
    },
    "sewer_horror": {
        "name": "Sewer Horror", "level": 11,
        "hp": 110, "damage": 24, "defense": 5,
        "credits_min": 0, "credits_max": 0,
        "guaranteed_loot": [],
        "loot_chance": 0.7,
        "loot_rolls": 2,
        "desc": "Once human. Now mostly tentacles. The water birthed it.",
    },
    "ishikawa_executive": {
        "name": "OmniCorp Executive Bodyguard", "level": 13,
        "hp": 150, "damage": 30, "defense": 12,
        "credits_min": 500, "credits_max": 1000,
        "guaranteed_loot": ["combat_armor"],
        "loot_chance": 0.95,
        "loot_rolls": 4,
        "desc": "Cybernetic. Loyal. The CEO's personal shield.",
    },
}


def get_enemy(enemy_id: str) -> dict:
    """Return a fresh copy of enemy stats."""
    if enemy_id not in ENEMIES:
        # Fallback for AI-named enemies not in DB
        return {
            "name": enemy_id.replace("_", " ").title(),
            "level": 3,
            "hp": 40, "damage": 10, "defense": 2,
            "credits_min": 10, "credits_max": 30,
            "guaranteed_loot": [],
            "loot_chance": 0.5,
            "loot_rolls": 1,
            "desc": "A hostile threat.",
        }
    return dict(ENEMIES[enemy_id])
