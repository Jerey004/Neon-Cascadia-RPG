"""Turn-based combat system."""
import random
from game import config
from game.enemies import get_enemy
from game.items import get_item, item_display_name


class Combat:
    """Manages a single combat encounter."""

    def __init__(self, player, enemy_id: str):
        self.player = player
        enemy_data = get_enemy(enemy_id)
        if not enemy_data:
            # Fallback generic enemy if AI-named one not in DB
            enemy_data = {
                "name": enemy_id.replace("_", " ").title(),
                "hp": 40, "damage": 10, "defense": 2,
                "credits": 20, "loot": [], "loot_chance": 0,
                "desc": "A hostile threat.",
            }
        self.enemy_id = enemy_id
        self.enemy = enemy_data
        self.enemy_max_hp = enemy_data["hp"]
        self.log = []

    # ============== ROLLS ==============

    def _roll_crit(self) -> bool:
        return random.random() < config.CRIT_CHANCE

    def _roll_hit(self, agility: int = 5) -> bool:
        # Higher agility = better hit chance (cap at 95%)
        chance = 0.6 + (agility * 0.04)
        return random.random() < min(0.95, chance)

    # ============== ACTIONS ==============

    def player_attack(self) -> str:
        if not self._roll_hit(self.player.stats["agility"]):
            return "You swing and miss."

        dmg = self.player.get_attack_damage()
        crit = self._roll_crit()
        if crit:
            dmg = int(dmg * config.CRIT_MULTIPLIER)

        actual = max(1, dmg - self.enemy["defense"])
        self.enemy["hp"] -= actual

        msg = "You hit the " + self.enemy["name"] + " for " + str(actual) + " damage"
        if crit:
            msg += " (CRITICAL)"
        msg += "."
        return msg

    def player_use_item(self, item_id: str) -> str:
        return self.player.use_item(item_id)

    def player_flee(self) -> tuple:
        """Returns (success, message)."""
        agility = self.player.stats["agility"]
        chance = config.FLEE_CHANCE + (agility * 0.02)
        if random.random() < chance:
            return True, "You break off and escape into the shadows."
        return False, "You try to flee but the " + self.enemy["name"] + " blocks your path."

    def enemy_attack(self) -> str:
        if not self._roll_hit():
            return "The " + self.enemy["name"] + " attacks but misses."
        dmg = self.enemy["damage"]
        actual = self.player.take_damage(dmg)
        return "The " + self.enemy["name"] + " hits you for " + str(actual) + " damage."

    # ============== STATUS ==============

    def is_enemy_dead(self) -> bool:
        return self.enemy["hp"] <= 0

    def is_player_dead(self) -> bool:
        return self.player.hp <= 0

    def reward_loot(self) -> list:
        """Returns list of reward messages."""
        rewards = []
        # Credits
        c = self.enemy.get("credits", 0)
        if c > 0:
            self.player.add_credits(c)
            rewards.append("Looted " + str(c) + " credits.")

        # Items
        for item_id in self.enemy.get("loot", []):
            if random.random() < self.enemy.get("loot_chance", 0):
                self.player.add_item(item_id)
                rewards.append("Found: " + item_display_name(item_id))
        return rewards

    def status_line(self) -> str:
        return ("ENEMY: " + self.enemy["name"] +
                " | HP " + str(max(0, self.enemy["hp"])) + "/" + str(self.enemy_max_hp))
