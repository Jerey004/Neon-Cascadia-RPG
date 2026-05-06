"""Companion system.

A companion NPC can join the player, fight in combat, and comment on events.
Currently supports: Street Kid Riku (unlocked via Old Marta's quest).

Companion stats scale with player level.
In combat, companion takes their own turn - simple AI: attacks if enemy alive.
Companion can be dismissed, can die (becomes incapacitated until healed).
"""

COMPANIONS = {
    "riku": {
        "name": "Riku",
        "full_name": "Street Kid Riku",
        "description": "Slum kid with cybereyes and a big mouth. Surprisingly dangerous.",
        "unlock_quest": "Find My Grandson",
        "base_damage": 8,
        "base_defense": 2,
        "personality": "Reckless, loyal, curious. Calls you 'choom'. Hates corpos.",
        "combat_lines": [
            "I got his back!",
            "Let's go, choom!",
            "Is that all you got?",
            "Don't die on me!",
        ],
        "idle_lines": [
            "This place smells like old chrome.",
            "You ever wonder what's really in those corpo towers?",
            "Marta's gonna worry. Let's not die.",
            "I know a shortcut through here. Probably.",
        ],
    },
}


class Companion:
    """Active companion traveling with the player."""

    def __init__(self, companion_id: str, player_level: int = 1):
        # Accept either "riku" or "Riku" etc.
        base = COMPANIONS.get(companion_id.lower(),
               COMPANIONS.get(companion_id, {}))
        self.companion_id = companion_id.lower()
        self.name = base.get("name", "Unknown")
        self.full_name = base.get("full_name", "Unknown")
        self.personality = base.get("personality", "")
        self.combat_lines = base.get("combat_lines", [])
        self.idle_lines = base.get("idle_lines", [])

        # Stats scale with player level
        self.max_hp = 30 + (player_level * 8)
        self.hp = self.max_hp
        self.damage = base.get("base_damage", 8) + (player_level * 2)
        self.defense = base.get("base_defense", 2) + player_level
        self.is_active = True        # Following player
        self.is_incapacitated = False  # Downed but alive

    def is_available(self) -> bool:
        return self.is_active and not self.is_incapacitated

    def take_damage(self, amount: int) -> int:
        actual = max(1, amount - self.defense)
        self.hp = max(0, self.hp - actual)
        if self.hp == 0:
            self.is_incapacitated = True
        return actual

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)
        if self.hp > 0:
            self.is_incapacitated = False

    def combat_attack(self, enemy: dict) -> str:
        """Companion attacks during player's combat turn."""
        import random
        if self.is_incapacitated:
            return self.name + " is down and can't fight."
        if random.random() < 0.75:   # 75% hit chance
            dmg = max(1, self.damage - enemy.get("defense", 0))
            enemy["hp"] -= dmg
            line = random.choice(self.combat_lines) if self.combat_lines else ""
            msg = self.name + " hits for " + str(dmg) + " damage."
            if line:
                msg += ' "' + line + '"'
            return msg
        return self.name + " misses."

    def random_idle_comment(self) -> str | None:
        """Occasionally says something while exploring."""
        import random
        if self.idle_lines and random.random() < 0.15:
            return self.name + ': "' + random.choice(self.idle_lines) + '"'
        return None

    def status_line(self) -> str:
        hp_color = "green" if self.hp > self.max_hp * 0.5 else (
            "yellow" if self.hp > self.max_hp * 0.25 else "red")
        status = " [INCAP]" if self.is_incapacitated else ""
        return ("[bold]" + self.name + "[/bold] " +
                "[" + hp_color + "]HP " + str(self.hp) +
                "/" + str(self.max_hp) + "[/" + hp_color + "]" + status)

    def to_dict(self) -> dict:
        return {
            "companion_id": self.companion_id,
            "name": self.name,
            "full_name": self.full_name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "damage": self.damage,
            "defense": self.defense,
            "is_active": self.is_active,
            "is_incapacitated": self.is_incapacitated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Companion":
        c = cls.__new__(cls)
        c.companion_id = data.get("companion_id", "riku")
        base = COMPANIONS.get(c.companion_id, {})
        c.name = data.get("name", "Riku")
        c.full_name = data.get("full_name", "Street Kid Riku")
        c.personality = base.get("personality", "")
        c.combat_lines = base.get("combat_lines", [])
        c.idle_lines = base.get("idle_lines", [])
        c.hp = data.get("hp", 50)
        c.max_hp = data.get("max_hp", 50)
        c.damage = data.get("damage", 10)
        c.defense = data.get("defense", 3)
        c.is_active = data.get("is_active", True)
        c.is_incapacitated = data.get("is_incapacitated", False)
        return c
