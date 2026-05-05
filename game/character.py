"""Character classes, skill system, and leveling mechanics."""

# ============================================================
# CLASSES (archetypes)
# ============================================================
# Each class has starting stat bonuses, starting skills, starting gear,
# starting faction rep, and a unique flavor description.

CLASSES = {
    "street_samurai": {
        "name": "Street Samurai",
        "description": (
            "Razors and reflexes. You live by the blade and the bullet. "
            "Combat is a religion, and you are devout."
        ),
        "stat_bonuses": {"strength": 3, "agility": 2, "tech": -1, "perception": 1, "charisma": -1},
        "skill_bonuses": {"combat": 3, "first_aid": 1, "intimidation": 2},
        "starting_gear": ["monoblade", "leather_jacket", "stim_pack", "stim_pack"],
        "starting_weapon": "monoblade",
        "starting_armor": "leather_jacket",
        "starting_credits": 200,
        "starting_rep": {"gangs": 10, "corpo": -15, "police": -10},
        "hp_bonus": 30,
    },
    "netrunner": {
        "name": "Netrunner",
        "description": (
            "You are ghost in the wires. Where others use guns, you use code. "
            "The net is your battlefield and ICE bleeds when you cut it."
        ),
        "stat_bonuses": {"strength": -1, "agility": 1, "tech": 4, "perception": 2, "charisma": -1},
        "skill_bonuses": {"hacking": 4, "stealth": 1, "tech_repair": 2},
        "starting_gear": ["cheap_pistol", "neural_jack", "virus_chip", "virus_chip", "stim_pack"],
        "starting_weapon": "cheap_pistol",
        "starting_armor": None,
        "starting_credits": 350,
        "starting_rep": {"hackers": 25, "corpo": -20},
        "hp_bonus": 0,
    },
    "fixer": {
        "name": "Fixer",
        "description": (
            "Connections are currency. You know everyone, and everyone owes "
            "you something. Talk first, shoot only when the deal goes bad."
        ),
        "stat_bonuses": {"strength": 0, "agility": 1, "tech": 1, "perception": 2, "charisma": 4},
        "skill_bonuses": {"persuasion": 4, "intimidation": 2, "streetwise": 3, "barter": 3},
        "starting_gear": ["cheap_pistol", "leather_jacket", "smokes", "smokes", "credstick"],
        "starting_weapon": "cheap_pistol",
        "starting_armor": "leather_jacket",
        "starting_credits": 500,
        "starting_rep": {"gangs": 5, "hackers": 5, "corpo": 5, "scavengers": 5},
        "hp_bonus": 10,
    },
    "tech": {
        "name": "Tech",
        "description": (
            "You build, repair, modify. Drones, cyberware, weapons - if it's "
            "made of metal, you can make it sing. Or explode."
        ),
        "stat_bonuses": {"strength": 1, "agility": 1, "tech": 3, "perception": 2, "charisma": -1},
        "skill_bonuses": {"tech_repair": 4, "hacking": 2, "first_aid": 2, "engineering": 3},
        "starting_gear": ["stun_baton", "leather_jacket", "trauma_kit", "cyber_eye"],
        "starting_weapon": "stun_baton",
        "starting_armor": "leather_jacket",
        "starting_credits": 300,
        "starting_rep": {"scavengers": 15, "hackers": 5},
        "hp_bonus": 15,
    },
    "medic": {
        "name": "Street Medic",
        "description": (
            "The slums chew people up. You are who they crawl to. You patch "
            "bullet wounds in alleys and ask questions later."
        ),
        "stat_bonuses": {"strength": 0, "agility": 1, "tech": 2, "perception": 3, "charisma": 1},
        "skill_bonuses": {"first_aid": 5, "biology": 3, "persuasion": 1, "streetwise": 2},
        "starting_gear": ["cheap_pistol", "leather_jacket", "trauma_kit", "trauma_kit", "stim_pack", "stim_pack"],
        "starting_weapon": "cheap_pistol",
        "starting_armor": "leather_jacket",
        "starting_credits": 250,
        "starting_rep": {"gangs": 5, "scavengers": 10, "police": 5},
        "hp_bonus": 20,
    },
    "ex_corpo": {
        "name": "Ex-Corporate",
        "description": (
            "You used to wear the suit. You know how the towers think, the "
            "back doors they leave, the people they trust. They hate you for it."
        ),
        "stat_bonuses": {"strength": 1, "agility": 0, "tech": 2, "perception": 2, "charisma": 2},
        "skill_bonuses": {"persuasion": 3, "hacking": 2, "barter": 2, "corporate_lore": 4},
        "starting_gear": ["smartgun", "kevlar_vest", "stim_pack", "credstick", "credstick"],
        "starting_weapon": "smartgun",
        "starting_armor": "kevlar_vest",
        "starting_credits": 800,
        "starting_rep": {"corpo": -30, "gangs": -5, "police": -10},
        "hp_bonus": 10,
    },
}


# ============================================================
# SKILLS
# ============================================================
# Skills are 0-10. They affect dice rolls, AI prompts, and gate certain actions.

SKILL_DEFINITIONS = {
    "combat": {
        "desc": "Hand-to-hand and ranged weapon proficiency.",
        "affects": "Combat hit chance, damage bonus.",
    },
    "hacking": {
        "desc": "Breaking into networks, bypassing ICE, cracking encryption.",
        "affects": "Net runs, electronic locks, AI hacking actions.",
    },
    "first_aid": {
        "desc": "Treating wounds, drug interactions, surgery.",
        "affects": "Healing item potency, mid-combat heal speed.",
    },
    "stealth": {
        "desc": "Moving unseen, palming items, evading drones.",
        "affects": "Sneak past enemies, avoid encounters, theft.",
    },
    "persuasion": {
        "desc": "Talking your way through. Reading people.",
        "affects": "NPC dialogue success, quest negotiation.",
    },
    "intimidation": {
        "desc": "Making people afraid. Backing it up if needed.",
        "affects": "Forcing concessions, avoiding fights via threat.",
    },
    "streetwise": {
        "desc": "Reading the city. Knowing who's who in the slums.",
        "affects": "Finding contacts, recognizing dangers, rumors.",
    },
    "barter": {
        "desc": "Squeezing better prices, spotting fakes.",
        "affects": "Better shop prices, item appraisals.",
    },
    "tech_repair": {
        "desc": "Fixing machines, jury-rigging gear, modifying weapons.",
        "affects": "Repair items, craft, install cyberware safely.",
    },
    "engineering": {
        "desc": "Designing systems, understanding infrastructure.",
        "affects": "Solve puzzles, sabotage, build traps.",
    },
    "biology": {
        "desc": "Knowledge of bodies - human, mutant, augmented.",
        "affects": "Identify drugs/toxins, anatomy strikes in combat.",
    },
    "corporate_lore": {
        "desc": "How the megacorps operate. Their secrets.",
        "affects": "Navigate corpo zones, find weaknesses, blackmail.",
    },
    "perception": {
        "desc": "Noticing things. Hidden doors, lies, ambushes.",
        "affects": "Find hidden items, detect threats, read NPCs.",
    },
}


# ============================================================
# LEVELING / XP
# ============================================================
# XP curve: each level requires more than the last.

def xp_for_level(level: int) -> int:
    """How much TOTAL XP is needed to reach a given level."""
    if level <= 1:
        return 0
    # Triangular-ish curve: lvl 2 = 100, lvl 3 = 250, lvl 4 = 450, lvl 5 = 700...
    return int(50 * level * (level - 1))


def xp_to_next_level(current_level: int, current_xp: int) -> int:
    """How much MORE XP needed to level up."""
    return xp_for_level(current_level + 1) - current_xp


# Per-level rewards on level up
def level_up_rewards(new_level: int) -> dict:
    """What you get when you level up."""
    return {
        "hp_gain": 10,
        "stat_points": 1 if new_level % 2 == 0 else 0,  # Stat point every 2 levels
        "skill_points": 3,
    }


# ============================================================
# XP REWARDS
# ============================================================
XP_REWARDS = {
    "kill_low": 25,       # junkie, pickpocket
    "kill_mid": 75,       # ganger, scavenger, drone
    "kill_high": 200,     # corpo security, war mech
    "discover_location": 15,
    "complete_quest_minor": 100,
    "complete_quest_major": 500,
    "successful_skill_check": 5,
    "first_time_action": 10,
}


def get_class(class_id: str) -> dict:
    return CLASSES.get(class_id)


def get_class_list() -> list:
    return list(CLASSES.keys())
