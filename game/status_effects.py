"""Status effects for combat and exploration.

Effects are stored as a list on the player/enemy: each entry is a dict:
  {"id": str, "name": str, "turns_left": int, "value": int}

Supported effects:
  bleeding   - takes `value` damage per turn, stacks
  stunned    - skips next attack, cleared after 1 turn
  poisoned   - takes `value` damage per turn
  hacked     - cyberware skill_mods disabled, cleared after N turns
  burning    - takes `value` damage per turn, high value
  weakened   - defense reduced by `value`
  slowed     - flee chance reduced, agility checks penalized
"""

ALL_EFFECTS = {
    "bleeding": {
        "name": "Bleeding",
        "color": "red",
        "desc": "Losing blood. Takes damage each turn.",
        "icon": "[red]BLD[/red]",
    },
    "stunned": {
        "name": "Stunned",
        "color": "yellow",
        "desc": "Can't act next turn.",
        "icon": "[yellow]STN[/yellow]",
    },
    "poisoned": {
        "name": "Poisoned",
        "color": "green",
        "desc": "Toxin in the blood. Damage per turn.",
        "icon": "[green]PSN[/green]",
    },
    "hacked": {
        "name": "Hacked",
        "color": "cyan",
        "desc": "Cyberware compromised. Skill mods disabled.",
        "icon": "[cyan]HCK[/cyan]",
    },
    "burning": {
        "name": "Burning",
        "color": "bold red",
        "desc": "On fire. High damage per turn.",
        "icon": "[bold red]BRN[/bold red]",
    },
    "weakened": {
        "name": "Weakened",
        "color": "yellow",
        "desc": "Defense reduced.",
        "icon": "[yellow]WKN[/yellow]",
    },
    "slowed": {
        "name": "Slowed",
        "color": "dim white",
        "desc": "Movement and reactions impaired.",
        "icon": "[dim]SLW[/dim]",
    },
}


def apply_effect(target_effects: list, effect_id: str, turns: int, value: int = 5):
    """Apply an effect to a target's effect list.

    Stacking: bleeding/poison/burning stack additively.
    Others refresh duration.
    """
    stackable = {"bleeding", "poisoned", "burning"}
    for e in target_effects:
        if e["id"] == effect_id:
            if effect_id in stackable:
                e["value"] += value
                e["turns_left"] = max(e["turns_left"], turns)
            else:
                e["turns_left"] = max(e["turns_left"], turns)
            return
    target_effects.append({
        "id": effect_id,
        "name": ALL_EFFECTS[effect_id]["name"],
        "turns_left": turns,
        "value": value,
    })


def tick_effects(target_effects: list) -> list:
    """Process one turn of effects. Returns list of event messages.

    Caller applies damage messages to actual HP.
    """
    messages = []
    expired = []
    for e in target_effects:
        eid = e["id"]
        if eid in ("bleeding", "poisoned", "burning"):
            messages.append(("damage", e["value"], e["name"]))
        elif eid == "stunned":
            messages.append(("stun", 0, "Stunned"))
        e["turns_left"] -= 1
        if e["turns_left"] <= 0:
            expired.append(e)
            messages.append(("expired", 0, e["name"] + " wore off"))

    for e in expired:
        target_effects.remove(e)

    return messages


def has_effect(target_effects: list, effect_id: str) -> bool:
    return any(e["id"] == effect_id for e in target_effects)


def clear_effect(target_effects: list, effect_id: str):
    target_effects[:] = [e for e in target_effects if e["id"] != effect_id]


def clear_all(target_effects: list):
    target_effects.clear()


def format_effects(target_effects: list) -> str:
    """Return a compact colored string of active effects."""
    if not target_effects:
        return ""
    parts = []
    for e in target_effects:
        info = ALL_EFFECTS.get(e["id"], {})
        icon = info.get("icon", e["name"][:3].upper())
        parts.append(icon + "(" + str(e["turns_left"]) + ")")
    return " ".join(parts)


def get_effect_defense_mod(target_effects: list) -> int:
    """Return total defense penalty from active effects."""
    mod = 0
    for e in target_effects:
        if e["id"] == "weakened":
            mod -= e["value"]
    return mod
