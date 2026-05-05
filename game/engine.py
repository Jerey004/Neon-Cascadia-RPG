"""Main game engine - orchestrates all subsystems."""
from game import ui, ai_engine, config
from game.player import Player
from game.world import WORLD, START_LOCATION
from game.items import get_item, item_display_name
from game.combat import Combat
from game.character import (
    CLASSES, SKILL_DEFINITIONS, get_class, XP_REWARDS,
)
from game import skills as skills_mod


class GameEngine:
    """Top-level game controller."""

    def __init__(self):
        self.player = None
        self.running = True

    # ============== STARTUP ==============

    def run(self):
        ui.clear()
        ui.print_header()
        self._intro()
        if self.player and self.player.is_alive():
            self._main_loop()

    def _intro(self):
        ui.console.print("\n[bold cyan]>> NEURAL UPLINK INITIALIZING[/bold cyan]")

        # Offer load
        existing = Player.load()
        if existing:
            ui.console.print("\n[yellow]Saved game found: " + existing.name +
                             " (" + (existing.class_name or "Unclassed") +
                             ", Lv " + str(existing.level) + ")[/yellow]")
            choice = ui.get_input("Load saved game? (y/n)").lower()
            if choice in ("y", "yes"):
                self.player = existing
                ui.success("Welcome back, " + self.player.name + ".")
                ui.pause()
                return

        self._character_creation()

    # ============== CHARACTER CREATION ==============

    def _character_creation(self):
        ui.clear()
        ui.print_header()

        ui.console.print("\n[bold cyan]>>> RUNNER PROFILE CREATION <<<[/bold cyan]")
        ui.console.print("[dim]Neo-Cascadia, 2087. The grid is hungry. Who are you?[/dim]\n")

        # Step 1: Name
        name = ""
        while not name:
            name = ui.get_input("Enter your handle:").strip() or "Ghost"

        # Step 2: Class selection
        ui.clear()
        ui.print_header()
        ui.console.print("\n[bold]Handle:[/bold] " + name)
        class_list = ui.show_class_selection()

        chosen_class = None
        while not chosen_class:
            choice = ui.get_input(
                "Select archetype (1-" + str(len(class_list)) + "):"
            ).strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(class_list):
                    chosen_class = class_list[idx]
                else:
                    ui.warn("Pick a number 1-" + str(len(class_list)))
            except ValueError:
                ui.warn("Enter a number.")

        # Step 3: Confirm
        cls = get_class(chosen_class)
        ui.clear()
        ui.print_header()
        ui.console.print("\n[bold cyan]CONFIRMED PROFILE[/bold cyan]\n")
        ui.console.print("[bold]Handle:[/bold] " + name)
        ui.console.print("[bold]Archetype:[/bold] " + cls["name"])
        ui.console.print("[dim]" + cls["description"] + "[/dim]")

        confirm = ui.get_input("Confirm? (y/n)").lower()
        if confirm not in ("y", "yes", ""):
            return self._character_creation()

        # Build the player
        self.player = Player(name=name, class_id=chosen_class)

        # Intro narrative
        ui.clear()
        ui.print_header()
        ui.console.print("\n[bold cyan]>> JACKING IN <<<[/bold cyan]\n")
        ui.console.print(Panel_intro_text(self.player))
        ui.pause("Press Enter to begin...")

    # ============== MAIN LOOP ==============

    def _main_loop(self):
        while self.running and self.player.is_alive():
            self._render_world()
            cmd = ui.get_input(">").strip()
            if not cmd:
                continue
            self._handle_input(cmd)

        if not self.player.is_alive():
            self._game_over()

    def _render_world(self):
        ui.clear()
        ui.print_header()
        ui.print_status(self.player)
        location = WORLD[self.player.location]
        ui.print_location(location, self.player)

    # ============== INPUT DISPATCH ==============

    def _handle_input(self, cmd: str):
        parts = cmd.lower().split()
        verb = parts[0]
        args = parts[1:]

        if verb in ("go", "move"):
            self._cmd_go(args)
        elif verb in ("north", "south", "east", "west", "up", "down"):
            self._cmd_go([verb])
        elif verb == "look":
            pass
        elif verb in ("inv", "inventory", "i"):
            self._cmd_inventory()
        elif verb == "stats":
            self._cmd_stats()
        elif verb == "skills":
            self._cmd_skills()
        elif verb == "levelup":
            self._cmd_levelup()
        elif verb in ("take", "pickup", "grab"):
            self._cmd_take(args)
        elif verb == "equip":
            self._cmd_equip(args)
        elif verb == "use":
            self._cmd_use(args)
        elif verb == "quests":
            self._cmd_quests()
        elif verb == "save":
            self._cmd_save()
        elif verb == "load":
            self._cmd_load()
        elif verb == "help":
            self._cmd_help()
        elif verb in ("quit", "exit"):
            self._cmd_quit()
        else:
            self._handle_ai(cmd)

    # ============== SYSTEM COMMANDS ==============

    def _cmd_go(self, args):
        if not args:
            ui.warn("Go where?")
            ui.pause()
            return
        success, msg, new_location = self.player.move(args[0], WORLD)
        if not success:
            ui.warn(msg)
            ui.pause()
            return
        # Award XP for discovering new locations
        if new_location:
            events = self.player.gain_xp(XP_REWARDS["discover_location"])
            ui.success("New area discovered!")
            for e in events:
                ui.success(e)
            ui.pause()

    def _cmd_inventory(self):
        ui.print_inventory(self.player)
        ui.pause()

    def _cmd_stats(self):
        ui.print_stats(self.player)
        ui.pause()

    def _cmd_skills(self):
        ui.console.print("\n[bold green]SKILLS[/bold green]")
        for skill, val in self.player.skills.items():
            bar = "[green]" + ("|" * val) + "[/green][dim]" + ("." * (10 - val)) + "[/dim]"
            desc = SKILL_DEFINITIONS.get(skill, {}).get("desc", "")
            ui.console.print(
                "  [cyan]" + skill.replace("_", " ").ljust(15) + "[/cyan] " +
                str(val) + "/10  " + bar + "  [dim]" + desc + "[/dim]"
            )
        ui.pause()

    def _cmd_levelup(self):
        if self.player.unspent_stat_points <= 0 and self.player.unspent_skill_points <= 0:
            ui.warn("No unspent points. Earn XP and level up first.")
            ui.pause()
            return

        while self.player.unspent_stat_points > 0 or self.player.unspent_skill_points > 0:
            ui.clear()
            ui.print_header()
            ui.show_levelup_menu(self.player)

            ui.console.print(
                "\n[bold]Commands:[/bold] [cyan]stat <name>[/cyan] | "
                "[cyan]skill <name>[/cyan] | [cyan]done[/cyan] to exit"
            )
            choice = ui.get_input("levelup>").strip().lower()
            if not choice:
                continue
            if choice == "done":
                break

            parts = choice.split()
            if len(parts) < 2:
                ui.warn("Format: stat <name> or skill <name>")
                ui.pause()
                continue

            kind = parts[0]
            target = "_".join(parts[1:])

            if kind == "stat":
                msg = self.player.spend_stat_point(target)
                ui.success(msg) if "Increased" in msg else ui.warn(msg)
                ui.pause()
            elif kind == "skill":
                msg = self.player.spend_skill_point(target)
                ui.success(msg) if "Increased" in msg else ui.warn(msg)
                ui.pause()
            else:
                ui.warn("Type 'stat <name>' or 'skill <name>' or 'done'")
                ui.pause()

        ui.success("Points spent. Returning to game.")
        ui.pause()

    def _cmd_take(self, args):
        if not args:
            ui.warn("Take what?")
            ui.pause()
            return
        target = "_".join(args)
        location = WORLD[self.player.location]

        if self.player.location in self.player.looted_locations:
            ui.warn("You've already looted this area.")
            ui.pause()
            return

        items_here = location.get("items", [])
        match = None
        for it in items_here:
            if it == target or target in it or it in target:
                match = it
                break

        if match:
            self.player.add_item(match)
            items_here.remove(match)
            if not items_here:
                self.player.looted_locations.add(self.player.location)
            ui.success("Picked up: " + item_display_name(match))
        else:
            ui.warn("No '" + target + "' here.")
        ui.pause()

    def _cmd_equip(self, args):
        if not args:
            ui.warn("Equip what?")
            ui.pause()
            return
        target = "_".join(args)
        match = None
        for it in self.player.inventory:
            if it == target or target in it:
                match = it
                break
        if match:
            ui.success(self.player.equip(match))
        else:
            ui.warn("You don't have '" + target + "'.")
        ui.pause()

    def _cmd_use(self, args):
        if not args:
            ui.warn("Use what?")
            ui.pause()
            return
        target = "_".join(args)
        match = None
        for it in self.player.inventory:
            if it == target or target in it:
                match = it
                break
        if match:
            ui.success(self.player.use_item(match))
        else:
            ui.warn("You don't have '" + target + "'.")
        ui.pause()

    def _cmd_quests(self):
        ui.print_quests(self.player)
        ui.pause()

    def _cmd_save(self):
        path = self.player.save()
        ui.success("Saved to " + path)
        ui.pause()

    def _cmd_load(self):
        loaded = Player.load()
        if loaded:
            self.player = loaded
            ui.success("Game loaded.")
        else:
            ui.warn("No save file found.")
        ui.pause()

    def _cmd_help(self):
        ui.print_help()
        ui.pause()

    def _cmd_quit(self):
        ui.console.print("[dim]Disconnecting from the grid...[/dim]")
        choice = ui.get_input("Save before quitting? (y/n)").lower()
        if choice in ("y", "yes"):
            self.player.save()
            ui.success("Saved.")
        self.running = False

    # ============== AI HANDLING ==============

    def _handle_ai(self, cmd: str):
        ui.info("\n>> connecting to grid...")
        location = WORLD[self.player.location]

        # Detect implicit skill check from action
        skill, dc, stat = skills_mod.detect_skill_check(cmd)
        check_result = None
        if skill:
            check_result = skills_mod.skill_check(self.player, skill, dc, stat)

        # Build context, optionally with skill check info
        context = ai_engine.build_context(self.player, location, cmd)
        if check_result:
            context += skills_mod.format_check_for_ai(check_result)

        raw = ai_engine.query_ollama(self.player.history, context)
        parsed = ai_engine.parse_response(raw)

        # Save to history
        self.player.add_to_history("user", "ACTION: " + cmd)
        self.player.add_to_history("assistant", raw)

        # Apply effects
        effect_msgs = self._apply_ai_effects(parsed)

        # Award skill check XP for successes
        if check_result and check_result["tier"] in ("success", "critical_success", "partial"):
            xp_events = self.player.gain_xp(XP_REWARDS["successful_skill_check"])
            effect_msgs.extend(xp_events)

        # Render
        self._render_world()
        ui.print_narrative(parsed)

        if check_result:
            tier_colors = {
                "critical_success": "bold green",
                "success": "green",
                "partial": "yellow",
                "failure": "red",
                "critical_failure": "bold red",
            }
            color = tier_colors.get(check_result["tier"], "white")
            ui.console.print(
                "\n[" + color + "]>> " + check_result["skill"].upper() +
                " check: " + check_result["tier"].replace("_", " ") +
                " (rolled " + str(check_result["total"]) +
                " vs DC " + str(check_result["dc"]) + ")[/" + color + "]"
            )

        for m in effect_msgs:
            ui.success(m)

        # Combat trigger
        if parsed.get("combat_start"):
            ui.pause("Press Enter when ready to fight...")
            self._run_combat(parsed["combat_start"])
            return

        ui.pause()

    def _apply_ai_effects(self, parsed: dict) -> list:
        msgs = []

        for item_id in parsed.get("item_gains", []):
            if get_item(item_id):
                self.player.add_item(item_id)
                msgs.append("+ " + item_display_name(item_id))
            else:
                self.player.inventory.append(item_id)
                msgs.append("+ " + item_display_name(item_id) + " (unknown)")

        for item_id in parsed.get("item_loses", []):
            if self.player.remove_item(item_id):
                msgs.append("- " + item_display_name(item_id))

        c = parsed.get("credits", 0)
        if c != 0:
            self.player.add_credits(c)
            sign = "+" if c > 0 else ""
            msgs.append(sign + str(c) + " credits")

        q = parsed.get("quest_offer")
        if q:
            self.player.add_quest(q[0], q[1])
            msgs.append("NEW QUEST: " + q[0])
            xp_events = self.player.gain_xp(XP_REWARDS["first_time_action"])
            msgs.extend(xp_events)

        return msgs

    # ============== COMBAT ==============

    def _run_combat(self, enemy_id: str):
        combat = Combat(self.player, enemy_id)
        self.player.in_combat = True

        log = []

        while self.player.is_alive() and not combat.is_enemy_dead():
            ui.clear()
            ui.print_header()
            ui.print_status(self.player)
            ui.print_combat(self.player, combat)
            ui.print_combat_log(log[-4:])

            cmd = ui.get_input("[COMBAT]").strip().lower()
            if not cmd:
                continue
            parts = cmd.split()
            verb = parts[0]
            args = parts[1:]

            if verb in ("attack", "a"):
                msg = combat.player_attack()
                log.append(msg)
                if combat.is_enemy_dead():
                    break
                log.append(combat.enemy_attack())

            elif verb == "use":
                if not args:
                    log.append("Use what?")
                    continue
                target = "_".join(args)
                match = None
                for it in self.player.inventory:
                    if it == target or target in it:
                        match = it
                        break
                if match:
                    log.append(combat.player_use_item(match))
                    log.append(combat.enemy_attack())
                else:
                    log.append("You don't have that.")

            elif verb in ("flee", "run"):
                ok, msg = combat.player_flee()
                log.append(msg)
                if ok:
                    self.player.in_combat = False
                    ui.warn(msg)
                    ui.pause()
                    return
                log.append(combat.enemy_attack())

            elif verb in ("inv", "i", "inventory"):
                ui.print_inventory(self.player)
                ui.pause()

            else:
                log.append("Combat: attack | use <item> | flee | inv")

        # Resolve
        ui.clear()
        ui.print_header()
        ui.print_status(self.player)

        if combat.is_enemy_dead():
            ui.success("\n>>> " + combat.enemy["name"] + " DEFEATED <<<")
            rewards = combat.reward_loot()
            for r in rewards:
                ui.success(r)

            # Award XP based on enemy difficulty
            xp_amount = self._enemy_xp_value(combat.enemy_id, combat.enemy)
            xp_events = self.player.gain_xp(xp_amount)
            for e in xp_events:
                ui.success(e)

            # Faction adjustments
            if "corpo" in enemy_id or "tower" in enemy_id or "elite" in enemy_id:
                self.player.adjust_reputation("corpo", -5)
                self.player.adjust_reputation("gangs", +2)
            elif "gang" in enemy_id or "rail" in enemy_id:
                self.player.adjust_reputation("gangs", -3)

        elif not self.player.is_alive():
            ui.error("\n>>> YOU HAVE BEEN KILLED <<<")

        self.player.in_combat = False
        ui.pause()

    def _enemy_xp_value(self, enemy_id: str, enemy_data: dict) -> int:
        """Calculate XP based on enemy max HP."""
        max_hp = enemy_data.get("hp", 30)  # remaining hp here, but original was set before
        # Use defense + damage as a difficulty proxy
        difficulty = enemy_data.get("damage", 5) + enemy_data.get("defense", 0)
        if difficulty < 12:
            return XP_REWARDS["kill_low"]
        elif difficulty < 22:
            return XP_REWARDS["kill_mid"]
        else:
            return XP_REWARDS["kill_high"]

    # ============== END ==============

    def _game_over(self):
        ui.clear()
        ui.print_header()
        ui.error("\n  D I S C O N N E C T E D  \n")
        ui.console.print("[dim]Your story ends here, " + self.player.name + ".[/dim]")
        ui.console.print("[dim]Level " + str(self.player.level) + " " + self.player.class_name + " - " +
                         str(self.player.xp) + " XP earned.[/dim]")
        ui.console.print("[dim]The neon flickers on without you.[/dim]\n")


def Panel_intro_text(player):
    """Generate intro narrative based on class."""
    intros = {
        "street_samurai": (
            "Steel and rain. The slums never sleep. Your blade hangs at your hip, "
            "still warm from last night's work. Somewhere out there is your name "
            "carved into someone's history. Time to make more cuts."
        ),
        "netrunner": (
            "The grid hums in your skull. Every wall is a door if you know how to ask. "
            "You've been off-net for three days - too long. Time to plug back in and "
            "see what's been happening in the wires."
        ),
        "fixer": (
            "Three jobs on your slate. Two debts owed to you. One person looking for "
            "you who shouldn't be. Just another Tuesday in Neo-Cascadia. The rain "
            "smells like fresh chrome and old promises."
        ),
        "tech": (
            "Your hands smell like solder. Three half-built drones cluttering your "
            "workbench. The order from Vex is past due. Better get moving before "
            "the wrong people start asking questions."
        ),
        "medic": (
            "Blood under your fingernails - someone else's. The trauma kit is nearly "
            "empty. Six patients last night, four lived. Decent odds for the slums. "
            "The sirens haven't stopped. They never do."
        ),
        "ex_corpo": (
            "Six months out. The skin between your shoulder blades still itches like "
            "they're watching. Your old badge is in a drawer. Your new life is in a "
            "duffel bag. They know you took the data. Time to use it before they catch up."
        ),
    }
    text = intros.get(player.class_id, "Welcome to Neo-Cascadia. Don't die.")

    from rich.panel import Panel as RPanel
    from rich import box as rbox
    return RPanel(
        text + "\n\n[dim]Type 'help' for commands, or just describe what you want to do.[/dim]",
        title="[bold cyan]" + player.name + " - " + (player.class_name or "Runner") + "[/bold cyan]",
        border_style="cyan",
        box=rbox.DOUBLE,
        padding=(1, 2),
    )
