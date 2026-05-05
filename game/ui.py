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
    hp_color = "green" if player.hp > player.max_hp * 0.5 else ("yellow" if player.hp > player.max_hp * 0.25 else "red")

    line = (
        "[bold]" + player.name + "[/bold] "
        "[dim]" + (player.class_name or "?") + "[/dim] "
        "[bold cyan]Lv" + str(player.level) + "[/bold cyan]  "
        "[" + hp_color + "]HP " + str(player.hp) + "/" + str(player.max_hp) + "[/" + hp_color + "]  "
        "[yellow]Cr " + str(player.credits) + "[/yellow]  "
        "[magenta]XP " + player.xp_progress_string() + "[/magenta]"
    )
    console.print(line)

    # Show unspent points warning
    if player.unspent_stat_points > 0 or player.unspent_skill_points > 0:
        notice = "[bold yellow]>> "
        if player.unspent_stat_points > 0:
            notice += str(player.unspent_stat_points) + " stat pts "
        if player.unspent_skill_points > 0:
            notice += str(player.unspent_skill_points) + " skill pts "
        notice += "unspent (type 'levelup')[/bold yellow]"
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

    info = (
        "[bold magenta]" + location["name"] + "[/bold magenta]\n"
        "[dim]" + location["description"] + "[/dim]\n\n"
        "[cyan]EXITS:[/cyan] " + exits + "\n"
        "[yellow]NPCS:[/yellow] " + npcs + "\n"
        "[green]ITEMS:[/green] " + items_str + "\n"
        "[red]DANGER:[/red] " + danger
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
    table = Table(title="INVENTORY", box=box.SIMPLE_HEAVY, border_style="cyan")
    table.add_column("Item", style="white")
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
        equipped = ""
        if item_id == player.equipped.get("weapon") or item_id == player.equipped.get("armor"):
            equipped = " [E]"
        table.add_row(
            item_display_name(item_id) + equipped,
            item["type"],
            stats,
            str(item.get("value", 0)) + " Cr",
        )
    console.print(table)


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

    # Equipment
    weapon = item_display_name(player.equipped["weapon"]) if player.equipped["weapon"] else "none"
    armor = item_display_name(player.equipped["armor"]) if player.equipped["armor"] else "none"
    cyberware = ", ".join(item_display_name(c) for c in player.cyberware) or "none"
    equip_text = (
        "[cyan]Weapon:[/cyan] " + weapon + "\n"
        "[cyan]Armor:[/cyan] " + armor + "\n"
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


def print_combat(player, combat):
    enemy = combat.enemy
    enemy_hp_pct = enemy["hp"] / combat.enemy_max_hp if combat.enemy_max_hp else 0
    enemy_color = "green" if enemy_hp_pct > 0.5 else ("yellow" if enemy_hp_pct > 0.25 else "red")

    panel_text = (
        "[bold red]>>> COMBAT <<<[/bold red]\n\n"
        "[bold]" + enemy["name"] + "[/bold]\n"
        "[" + enemy_color + "]HP " + str(max(0, enemy["hp"])) + "/" + str(combat.enemy_max_hp) +
        "[/" + enemy_color + "]\n"
        "[dim]" + enemy.get("desc", "") + "[/dim]\n\n"
        "[cyan]COMMANDS:[/cyan] attack | use <item> | flee | inv"
    )
    console.print(Panel(panel_text, border_style="red", box=box.DOUBLE))


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
    table = Table(title="COMMANDS", box=box.SIMPLE_HEAVY, border_style="cyan")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="white")
    cmds = [
        ("go <dir>", "Move (north/south/east/west/up/down)"),
        ("look", "Re-examine surroundings"),
        ("take <item>", "Pick up an item"),
        ("inv / inventory", "Show inventory"),
        ("stats / char", "Full character sheet with all stats"),
        ("skills", "Show all skills with levels"),
        ("levelup", "Spend stat/skill points after leveling"),
        ("equip <item>", "Equip a weapon or armor"),
        ("use <item>", "Use consumable / install cyberware"),
        ("quests / journal", "View active quest log"),
        ("accept", "Accept a pending quest offer"),
        ("decline", "Decline a pending quest offer"),
        ("save", "Save game"),
        ("load", "Load saved game"),
        ("help", "Show this help"),
        ("quit", "Exit (offers save)"),
        ("anything else", "Sent to AI - talk, hack, search, attack..."),
    ]
    for c, d in cmds:
        table.add_row(c, d)
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
