"""Terminal UI rendering using rich."""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
from game.items import get_item, item_display_name
from game.character import CLASSES, SKILL_DEFINITIONS, xp_for_level

console = Console()


def clear():
    console.clear()


def print_header():
    title = Text("[ NEON CASCADIA  v2087 ]", style="bold cyan")
    console.print(Panel(title, box=box.DOUBLE, border_style="cyan", padding=(0, 1)))


def print_status(player):
    weapon = item_display_name(player.equipped["weapon"]) if player.equipped["weapon"] else "fists"
    hp_color = "green" if player.hp > player.max_hp * 0.5 else (
        "yellow" if player.hp > player.max_hp * 0.25 else "red")

    # Time of day
    time_str = ""
    if hasattr(player, "time"):
        t = player.time
        time_str = "[" + t.period_color + "]" + t.time_string() + "[/" + t.period_color + "]  "

    line = (
        "[bold]" + player.name + "[/bold] "
        "[dim]" + (player.class_name or "?") + "[/dim] "
        "[bold cyan]Lv" + str(player.level) + "[/bold cyan]  "
        "[" + hp_color + "]HP " + str(player.hp) + "/" + str(player.max_hp) +
        "[/" + hp_color + "]  "
        "[yellow]Cr " + str(player.credits) + "[/yellow]  "
        "[magenta]XP " + player.xp_progress_string() + "[/magenta]  "
        + time_str
    )
    console.print(line)

    # Status effects
    if hasattr(player, "status_effects") and player.status_effects:
        from game.status_effects import format_effects
        console.print("[yellow]STATUS: " + format_effects(player.status_effects) + "[/yellow]")

    # Companion
    if hasattr(player, "companion") and player.companion:
        console.print(player.companion.status_line())

    # Unspent points warning
    if player.unspent_stat_points > 0 or player.unspent_skill_points > 0:
        notice = "[bold yellow]>> "
        if player.unspent_stat_points > 0:
            notice += str(player.unspent_stat_points) + " stat pts "
        if player.unspent_skill_points > 0:
            notice += str(player.unspent_skill_points) + " skill pts "
        notice += "unspent  type 'levelup'[/bold yellow]"
        console.print(notice)


def print_location(location: dict, player):
    exits = " | ".join(
        "[cyan]" + d + "[/cyan]>" + loc.replace("_", " ")
        for d, loc in location.get("exits", {}).items()
    )
    npcs = ", ".join(location.get("npcs", [])) or "none"

    visible_items = location.get("items", [])
    if player.location in player.looted_locations:
        visible_items = []
    items_str = ", ".join(item_display_name(i) for i in visible_items) or "none visible"

    danger = "[red]" + ("|" * location.get("danger", 1)) + "[/red]"

    # Shops at this location
    shops = location.get("shops", [])
    shop_line = ""
    if shops:
        shop_line = "\n[yellow]SHOPS:[/yellow] " + ", ".join(shops) + " [dim](type 'shop')[/dim]"

    # Corpses at this location
    corpses = player.get_corpses_at(player.location)
    fresh = [c for c in corpses if not c["looted"]]
    corpse_line = ""
    if fresh:
        names = ", ".join(c["name"] for c in fresh)
        corpse_line = "\n[red]BODIES:[/red] " + names + " [dim](type 'search')[/dim]"

    info = (
        "[bold magenta]" + location["name"] + "[/bold magenta]\n"
        "[dim]" + location["description"] + "[/dim]\n\n"
        "[cyan]EXITS:[/cyan] " + exits + "\n"
        "[yellow]NPCS:[/yellow] " + npcs + "\n"
        "[green]ITEMS:[/green] " + items_str + "\n"
        "[red]DANGER:[/red] " + danger + shop_line + corpse_line
    )
    console.print(Panel(info, border_style="magenta", box=box.SIMPLE_HEAVY, padding=(0, 1)))


def print_narrative(parsed: dict):
    text = parsed.get("narrative", "")
    if text:
        console.print(Panel(text, border_style="white", box=box.ROUNDED, padding=(0, 1)))

    options = parsed.get("options", [])
    if options:
        console.print("\n[bold cyan]>> SUGGESTED:[/bold cyan]")
        for i, opt in enumerate(options, 1):
            console.print("  [yellow]" + str(i) + ".[/yellow] " + opt)


def print_inventory(player):
    from game.items import tier_label
    table = Table(title="INVENTORY", box=box.SIMPLE_HEAVY, border_style="cyan")
    table.add_column("Item", style="white")
    table.add_column("Tier")
    table.add_column("Type", style="cyan")
    table.add_column("Stats", style="yellow")
    table.add_column("Value", style="green")

    if not player.inventory:
        console.print("[dim]Inventory empty.[/dim]")
        return

    for item_id in player.inventory:
        item = get_item(item_id)
        if not item:
            continue
        stats = ""
        if "damage" in item:
            stats = "DMG " + str(item["damage"])
        elif "defense" in item:
            stats = "DEF " + str(item["defense"])
        elif "heal" in item:
            stats = "HEAL " + str(item["heal"])
        elif "bonus" in item:
            stats = "+" + str(item["bonus"]) + " " + item.get("stat", "")
        # Skill mods
        if "skill_mods" in item:
            mods = ", ".join("+" + str(v) + " " + k for k, v in item["skill_mods"].items())
            stats += " (" + mods + ")"
        equipped = ""
        if item_id in player.equipped.values():
            equipped = " [E]"
        tier = tier_label(item.get("tier", 1))
        table.add_row(
            item_display_name(item_id) + equipped,
            tier,
            item["type"],
            stats,
            str(item.get("value", 0)) + " Cr",
        )
    console.print(table)
    console.print("\n[dim]Credits:[/dim] [yellow]" + str(player.credits) + "[/yellow]")


def print_stats(player):
    """Full character sheet."""
    # Header panel
    header = (
        "[bold cyan]" + player.name + "[/bold cyan]   "
        "[white]" + (player.class_name or "Unclassed") + "[/white]   "
        "[yellow]Level " + str(player.level) + "[/yellow]   "
        "[magenta]XP " + player.xp_progress_string() + "[/magenta]"
    )
    console.print(Panel(header, border_style="cyan", box=box.DOUBLE))

    # Core stats
    stats_table = Table(title="ATTRIBUTES", box=box.SIMPLE, border_style="cyan")
    stats_table.add_column("Stat", style="cyan", width=12)
    stats_table.add_column("Value", style="white")
    for stat, val in player.stats.items():
        stats_table.add_row(stat.capitalize(), str(val))
    stats_table.add_row("[bold]Defense (total)[/bold]", "[bold]" + str(player.get_defense()) + "[/bold]")
    stats_table.add_row("[bold]Attack (total)[/bold]", "[bold]" + str(player.get_attack_damage()) + "[/bold]")
    console.print(stats_table)

    # Skills - bar chart style
    skills_table = Table(title="SKILLS", box=box.SIMPLE, border_style="green")
    skills_table.add_column("Skill", style="green", width=15)
    skills_table.add_column("Level", justify="right", width=6)
    skills_table.add_column("Bar")
    skills_table.add_column("Description", style="dim")

    for skill, val in player.skills.items():
        bar = "[green]" + ("|" * val) + "[/green]" + "[dim]" + ("." * (10 - val)) + "[/dim]"
        desc = SKILL_DEFINITIONS.get(skill, {}).get("desc", "")
        skills_table.add_row(skill.replace("_", " "), str(val) + "/10", bar, desc)
    console.print(skills_table)

    # Equipment - now with 4 armor slots
    weapon = item_display_name(player.equipped["weapon"]) if player.equipped["weapon"] else "none"
    head = item_display_name(player.equipped.get("head", "")) if player.equipped.get("head") else "none"
    body = item_display_name(player.equipped.get("body", "")) if player.equipped.get("body") else "none"
    hands = item_display_name(player.equipped.get("hands", "")) if player.equipped.get("hands") else "none"
    feet = item_display_name(player.equipped.get("feet", "")) if player.equipped.get("feet") else "none"
    cyberware = ", ".join(item_display_name(c) for c in player.cyberware) or "none"
    equip_text = (
        "[cyan]Weapon:[/cyan] " + weapon + "\n"
        "[cyan]Head:  [/cyan] " + head + "\n"
        "[cyan]Body:  [/cyan] " + body + "\n"
        "[cyan]Hands: [/cyan] " + hands + "\n"
        "[cyan]Feet:  [/cyan] " + feet + "\n"
        "[cyan]Cyberware:[/cyan] " + cyberware
    )
    console.print(Panel(equip_text, title="EQUIPMENT", border_style="yellow", box=box.SIMPLE))

    # Reputation
    rep_table = Table(title="FACTION REPUTATION", box=box.SIMPLE, border_style="magenta")
    rep_table.add_column("Faction", style="magenta")
    rep_table.add_column("Standing", style="white")
    for f, v in player.reputation.items():
        if v > 25:
            color, label = "green", "Allied"
        elif v > 0:
            color, label = "cyan", "Friendly"
        elif v == 0:
            color, label = "white", "Neutral"
        elif v > -25:
            color, label = "yellow", "Wary"
        else:
            color, label = "red", "Hostile"
        rep_table.add_row(f, "[" + color + "]" + label + " (" + str(v) + ")[/" + color + "]")
    console.print(rep_table)


def print_quests(player):
    if not player.quests:
        console.print("[dim]No active quests.[/dim]")
        return
    console.print("[bold yellow]ACTIVE QUESTS[/bold yellow]")
    for q in player.quests:
        marker = "[green][DONE][/green]" if q["done"] else "[yellow][...][/yellow]"
        console.print("  " + marker + " [bold]" + q["title"] + "[/bold]")
        console.print("        [dim]" + q["description"] + "[/dim]")


def print_combat_log(messages: list):
    for msg in messages:
        if "you hit" in msg.lower() or "critical" in msg.lower():
            console.print("[green]> " + msg + "[/green]")
        elif "hits you" in msg.lower():
            console.print("[red]> " + msg + "[/red]")
        elif "miss" in msg.lower():
            console.print("[dim]> " + msg + "[/dim]")
        else:
            console.print("[white]> " + msg + "[/white]")


def print_pending_quest(quest: tuple):
    """Show a banner for a quest waiting for accept/decline."""
    title, desc = quest
    text = (
        "[bold yellow]>> QUEST OFFERED: " + title + "[/bold yellow]\n"
        "[dim]" + desc + "[/dim]\n\n"
        "[cyan]accept[/cyan]  to take it    [red]decline[/red]  to refuse"
    )
    console.print(Panel(text, border_style="yellow", box=box.HEAVY, padding=(0, 1)))


def print_help():
    table = Table(title="COMMANDS", box=box.SIMPLE_HEAVY, border_style="cyan")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")
    cmds = [
        ("go <dir>", "Move (north/south/east/west/up/down)"),
        ("look", "Re-examine surroundings"),
        ("map / m", "Show city map with your location"),
        ("districts", "Districts discovered"),
        ("travel", "Fast travel between transit hubs"),
        ("take <item>", "Pick up item from area"),
        ("search / loot", "Search bodies of fallen enemies"),
        ("shop / buy / sell", "Trade with shopkeepers here"),
        ("craft", "Craft items from ingredients"),
        ("inv / inventory", "Show inventory"),
        ("stats / char", "Full character sheet"),
        ("skills", "Show all skills with levels"),
        ("relations / rep", "Faction and NPC relationships"),
        ("journal / lore", "View journal and lore entries"),
        ("time", "Current time of day"),
        ("companion", "Companion status"),
        ("levelup", "Spend stat/skill points"),
        ("equip <item>", "Equip weapon or armor"),
        ("use <item>", "Use consumable / install cyberware"),
        ("quests", "View active quest log"),
        ("note <text>", "Add a personal note to journal"),
        ("accept", "Accept pending quest"),
        ("decline", "Decline pending quest"),
        ("rest", "Rest to recover HP (risk of encounter)"),
        ("save", "Save game"),
        ("load", "Load saved game"),
        ("help", "Show this help"),
        ("quit", "Exit"),
        ("anything else", "Sent to AI - talk, hack, fight, explore..."),
    ]
    for c, d in cmds:
        table.add_row(c, d)
    console.print(table)


def print_journal(player):
    """Display journal entries, clues, NPCs met."""
    j = player.journal

    if j.entries:
        console.print("\n[bold cyan]>> LORE DISCOVERED <<[/bold cyan]")
        for entry in j.entries:
            console.print("\n[bold cyan]" + entry["title"] + "[/bold cyan]")
            console.print("[dim]" + entry["text"] + "[/dim]")

    if j.clues:
        console.print("\n[bold yellow]>> INVESTIGATION CLUES <<[/bold yellow]")
        for i, clue in enumerate(j.clues, 1):
            console.print("  [yellow]" + str(i) + ".[/yellow] " + clue)

    if j.npcs_met:
        console.print("\n[bold magenta]>> NPCS MET <<[/bold magenta]")
        console.print("  " + ", ".join(j.npcs_met))

    if j.notes:
        console.print("\n[bold white]>> YOUR NOTES <<[/bold white]")
        for i, note in enumerate(j.notes, 1):
            console.print("  [dim]" + str(i) + ". " + note + "[/dim]")

    if not j.entries and not j.clues and not j.notes:
        console.print("[dim]Journal is empty. Explore, talk to people, find clues.[/dim]")


def print_crafting_menu(craftable: list):
    """Show available crafting recipes."""
    table = Table(title="CRAFTING", box=box.SIMPLE_HEAVY, border_style="green")
    table.add_column("#", style="yellow", width=3)
    table.add_column("Recipe", style="white")
    table.add_column("Ingredients", style="cyan")
    table.add_column("Result", style="green")
    table.add_column("Skill", style="magenta")
    table.add_column("Ready", style="bold")

    from game.items import item_display_name
    for i, (rid, recipe, has_all) in enumerate(craftable, 1):
        ingr = ", ".join(
            item_display_name(k) + " x" + str(v)
            for k, v in recipe["ingredients"].items()
        )
        skills_req = ", ".join(
            s + " " + str(v)
            for s, v in recipe.get("required_skill", {}).items()
        )
        ready = "[green]YES[/green]" if has_all else "[red]NO[/red]"
        table.add_row(
            str(i),
            recipe["name"],
            ingr,
            item_display_name(recipe["result"]),
            skills_req,
            ready,
        )
    console.print(table)


def print_combat(player, combat):
    """Combat HUD with status effects."""
    from game.status_effects import format_effects
    enemy = combat.enemy
    enemy_hp_pct = enemy["hp"] / combat.enemy_max_hp if combat.enemy_max_hp else 0
    enemy_color = "green" if enemy_hp_pct > 0.5 else ("yellow" if enemy_hp_pct > 0.25 else "red")

    phase_text = ""
    if combat.is_boss_fight:
        if combat.phase_two_active:
            phase_text = "\n[bold red]>>> PHASE 2 - ENRAGED <<<[/bold red]"
        else:
            phase_text = "\n[bold yellow][ BOSS FIGHT ][/bold yellow]"

    efx = format_effects(combat.enemy_effects)
    pfx = format_effects(player.status_effects)

    panel_text = (
        "[bold red]>>> COMBAT <<<[/bold red]\n\n"
        "[bold]" + enemy["name"] + "[/bold]"
        + (" - " + enemy.get("title", "") if combat.is_boss_fight and enemy.get("title") else "") + "\n"
        "[" + enemy_color + "]HP " + str(max(0, enemy["hp"])) + "/" + str(combat.enemy_max_hp) +
        "[/" + enemy_color + "]"
        + ("  " + efx if efx else "") + "\n"
        "[dim]" + enemy.get("desc", "") + "[/dim]"
        + phase_text + "\n\n"
        + ("YOUR STATUS: " + pfx + "\n\n" if pfx else "")
        + "[cyan]attack  |  use <item>  |  flee  |  inv[/cyan]"
    )
    console.print(Panel(panel_text, border_style="red", box=box.DOUBLE))


def print_fast_travel(hubs: list, player):
    """Display fast travel options."""
    from game.fast_travel import TRANSIT_HUBS, TRANSIT_COST_CREDITS
    has_card = "transit_card" in player.inventory
    cost_str = "Transit Card" if has_card else str(TRANSIT_COST_CREDITS) + " credits"

    console.print("\n[bold cyan]>> FAST TRAVEL <<[/bold cyan]")
    console.print("[dim]Cost per trip: " + cost_str + "[/dim]\n")

    if not hubs:
        console.print("[dim]No transit hubs visited yet. Find the Rail Station.[/dim]")
        return

    table = Table(box=box.SIMPLE, border_style="cyan")
    table.add_column("#", style="yellow", width=3)
    table.add_column("Destination", style="cyan")
    table.add_column("Hub Name", style="white")
    for i, (loc_id, hub_name) in enumerate(hubs, 1):
        table.add_row(str(i), loc_id.replace("_", " ").title(), hub_name)
    console.print(table)


# ============== CHARACTER CREATION ==============

def show_class_selection():
    """Display class options for character creation."""
    console.print("\n[bold cyan]>> CHOOSE YOUR ARCHETYPE[/bold cyan]\n")

    class_list = list(CLASSES.keys())
    for i, class_id in enumerate(class_list, 1):
        cls = CLASSES[class_id]

        # Build stat summary
        stat_summary = []
        for stat, bonus in cls.get("stat_bonuses", {}).items():
            if bonus > 0:
                stat_summary.append("[green]+" + str(bonus) + " " + stat + "[/green]")
            elif bonus < 0:
                stat_summary.append("[red]" + str(bonus) + " " + stat + "[/red]")

        skill_summary = []
        for skill, bonus in cls.get("skill_bonuses", {}).items():
            skill_summary.append("[cyan]+" + str(bonus) + " " + skill + "[/cyan]")

        gear = ", ".join(item_display_name(g) for g in cls.get("starting_gear", []))

        text = (
            "[dim]" + cls["description"] + "[/dim]\n\n"
            "[bold]Stats:[/bold] " + ", ".join(stat_summary) + "\n"
            "[bold]Skills:[/bold] " + ", ".join(skill_summary) + "\n"
            "[bold]Starting Gear:[/bold] " + gear + "\n"
            "[bold]Credits:[/bold] " + str(cls.get("starting_credits", 0)) + " | "
            "[bold]Bonus HP:[/bold] +" + str(cls.get("hp_bonus", 0))
        )

        title = "[" + str(i) + "] " + cls["name"].upper()
        console.print(Panel(text, title=title, border_style="cyan", box=box.ROUNDED))

    return class_list


def show_levelup_menu(player):
    """Display interactive level-up screen."""
    console.print("\n[bold yellow]>> LEVEL UP - SPEND POINTS <<<[/bold yellow]\n")

    if player.unspent_stat_points > 0:
        console.print("[bold cyan]ATTRIBUTE POINTS: " + str(player.unspent_stat_points) + "[/bold cyan]")
        stat_table = Table(box=box.SIMPLE)
        stat_table.add_column("#", style="yellow")
        stat_table.add_column("Stat", style="cyan")
        stat_table.add_column("Current", style="white")
        spendable_stats = [s for s in player.stats if s != "defense"]
        for i, stat in enumerate(spendable_stats, 1):
            stat_table.add_row(str(i), stat.capitalize(), str(player.stats[stat]))
        console.print(stat_table)

    if player.unspent_skill_points > 0:
        console.print("\n[bold green]SKILL POINTS: " + str(player.unspent_skill_points) + "[/bold green]")
        skill_table = Table(box=box.SIMPLE)
        skill_table.add_column("#", style="yellow")
        skill_table.add_column("Skill", style="green")
        skill_table.add_column("Current", style="white")
        skill_table.add_column("Description", style="dim")
        skill_list = list(player.skills.keys())
        for i, skill in enumerate(skill_list, 1):
            skill_table.add_row(
                str(i),
                skill.replace("_", " "),
                str(player.skills[skill]) + "/10",
                SKILL_DEFINITIONS.get(skill, {}).get("desc", "")[:50],
            )
        console.print(skill_table)


def get_input(prompt: str = ">") -> str:
    return console.input("\n[bold yellow]" + prompt + "[/bold yellow] ").strip()


def info(msg: str):
    console.print("[dim cyan]" + msg + "[/dim cyan]")


def warn(msg: str):
    console.print("[bold yellow]" + msg + "[/bold yellow]")


def error(msg: str):
    console.print("[bold red]" + msg + "[/bold red]")


def success(msg: str):
    console.print("[bold green]" + msg + "[/bold green]")


def pause(msg: str = "Press Enter..."):
    console.input("\n[dim]" + msg + "[/dim]")
