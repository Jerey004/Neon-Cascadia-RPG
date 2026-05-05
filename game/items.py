"""Item definitions for Neon Cascadia.

Items are categorized:
- weapon: usable in combat
- armor: reduces damage taken
- consumable: one-time use (heal, buff)
- cyberware: permanent stat bonus when installed
- quest: story items
- misc: trade goods, junk
"""

ITEMS = {
    # ============== WEAPONS ==============
    "rusty_pipe": {
        "type": "weapon", "damage": 8, "value": 15,
        "desc": "A length of rebar. Crude but it'll cave a skull.",
    },
    "crowbar": {
        "type": "weapon", "damage": 12, "value": 30,
        "desc": "Heavy steel. Doubles for breaking and entering.",
    },
    "cheap_pistol": {
        "type": "weapon", "damage": 18, "value": 80, "ranged": True,
        "desc": "Plastic-frame 9mm. Untraceable. Probably.",
    },
    "monoblade": {
        "type": "weapon", "damage": 28, "value": 350,
        "desc": "Mono-molecular edge. Cuts chrome like butter.",
    },
    "smartgun": {
        "type": "weapon", "damage": 35, "value": 800, "ranged": True,
        "desc": "Auto-targeting. Links to your neural jack.",
    },
    "stun_baton": {
        "type": "weapon", "damage": 14, "value": 120, "stun": True,
        "desc": "OmniCorp issue. Disables cyberware on hit.",
    },

    # ============== ARMOR ==============
    "leather_jacket": {
        "type": "armor", "defense": 3, "value": 40,
        "desc": "Worn synth-leather. Stops a knife. Maybe.",
    },
    "kevlar_vest": {
        "type": "armor", "defense": 8, "value": 200,
        "desc": "Police surplus. Stops most pistol rounds.",
    },
    "combat_armor": {
        "type": "armor", "defense": 15, "value": 600,
        "desc": "Mil-spec ablative plates. You feel invincible.",
    },

    # ============== CONSUMABLES ==============
    "ration_pack": {
        "type": "consumable", "heal": 15, "value": 8,
        "desc": "Synth-protein bar. Tastes like wet cardboard.",
    },
    "stim_pack": {
        "type": "consumable", "heal": 40, "value": 35,
        "desc": "Combat med-stim. Burns going in.",
    },
    "trauma_kit": {
        "type": "consumable", "heal": 80, "value": 120,
        "desc": "Full-spectrum medical. Saves lives.",
    },
    "synth_coffee": {
        "type": "consumable", "heal": 5, "value": 4,
        "desc": "Hot. Bitter. Caffeine kicks like a mule.",
    },

    # ============== CYBERWARE ==============
    "neural_jack": {
        "type": "cyberware", "stat": "tech", "bonus": 2, "value": 250,
        "desc": "Standard data port. Plug into the net.",
    },
    "reflex_booster": {
        "type": "cyberware", "stat": "agility", "bonus": 3, "value": 500,
        "desc": "Wired reflexes. Time slows in combat.",
    },
    "subdermal_armor": {
        "type": "cyberware", "stat": "defense", "bonus": 4, "value": 700,
        "desc": "Ballistic mesh under the skin. Permanent.",
    },
    "cyber_eye": {
        "type": "cyberware", "stat": "perception", "bonus": 3, "value": 400,
        "desc": "Zoom, IR, threat detection. The world looks different.",
    },

    # ============== QUEST / SPECIAL ==============
    "data_shard": {
        "type": "quest", "value": 0,
        "desc": "Encrypted data crystal. Someone wants this badly.",
    },
    "virus_chip": {
        "type": "consumable", "value": 80, "hack": True,
        "desc": "One-shot ICE breaker. Single-use.",
    },
    "transit_card": {
        "type": "misc", "value": 5,
        "desc": "Magrail transit pass. Most readers still take it.",
    },
    "credstick": {
        "type": "misc", "value": 100,
        "desc": "Anonymous credit chip. Clean money.",
    },
    "smokes": {
        "type": "misc", "value": 12,
        "desc": "Pack of synth-cigarettes. Useful for trading.",
    },
}


def get_item(name: str) -> dict:
    """Get item data by name, or None if not found."""
    return ITEMS.get(name.lower().replace(" ", "_"))


def item_display_name(name: str) -> str:
    """Convert internal name to display name."""
    return name.replace("_", " ").title()
