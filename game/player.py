"""Player state - now with classes, levels, XP, and skills."""
import json
import os
from game.items import get_item, item_display_name
from game import config
from game.character import (
    CLASSES, SKILL_DEFINITIONS, get_class,
    xp_for_level, xp_to_next_level, level_up_rewards,
)


class Player:
    """Represents the player character with full RPG progression."""

    def __init__(self, name: str = "Ghost", class_id: str = "street_samurai"):
        self.name = name
        self.class_id = class_id
        self.class_name = ""

        # Level / XP
        self.level = 1
        self.xp = 0

        # Unspent points
        self.unspent_stat_points = 0
        self.unspent_skill_points = 0

        # Core stats (1-10 typical, can go higher with cyberware)
        self.stats = {
            "strength": 5,
            "agility": 5,
            "tech": 5,
            "perception": 5,
            "charisma": 5,
            "defense": 0,
        }

        # Skills (0-10)
        self.skills = {skill: 0 for skill in SKILL_DEFINITIONS}

        # HP & resources
        self.hp = config.STARTING_HP
        self.max_hp = config.STARTING_HP
        self.credits = config.STARTING_CREDITS
        self.location = "slums"

        # Inventory
        self.inventory = []

        # Equipment
        self.equipped = {
            "weapon": None,
            "armor": None,
        }

        # Cyberware
        self.cyberware = []

        # Quests
        self.quests = []

        # Faction reputation
        self.reputation = {
            "gangs": 0,
            "corpo": 0,
            "hackers": 0,
            "scavengers": 0,
            "police": 0,
        }

        # AI history
        self.history = []

        # Exploration
        self.visited = {"slums"}
        self.looted_locations = set()

        # Combat state
        self.in_combat = False
        self.current_enemy = None

        # Apply class
        if class_id and class_id in CLASSES:
            self._apply_class(class_id)

    # ============== CLASS APPLICATION ==============

    def _apply_class(self, class_id: str):
        """Apply class bonuses, gear, etc. Called once at character creation."""
        cls = get_class(class_id)
        if not cls:
            return

        self.class_id = class_id
        self.class_name = cls["name"]

        # Stat bonuses
        for stat, bonus in cls.get("stat_bonuses", {}).items():
            if stat in self.stats:
                self.stats[stat] += bonus

        # Skill bonuses
        for skill, bonus in cls.get("skill_bonuses", {}).items():
            if skill in self.skills:
                self.skills[skill] += bonus

        # HP bonus
        hp_bonus = cls.get("hp_bonus", 0)
        self.max_hp += hp_bonus
        self.hp = self.max_hp

        # Credits
        self.credits = cls.get("starting_credits", config.STARTING_CREDITS)

        # Gear
        self.inventory = list(cls.get("starting_gear", []))

        starting_weapon = cls.get("starting_weapon")
        starting_armor = cls.get("starting_armor")
        if starting_weapon and starting_weapon in self.inventory:
            self.equipped["weapon"] = starting_weapon
        if starting_armor and starting_armor in self.inventory:
            self.equipped["armor"] = starting_armor

        # Reputation
        for faction, val in cls.get("starting_rep", {}).items():
            if faction in self.reputation:
                self.reputation[faction] = val

    # ============== MOVEMENT ==============

    def move(self, direction: str, world: dict):
        loc = world.get(self.location, {})
        exits = loc.get("exits", {})
        if direction in exits:
            self.location = exits[direction]
            new_loc = self.location not in self.visited
            self.visited.add(self.location)
            return True, "You move " + direction + ".", new_loc
        return False, "No exit that way.", False

    # ============== INVENTORY ==============

    def add_item(self, item_id: str) -> str:
        item = get_item(item_id)
        if not item:
            return ""
        self.inventory.append(item_id)
        return "Picked up: " + item_display_name(item_id)

    def remove_item(self, item_id: str) -> bool:
        if item_id in self.inventory:
            self.inventory.remove(item_id)
            return True
        return False

    def has_item(self, item_id: str) -> bool:
        return item_id in self.inventory

    def use_item(self, item_id: str) -> str:
        if not self.has_item(item_id):
            return "You don't have that."
        item = get_item(item_id)
        if not item:
            return "Unknown item."

        if item["type"] == "consumable":
            heal = item.get("heal", 0)
            heal_bonus = self.skills.get("first_aid", 0) // 2
            heal += heal_bonus
            old_hp = self.hp
            self.hp = min(self.max_hp, self.hp + heal)
            self.remove_item(item_id)
            msg = "Used " + item_display_name(item_id) + ". Restored " + str(self.hp - old_hp) + " HP."
            if heal_bonus > 0:
                msg += " (First Aid +" + str(heal_bonus) + ")"
            return msg

        if item["type"] == "cyberware":
            return self.install_cyberware(item_id)

        return "You can't use that directly. Try EQUIP."

    def equip(self, item_id: str) -> str:
        if not self.has_item(item_id):
            return "You don't have that."
        item = get_item(item_id)
        if not item:
            return "Unknown item."

        slot = item["type"]
        if slot not in ("weapon", "armor"):
            return "You can't equip that."

        old = self.equipped.get(slot)
        self.equipped[slot] = item_id
        msg = "Equipped " + item_display_name(item_id)
        if old:
            msg += " (was " + item_display_name(old) + ")"
        return msg

    def install_cyberware(self, item_id: str) -> str:
        item = get_item(item_id)
        if item["type"] != "cyberware":
            return "Not cyberware."
        if item_id in self.cyberware:
            return "Already installed."
        self.cyberware.append(item_id)
        self.remove_item(item_id)
        stat = item.get("stat")
        bonus = item.get("bonus", 0)
        if stat in self.stats:
            self.stats[stat] += bonus
        return "Installed " + item_display_name(item_id) + " (+" + str(bonus) + " " + stat + ")"

    # ============== COMBAT STATS ==============

    def get_attack_damage(self) -> int:
        weapon = self.equipped.get("weapon")
        base = 3
        if weapon:
            item = get_item(weapon)
            if item:
                base = item.get("damage", 3)
        return base + self.stats["strength"] // 2 + self.skills.get("combat", 0) // 2

    def get_defense(self) -> int:
        d = self.stats["defense"]
        armor = self.equipped.get("armor")
        if armor:
            item = get_item(armor)
            if item:
                d += item.get("defense", 0)
        return d

    def get_hit_chance_bonus(self) -> float:
        return self.skills.get("combat", 0) * 0.02

    def take_damage(self, amount: int) -> int:
        actual = max(1, amount - self.get_defense())
        self.hp = max(0, self.hp - actual)
        return actual

    def heal(self, amount: int):
        self.hp = min(self.max_hp, self.hp + amount)

    def is_alive(self) -> bool:
        return self.hp > 0

    # ============== ECONOMY ==============

    def add_credits(self, amount: int):
        self.credits = max(0, self.credits + amount)

    def spend_credits(self, amount: int) -> bool:
        if self.credits >= amount:
            self.credits -= amount
            return True
        return False

    # ============== FACTIONS ==============

    def adjust_reputation(self, faction: str, delta: int):
        if faction in self.reputation:
            self.reputation[faction] = max(-100, min(100, self.reputation[faction] + delta))

    # ============== QUESTS ==============

    def add_quest(self, title: str, description: str):
        for q in self.quests:
            if q["title"] == title:
                return
        self.quests.append({"title": title, "description": description, "done": False})

    def complete_quest(self, title: str):
        for q in self.quests:
            if q["title"] == title and not q["done"]:
                q["done"] = True
                return True
        return False

    # ============== XP / LEVELING ==============

    def gain_xp(self, amount: int) -> list:
        """Award XP. Returns list of level-up event messages."""
        self.xp += amount
        events = ["+ " + str(amount) + " XP"]

        while self.xp >= xp_for_level(self.level + 1):
            self.level += 1
            rewards = level_up_rewards(self.level)
            self.max_hp += rewards["hp_gain"]
            self.hp = self.max_hp
            self.unspent_stat_points += rewards["stat_points"]
            self.unspent_skill_points += rewards["skill_points"]

            events.append(">>> LEVEL UP! Now level " + str(self.level) + " <<<")
            events.append("    +" + str(rewards["hp_gain"]) + " Max HP (fully healed)")
            if rewards["stat_points"] > 0:
                events.append("    +" + str(rewards["stat_points"]) + " stat point")
            events.append("    +" + str(rewards["skill_points"]) + " skill points")
            events.append("    Type 'levelup' to spend points")

        return events

    def spend_stat_point(self, stat: str) -> str:
        if self.unspent_stat_points <= 0:
            return "No stat points to spend."
        if stat not in self.stats:
            return "Unknown stat: " + stat
        if stat == "defense":
            return "Defense is gained from gear and cyberware, not points."
        self.stats[stat] += 1
        self.unspent_stat_points -= 1
        return "Increased " + stat + " to " + str(self.stats[stat])

    def spend_skill_point(self, skill: str) -> str:
        if self.unspent_skill_points <= 0:
            return "No skill points to spend."
        if skill not in self.skills:
            return "Unknown skill: " + skill
        if self.skills[skill] >= 10:
            return skill + " is already maxed (10)."
        self.skills[skill] += 1
        self.unspent_skill_points -= 1
        return "Increased " + skill + " to " + str(self.skills[skill])

    def xp_progress_string(self) -> str:
        next_total = xp_for_level(self.level + 1)
        return str(self.xp) + " / " + str(next_total)

    # ============== HISTORY ==============

    def add_to_history(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        if len(self.history) > config.HISTORY_LIMIT:
            self.history = self.history[-config.HISTORY_LIMIT:]

    # ============== SAVE / LOAD ==============

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "class_id": self.class_id,
            "class_name": self.class_name,
            "level": self.level,
            "xp": self.xp,
            "unspent_stat_points": self.unspent_stat_points,
            "unspent_skill_points": self.unspent_skill_points,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "credits": self.credits,
            "location": self.location,
            "stats": self.stats,
            "skills": self.skills,
            "inventory": self.inventory,
            "equipped": self.equipped,
            "cyberware": self.cyberware,
            "quests": self.quests,
            "reputation": self.reputation,
            "history": self.history,
            "visited": list(self.visited),
            "looted_locations": list(self.looted_locations),
        }

    @classmethod
    def from_dict(cls, data: dict):
        p = cls.__new__(cls)
        p.name = data.get("name", "Ghost")
        p.class_id = data.get("class_id", "")
        p.class_name = data.get("class_name", "")
        p.level = data.get("level", 1)
        p.xp = data.get("xp", 0)
        p.unspent_stat_points = data.get("unspent_stat_points", 0)
        p.unspent_skill_points = data.get("unspent_skill_points", 0)
        p.hp = data.get("hp", config.STARTING_HP)
        p.max_hp = data.get("max_hp", config.STARTING_HP)
        p.credits = data.get("credits", config.STARTING_CREDITS)
        p.location = data.get("location", "slums")
        p.stats = data.get("stats", {})
        p.skills = data.get("skills", {})
        for s in SKILL_DEFINITIONS:
            if s not in p.skills:
                p.skills[s] = 0
        p.inventory = data.get("inventory", [])
        p.equipped = data.get("equipped", {"weapon": None, "armor": None})
        p.cyberware = data.get("cyberware", [])
        p.quests = data.get("quests", [])
        p.reputation = data.get("reputation", {})
        p.history = data.get("history", [])
        p.visited = set(data.get("visited", ["slums"]))
        p.looted_locations = set(data.get("looted_locations", []))
        p.in_combat = False
        p.current_enemy = None
        return p

    def save(self, filename: str = None):
        os.makedirs(config.SAVE_DIR, exist_ok=True)
        path = os.path.join(config.SAVE_DIR, filename or config.AUTOSAVE_FILE)
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        return path

    @classmethod
    def load(cls, filename: str = None):
        path = os.path.join(config.SAVE_DIR, filename or config.AUTOSAVE_FILE)
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            return cls.from_dict(json.load(f))
