"""NPC memory system.

Tracks per-NPC conversation history, relationship events, and known facts.
This gets injected into AI prompts when the player talks to a known NPC,
making conversations feel persistent across sessions.

Each NPC entry:
  relationship_score: int (-100 to 100)
  history: [{"role": str, "content": str}] - last N exchanges
  known_facts: [str] - things this NPC knows about the player
  events: [str] - key things that happened between player and NPC
  first_met: str - location/context of first meeting
  times_met: int
"""

MAX_NPC_HISTORY = 10   # Keep last 10 exchanges per NPC


class NPCMemory:
    """Stores per-NPC state across sessions."""

    def __init__(self):
        self.npcs = {}   # {npc_name: {history, score, events, facts, ...}}

    def _ensure(self, npc_name: str) -> dict:
        clean = npc_name.split("(")[0].strip()
        if clean not in self.npcs:
            self.npcs[clean] = {
                "score": 0,
                "history": [],
                "events": [],
                "known_facts": [],
                "first_met": "",
                "times_met": 0,
            }
        return self.npcs[clean]

    def record_meeting(self, npc_name: str, location: str):
        entry = self._ensure(npc_name)
        entry["times_met"] += 1
        if not entry["first_met"]:
            entry["first_met"] = location

    def add_exchange(self, npc_name: str, player_action: str, npc_response: str):
        """Record a conversation exchange with this NPC."""
        entry = self._ensure(npc_name)
        entry["history"].append({
            "role": "user",
            "content": "PLAYER: " + player_action,
        })
        entry["history"].append({
            "role": "assistant",
            "content": "NPC: " + npc_response[:300],  # truncate long responses
        })
        # Trim to last N exchanges
        if len(entry["history"]) > MAX_NPC_HISTORY * 2:
            entry["history"] = entry["history"][-(MAX_NPC_HISTORY * 2):]

    def add_event(self, npc_name: str, event: str):
        """Log a significant event (quest given, betrayal, favor, etc.)."""
        entry = self._ensure(npc_name)
        if event not in entry["events"]:
            entry["events"].append(event)

    def add_known_fact(self, npc_name: str, fact: str):
        """Things the NPC now knows about the player."""
        entry = self._ensure(npc_name)
        if fact not in entry["known_facts"]:
            entry["known_facts"].append(fact)

    def adjust_score(self, npc_name: str, delta: int) -> int:
        entry = self._ensure(npc_name)
        entry["score"] = max(-100, min(100, entry["score"] + delta))
        return entry["score"]

    def get_score(self, npc_name: str) -> int:
        return self.npcs.get(npc_name.split("(")[0].strip(), {}).get("score", 0)

    def get_history(self, npc_name: str) -> list:
        clean = npc_name.split("(")[0].strip()
        return self.npcs.get(clean, {}).get("history", [])

    def build_context_for_ai(self, npc_name: str, player) -> str:
        """Generate a context block to inject into AI prompts for this NPC."""
        from game import relationships
        clean = npc_name.split("(")[0].strip()
        entry = self.npcs.get(clean)
        if not entry:
            return ""

        lines = ["=== NPC MEMORY: " + clean + " ==="]

        score = entry["score"]
        tier = relationships.get_tier_name(score)
        lines.append("Personal relationship with player: " + tier +
                     " (" + str(score) + ")")
        lines.append("Times met: " + str(entry["times_met"]))

        if entry["first_met"]:
            lines.append("First met at: " + entry["first_met"])

        if entry["events"]:
            lines.append("Key events: " + "; ".join(entry["events"][-5:]))

        if entry["known_facts"]:
            lines.append("Knows about player: " + "; ".join(entry["known_facts"][-5:]))

        if entry["history"]:
            lines.append("Recent exchanges (last " +
                         str(len(entry["history"]) // 2) + "):")
            for h in entry["history"][-6:]:   # Last 3 exchanges
                lines.append("  " + h["content"][:100])

        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {"npcs": self.npcs}

    @classmethod
    def from_dict(cls, data: dict) -> "NPCMemory":
        nm = cls()
        nm.npcs = data.get("npcs", {})
        return nm
