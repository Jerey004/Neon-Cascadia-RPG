"""AI engine - Ollama client and context assembly.

Every call to the LLM is built to serve the core purpose:
  - Rich player state so NPCs react to who you ARE
  - NPC memory so conversations feel persistent
  - Story context so the world feels coherent
  - Skill results so your build actually matters
  - World lore so NPCs reference the same reality
"""
import re
import requests
from game import config
from game.items import item_display_name
from game.story import get_story_context, get_npc_context, STORY_HOOKS
import random


# ============================================================
# OLLAMA CLIENT
# ============================================================

def query_ollama(history: list, context: str) -> str:
    """Send assembled context + conversation history to Ollama."""

    # System prompt includes the purpose-driven NPC rules + world lore
    full_system = config.GAME_SYSTEM_PROMPT + "\n\n=== CURRENT WORLD STATE ===\n"
    full_system += get_story_context()

    messages = [{"role": "system", "content": full_system}]
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
                ". Check Tailscale is running on both devices.]")
    except requests.Timeout:
        return "[ERROR: Ollama timed out. Try a smaller model or increase OLLAMA_TIMEOUT.]"
    except Exception as e:
        return "[ERROR: " + str(e) + "]"


# ============================================================
# CONTEXT ASSEMBLY
# ============================================================

def build_context(player, location: dict, action: str,
                  npc_memory_ctx: str = "", skill_ctx: str = "") -> str:
    """Assemble the complete context for a player action.

    Layers:
      1. Player identity - who they are (class, level, skills, reputation)
      2. Player state - current HP, credits, inventory, quests, cyberware
      3. Location context - where they are, who's there
      4. NPC memory - what this specific NPC remembers (if talking to one)
      5. Skill check result - how well they're doing what they're trying to do
      6. Action itself + instructions for the AI
      7. Ambient story hook (occasional) - keeps the world feeling alive
    """
    # ── Identity ──────────────────────────────────────────────
    inv = ", ".join(item_display_name(i) for i in player.inventory) or "empty"

    weapon = item_display_name(player.equipped["weapon"]) if player.equipped.get("weapon") else "fists"
    armor_pieces = []
    for slot in ("head", "body", "hands", "feet"):
        item_id = player.equipped.get(slot)
        if item_id:
            armor_pieces.append(item_display_name(item_id))
    armor = ", ".join(armor_pieces) if armor_pieces else "none"

    cyberware = ", ".join(item_display_name(c) for c in player.cyberware) or "none"
    quests_active = [q["title"] for q in player.quests if not q["done"]]
    quests = ", ".join(quests_active) or "none"

    # ── Skill summary ────────────────────────────────────────
    top_skills = sorted(player.skills.items(), key=lambda x: -x[1])
    strong_skills = [s + " " + str(v) for s, v in top_skills if v >= 3][:6]
    skill_summary = ", ".join(strong_skills) or "no strong skills yet"

    # ── Equipment skill mods ─────────────────────────────────
    from game.items import get_skill_mods_summary
    gear_mods = get_skill_mods_summary(player)
    gear_bonus_str = ""
    if gear_mods:
        gear_bonus_str = " [gear bonuses: " + ", ".join(
            "+" + str(v) + " " + k for k, v in gear_mods.items()) + "]"

    # ── Faction reputation summary ────────────────────────────
    from game import relationships
    rep_lines = []
    for faction, score in player.reputation.items():
        tier = relationships.get_tier_name(score)
        if tier != "Neutral":
            rep_lines.append(faction + ": " + tier + " (" + str(score) + ")")
    rep_summary = ", ".join(rep_lines) if rep_lines else "all neutral"

    # ── NPCs present ─────────────────────────────────────────
    npcs = ", ".join(location.get("npcs", [])) or "none"

    # ── Time context ─────────────────────────────────────────
    time_ctx = player.time.period_name + " (" + player.time.time_string() + ")"

    # ── Companion ────────────────────────────────────────────
    comp_ctx = ""
    if player.companion and player.companion.is_active:
        comp_ctx = "\nCOMPANION PRESENT: " + player.companion.full_name

    # ── NPC bible (from story.py) for named NPCs in action ───
    npc_bible = ""
    for npc_full in location.get("npcs", []):
        clean = npc_full.split("(")[0].strip()
        if clean.lower() in action.lower():
            bible = get_npc_context(clean)
            if bible:
                npc_bible = "\n" + bible
            break

    # ── Status effects ────────────────────────────────────────
    from game.status_effects import format_effects
    status_str = format_effects(player.status_effects)
    status_ctx = "\nPLAYER STATUS EFFECTS: " + status_str if status_str else ""

    # ── Occasional ambient hook ───────────────────────────────
    # 1 in 7 actions gets a random story hook to keep the world feeling alive
    ambient = ""
    if random.random() < 0.14:
        ambient = ("\n\n=== AMBIENT WORLD DETAIL ===\n"
                   "Weave this into the narration naturally if it fits: "
                   + random.choice(STORY_HOOKS))

    # ── Assemble ─────────────────────────────────────────────
    context = (
        "=== WHO THE PLAYER IS ===\n"
        "Name: " + player.name + "  |  Class: " + (player.class_name or "Runner") +
        "  |  Level " + str(player.level) + "\n"
        "HP: " + str(player.hp) + "/" + str(player.max_hp) +
        "  |  Credits: " + str(player.credits) + "\n"
        "Stats: str " + str(player.stats.get("strength", 5)) +
        " agi " + str(player.stats.get("agility", 5)) +
        " tech " + str(player.stats.get("tech", 5)) +
        " per " + str(player.stats.get("perception", 5)) +
        " cha " + str(player.stats.get("charisma", 5)) + "\n"
        "Strong Skills: " + skill_summary + gear_bonus_str + "\n"
        "Weapon: " + weapon + "  |  Armor: " + armor + "\n"
        "Cyberware: " + cyberware + "\n"
        "Faction Standing: " + rep_summary + "\n"
        "Active Quests: " + quests + "\n"
        "Time: " + time_ctx +
        status_ctx + comp_ctx +
        "\n\n=== WHERE THEY ARE ===\n"
        + location["name"] + " [" + location.get("district", "Unknown") + " district]\n"
        + location["description"] + "\n"
        "NPCs present: " + npcs +
        npc_bible +
        "\n\n=== NPC MEMORY ===" +
        (("\n" + npc_memory_ctx) if npc_memory_ctx else "\n(No prior history with NPCs here)") +
        "\n\n=== PLAYER ACTION ===\n"
        + action +
        "\n\n=== INSTRUCTIONS ===\n"
        "Narrate what happens. Voice the NPC authentically. Use their history with the player.\n"
        "DO NOT decide what the player says, thinks, or does next.\n"
        "Make the player's class and skills color how the world reacts to them.\n"
        "Reference faction standing naturally - it affects how NPCs treat the player.\n"
        "If this is a significant moment, raise the stakes. The world is watching."
        + (skill_ctx if skill_ctx else "") +
        ambient
    )
    return context


# ============================================================
# RESPONSE PARSER
# ============================================================

def parse_response(text: str) -> dict:
    """Extract structured game tags from AI response.

    Tags supported:
      [COMBAT_START: enemy_id]
      [QUEST_OFFER: Title | Description]
      [QUEST_COMPLETE: Title]
      [ITEM_GAIN: item_name]
      [ITEM_LOSE: item_name]
      [CREDITS: +50] / [CREDITS: -20]
      [JOURNAL: clue text to record]
    """
    result = {
        "narrative": text,
        "options": [],
        "combat_start": None,
        "quest_offer": None,
        "quest_complete": None,
        "item_gains": [],
        "item_loses": [],
        "credits": 0,
        "journal_entry": None,
    }

    # ACTION_OPTIONS
    m = re.search(r"\[ACTION_OPTIONS:\s*(.*?)\]", text, re.IGNORECASE)
    if m:
        result["options"] = [o.strip() for o in m.group(1).split("|") if o.strip()]
        text = text.replace(m.group(0), "")

    # COMBAT_START
    m = re.search(r"\[COMBAT_START:\s*([^\]]+)\]", text, re.IGNORECASE)
    if m:
        result["combat_start"] = m.group(1).strip().lower().replace(" ", "_")
        text = text.replace(m.group(0), "")

    # QUEST_OFFER (strict: title | description)
    m = re.search(r"\[QUEST_OFFER:\s*([^|\]]+)\|([^\]]+)\]", text, re.IGNORECASE)
    if m:
        result["quest_offer"] = (m.group(1).strip(), m.group(2).strip())
        text = text.replace(m.group(0), "")
    else:
        # Loose fallback: no pipe
        m = re.search(r"\[QUEST_OFFER:\s*([^\]]+)\]", text, re.IGNORECASE)
        if m:
            result["quest_offer"] = (m.group(1).strip(), "Objective unknown - ask for details.")
            text = text.replace(m.group(0), "")

    # QUEST_COMPLETE
    m = re.search(r"\[QUEST_COMPLETE:\s*([^\]]+)\]", text, re.IGNORECASE)
    if m:
        result["quest_complete"] = m.group(1).strip()
        text = text.replace(m.group(0), "")

    # ITEM_GAIN (multiple)
    for m in re.finditer(r"\[ITEM_GAIN:\s*([^\]]+)\]", text, re.IGNORECASE):
        result["item_gains"].append(m.group(1).strip().lower().replace(" ", "_"))
    text = re.sub(r"\[ITEM_GAIN:[^\]]+\]", "", text, flags=re.IGNORECASE)

    # ITEM_LOSE (multiple)
    for m in re.finditer(r"\[ITEM_LOSE:\s*([^\]]+)\]", text, re.IGNORECASE):
        result["item_loses"].append(m.group(1).strip().lower().replace(" ", "_"))
    text = re.sub(r"\[ITEM_LOSE:[^\]]+\]", "", text, flags=re.IGNORECASE)

    # CREDITS
    m = re.search(r"\[CREDITS:\s*([+-]?\d+)\]", text, re.IGNORECASE)
    if m:
        result["credits"] = int(m.group(1))
        text = text.replace(m.group(0), "")

    # JOURNAL (new - AI can trigger journal entries)
    m = re.search(r"\[JOURNAL:\s*([^\]]+)\]", text, re.IGNORECASE)
    if m:
        result["journal_entry"] = m.group(1).strip()
        text = text.replace(m.group(0), "")

    result["narrative"] = text.strip()
    return result


def get_random_story_hook() -> str:
    """Return a random ambient story hook."""
    return random.choice(STORY_HOOKS)
