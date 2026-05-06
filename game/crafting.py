"""Crafting system.

Tech class (and others with high tech_repair/engineering) can combine
components to create new items, upgrade weapons, or brew consumables.

Recipes have:
  ingredients: {item_id: count}
  result: item_id
  result_count: int
  required_skill: {skill: min_level}
  class_bonus: [class_id] - these classes get a guaranteed success

Skill check: tech_repair or engineering roll vs DC determines quality:
  critical_success: result + bonus
  success:          normal result
  partial:          result but reduced count or degraded
  failure:          lose half ingredients
  critical_failure: lose all ingredients
"""

RECIPES = {
    # ============== CONSUMABLES ==============
    "brew_stim_pack": {
        "name": "Brew Stim Pack",
        "desc": "Combine painkillers and synth-coffee into a combat stim.",
        "ingredients": {"cheap_painkillers": 2, "synth_coffee": 1},
        "result": "stim_pack",
        "result_count": 1,
        "required_skill": {"tech_repair": 2},
        "skill_used": "tech_repair",
        "dc": 10,
        "class_bonus": ["medic", "tech"],
    },
    "brew_trauma_kit": {
        "name": "Craft Trauma Kit",
        "desc": "Upgrade two stim packs into a full trauma kit.",
        "ingredients": {"stim_pack": 2},
        "result": "trauma_kit",
        "result_count": 1,
        "required_skill": {"first_aid": 4},
        "skill_used": "first_aid",
        "dc": 15,
        "class_bonus": ["medic"],
    },
    "brew_neural_clarifier": {
        "name": "Synthesize Neural Clarifier",
        "desc": "Distil a cognitive enhancement from memory boosters.",
        "ingredients": {"mem_booster": 2},
        "result": "neural_clarifier",
        "result_count": 1,
        "required_skill": {"biology": 3, "tech_repair": 2},
        "skill_used": "biology",
        "dc": 14,
        "class_bonus": ["medic", "netrunner"],
    },

    # ============== WEAPONS ==============
    "upgrade_pistol": {
        "name": "Upgrade Pistol",
        "desc": "Attach scrap modifications to improve a cheap pistol.",
        "ingredients": {"cheap_pistol": 1, "scrap_metal": 3},
        "result": "tactical_smg",
        "result_count": 1,
        "required_skill": {"tech_repair": 4, "engineering": 2},
        "skill_used": "engineering",
        "dc": 16,
        "class_bonus": ["tech"],
    },
    "craft_emp_grenade": {
        "name": "Craft EMP Grenade",
        "desc": "Build an EMP device from salvaged electronics.",
        "ingredients": {"scrap_metal": 4, "data_chip_corrupted": 2},
        "result": "emp_grenade",
        "result_count": 1,
        "required_skill": {"engineering": 3},
        "skill_used": "engineering",
        "dc": 14,
        "class_bonus": ["tech"],
    },
    "craft_virus_chip": {
        "name": "Compile Virus Chip",
        "desc": "Write a custom ICE breaker from corrupted data.",
        "ingredients": {"data_chip_corrupted": 3},
        "result": "virus_chip",
        "result_count": 1,
        "required_skill": {"hacking": 4},
        "skill_used": "hacking",
        "dc": 16,
        "class_bonus": ["netrunner", "tech"],
    },

    # ============== ARMOR ==============
    "reinforce_jacket": {
        "name": "Reinforce Jacket",
        "desc": "Sew scrap metal into a leather jacket for better protection.",
        "ingredients": {"leather_jacket": 1, "scrap_metal": 4},
        "result": "kevlar_vest",
        "result_count": 1,
        "required_skill": {"tech_repair": 3},
        "skill_used": "tech_repair",
        "dc": 13,
        "class_bonus": ["tech"],
    },

    # ============== CYBERWARE ==============
    "assemble_neural_jack": {
        "name": "Assemble Neural Jack",
        "desc": "Build a basic data port from salvaged components.",
        "ingredients": {"scrap_metal": 5, "data_chip_corrupted": 2},
        "result": "neural_jack",
        "result_count": 1,
        "required_skill": {"tech_repair": 5, "engineering": 3},
        "skill_used": "tech_repair",
        "dc": 18,
        "class_bonus": ["tech"],
    },
    "assemble_low_light": {
        "name": "Assemble Low-Light Lenses",
        "desc": "Craft basic night vision from salvaged optics.",
        "ingredients": {"scrap_metal": 3, "data_chip_corrupted": 1},
        "result": "low_light_lenses",
        "result_count": 1,
        "required_skill": {"tech_repair": 4},
        "skill_used": "tech_repair",
        "dc": 16,
        "class_bonus": ["tech"],
    },
}


def get_recipe(recipe_id: str) -> dict:
    return RECIPES.get(recipe_id)


def list_craftable(player) -> list:
    """Return list of (recipe_id, recipe) tuples the player can attempt."""
    craftable = []
    for rid, recipe in RECIPES.items():
        # Check if player meets skill requirements
        reqs = recipe.get("required_skill", {})
        meets_reqs = all(player.skills.get(s, 0) >= v for s, v in reqs.items())
        if not meets_reqs:
            continue
        # Check if player has ingredients (show even if partial)
        has_all = True
        for item_id, count in recipe["ingredients"].items():
            player_count = sum(1 for i in player.inventory if i == item_id)
            if player_count < count:
                has_all = False
                break
        craftable.append((rid, recipe, has_all))
    return craftable


def attempt_craft(player, recipe_id: str) -> dict:
    """Attempt to craft a recipe.

    Returns:
      success: bool
      result: item_id or None
      result_count: int
      message: str
      lost_ingredients: list of item_ids lost
    """
    import random
    from game import skills as skills_mod

    recipe = RECIPES.get(recipe_id)
    if not recipe:
        return {"success": False, "message": "Unknown recipe.", "result": None,
                "result_count": 0, "lost_ingredients": []}

    # Check ingredients
    for item_id, count in recipe["ingredients"].items():
        have = sum(1 for i in player.inventory if i == item_id)
        if have < count:
            return {"success": False,
                    "message": "Missing ingredients: " + item_id.replace("_", " "),
                    "result": None, "result_count": 0, "lost_ingredients": []}

    # Skill check
    skill = recipe["skill_used"]
    dc = recipe["dc"]
    stat_map = {
        "tech_repair": "tech", "engineering": "tech",
        "hacking": "tech", "first_aid": "tech", "biology": "tech",
    }
    stat = stat_map.get(skill, "tech")

    # Class bonus = automatic success threshold lower
    if player.class_id in recipe.get("class_bonus", []):
        dc -= 3

    check = skills_mod.skill_check(player, skill, dc, stat)
    tier = check["tier"]

    # Always consume ingredients
    lost = []
    for item_id, count in recipe["ingredients"].items():
        for _ in range(count):
            player.inventory.remove(item_id)
            lost.append(item_id)

    if tier == "critical_failure":
        # Lose everything, no result
        return {
            "success": False,
            "message": "Critical failure! The work explodes in your hands. Ingredients lost.",
            "result": None, "result_count": 0, "lost_ingredients": lost,
        }
    elif tier == "failure":
        # Refund half ingredients
        refund = lost[: len(lost) // 2]
        for item_id in refund:
            player.inventory.append(item_id)
        return {
            "success": False,
            "message": "Craft failed. Recovered some materials.",
            "result": None, "result_count": 0,
            "lost_ingredients": [i for i in lost if i not in refund],
        }
    elif tier == "partial":
        count = max(1, recipe["result_count"] - 1) if recipe["result_count"] > 1 else 1
        result_item = recipe["result"]
        for _ in range(count):
            player.inventory.append(result_item)
        return {
            "success": True,
            "message": "Partial success. Made " + str(count) + "x " +
                       result_item.replace("_", " ").title() + " (substandard)",
            "result": result_item, "result_count": count, "lost_ingredients": [],
        }
    else:  # success or critical_success
        bonus = 1 if tier == "critical_success" else 0
        count = recipe["result_count"] + bonus
        result_item = recipe["result"]
        for _ in range(count):
            player.inventory.append(result_item)
        msg = "Crafted " + str(count) + "x " + result_item.replace("_", " ").title()
        if tier == "critical_success":
            msg += " (EXCEPTIONAL - bonus item!)"
        return {
            "success": True,
            "message": msg,
            "result": result_item, "result_count": count, "lost_ingredients": [],
        }
