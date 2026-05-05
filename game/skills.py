"""Skill check resolution system.

Used for things like:
- "I try to hack the door" -> hacking check
- "I try to talk my way past the guard" -> persuasion check
- "I look for hidden items" -> perception check

Skill checks return a result tier (critical/success/partial/failure) and a roll value.
The AI prompt is then enriched with the result so the LLM can narrate accordingly.
"""
import random


# Difficulty class (DC) thresholds
DC_TRIVIAL = 5
DC_EASY = 10
DC_MEDIUM = 15
DC_HARD = 20
DC_VERY_HARD = 25
DC_LEGENDARY = 30


DC_NAMES = {
    DC_TRIVIAL: "trivial",
    DC_EASY: "easy",
    DC_MEDIUM: "medium",
    DC_HARD: "hard",
    DC_VERY_HARD: "very hard",
    DC_LEGENDARY: "legendary",
}


def skill_check(player, skill: str, dc: int, stat: str = None) -> dict:
    """Perform a skill check.

    Roll: d20 + skill_level + (stat_bonus / 2 if stat provided)

    Returns dict:
        tier: "critical_success" | "success" | "partial" | "failure" | "critical_failure"
        roll: the d20 roll
        total: roll + modifiers
        dc: the difficulty
        skill: skill name used
        margin: total - dc (positive = passed, negative = failed)
    """
    roll = random.randint(1, 20)
    skill_val = player.skills.get(skill, 0)
    stat_bonus = 0
    if stat:
        stat_val = player.stats.get(stat, 5)
        stat_bonus = (stat_val - 5) // 2  # +1 for every 2 stat above 5

    total = roll + skill_val + stat_bonus
    margin = total - dc

    if roll == 20:
        tier = "critical_success"
    elif roll == 1:
        tier = "critical_failure"
    elif margin >= 5:
        tier = "success"
    elif margin >= 0:
        tier = "partial"
    else:
        tier = "failure"

    return {
        "tier": tier,
        "roll": roll,
        "total": total,
        "dc": dc,
        "dc_name": DC_NAMES.get(dc, "custom"),
        "skill": skill,
        "skill_val": skill_val,
        "stat": stat,
        "stat_bonus": stat_bonus,
        "margin": margin,
    }


def detect_skill_check(action: str) -> tuple:
    """Heuristically figure out if a player action implies a skill check.

    Returns (skill, dc, stat) or (None, None, None) if no check needed.
    The AI handles narrative; this just adds dice context for the prompt.
    """
    a = action.lower()

    # Barter (check first since "haggle" might match other keywords)
    if any(k in a for k in ["haggle", "barter", "negotiate price", "lower the price", "cheaper"]):
        return ("barter", DC_MEDIUM, "charisma")

    # Hacking
    if any(k in a for k in ["hack", "bypass", "decrypt", "crack", "jack into", "netrun", "break ice"]):
        return ("hacking", DC_MEDIUM, "tech")

    # Stealth
    if any(k in a for k in ["sneak", "hide", "stealth", "slip past", "unseen", "shadows", "palm "]):
        return ("stealth", DC_MEDIUM, "agility")

    # Persuasion
    if any(k in a for k in ["convince", "persuade", "negotiate", "talk down", "reason with", "charm", "flirt"]):
        return ("persuasion", DC_MEDIUM, "charisma")

    # Intimidation
    if any(k in a for k in ["threaten", "intimidate", "scare", "menace"]):
        return ("intimidation", DC_MEDIUM, "strength")

    # Perception
    if any(k in a for k in ["search", "look for", "examine", "investigate", "scan", "inspect", "check for"]):
        return ("perception", DC_EASY, "perception")

    # First aid
    if any(k in a for k in ["heal", "patch up", "treat", "first aid", "bandage", "stabilize"]):
        return ("first_aid", DC_EASY, "tech")

    # Tech repair
    if any(k in a for k in ["repair", "fix", "jury rig", "tinker", "modify", "rewire"]):
        return ("tech_repair", DC_MEDIUM, "tech")

    # Streetwise
    if any(k in a for k in ["ask around", "rumors", "word on the street", "contacts", "who knows"]):
        return ("streetwise", DC_EASY, "charisma")

    return (None, None, None)


def format_check_for_ai(check: dict) -> str:
    """Format a skill check result for inclusion in the AI prompt."""
    if not check:
        return ""

    tier_descriptions = {
        "critical_success": "EXCEPTIONAL SUCCESS - the action goes far better than expected",
        "success": "SUCCESS - the action works as intended",
        "partial": "PARTIAL SUCCESS - the action works but with some complication or cost",
        "failure": "FAILURE - the action does not succeed",
        "critical_failure": "CRITICAL FAILURE - the action fails badly with serious consequence",
    }

    return (
        "\n[SKILL CHECK: " + check["skill"].upper() +
        " (DC " + str(check["dc"]) + " " + check["dc_name"] + ")] " +
        "Player rolled " + str(check["total"]) +
        " (d20=" + str(check["roll"]) +
        " + skill " + str(check["skill_val"]) +
        " + stat " + str(check["stat_bonus"]) + ")" +
        " -> " + tier_descriptions.get(check["tier"], check["tier"]) +
        ". Narrate accordingly."
    )
