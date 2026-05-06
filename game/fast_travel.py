"""Fast travel system.

Players can fast-travel between visited rail/transit hubs using a transit card.
Travel is instant but costs 1 transit card use (or 15 credits without one).

Hub locations are the "transit nodes" of the city.
Fast travel is only available to previously visited locations.
"""

# Locations that serve as transit hubs
TRANSIT_HUBS = {
    "slums":            "Block 9 Terminal",
    "neon_market":      "Market Square Stop",
    "undercity_rail":   "Undercity Rail Central",
    "hacker_den":       "Net District Access",
    "corpo_plaza":      "OmniCorp Plaza Hub",
    "factory_ruins":    "Industrial Zone Stop",
    "sewers":           "Maintenance Access Point",
}

TRANSIT_COST_CREDITS = 15   # Cost without transit card
TRANSIT_COST_CARD = "transit_card"


def get_available_hubs(player) -> list:
    """Return list of (location_id, hub_name) tuples the player can fast-travel to.

    Only visited hubs are available (except current location).
    """
    available = []
    for loc_id, hub_name in TRANSIT_HUBS.items():
        if loc_id in player.visited and loc_id != player.location:
            available.append((loc_id, hub_name))
    return sorted(available, key=lambda x: x[1])


def can_fast_travel(player) -> tuple:
    """Check if fast travel is possible from current location.

    Returns (can_travel: bool, reason: str, has_card: bool)
    """
    # Must be at or near a transit hub (within 1 step)
    current = player.location
    if current in TRANSIT_HUBS:
        has_card = TRANSIT_COST_CARD in player.inventory
        return True, "At transit hub.", has_card

    # Check if adjacent to a hub
    from game.world import WORLD
    loc = WORLD.get(current, {})
    for direction, dest in loc.get("exits", {}).items():
        if dest in TRANSIT_HUBS:
            has_card = TRANSIT_COST_CARD in player.inventory
            return True, "Adjacent to " + TRANSIT_HUBS[dest] + ".", has_card

    return False, "No transit hub nearby. Find the Rail Station or a transit stop.", False


def fast_travel(player, destination_id: str) -> dict:
    """Execute fast travel.

    Returns {"success": bool, "message": str, "cost": str}
    """
    can, reason, has_card = can_fast_travel(player)
    if not can:
        return {"success": False, "message": reason, "cost": ""}

    if destination_id not in TRANSIT_HUBS:
        return {"success": False, "message": "Not a transit hub.", "cost": ""}

    if destination_id not in player.visited:
        return {"success": False, "message": "You haven't been there yet.", "cost": ""}

    if destination_id == player.location:
        return {"success": False, "message": "You're already there.", "cost": ""}

    # Pay for travel
    if has_card:
        player.inventory.remove(TRANSIT_COST_CARD)
        cost_str = "1x Transit Card used"
    elif player.credits >= TRANSIT_COST_CREDITS:
        player.credits -= TRANSIT_COST_CREDITS
        cost_str = str(TRANSIT_COST_CREDITS) + " credits"
    else:
        return {
            "success": False,
            "message": "Need a transit card or " + str(TRANSIT_COST_CREDITS) +
                       " credits for the fare.",
            "cost": "",
        }

    player.location = destination_id
    hub_name = TRANSIT_HUBS[destination_id]
    return {
        "success": True,
        "message": "Arrived at " + hub_name + ". (" + cost_str + ")",
        "cost": cost_str,
    }
