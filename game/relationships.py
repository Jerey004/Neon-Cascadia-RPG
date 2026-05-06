"""Relationship tiers for NPCs and factions.

Both NPCs and factions track a -100 to +100 score with tiered labels.

Faction reputation affects: shop prices, NPC reception, hostile encounters,
quest availability.

NPC relationships affect: dialogue tone, willingness to help, prices, betrayals.
"""

# ============================================================
# RELATIONSHIP TIERS
# ============================================================
# (score >= threshold, tier_name, color, description)
TIERS = [
    (75,  "Sworn Ally",  "bold green",  "Will die for you. Discounts, free help, special quests."),
    (40,  "Friend",      "green",       "Trusted. Discounts, helps in fights, shares info."),
    (15,  "Friendly",    "cyan",        "Likes you. Mild discounts. Will talk freely."),
    (-15, "Neutral",     "white",       "No strong feelings. Standard prices."),
    (-40, "Wary",        "yellow",      "Doesn't trust you. Inflated prices. May refuse service."),
    (-75, "Hostile",     "red",         "Hates you. Will not deal. Calls guards/gang."),
    (-100,"Sworn Enemy", "bold red",    "Will attack on sight. Bounty on your head."),
]


def get_tier(score: int) -> dict:
    """Get tier info for a given relationship score."""
    for threshold, name, color, desc in TIERS:
        if score >= threshold:
            return {
                "name": name,
                "color": color,
                "desc": desc,
                "score": score,
                "threshold": threshold,
            }
    # Should never reach here since -100 is in TIERS
    return {"name": "Unknown", "color": "white", "desc": "", "score": score, "threshold": 0}


def get_tier_name(score: int) -> str:
    return get_tier(score)["name"]


def format_relationship(score: int) -> str:
    """Return a colored display string for a score."""
    tier = get_tier(score)
    return "[" + tier["color"] + "]" + tier["name"] + " (" + str(score) + ")[/" + tier["color"] + "]"


# ============================================================
# PRICE MODIFIERS
# ============================================================
# Friendlier NPCs/factions give better prices.

def get_buy_modifier(relationship_score: int) -> float:
    """Multiplier on buy prices (lower = cheaper)."""
    if relationship_score >= 75:
        return 0.6   # 40% off
    elif relationship_score >= 40:
        return 0.75  # 25% off
    elif relationship_score >= 15:
        return 0.9   # 10% off
    elif relationship_score >= -15:
        return 1.0   # full price
    elif relationship_score >= -40:
        return 1.5   # 50% markup
    else:
        return 2.5   # punitive


def get_sell_modifier(relationship_score: int) -> float:
    """Multiplier on sell prices (higher = better return)."""
    if relationship_score >= 75:
        return 0.7   # 70% of value (great)
    elif relationship_score >= 40:
        return 0.6
    elif relationship_score >= 15:
        return 0.5   # 50% (default)
    elif relationship_score >= -15:
        return 0.4
    elif relationship_score >= -40:
        return 0.25
    else:
        return 0.1   # ripoff


# ============================================================
# REPUTATION CHANGES (helper)
# ============================================================

REP_EVENTS = {
    "killed_their_member":      -25,
    "stole_from_them":          -15,
    "refused_their_quest":       -3,
    "completed_their_quest":     15,
    "saved_their_member":        20,
    "did_them_favor":            10,
    "betrayed_them":            -50,
    "killed_their_enemy":         8,
    "spent_money_with_them":      2,
}


def apply_event(rep_dict: dict, faction: str, event: str) -> int:
    """Apply a rep event. Returns the change applied."""
    delta = REP_EVENTS.get(event, 0)
    if faction in rep_dict:
        old = rep_dict[faction]
        rep_dict[faction] = max(-100, min(100, old + delta))
        return rep_dict[faction] - old
    return 0
