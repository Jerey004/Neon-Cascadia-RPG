"""Random encounter system.

Chance of ambush when:
 - Moving into a high-danger location
 - Resting / waiting in dangerous areas
 - After completing certain actions

Encounter chance = base_danger_rate[danger] + modifiers
Modifiers:
  - Stealth skill: -3% per level
  - Time of day (night adds 10%)
  - Faction reputation (hostile faction area adds 10%)
"""
import random
from game.world import WORLD
from game.enemies import ENEMIES, get_enemy

# Base encounter chance by danger level (0-5)
DANGER_ENCOUNTER_RATES = {
    0: 0.00,   # Safe (clinic, fixer office)
    1: 0.05,   # Low  (slums day)
    2: 0.12,   # Low-mid (market)
    3: 0.22,   # Mid (rail station)
    4: 0.35,   # High (factory, corpo)
    5: 0.50,   # Very high (robot pit, sewers)
}

# Which enemies can spawn at which locations (by enemy_id)
LOCATION_ENCOUNTER_TABLE = {
    "slums":            [("junkie", 50), ("lowlife_thug", 50)],
    "alley_network":    [("alley_ganger", 55), ("mugger", 30), ("feral_dog", 15)],
    "sewers":           [("mutant_rat", 40), ("scavenger", 40), ("rogue_drone", 20)],
    "neon_market":      [("pickpocket", 70), ("mugger", 30)],
    "back_alley":       [("mugger", 60), ("alley_ganger", 40)],
    "undercity_rail":   [("rail_ganger", 60), ("rogue_drone", 40)],
    "factory_ruins":    [("broken_servitor", 50), ("scavenger", 50)],
    "robot_pit":        [("broken_servitor", 40), ("rogue_drone", 40), ("war_machine", 20)],
    "abandoned_arcade": [("junkie", 50), ("alley_ganger", 50)],
    "hacker_den":       [],   # No random encounters (safe space)
    "underground_lab":  [("security_drone", 100)],
    "sewer_chokepoint": [("sewer_horror", 40), ("mutant_rat", 35), ("scavenger", 25)],
    "corpo_plaza":      [("corpo_security", 60), ("security_drone", 40)],
    "executive_tower":  [("elite_guard", 60), ("corpo_security", 40)],
    "clinic":           [],
    "fixer_office":     [],
}


def roll_encounter(player, location_id: str, time_is_night: bool = False) -> str | None:
    """Roll for a random encounter. Returns enemy_id or None."""
    location = WORLD.get(location_id, {})
    danger = location.get("danger", 0)
    base_chance = DANGER_ENCOUNTER_RATES.get(danger, 0.0)

    if base_chance == 0:
        return None

    # Stealth reduces encounter chance
    stealth = player.skills.get("stealth", 0)
    stealth_mod = stealth * 0.03   # 3% per level, max -30% at 10

    # Night is more dangerous
    night_mod = 0.10 if time_is_night else 0.0

    # Hostile faction in this district
    faction_mod = 0.0
    district = location.get("district", "")
    if district == "Corpo" and player.reputation.get("corpo", 0) < -40:
        faction_mod = 0.10
    elif district == "Slums" and player.reputation.get("gangs", 0) < -40:
        faction_mod = 0.10

    final_chance = min(0.90, base_chance + night_mod + faction_mod - stealth_mod)

    if random.random() < final_chance:
        return _pick_enemy(location_id)
    return None


def roll_rest_encounter(player, location_id: str) -> str | None:
    """Higher chance when resting - you're stationary."""
    location = WORLD.get(location_id, {})
    danger = location.get("danger", 0)
    # Double the normal chance when resting
    base = DANGER_ENCOUNTER_RATES.get(danger, 0.0) * 2.0
    stealth = player.skills.get("stealth", 0)
    final = min(0.95, base - stealth * 0.02)
    if random.random() < final:
        return _pick_enemy(location_id)
    return None


def _pick_enemy(location_id: str) -> str | None:
    """Pick a weighted random enemy for this location."""
    table = LOCATION_ENCOUNTER_TABLE.get(location_id, [])
    if not table:
        return None
    enemies, weights = zip(*table)
    return random.choices(enemies, weights=weights, k=1)[0]


def describe_encounter(enemy_id: str) -> str:
    """Return a short encounter description."""
    enemy = get_enemy(enemy_id)
    if not enemy:
        return "Something moves in the shadows."
    descs = {
        "junkie":           "A strung-out addict lunges at you from a doorway.",
        "lowlife_thug":     "A thug steps out of the shadows, blade drawn.",
        "pickpocket":       "You feel hands at your pockets — they bolt when you turn.",
        "mugger":           "Someone presses a knife to your ribs. 'Credits. Now.'",
        "feral_dog":        "A cyber-dog locks eyes on you and snarls.",
        "alley_ganger":     "A Crimson Fang ganger blocks your path. 'Wrong street.'",
        "rail_ganger":      "A Rail Rat enforcer drops from the ceiling.",
        "scavenger":        "A desperate scavenger charges from the dark.",
        "mutant_rat":       "Something dog-sized and wrong launches at you.",
        "broken_servitor":  "A factory bot turns toward you, red eyes online.",
        "rogue_drone":      "A security drone locks targeting on you.",
        "corpo_security":   "OmniCorp security moves to intercept.",
        "security_drone":   "A patrol drone opens fire.",
        "war_machine":      "The ground shakes. Something huge activates.",
        "elite_guard":      "A guard in black armor steps in front of you.",
        "sewer_horror":     "The water explodes. It has too many arms.",
        "ishikawa_executive": "A bodyguard in a suit recognizes your face.",
    }
    return descs.get(enemy_id, "A hostile figure moves to attack.")
