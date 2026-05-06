"""Shop / market system.

Each location can have one or more shopkeepers (defined in world.py as 'shops').
A shop has an inventory of items at certain tiers.

Prices are modified by:
- Player's faction reputation with the shopkeeper's faction
- Player's barter skill (each level reduces buy price by 2%)

Sells items back at relationship-modified rate.
"""
from game.items import ITEMS, get_item, item_display_name, TIER_NAMES, TIER_COLORS, tier_label
from game import relationships


# ============================================================
# SHOP DEFINITIONS
# ============================================================
# Each shop has:
#   - npc: NPC name (matches world.py)
#   - faction: which faction's rep applies
#   - tier_range: (min, max) - what tiers they stock
#   - stock: explicit list of items they always have
#   - greeting: opening line
#   - personality: short description for AI

SHOPS = {
    "Old Marta": {
        "faction": "scavengers",
        "tier_range": (1, 2),
        "stock": ["ration_pack", "ration_pack", "ration_pack",
                  "synth_coffee", "synth_coffee", "smokes",
                  "cheap_painkillers", "cheap_painkillers",
                  "military_rations", "broken_bottle"],
        "greeting": "What can I get you, kid? Got food, smokes, the basics.",
        "personality": "Maternal, gruff. Won't sell to anyone she sees as a threat to the slums.",
    },
    "Zhen": {
        "faction": "gangs",
        "tier_range": (2, 4),
        "stock": ["cheap_pistol", "switchblade", "combat_knife", "sawn_off",
                  "stim_pack", "stim_pack", "adrenaline_shot",
                  "leather_jacket", "kevlar_vest", "running_boots",
                  "neural_jack", "cyber_eye", "monoblade", "trauma_kit",
                  "voice_modulator", "encrypted_comms"],
        "greeting": "Looking for chrome, eh? I got the best in the market. Cash only.",
        "personality": "Loud, friendly, ALWAYS overcharging. Discount only for big spenders.",
    },
    "Doc Sato": {
        "faction": "scavengers",
        "tier_range": (2, 4),
        "stock": ["stim_pack", "stim_pack", "trauma_kit", "trauma_kit",
                  "nano_bandages", "nano_bandages", "cheap_painkillers",
                  "cyber_eye", "neural_jack", "biomonitor",
                  "subdermal_armor", "med_implant"],
        "greeting": "You hurt? Or buying? Either way, sit down, don't bleed on the floor.",
        "personality": "Tired but kind. Heals for 30 credits. Can install cyberware safely.",
    },
    "Vex": {
        "faction": "gangs",
        "tier_range": (3, 5),
        "stock": ["tactical_smg", "combat_shotgun", "assault_rifle",
                  "kevlar_vest", "tactical_visor", "smart_helmet",
                  "smartgun", "combat_armor", "elite_med_kit",
                  "berserker_dose", "deal_maker_glock"],
        "greeting": "What you need? I got jobs and I got gear. Both cost.",
        "personality": "Sharp fixer. Stocks gear for runners. Best prices for friends only.",
    },
    "Cipher": {
        "faction": "hackers",
        "tier_range": (3, 5),
        "stock": ["virus_chip", "virus_chip", "virus_chip",
                  "ghost_overlay", "neural_clarifier", "neural_clarifier",
                  "pocket_jammer", "ice_breaker_rig", "hacker_rig",
                  "data_chip_corrupted", "encrypted_comms"],
        "greeting": "You need to break some ICE? I got tools.",
        "personality": "Quiet. Sells only to those with hacker rep.",
    },
    "Rail Rat Smuggler": {
        "faction": "gangs",
        "tier_range": (2, 4),
        "stock": ["transit_card", "smokes", "credstick", "tactical_smg",
                  "stim_pack", "data_shard", "corpo_id_card", "sewer_map"],
        "greeting": "Whatcha need? I can get it. For a price.",
        "personality": "Smuggler. Will sell anything to anyone with cash.",
    },
    "Scrap Boss": {
        "faction": "scavengers",
        "tier_range": (1, 3),
        "stock": ["scrap_metal", "scrap_metal", "rusty_pipe", "crowbar",
                  "wrench", "work_gloves", "tool_belt",
                  "stim_pack", "ration_pack", "exo_gauntlet"],
        "greeting": "You buying scrap or selling scrap?",
        "personality": "Pays decent for scrap. Hates corpos.",
    },
    "Synth Noodle Cook": {
        "faction": "scavengers",
        "tier_range": (1, 1),
        "stock": ["ration_pack"] * 5 + ["synth_coffee"] * 3 + ["military_rations"] * 2,
        "greeting": "Bowl of noodles? Three creds. Best in the market.",
        "personality": "Cheerful. Knows everyone's gossip.",
    },
    "Suspicious Vendor": {
        "faction": "gangs",
        "tier_range": (2, 4),
        "stock": ["leather_jacket", "switchblade", "briefcase_pistol",
                  "corpo_id_card", "virus_chip", "smokes", "sawn_off"],
        "greeting": "...you didn't see me. What you want?",
        "personality": "Black-market everything. No questions.",
    },
    "Information Broker": {
        "faction": "hackers",
        "tier_range": (2, 3),
        "stock": ["data_chip_corrupted", "data_chip_corrupted",
                  "transit_card", "credstick",
                  "sewer_map", "encrypted_comms"],
        "greeting": "Information is the only currency that matters. Cash works too.",
        "personality": "Sells data shards and rumors. Scoffs at the ignorant.",
    },
    "Dr. Vance": {
        "faction": "hackers",
        "tier_range": (4, 5),
        "stock": ["reflex_booster", "subdermal_armor", "ghost_overlay",
                  "berserker_chip", "overclock_chip", "nanite_welder",
                  "corpo_override_chip", "shadow_network"],
        "greeting": "Mmm. Custom modifications. Expensive. But beautiful.",
        "personality": "Reclusive cyberware genius. Only deals with hacker faction.",
    },
    "Dealer": {
        "faction": "gangs",
        "tier_range": (2, 4),
        "stock": ["smokes", "smokes", "cheap_painkillers", "cheap_painkillers",
                  "stim_pack", "adrenaline_shot", "combat_stim", "surge_capsule",
                  "virus_chip", "data_chip_corrupted", "neural_clarifier"],
        "greeting": "You want something? Make it quick.",
        "personality": "Twitchy drug and stim dealer. Cash only, no receipts.",
    },
}


def get_shop(npc_name: str) -> dict:
    """Get shop data for an NPC, or None."""
    for key, shop in SHOPS.items():
        if key.lower() in npc_name.lower() or npc_name.lower() in key.lower():
            return {**shop, "name": key}
    return None


def shops_at_location(location: dict) -> list:
    """Return list of shop dicts available at this location."""
    shops = []
    for npc in location.get("shops", []):
        shop = get_shop(npc)
        if shop:
            shops.append(shop)
    return shops



# Tier sell multipliers - higher tier items retain more value
# T1=30%, T2=40%, T3=50%, T4=55%, T5=60%, T6=70% of base value (before rep mod)
TIER_BASE_SELL_RATE = {
    1: 0.30,
    2: 0.40,
    3: 0.50,
    4: 0.55,
    5: 0.60,
    6: 0.70,
}


def calculate_buy_price(item_id: str, player, faction: str) -> int:
    """Calculate the BUY price for the player.

    Formula: base_value * rep_modifier * (1 - barter_discount)
    Rep modifier: Ally=60%, Friend=75%, Friendly=90%, Neutral=100%, Wary=150%, Hostile=250%
    Barter: each skill level = 2% off (max 20% at skill 10)
    """
    item = get_item(item_id)
    if not item:
        return 0
    base = item.get("value", 0)
    rep_score = player.reputation.get(faction, 0)
    rep_mod = relationships.get_buy_modifier(rep_score)
    barter_mod = 1.0 - (player.skills.get("barter", 0) * 0.02)
    final = int(base * rep_mod * barter_mod)
    return max(1, final)


def calculate_sell_price(item_id: str, player, faction: str) -> int:
    """Calculate the SELL price the shop pays the player.

    Formula: base_value * tier_base_rate * rep_sell_modifier * (1 + barter_bonus)

    Tier base rates:
      T1=30%  T2=40%  T3=50%  T4=55%  T5=60%  T6=70%

    Rep sell modifiers (from relationships.py):
      Ally=70%  Friend=60%  Neutral=50%  Wary=25%  Hostile=10%

    Barter: each level = 2% bonus on sell (max +20% at skill 10)

    Example: T4 smartgun (base 800cr), Neutral rep, Barter 5:
      800 * 0.55 * 0.50 * 1.10 = 242 credits
    """
    item = get_item(item_id)
    if not item:
        return 0
    if item.get("type") == "quest":
        return 0  # Quest items not sellable
    base = item.get("value", 0)
    tier = item.get("tier", 1)
    tier_rate = TIER_BASE_SELL_RATE.get(tier, 0.40)
    rep_score = player.reputation.get(faction, 0)
    rep_mod = relationships.get_sell_modifier(rep_score)
    barter_mod = 1.0 + (player.skills.get("barter", 0) * 0.02)
    final = int(base * tier_rate * rep_mod * barter_mod)
    return max(0, final)


def get_sell_price_breakdown(item_id: str, player, faction: str) -> str:
    """Return a human-readable breakdown of sell price components."""
    item = get_item(item_id)
    if not item:
        return ""
    from game.items import TIER_NAMES
    tier = item.get("tier", 1)
    tier_rate = TIER_BASE_SELL_RATE.get(tier, 0.40)
    rep_score = player.reputation.get(faction, 0)
    rep_mod = relationships.get_sell_modifier(rep_score)
    barter_mod = 1.0 + (player.skills.get("barter", 0) * 0.02)
    price = calculate_sell_price(item_id, player, faction)
    return (TIER_NAMES.get(tier, "?") + " base " + str(int(tier_rate * 100)) +
            "% | rep " + str(int(rep_mod * 100)) + "% | barter +" +
            str(player.skills.get("barter", 0) * 2) + "% = " + str(price) + " Cr")
