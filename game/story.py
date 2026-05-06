"""Story bible for Neon Cascadia.

This module contains lore, recurring NPCs, faction backstory, and main plot
threads. It's all fed to the LLM so it can drive the story consistently.

The structure:
- WORLD_LORE: setting backstory & current situation
- FACTIONS: detailed faction info with leaders, agendas, conflicts
- RECURRING_NPCS: NPCs the AI should remember across encounters
- MAIN_PLOT: the central story thread
- STORY_HOOKS: ideas the AI can pull from when narrating
"""

# ============================================================
# WORLD LORE
# ============================================================
WORLD_LORE = """
NEO-CASCADIA, 2087 - the megacity that grew on the bones of Seattle, Portland,
and Vancouver after the Cascadia Quake of 2061. Three trillion-dollar arcologies
rule the skyline. Below them, twenty million people live in the rain.

THE CURRENT MOMENT:
- OmniCorp just acquired Kazumi Industries, completing a near-monopoly on cybernetics.
- A new street drug called BLACKWIRE is killing people - it's reportedly tied to a
  rogue AI that infects neural implants.
- The Crimson Fang gang and the Rail Rats are quietly at war for slum territory.
- An underground hacker collective called THE NULL POINTER is leaking corpo secrets,
  and OmniCorp is hunting them hard.
- Rumors of something LIVING in the deep sewers below the city. People go down. They
  don't come back.

THE PLAYER ARRIVES INTO THIS. The story should pull them into one or more of these
threads based on their class, choices, and faction reputation.
"""


# ============================================================
# FACTIONS (deep)
# ============================================================
FACTIONS = {
    "OmniCorp": {
        "type": "corpo",
        "leader": "CEO Ishikawa Yuto - cold, ruthless, has ten cybernetic upgrades",
        "agenda": "Total monopoly. Buy or destroy all competitors. Suppress THE NULL POINTER.",
        "headquarters": "OmniCorp Tower (corpo_plaza district)",
        "enemies": ["THE NULL POINTER", "Crimson Fang"],
        "allies": ["Neo-Cascadia Police"],
        "story_hooks": [
            "Hiring deniable freelancers to kidnap a defector scientist",
            "Black-bagging hackers in the night",
            "Selling experimental cyberware that fails dangerously",
        ],
    },
    "Crimson Fang": {
        "type": "gang",
        "leader": "Riza Volkov - charismatic, brutal, missing one eye, replaced with chrome",
        "agenda": "Control all slum territory. Push out the Rail Rats. Defy the corpos.",
        "headquarters": "Hidden in the abandoned arcade",
        "enemies": ["Rail Rats", "OmniCorp"],
        "allies": ["Some scavengers"],
        "story_hooks": [
            "Recruiting new members from the slums",
            "Hijacking corpo shipments",
            "Threatening shopkeepers who pay protection",
        ],
    },
    "Rail Rats": {
        "type": "gang",
        "leader": "Hex Murakami - paranoid genius, runs a smuggling ring through the magrail tunnels",
        "agenda": "Smuggle anything for anyone. Survive the Crimson Fang. Hide from corpos.",
        "headquarters": "Undercity Rail Station",
        "enemies": ["Crimson Fang", "Neo-Cascadia Police"],
        "allies": ["THE NULL POINTER (sometimes)"],
        "story_hooks": [
            "Looking for couriers who won't ask questions",
            "Selling smuggled cyberware at half price",
            "Dealing with the BLACKWIRE drug crisis",
        ],
    },
    "THE NULL POINTER": {
        "type": "hackers",
        "leader": "Ghost - identity unknown. Communicates only through encrypted channels.",
        "agenda": "Expose corpo crimes. Free the data. Liberate cyberware from corpo control.",
        "headquarters": "The Null Pointer (hidden in net district)",
        "enemies": ["OmniCorp", "Neo-Cascadia Police"],
        "allies": ["Some Rail Rats"],
        "story_hooks": [
            "Recruiting netrunners for a major data heist",
            "Hiding fugitive whistleblowers",
            "Investigating BLACKWIRE - they think OmniCorp made it",
        ],
    },
    "Scavengers": {
        "type": "scavengers",
        "leader": "Old Gris - lost both legs, runs the scrap trade from a wheeled chair",
        "agenda": "Strip the dead industrial zones. Survive. Keep the deep tunnels secret.",
        "headquarters": "Old Kazumi Factory",
        "enemies": ["The thing in the sewers"],
        "allies": ["Tech freelancers"],
        "story_hooks": [
            "Lost three scavengers in the sewers last week",
            "Found something strange in the factory ruins",
            "Selling salvaged smartguns and combat armor cheap",
        ],
    },
}


# ============================================================
# RECURRING NPCS
# ============================================================
RECURRING_NPCS = {
    "Old Marta": {
        "location": "slums",
        "role": "Food vendor, neighborhood mom-figure",
        "personality": "Gruff but caring. Knows everyone. Survived three gang wars.",
        "knowledge": [
            "Who's new in the slums",
            "Which kids have gone missing",
            "Rumors about BLACKWIRE deaths",
        ],
        "can_offer": ["Find My Grandson (Riku has gone missing)"],
    },
    "Vex": {
        "location": "fixer_office",
        "role": "Fixer - middlewoman for jobs",
        "personality": "Sharp, paranoid, never sits with her back to the door.",
        "knowledge": [
            "What jobs are paying right now",
            "Which corpo middle-managers are corrupt",
            "Where the action is",
        ],
        "can_offer": [
            "Data Snatch (steal a shard from corpo courier - 500 credits)",
            "Bodyguard Run (escort a defector through the slums - 800 credits)",
            "Wetwork (an OmniCorp exec is corrupting someone - 1500 credits)",
        ],
    },
    "Doc Sato": {
        "location": "clinic",
        "role": "Ripperdoc - back-alley cybersurgeon",
        "personality": "Tired, kind, drinks too much. Never asks questions.",
        "knowledge": [
            "All the cyberware on the streets",
            "Why people keep coming in with BLACKWIRE symptoms",
            "Which gangs are getting modified",
        ],
        "can_offer": ["Investigate the BLACKWIRE Outbreak"],
        "services": ["Heals 50 HP for 30 credits", "Installs cyberware safely"],
    },
    "Ghost": {
        "location": "hacker_den",
        "role": "Leader of THE NULL POINTER",
        "personality": "Never shows their face. Voice modulator. Speaks in riddles.",
        "knowledge": [
            "Everything happening in the wires",
            "OmniCorp's deepest secrets",
            "Who BLACKWIRE's real maker is",
        ],
        "can_offer": [
            "Crack the OmniCorp Mainframe (major heist)",
            "Free a captured netrunner (rescue mission)",
        ],
    },
    "Zhen": {
        "location": "neon_market",
        "role": "Black-market ripperdoc & gear seller",
        "personality": "Loud, friendly, will absolutely overcharge you.",
        "knowledge": [
            "What's hot in the cyberware black market",
            "Who just bought what",
        ],
        "services": ["Sells weapons and cyberware at 1.5x value"],
    },
    "Riza Volkov": {
        "location": "abandoned_arcade",
        "role": "Crimson Fang gang leader",
        "personality": "Charismatic. Speaks softly, listens carefully, kills suddenly.",
        "knowledge": ["Crimson Fang operations", "Where OmniCorp's weak points are"],
        "can_offer": ["Hit a Rail Rat smuggler", "Defend Crimson Fang turf"],
    },
    "Hex Murakami": {
        "location": "undercity_rail",
        "role": "Rail Rat boss",
        "personality": "Twitchy. Brilliant. Has six monitors and a paranoid AI watching them.",
        "knowledge": ["All smuggling routes", "Corpo movement through the city"],
        "can_offer": ["Run a package through Crimson Fang turf", "Hijack a corpo van"],
    },
}


# ============================================================
# MAIN PLOT THREAD
# ============================================================
MAIN_PLOT = """
THE BLACKWIRE CONSPIRACY (overarching plot - drip out clues over time)

ACT 1 - HOOK: People in the slums are dying from a new drug called BLACKWIRE.
Old Marta has lost neighbors. Doc Sato has seen six deaths. The street-level
mystery: who's making it and why?

ACT 2 - REVELATION: BLACKWIRE isn't a drug - it's a virus designed to infect
cybernetic implants. The Null Pointer suspects OmniCorp made it as a way to
control rebellious cyborgs. They want proof.

ACT 3 - HEIST: The player must infiltrate OmniCorp Tower to retrieve the
master file proving BLACKWIRE is corpo bioweapon research. Multiple paths:
hack in, fight in, talk in, sneak in.

ACT 4 - CHOICE: Once they have the data, multiple endings:
  - Leak to the public (massive corpo retaliation, gang uprising)
  - Sell back to OmniCorp (rich but hated)
  - Give to Null Pointer (they release it strategically)
  - Use it personally (blackmail Ishikawa, become a power player)

The AI should weave these threads in. Don't dump it all at once. Let it emerge
through NPC conversations and discovered clues.
"""


# ============================================================
# STORY HOOKS (random ideas the AI can pull)
# ============================================================
STORY_HOOKS = [
    "A child runs past you, terrified, clutching something. Two suits chase her.",
    "Sirens wail in the distance. Police lights paint the rain blue and red.",
    "A drunk in the corner is crying about his dead brother - 'they got him with the wire'.",
    "Graffiti says: 'OMNICORP KILLS - WAKE UP'.",
    "A homeless veteran offers to sell information for a stim pack.",
    "A dying ganger crawls into view, riddled with bullets, gasping a name: 'Volkov...'",
    "Your contact texts: 'Don't go to Block 7. Trust me.'",
    "A shop window flickers, showing a news report you can almost catch.",
    "Someone has been watching you. You feel it. You always feel it.",
    "A street preacher screams about 'the worm in the wires' and points at your cyberware.",
]


def get_story_context() -> str:
    """Generate a condensed lore + plot summary for the LLM system prompt."""
    return WORLD_LORE + "\n\n" + MAIN_PLOT


def get_npc_context(npc_name: str) -> str:
    """If the NPC is recurring, return their character bible."""
    for key, npc in RECURRING_NPCS.items():
        if key.lower() in npc_name.lower() or npc_name.lower() in key.lower():
            text = "RECURRING NPC: " + key + "\n"
            text += "Role: " + npc["role"] + "\n"
            text += "Personality: " + npc["personality"] + "\n"
            text += "They know about: " + ", ".join(npc["knowledge"]) + "\n"
            if npc.get("can_offer"):
                text += "Can offer quests: " + "; ".join(npc["can_offer"]) + "\n"
            if npc.get("services"):
                text += "Services: " + "; ".join(npc["services"]) + "\n"
            return text
    return ""


def get_faction_context(faction_name: str) -> str:
    """Return faction info."""
    for key, fac in FACTIONS.items():
        if key.lower() in faction_name.lower() or faction_name.lower() in key.lower():
            text = "FACTION: " + key + "\n"
            text += "Leader: " + fac["leader"] + "\n"
            text += "Agenda: " + fac["agenda"] + "\n"
            text += "Enemies: " + ", ".join(fac["enemies"]) + "\n"
            return text
    return ""
