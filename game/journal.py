"""Player journal system.

Tracks:
  - Discovered lore entries (key facts about the world)
  - Investigation clues (BLACKWIRE conspiracy thread)
  - Named NPCs met
  - Locations of interest noted
  - General notes added by the player

Journal entries are added by the engine when:
  - Player picks up quest items
  - AI response contains [JOURNAL: entry text]
  - Player visits certain locations for the first time
  - Player completes certain quests

Auto-triggered entries are in LOCATION_DISCOVERIES and ITEM_DISCOVERIES.
"""

# Auto-journal entries triggered on first location visit
LOCATION_DISCOVERIES = {
    "sewers": (
        "MAINTENANCE TUNNELS",
        "The tunnels run deep under Block 9. Old maps show they connect to "
        "the factory ruins and something labeled SECTOR 7 that isn't on any "
        "public map. Someone has been living down here."
    ),
    "underground_lab": (
        "SECRET R&D LAB",
        "Hidden beneath the Null Pointer. The equipment is cutting-edge - "
        "OmniCorp markings on everything. Someone stripped it from their "
        "supply chain. The tanks of green fluid still have specimens in them. "
        "One of the labels reads: PROJECT BLACKWIRE - PHASE 2."
    ),
    "hacker_den": (
        "THE NULL POINTER",
        "An underground collective of netrunners. They call themselves the "
        "last free people in the city. Ghost leads them - nobody knows "
        "their real name. They're compiling evidence against OmniCorp."
    ),
    "executive_tower": (
        "OMNICORP TOWER",
        "The nerve center. CEO Ishikawa's office is on the 80th floor. "
        "The building has its own power grid, water supply, and private army. "
        "Whatever OmniCorp is hiding - the proof is here."
    ),
    "abandoned_arcade": (
        "THE ARCADE",
        "Crimson Fang territory. Riza Volkov runs operations from somewhere "
        "in the back. The gang is on a war footing - Rail Rats have been "
        "moving on their corners. And someone's been supplying the Rats "
        "with military-grade hardware."
    ),
    "sewer_chokepoint": (
        "SEWER JUNCTION",
        "Something is wrong here. The scavengers lost three people in this "
        "chamber last week. The walls have scratch marks at nine feet high. "
        "The water is contaminated with something - Bio-marker: UNKNOWN. "
        "This connects to the BLACKWIRE research somehow."
    ),
}

# Auto-journal entries triggered when picking up specific items
ITEM_DISCOVERIES = {
    "blackwire_sample": (
        "BLACKWIRE SAMPLE",
        "It looks like a drug but it isn't. The compound reacts to "
        "cyberware interfaces. Whoever designed this knew exactly what "
        "they were doing. Doc Sato might be able to analyze it. "
        "This is what's been killing people."
    ),
    "data_shard": (
        "ENCRYPTED DATA SHARD",
        "Heavy encryption - 256-bit minimum. Whatever is on this, "
        "someone didn't want it found. Ghost at the Null Pointer "
        "could crack it. Or it's bait."
    ),
    "encrypted_drive": (
        "ENCRYPTED HARD DRIVE",
        "Found in OmniCorp territory. Size suggests it contains "
        "substantial data - project files, personnel records, or "
        "financial transactions. The Null Pointer would pay well "
        "for this. So would OmniCorp, to get it back."
    ),
    "ishikawa_keycard": (
        "ISHIKAWA KEYCARD",
        "CEO-level biometric override. With this you can access any "
        "room in OmniCorp Tower. How this left the building is itself "
        "a mystery worth investigating. Someone inside is helping you."
    ),
}


class Journal:
    """Player journal - saves with player data."""

    def __init__(self):
        self.entries = []      # [{"title": str, "text": str, "turn": int}]
        self.clues = []        # [str] - BLACKWIRE investigation clues
        self.npcs_met = []     # [str] - NPC names encountered
        self.notes = []        # [str] - player-written notes
        self._entry_titles = set()   # Dedup

    def add_entry(self, title: str, text: str, turn: int = 0):
        """Add a lore entry (deduped by title)."""
        if title in self._entry_titles:
            return False
        self._entry_titles.add(title)
        self.entries.append({"title": title, "text": text, "turn": turn})
        return True

    def add_clue(self, clue: str):
        if clue not in self.clues:
            self.clues.append(clue)
            return True
        return False

    def meet_npc(self, name: str):
        clean = name.split("(")[0].strip()
        if clean not in self.npcs_met:
            self.npcs_met.append(clean)

    def add_note(self, note: str):
        self.notes.append(note)

    def to_dict(self) -> dict:
        return {
            "entries": self.entries,
            "clues": self.clues,
            "npcs_met": self.npcs_met,
            "notes": self.notes,
            "entry_titles": list(self._entry_titles),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Journal":
        j = cls()
        j.entries = data.get("entries", [])
        j.clues = data.get("clues", [])
        j.npcs_met = data.get("npcs_met", [])
        j.notes = data.get("notes", [])
        j._entry_titles = set(data.get("entry_titles", []))
        # Rebuild set from entries if missing
        if not j._entry_titles:
            j._entry_titles = {e["title"] for e in j.entries}
        return j

    def check_location(self, location_id: str, turn: int = 0) -> str | None:
        """Check if this location has an auto-journal entry. Returns title or None."""
        if location_id in LOCATION_DISCOVERIES:
            title, text = LOCATION_DISCOVERIES[location_id]
            if self.add_entry(title, text, turn):
                return title
        return None

    def check_item(self, item_id: str, turn: int = 0) -> str | None:
        """Check if picking up this item triggers a journal entry."""
        if item_id in ITEM_DISCOVERIES:
            title, text = ITEM_DISCOVERIES[item_id]
            if self.add_entry(title, text, turn):
                return title
        return None
