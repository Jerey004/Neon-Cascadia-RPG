"""Named boss enemies.

Bosses are unique, named enemies with:
  - Much higher HP/damage than regular enemies
  - Guaranteed legendary or epic loot
  - Special phases (they get harder when low HP)
  - Unique kill messages
  - Significant faction rep changes on defeat

Bosses are triggered by the AI using [COMBAT_START: boss_id]
or by engine events (e.g., completing certain quests).
"""

BOSSES = {
    "riza_volkov": {
        "name": "Riza Volkov",
        "title": "Crimson Fang Leader",
        "level": 12,
        "hp": 200,
        "damage": 28,
        "defense": 8,
        "credits_min": 500,
        "credits_max": 1000,
        "guaranteed_loot": ["plasma_blade", "combat_armor"],
        "loot_chance": 1.0,
        "loot_rolls": 2,
        "desc": "One eye chrome. One eye hungry. She moves like a blade.",
        "phase_two_hp": 100,          # HP threshold for phase 2
        "phase_two_damage_bonus": 8,  # Extra damage in phase 2
        "kill_message": (
            "Volkov hits the floor hard. The chrome eye flickers and dies. "
            "The Crimson Fang will fracture without her. The city just shifted."
        ),
        "rep_changes": {"gangs": -25, "corpo": +5, "scavengers": +5},
    },
    "hex_murakami": {
        "name": "Hex Murakami",
        "title": "Rail Rat Boss",
        "level": 11,
        "hp": 175,
        "damage": 24,
        "defense": 7,
        "credits_min": 400,
        "credits_max": 800,
        "guaranteed_loot": ["smartgun", "tactical_visor"],
        "loot_chance": 1.0,
        "loot_rolls": 2,
        "desc": "Twitchy. Wired. Six cybernetic eyes. Sees everything.",
        "phase_two_hp": 85,
        "phase_two_damage_bonus": 6,
        "kill_message": (
            "Murakami's paranoid AI fires one last alert as he goes down. "
            "The smuggling routes die with him. Or someone else takes over."
        ),
        "rep_changes": {"gangs": -20, "corpo": +5},
    },
    "ishikawa_yuto": {
        "name": "CEO Ishikawa Yuto",
        "title": "OmniCorp CEO",
        "level": 15,
        "hp": 250,
        "damage": 35,
        "defense": 12,
        "credits_min": 2000,
        "credits_max": 5000,
        "guaranteed_loot": ["ishikawa_keycard", "deus_machina"],
        "loot_chance": 1.0,
        "loot_rolls": 3,
        "desc": (
            "Ten cybernetic upgrades. The kind money buys. Cold eyes. "
            "He's fought wars from boardrooms. Now he'll fight one in person."
        ),
        "phase_two_hp": 125,
        "phase_two_damage_bonus": 12,
        "kill_message": (
            "The most powerful man in Neo-Cascadia crumples like anyone else. "
            "His last expression is surprise. The BLACKWIRE files are yours. "
            "The city will never be the same."
        ),
        "rep_changes": {"gangs": +20, "hackers": +25, "corpo": -50, "police": -20},
        "triggers_ending": True,
    },
}


def get_boss(boss_id: str) -> dict:
    """Return a fresh copy of boss stats."""
    if boss_id not in BOSSES:
        return None
    return dict(BOSSES[boss_id])


def is_boss(enemy_id: str) -> bool:
    return enemy_id in BOSSES
