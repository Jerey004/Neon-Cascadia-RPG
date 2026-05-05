"""Ollama AI client with structured response parsing and rich character context."""
import re
import requests
from game import config
from game.items import item_display_name


def query_ollama(history: list, context: str) -> str:
    """Send context + history to Ollama, get narrative response."""
    messages = [{"role": "system", "content": config.GAME_SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": context})

    try:
        resp = requests.post(
            config.OLLAMA_HOST + "/api/chat",
            json={
                "model": config.OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
            },
            timeout=config.OLLAMA_TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]

    except requests.ConnectionError:
        return ("[ERROR: Cannot reach Ollama at " + config.OLLAMA_HOST +
                ". Check Tailscale connection.]")
    except requests.Timeout:
        return "[ERROR: Ollama timed out. The model may be loading - try again.]"
    except Exception as e:
        return "[ERROR: " + str(e) + "]"


def build_context(player, location: dict, action: str) -> str:
    """Package game state into a rich prompt for the LLM."""
    inv = ", ".join(item_display_name(i) for i in player.inventory) or "empty"
    weapon = item_display_name(player.equipped["weapon"]) if player.equipped["weapon"] else "fists"
    armor = item_display_name(player.equipped["armor"]) if player.equipped["armor"] else "none"
    cyberware = ", ".join(item_display_name(c) for c in player.cyberware) or "none"
    quests = ", ".join(q["title"] for q in player.quests if not q["done"]) or "none"
    npcs = ", ".join(location.get("npcs", [])) or "none"

    rep_summary = ", ".join(f + ":" + str(v) for f, v in player.reputation.items())

    # Top skills (>= 3) so AI knows what player is good at
    top_skills = sorted(player.skills.items(), key=lambda x: -x[1])
    notable_skills = [s + " " + str(v) for s, v in top_skills if v >= 3][:5]
    skill_summary = ", ".join(notable_skills) or "no notable skills"

    # Stats
    stats_summary = ", ".join(s + " " + str(v) for s, v in player.stats.items() if s != "defense")

    context = (
        "=== PLAYER PROFILE ===\n"
        "Name: " + player.name + " | Class: " + (player.class_name or "Runner") +
        " | Level " + str(player.level) + "\n"
        "HP " + str(player.hp) + "/" + str(player.max_hp) +
        " | Credits " + str(player.credits) + "\n"
        "Stats: " + stats_summary + "\n"
        "Notable Skills: " + skill_summary + "\n"
        "Weapon: " + weapon + " | Armor: " + armor + "\n"
        "Cyberware: " + cyberware + "\n"
        "Inventory: " + inv + "\n"
        "Active Quests: " + quests + "\n"
        "Faction Reputation: " + rep_summary + "\n\n"
        "=== CURRENT LOCATION ===\n"
        + location["name"] + " - " + location["description"] + "\n"
        "NPCs Present: " + npcs + "\n\n"
        "=== PLAYER ACTION ===\n"
        + action + "\n\n"
        "Narrate the result in character. Use the player's class and skills to "
        "color how NPCs react and what they say. A Netrunner reads tech differently "
        "than a Street Samurai. A Fixer talks differently than an Ex-Corpo. "
        "Stay atmospheric, under 150 words. End with [ACTION_OPTIONS: ...]."
    )
    return context


def parse_response(text: str) -> dict:
    """Extract structured tags from AI response."""
    result = {
        "narrative": text,
        "options": [],
        "combat_start": None,
        "quest_offer": None,
        "item_gains": [],
        "item_loses": [],
        "credits": 0,
    }

    m = re.search(r"\[ACTION_OPTIONS:\s*(.*?)\]", text, re.IGNORECASE)
    if m:
        result["options"] = [o.strip() for o in m.group(1).split("|") if o.strip()]
        text = text.replace(m.group(0), "")

    m = re.search(r"\[COMBAT_START:\s*([^\]]+)\]", text, re.IGNORECASE)
    if m:
        enemy = m.group(1).strip().lower().replace(" ", "_")
        result["combat_start"] = enemy
        text = text.replace(m.group(0), "")

    # Strict format: [QUEST_OFFER: title | description]
    m = re.search(r"\[QUEST_OFFER:\s*([^|\]]+)\|([^\]]+)\]", text, re.IGNORECASE)
    if m:
        result["quest_offer"] = (m.group(1).strip(), m.group(2).strip())
        text = text.replace(m.group(0), "")
    else:
        # Loose fallback: [QUEST_OFFER: title] with no pipe separator
        m = re.search(r"\[QUEST_OFFER:\s*([^\]]+)\]", text, re.IGNORECASE)
        if m:
            title = m.group(1).strip()
            result["quest_offer"] = (title, "Objective unknown - ask for details.")
            text = text.replace(m.group(0), "")

    for m in re.finditer(r"\[ITEM_GAIN:\s*([^\]]+)\]", text, re.IGNORECASE):
        result["item_gains"].append(m.group(1).strip().lower().replace(" ", "_"))
    text = re.sub(r"\[ITEM_GAIN:[^\]]+\]", "", text, flags=re.IGNORECASE)

    for m in re.finditer(r"\[ITEM_LOSE:\s*([^\]]+)\]", text, re.IGNORECASE):
        result["item_loses"].append(m.group(1).strip().lower().replace(" ", "_"))
    text = re.sub(r"\[ITEM_LOSE:[^\]]+\]", "", text, flags=re.IGNORECASE)

    m = re.search(r"\[CREDITS:\s*([+-]?\d+)\]", text, re.IGNORECASE)
    if m:
        result["credits"] = int(m.group(1))
        text = text.replace(m.group(0), "")

    result["narrative"] = text.strip()
    return result
