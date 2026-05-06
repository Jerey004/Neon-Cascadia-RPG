"""Combat system - now with status effects, companion attacks, and boss phases."""
import random
from game import config
from game.enemies import get_enemy
from game.bosses import get_boss, is_boss
from game.items import get_item, item_display_name, roll_loot, ITEMS
from game.status_effects import (
    apply_effect, tick_effects, has_effect,
    clear_effect, format_effects, get_effect_defense_mod,
)


class Combat:
    """Manages a single combat encounter (regular or boss)."""

    def __init__(self, player, enemy_id: str):
        self.player = player
        self.enemy_id = enemy_id

        # Check if this is a boss fight
        boss = get_boss(enemy_id)
        if boss:
            self.enemy = boss
            self.is_boss_fight = True
        else:
            self.enemy = get_enemy(enemy_id)
            self.is_boss_fight = False

        self.enemy_max_hp = self.enemy["hp"]
        self.enemy_effects = []      # Status effects on the enemy
        self.phase_two_active = False
        self.log = []

    # ============== ROLL HELPERS ==============

    def _crit(self) -> bool:
        return random.random() < config.CRIT_CHANCE

    def _hit(self, agility: int = 5, bonus: float = 0.0) -> bool:
        return random.random() < min(0.95, 0.6 + agility * 0.04 + bonus)

    # ============== PLAYER ACTIONS ==============

    def player_attack(self) -> str:
        # Stunned = skip turn
        if has_effect(self.player.status_effects, "stunned"):
            clear_effect(self.player.status_effects, "stunned")
            return "You are stunned and lose your turn."

        if not self._hit(self.player.stats["agility"],
                         self.player.get_hit_chance_bonus()):
            return "You swing and miss."

        dmg = self.player.get_attack_damage()
        crit = self._crit()
        if crit:
            dmg = int(dmg * config.CRIT_MULTIPLIER)

        # Check if weapon has special effects
        weapon_id = self.player.equipped.get("weapon")
        weapon_item = get_item(weapon_id) if weapon_id else None

        # Apply defense (minus weakness effect)
        enemy_def = max(0, self.enemy["defense"] + get_effect_defense_mod(self.enemy_effects))
        actual = max(1, dmg - enemy_def)
        self.enemy["hp"] -= actual

        msg = "You hit the " + self.enemy["name"] + " for " + str(actual) + " damage"
        if crit:
            msg += " (CRITICAL)"

        # Weapon special effects
        if weapon_item:
            if weapon_item.get("stun") and random.random() < 0.35:
                apply_effect(self.enemy_effects, "stunned", turns=1, value=0)
                msg += " [STUNNED]"
            elif weapon_id in ("emp_grenade",) and random.random() < 0.5:
                apply_effect(self.enemy_effects, "hacked", turns=3, value=0)
                msg += " [HACKED]"

        msg += "."
        return msg

    def player_use_item(self, item_id: str) -> str:
        return self.player.use_item(item_id)

    def player_flee(self) -> tuple:
        if has_effect(self.player.status_effects, "slowed"):
            return False, "You're slowed - can't escape."
        agility = self.player.stats["agility"]
        chance = config.FLEE_CHANCE + agility * 0.02
        if random.random() < chance:
            return True, "You break off and escape into the shadows."
        return False, "You try to flee but " + self.enemy["name"] + " blocks your path."

    # ============== COMPANION ACTION ==============

    def companion_attack(self) -> str:
        """If player has an active companion, they attack too."""
        comp = self.player.companion
        if not comp or not comp.is_available():
            return ""
        if self.is_enemy_dead():
            return ""
        return comp.combat_attack(self.enemy)

    # ============== ENEMY ACTION ==============

    def enemy_attack(self) -> str:
        # Check enemy stun
        if has_effect(self.enemy_effects, "stunned"):
            clear_effect(self.enemy_effects, "stunned")
            return "The " + self.enemy["name"] + " is stunned and loses a turn."

        if not self._hit():
            return "The " + self.enemy["name"] + " attacks but misses."

        # Boss phase 2 damage bonus
        bonus_dmg = 0
        if self.is_boss_fight and self.phase_two_active:
            bonus_dmg = self.enemy.get("phase_two_damage_bonus", 0)

        dmg = self.enemy["damage"] + bonus_dmg
        actual = self.player.take_damage(dmg)

        msg = "The " + self.enemy["name"] + " hits you for " + str(actual) + " damage."

        # Random enemy special attacks
        if random.random() < 0.15:
            etype = random.choice(["bleeding", "slowed", "weakened"])
            apply_effect(self.player.status_effects, etype, turns=2, value=4)
            msg += " [" + etype.upper() + "]"

        return msg

    # ============== STATUS EFFECT TICK ==============

    def tick_player_effects(self) -> list:
        """Process player status effects at end of turn. Returns damage events."""
        msgs = []
        events = tick_effects(self.player.status_effects)
        for kind, value, name in events:
            if kind == "damage":
                self.player.hp = max(0, self.player.hp - value)
                msgs.append("[" + name + "] " + str(value) + " damage")
            elif kind == "expired":
                msgs.append(name)
        return msgs

    def tick_enemy_effects(self) -> list:
        """Process enemy status effects. Returns event messages."""
        msgs = []
        events = tick_effects(self.enemy_effects)
        for kind, value, name in events:
            if kind == "damage":
                self.enemy["hp"] = max(0, self.enemy["hp"] - value)
                msgs.append("Enemy [" + name + "] " + str(value) + " damage")
            elif kind == "expired":
                msgs.append("Enemy: " + name)
        return msgs

    # ============== BOSS PHASE CHECKING ==============

    def check_phase_two(self) -> bool:
        """Returns True if boss just entered phase 2."""
        if not self.is_boss_fight or self.phase_two_active:
            return False
        threshold = self.enemy.get("phase_two_hp", self.enemy_max_hp // 2)
        if self.enemy["hp"] <= threshold:
            self.phase_two_active = True
            return True
        return False

    # ============================================================
    # LOOT
    # ============================================================

    def calculate_loot(self) -> dict:
        """Determine loot dropped by the enemy."""
        loot_items = []

        for item_id in self.enemy.get("guaranteed_loot", []):
            loot_items.append(item_id)

        enemy_level = self.enemy.get("level", 3)
        loot_chance = self.enemy.get("loot_chance", 0.5)
        loot_rolls = self.enemy.get("loot_rolls", 1)
        prefer = self.player.class_id if random.random() < 0.3 else None

        for _ in range(loot_rolls):
            if random.random() < loot_chance:
                rolled = roll_loot(enemy_level, count=1, prefer_class=prefer)
                loot_items.extend(rolled)

        c_min = self.enemy.get("credits_min", 0)
        c_max = self.enemy.get("credits_max", 0)
        credits = random.randint(c_min, c_max) if c_max > 0 else 0

        return {"credits": credits, "items": loot_items}

    # ============================================================
    # STATUS
    # ============================================================

    def is_enemy_dead(self) -> bool:
        return self.enemy["hp"] <= 0

    def is_player_dead(self) -> bool:
        return self.player.hp <= 0

    def status_line(self) -> str:
        fx = format_effects(self.player.status_effects)
        efx = format_effects(self.enemy_effects)
        line = ("ENEMY: " + self.enemy["name"] +
                " | HP " + str(max(0, self.enemy["hp"])) + "/" + str(self.enemy_max_hp) +
                " | Lv" + str(self.enemy.get("level", 1)))
        if efx:
            line += " " + efx
        if fx:
            line += "  YOU: " + fx
        return line
