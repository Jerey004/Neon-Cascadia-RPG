"""Main game engine - orchestrates all subsystems."""
from game import ui, ai_engine, config, cutscene, city_map
from game import encounters, crafting as crafting_mod, fast_travel as ft_mod
from game.player import Player
from game.world import WORLD, START_LOCATION
from game.items import get_item, item_display_name
from game.combat import Combat
from game.bosses import get_boss, is_boss, BOSSES
from game.character import CLASSES, SKILL_DEFINITIONS, get_class, XP_REWARDS
from game import skills as skills_mod


class GameEngine:
    """Top-level game controller."""

    def __init__(self):
        self.player = None
        self.running = True

    # ============== STARTUP ==============

    def run(self):
        cutscene.play_title_screen()
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

        # Play full cinematic intro
        cutscene.play_intro_cutscene(self.player)

    # ============== MAIN LOOP ==============

    def _main_loop(self):
        # Render the world once at the start
        self._render_world()
        while self.running and self.player.is_alive():
            cmd = ui.get_input(">").strip()
            if not cmd:
                continue
            # Track if we should redraw the world after this command
            redraw = self._handle_input(cmd)
            if redraw:
                self._render_world()

        if not self.player.is_alive():
            self._game_over()

    def _render_world(self):
        ui.clear()
        ui.print_header()
        ui.print_status(self.player)
        location = WORLD[self.player.location]
        ui.print_location(location, self.player)
        # Show pending quest banner if one is waiting
        if self.player.pending_quest:
            ui.print_pending_quest(self.player.pending_quest)

    # ============== INPUT DISPATCH ==============

    def _handle_input(self, cmd: str) -> bool:
        """Returns True if the world should be re-rendered after this command."""
        parts = cmd.lower().split()
        verb = parts[0]
        args = parts[1:]

        if verb in ("go", "move"):
            self._cmd_go(args)
            return True
        elif verb in ("north", "south", "east", "west", "up", "down"):
            self._cmd_go([verb])
            return True
        elif verb == "look":
            return True  # forces a redraw
        elif verb in ("inv", "inventory", "i"):
            self._cmd_inventory()
            return True
        elif verb in ("stats", "char", "character", "sheet"):
            self._cmd_stats()
            return True
        elif verb == "skills":
            self._cmd_skills()
            return True
        elif verb in ("map", "m"):
            self._cmd_map()
            return True
        elif verb == "districts":
            self._cmd_districts()
            return True
        elif verb == "levelup":
            self._cmd_levelup()
            return True
        elif verb in ("take", "pickup", "grab"):
            self._cmd_take(args)
            return True
        elif verb in ("search", "loot"):
            self._cmd_search(args)
            return True
        elif verb in ("shop", "buy", "sell", "trade"):
            self._cmd_shop(args, verb)
            return True
        elif verb in ("relations", "rep", "factions"):
            self._cmd_relations()
            return True
        elif verb in ("travel", "fast_travel", "transit"):
            self._cmd_travel()
            return True
        elif verb == "craft":
            self._cmd_craft()
            return True
        elif verb in ("journal", "lore", "notes"):
            self._cmd_journal()
            return True
        elif verb == "note" and args:
            self._cmd_add_note(" ".join(args))
            return False
        elif verb == "time":
            self._cmd_time()
            return False
        elif verb in ("companion", "comp"):
            self._cmd_companion()
            return False
        elif verb == "rest":
            self._cmd_rest()
            return True
        elif verb == "equip":
            self._cmd_equip(args)
            return True
        elif verb == "use":
            self._cmd_use(args)
            return True
        elif verb in ("quests", "q", "log"):
            self._cmd_quests()
            return True
        elif verb in ("accept", "yes") and self.player.pending_quest:
            self._cmd_accept_quest()
            return True
        elif verb in ("decline", "refuse", "reject", "no") and self.player.pending_quest:
            self._cmd_decline_quest()
            return True
        elif verb == "save":
            self._cmd_save()
            return False
        elif verb == "load":
            self._cmd_load()
            return True
        elif verb == "help":
            self._cmd_help()
            return False
        elif verb in ("quit", "exit"):
            self._cmd_quit()
            return False
        else:
            # AI action - stays in dialogue, no world redraw
            self._handle_ai(cmd)
            return False

    # ============== SYSTEM COMMANDS ==============

    def _cmd_go(self, args):
        if not args:
            ui.warn("Go where?")
            return
        old_district = WORLD[self.player.location].get("district", "")

        success, msg, new_location = self.player.move(args[0], WORLD)
        if not success:
            ui.warn(msg)
            return

        # Advance time + turn counter
        self.player.time.advance(1)
        self.player.turn_count += 1

        new_loc = self.player.location
        new_district = WORLD[new_loc].get("district", "")

        # District transition cutscene (first visit to new district)
        if new_district and new_district != old_district:
            cutscene.play_district_transition(new_district)

        # Journal auto-entry for key locations
        if new_location:
            events = self.player.gain_xp(XP_REWARDS["discover_location"])
            ui.success("New area discovered! +" + str(XP_REWARDS["discover_location"]) + " XP")
            self._check_levelup_cutscene(events)

            entry = self.player.journal.check_location(new_loc, self.player.turn_count)
            if entry:
                ui.success("[JOURNAL] " + entry + " recorded.")

            # Story cutscenes for first visit to key locations
            if new_loc in ("sewers", "sewer_chokepoint", "underground_lab"):
                cutscene.play_discover_underground()
            if new_loc in ("corpo_plaza", "executive_tower"):
                cutscene.play_enter_omnicorp()

        # Random encounter on move
        enemy_id = encounters.roll_encounter(
            self.player, new_loc,
            time_is_night=self.player.time.is_night)
        if enemy_id:
            desc = encounters.describe_encounter(enemy_id)
            ui.console.print()
            ui.warn(desc)
            import time as t; t.sleep(1.2)
            self._run_combat(enemy_id)

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

    def _cmd_travel(self):
        """Fast travel to a visited hub."""
        can, reason, has_card = ft_mod.can_fast_travel(self.player)
        if not can:
            ui.warn(reason)
            ui.pause()
            return
        hubs = ft_mod.get_available_hubs(self.player)
        ui.print_fast_travel(hubs, self.player)
        if not hubs:
            ui.pause()
            return
        choice = ui.get_input("Travel to # (or cancel)").strip().lower()
        if choice in ("cancel", "c", ""):
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(hubs):
                dest_id, dest_name = hubs[idx]
                result = ft_mod.fast_travel(self.player, dest_id)
                if result["success"]:
                    ui.success(result["message"])
                    # Journal/time tick
                    self.player.time.advance(8)  # Travel takes 2 hours
                    # Check journal
                    entry = self.player.journal.check_location(
                        dest_id, self.player.turn_count)
                    if entry:
                        ui.success("[JOURNAL] " + entry + " added.")
                else:
                    ui.warn(result["message"])
            else:
                ui.warn("Invalid number.")
        except ValueError:
            ui.warn("Enter a number.")
        ui.pause()

    def _cmd_craft(self):
        """Open crafting interface."""
        craftable = crafting_mod.list_craftable(self.player)
        if not craftable:
            ui.warn("No recipes available with your current skills and materials.")
            ui.info("Raise tech_repair, engineering, or first_aid to unlock recipes.")
            ui.pause()
            return
        ui.print_crafting_menu(craftable)
        ui.console.print("\n[bold]craft <number>[/bold] or [bold]cancel[/bold]")
        choice = ui.get_input("craft>").strip().lower()
        if choice in ("cancel", "c", ""):
            return
        parts = choice.split()
        if parts[0] != "craft" or len(parts) < 2:
            ui.warn("Type 'craft <number>'")
            ui.pause()
            return
        try:
            idx = int(parts[1]) - 1
            if 0 <= idx < len(craftable):
                recipe_id, recipe, _ = craftable[idx]
                result = crafting_mod.attempt_craft(self.player, recipe_id)
                if result["success"]:
                    ui.success(result["message"])
                    xp_events = self.player.gain_xp(20)
                    for e in xp_events:
                        ui.success(e)
                    self._check_levelup_cutscene(xp_events)
                else:
                    ui.warn(result["message"])
            else:
                ui.warn("Invalid number.")
        except ValueError:
            ui.warn("Enter a number.")
        ui.pause()

    def _cmd_journal(self):
        ui.print_journal(self.player)
        ui.pause()

    def _cmd_add_note(self, note: str):
        self.player.journal.add_note(note)
        ui.success("Note added to journal.")

    def _cmd_time(self):
        t = self.player.time
        ui.console.print("\n[bold cyan]" + t.time_string() + "[/bold cyan]")
        ui.console.print("[dim]" + t.period_desc + "[/dim]")

    def _cmd_companion(self):
        comp = self.player.companion
        if not comp:
            ui.console.print("[dim]No companion. Complete Old Marta's quest to recruit Riku.[/dim]")
        else:
            ui.console.print("\n[bold magenta]COMPANION: " + comp.full_name + "[/bold magenta]")
            ui.console.print(comp.status_line())
            ui.console.print("[dim]" + comp.personality + "[/dim]")

    def _cmd_rest(self):
        """Rest to recover HP. Risk of random encounter."""
        location = WORLD[self.player.location]
        ui.info("You rest...")
        self.player.time.advance(4)  # Rest = 1 hour

        # Check for encounter while resting
        enemy_id = encounters.roll_rest_encounter(
            self.player, self.player.location)
        if enemy_id:
            desc = encounters.describe_encounter(enemy_id)
            ui.warn("\n" + desc)
            ui.pause("Press Enter to fight...")
            self._run_combat(enemy_id)
            return

        # Recover HP
        recover = max(10, self.player.max_hp // 5)
        self.player.hp = min(self.player.max_hp, self.player.hp + recover)
        ui.success("Rested. Recovered " + str(recover) + " HP. (HP: " +
                   str(self.player.hp) + "/" + str(self.player.max_hp) + ")")
        ui.pause()

    def _cmd_map(self):
        ui.clear()
        ui.print_header()
        city_map.print_map(self.player)
        ui.pause()

    def _cmd_districts(self):
        ui.clear()
        ui.print_header()
        city_map.print_district_summary(self.player)
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
            from game.items import get_item, tier_label
            item_data = get_item(match)
            tier_info = ""
            if item_data:
                tier_info = " " + tier_label(item_data.get("tier", 1))
            ui.success("Picked up: " + item_display_name(match) + tier_info)
            # Story triggers
            if match == "blackwire_sample":
                cutscene.play_first_blackwire()
            elif item_data and item_data.get("tier", 1) >= 6:
                cutscene.play_found_legendary(item_display_name(match))
        else:
            ui.warn("No '" + target + "' here.")
        ui.pause()

    def _cmd_search(self, args):
        """Search for corpses or specific corpse to loot."""
        corpses = self.player.get_corpses_at(self.player.location)
        unfresh = [c for c in corpses if not c["looted"]]
        if not unfresh:
            ui.warn("No fresh bodies to search here.")
            ui.pause()
            return

        # If only one, auto-loot it
        if len(unfresh) == 1:
            idx = corpses.index(unfresh[0])
            self._do_loot_corpse(idx)
            return

        # Otherwise, show menu
        ui.console.print("\n[bold cyan]Bodies you can search:[/bold cyan]")
        for i, c in enumerate(corpses):
            if c["looted"]:
                continue
            ui.console.print("  [yellow]" + str(i + 1) + ".[/yellow] " + c["name"])

        choice = ui.get_input("Search which? (number, or 'cancel')").strip().lower()
        if choice in ("cancel", "c", ""):
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(corpses):
                self._do_loot_corpse(idx)
        except ValueError:
            ui.warn("Invalid choice.")
            ui.pause()

    def _do_loot_corpse(self, index: int):
        """Actually loot a corpse and show results."""
        loot = self.player.loot_corpse(self.player.location, index)
        if not loot:
            ui.warn("Nothing to loot.")
            ui.pause()
            return
        ui.success("\n>>> SEARCHED THE BODY <<<")
        if loot["credits"] > 0:
            ui.success("Found: " + str(loot["credits"]) + " credits")
        if loot["items"]:
            from game.items import tier_label, get_item
            for item_id in loot["items"]:
                item = get_item(item_id)
                if item:
                    tier = tier_label(item.get("tier", 1))
                    ui.success("Found: " + item_display_name(item_id) + " " + tier)
                    # Legendary find cutscene
                    if item.get("tier", 1) >= 6:
                        cutscene.play_found_legendary(item_display_name(item_id))
                    # Blackwire discovery
                    if item_id == "blackwire_sample":
                        cutscene.play_first_blackwire()
                else:
                    ui.success("Found: " + item_display_name(item_id))
        else:
            if loot["credits"] == 0:
                ui.console.print("[dim]Empty pockets. Nothing of value.[/dim]")
        ui.pause()

    def _cmd_shop(self, args, verb):
        """Open shop interface for the location's shopkeepers."""
        from game import shop as shop_mod

        location = WORLD[self.player.location]
        available_shops = shop_mod.shops_at_location(location)
        if not available_shops:
            ui.warn("No shops here.")
            ui.pause()
            return

        # Pick which shop
        if len(available_shops) == 1:
            chosen = available_shops[0]
        else:
            ui.console.print("\n[bold cyan]Shops here:[/bold cyan]")
            for i, s in enumerate(available_shops):
                ui.console.print("  [yellow]" + str(i + 1) + ".[/yellow] " + s["name"])
            choice = ui.get_input("Visit which? (number, or 'cancel')").strip().lower()
            if choice in ("cancel", "c", ""):
                return
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(available_shops):
                    chosen = available_shops[idx]
                else:
                    ui.warn("Invalid choice.")
                    ui.pause()
                    return
            except ValueError:
                ui.warn("Invalid choice.")
                ui.pause()
                return

        self._run_shop(chosen)

    def _run_shop(self, shop):
        """Interactive shop loop."""
        from game import shop as shop_mod
        from game.items import get_item, item_display_name, tier_label
        from game import relationships

        # First-time shop tutorial hint
        if not self.player.first_shop_opened:
            self.player.first_shop_opened = True
            cutscene.play_first_shop()

        npc_name = shop["name"]
        faction = shop["faction"]

        while True:
            ui.clear()
            ui.print_header()
            ui.print_status(self.player)

            # Header with shop info
            rep_score = self.player.reputation.get(faction, 0)
            rep_str = relationships.format_relationship(rep_score)
            ui.console.print("\n[bold cyan]+" + ("=" * 60) + "+[/bold cyan]")
            ui.console.print("[bold cyan]| " + npc_name.upper().ljust(58) + "|[/bold cyan]")
            ui.console.print("[bold cyan]+" + ("=" * 60) + "+[/bold cyan]")
            ui.console.print("[dim italic]\"" + shop["greeting"] + "\"[/dim italic]\n")
            ui.console.print("Faction: " + faction + "  |  Standing: " + rep_str)
            ui.console.print("Your credits: [yellow]" + str(self.player.credits) + "[/yellow]\n")

            # Show stock
            ui.console.print("[bold green]>> STOCK <<[/bold green]")
            stock_unique = []
            seen = {}
            for item_id in shop["stock"]:
                seen[item_id] = seen.get(item_id, 0) + 1
            for item_id, count in seen.items():
                stock_unique.append((item_id, count))

            for i, (item_id, count) in enumerate(stock_unique, 1):
                item = get_item(item_id)
                if not item:
                    continue
                price = shop_mod.calculate_buy_price(item_id, self.player, faction)
                tier = tier_label(item.get("tier", 1))
                affordable = "[green]" if price <= self.player.credits else "[red]"
                ui.console.print(
                    "  " + affordable + str(i) + ".[/" + affordable.strip("[]") + "] " +
                    item_display_name(item_id) + " " + tier +
                    "  [yellow]" + str(price) + " Cr[/yellow]" +
                    "  x" + str(count) + "  [dim]" + item.get("desc", "") + "[/dim]"
                )

            ui.console.print("\n[bold]Commands:[/bold]")
            ui.console.print("  [cyan]buy <number>[/cyan] - purchase")
            ui.console.print("  [cyan]sell[/cyan] - browse your inventory to sell")
            ui.console.print("  [cyan]leave[/cyan] - exit shop")

            choice = ui.get_input("shop>").strip().lower()
            if not choice:
                continue
            parts = choice.split()
            verb = parts[0]
            cargs = parts[1:]

            if verb in ("leave", "exit", "back", "l"):
                ui.success("You leave " + npc_name + "'s.")
                ui.pause()
                return

            elif verb == "buy":
                if not cargs:
                    ui.warn("Buy what number?")
                    ui.pause()
                    continue
                try:
                    idx = int(cargs[0]) - 1
                    if 0 <= idx < len(stock_unique):
                        item_id, _ = stock_unique[idx]
                        price = shop_mod.calculate_buy_price(item_id, self.player, faction)
                        if self.player.spend_credits(price):
                            self.player.add_item(item_id)
                            shop["stock"].remove(item_id)  # remove one copy
                            self.player.adjust_reputation(faction, +1)
                            ui.success("Bought " + item_display_name(item_id) + " for " +
                                       str(price) + " Cr")
                            ui.pause()
                        else:
                            ui.warn("Not enough credits. (Need " + str(price) +
                                    ", have " + str(self.player.credits) + ")")
                            ui.pause()
                    else:
                        ui.warn("Invalid item number.")
                        ui.pause()
                except ValueError:
                    ui.warn("Use 'buy <number>'")
                    ui.pause()

            elif verb == "sell":
                self._sell_to_shop(shop, faction)

            else:
                ui.warn("Unknown shop command.")
                ui.pause()

    def _sell_to_shop(self, shop, faction):
        """Show player's sellable inventory and let them sell."""
        from game import shop as shop_mod
        from game.items import get_item, item_display_name

        ui.clear()
        ui.print_header()
        ui.console.print("\n[bold cyan]>> SELL TO " + shop["name"].upper() + " <<[/bold cyan]\n")
        ui.console.print("Your credits: [yellow]" + str(self.player.credits) + "[/yellow]\n")

        sellable = [i for i in self.player.inventory if get_item(i) and get_item(i)["type"] != "quest"]
        if not sellable:
            ui.warn("Nothing to sell.")
            ui.pause()
            return

        for i, item_id in enumerate(sellable, 1):
            item = get_item(item_id)
            sell_price = shop_mod.calculate_sell_price(item_id, self.player, faction)
            breakdown = shop_mod.get_sell_price_breakdown(item_id, self.player, faction)
            equipped = ""
            if item_id in self.player.equipped.values():
                equipped = " [E]"
            from game.items import tier_label
            tier = tier_label(item.get("tier", 1)) if item else ""
            ui.console.print(
                "  [yellow]" + str(i) + ".[/yellow] " +
                item_display_name(item_id) + equipped + " " + tier +
                "  [green]" + str(sell_price) + " Cr[/green]" +
                "  [dim]" + breakdown + "[/dim]"
            )

        ui.console.print("\n[bold]'sell <number>' or 'back'[/bold]")
        choice = ui.get_input("sell>").strip().lower()
        if choice in ("back", "b", "cancel", ""):
            return
        parts = choice.split()
        if parts[0] != "sell" or len(parts) < 2:
            ui.warn("Use 'sell <number>'")
            ui.pause()
            return
        try:
            idx = int(parts[1]) - 1
            if 0 <= idx < len(sellable):
                item_id = sellable[idx]
                # Check if item is equipped in any slot
                equipped_slot = None
                for slot, equipped_id in self.player.equipped.items():
                    if equipped_id == item_id:
                        equipped_slot = slot
                        break
                if equipped_slot:
                    confirm = ui.get_input("That's equipped (" + equipped_slot + "). Sell anyway? (y/n)").lower()
                    if confirm not in ("y", "yes"):
                        return
                    self.player.equipped[equipped_slot] = None

                price = shop_mod.calculate_sell_price(item_id, self.player, faction)
                self.player.remove_item(item_id)
                self.player.add_credits(price)
                ui.success("Sold " + item_display_name(item_id) + " for " + str(price) + " Cr")
                ui.pause()
        except ValueError:
            ui.warn("Invalid number.")
            ui.pause()

    def _cmd_relations(self):
        """Show all NPC and faction relationships."""
        from game import relationships
        from rich.table import Table
        from rich import box

        ui.clear()
        ui.print_header()

        # Factions
        ui.console.print("\n[bold cyan]>> FACTION STANDINGS <<[/bold cyan]\n")
        ftable = Table(box=box.SIMPLE_HEAVY, border_style="cyan")
        ftable.add_column("Faction", style="cyan")
        ftable.add_column("Standing")
        ftable.add_column("Effect", style="dim")
        for fac, score in self.player.reputation.items():
            tier = relationships.get_tier(score)
            ftable.add_row(
                fac,
                "[" + tier["color"] + "]" + tier["name"] + " (" + str(score) + ")[/" + tier["color"] + "]",
                tier["desc"],
            )
        ui.console.print(ftable)

        # NPCs
        if self.player.npc_relationships:
            ui.console.print("\n[bold magenta]>> KNOWN NPCS <<[/bold magenta]\n")
            ntable = Table(box=box.SIMPLE_HEAVY, border_style="magenta")
            ntable.add_column("NPC", style="magenta")
            ntable.add_column("Relationship")
            for npc, score in self.player.npc_relationships.items():
                tier = relationships.get_tier(score)
                ntable.add_row(
                    npc,
                    "[" + tier["color"] + "]" + tier["name"] + " (" + str(score) + ")[/" + tier["color"] + "]",
                )
            ui.console.print(ntable)
        else:
            ui.console.print("\n[dim]No notable NPC relationships yet. Talk to people.[/dim]")

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

    def _cmd_accept_quest(self):
        q = self.player.pending_quest
        if not q:
            ui.warn("No pending quest to accept.")
            ui.pause()
            return
        self.player.add_quest(q[0], q[1])
        self.player.pending_quest = None
        xp_events = self.player.gain_xp(XP_REWARDS["first_time_action"])
        cutscene.play_quest_accepted(q[0])
        ui.success("Quest accepted: " + q[0])
        for e in xp_events:
            ui.success(e)
        self._check_levelup_cutscene(xp_events)
        self.player.save()
        ui.pause()

    def _cmd_decline_quest(self):
        q = self.player.pending_quest
        if not q:
            ui.warn("No pending quest to decline.")
            ui.pause()
            return
        self.player.pending_quest = None
        ui.warn("You declined: " + q[0])
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

    # ============================================================
    # AI HANDLING
    # ============================================================

    def _handle_ai(self, cmd: str):
        """Handle a freeform AI action. Core of the AI NPC experience.

        Assembles the richest possible context so the AI can deliver
        on the core purpose: living NPCs that remember, react, and feel real.
        """
        ui.console.print()
        ui.info(">> connecting to grid...")

        self.player.turn_count += 1
        self.player.time.advance(1)

        location = WORLD[self.player.location]

        # ── Skill check detection ──────────────────────────────
        skill, dc, stat = skills_mod.detect_skill_check(cmd)
        check_result = None
        skill_ctx = ""
        if skill:
            check_result = skills_mod.skill_check(self.player, skill, dc, stat)
            skill_ctx = skills_mod.format_check_for_ai(check_result)

        # ── NPC memory injection ───────────────────────────────
        # Detect every NPC mentioned or present when player is talking
        npc_memory_parts = []
        talked_to_npcs = []
        is_social = any(w in cmd.lower() for w in
                        ["talk", "ask", "tell", "say", "speak", "approach",
                         "greet", "question", "negotiate", "persuade", "threaten"])
        for npc_full in location.get("npcs", []):
            clean = npc_full.split("(")[0].strip()
            npc_named = clean.lower() in cmd.lower()
            if npc_named or is_social:
                self.player.npc_memory.record_meeting(clean, location["name"])
                self.player.journal.meet_npc(clean)
                mem_ctx = self.player.npc_memory.build_context_for_ai(clean, self.player)
                if mem_ctx:
                    npc_memory_parts.append(mem_ctx)
                talked_to_npcs.append(clean)
                if npc_named:
                    break

        npc_memory_ctx = "\n\n".join(npc_memory_parts)

        # ── Build and send ─────────────────────────────────────
        context = ai_engine.build_context(
            self.player, location, cmd,
            npc_memory_ctx=npc_memory_ctx,
            skill_ctx=skill_ctx,
        )
        raw = ai_engine.query_ollama(self.player.history, context)
        parsed = ai_engine.parse_response(raw)

        # ── Persist to history and NPC memory ─────────────────
        self.player.add_to_history("user", "ACTION: " + cmd)
        self.player.add_to_history("assistant", raw)

        for npc_name in talked_to_npcs:
            self.player.npc_memory.add_exchange(
                npc_name, cmd, parsed["narrative"][:250])
            if parsed.get("quest_offer") or parsed.get("credits", 0) > 0:
                self.player.npc_memory.adjust_score(npc_name, +5)

        # ── Apply structured effects ───────────────────────────
        effect_msgs = self._apply_ai_effects(parsed)

        # ── Skill XP ──────────────────────────────────────────
        if check_result and check_result["tier"] in ("success", "critical_success", "partial"):
            xp_events = self.player.gain_xp(XP_REWARDS["successful_skill_check"])
            effect_msgs.extend(xp_events)

        # ── Render inline ─────────────────────────────────────
        ui.console.print()
        ui.print_narrative(parsed)

        if check_result:
            tier_colors = {
                "critical_success": "bold green", "success": "green",
                "partial": "yellow", "failure": "red", "critical_failure": "bold red",
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

        if parsed.get("quest_offer") and self.player.pending_quest:
            ui.console.print()
            ui.print_pending_quest(self.player.pending_quest)

        # Companion idle comment (15% chance)
        if self.player.companion and self.player.companion.is_active:
            comment = self.player.companion.random_idle_comment()
            if comment:
                ui.console.print("\n[dim italic]" + comment + "[/dim italic]")

        self._check_levelup_cutscene(effect_msgs)

        if parsed.get("combat_start"):
            ui.console.print()
            ui.warn("Combat is starting...")
            import time as _t
            _t.sleep(0.8)
            self._run_combat(parsed["combat_start"])
            self._render_world()
            return



    def _apply_ai_effects(self, parsed: dict) -> list:
        msgs = []

        for item_id in parsed.get("item_gains", []):
            if get_item(item_id):
                self.player.add_item(item_id)
                msgs.append("+ " + item_display_name(item_id))
                # Trigger story cutscenes for special items
                if item_id == "blackwire_sample":
                    cutscene.play_first_blackwire()
                elif get_item(item_id) and get_item(item_id).get("tier", 1) >= 6:
                    cutscene.play_found_legendary(item_display_name(item_id))
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
            self.player.pending_quest = q
            msgs.append("[QUEST OFFERED: " + q[0] + "]")
            msgs.append("Type 'accept' to take it or 'decline' to refuse.")

        qc = parsed.get("quest_complete")
        if qc:
            if self.player.complete_quest(qc):
                from game.character import XP_REWARDS
                xp_events = self.player.gain_xp(XP_REWARDS.get("complete_quest_minor", 100))
                msgs.extend(xp_events)
                msgs.append("QUEST COMPLETE: " + qc)
                cutscene.play_quest_completed(qc, XP_REWARDS.get("complete_quest_minor", 100))

        # Journal entry from AI
        jentry = parsed.get("journal_entry")
        if jentry:
            if self.player.journal.add_clue(jentry):
                msgs.append("[JOURNAL] Clue recorded.")

        return msgs

    # ============== COMBAT ==============

    def _run_combat(self, enemy_id: str):
        combat = Combat(self.player, enemy_id)
        self.player.in_combat = True

        # Play combat intro cutscene
        cutscene.play_combat_intro(combat.enemy["name"])

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
                # Companion attacks too
                comp_msg = combat.companion_attack()
                if comp_msg:
                    log.append(comp_msg)
                if combat.is_enemy_dead():
                    break
                # Boss phase 2 check
                if combat.check_phase_two():
                    log.append("[bold red]" + combat.enemy["name"] + " ENRAGES![/bold red]")
                # Enemy turn
                log.append(combat.enemy_attack())
                # Status effect ticks
                log.extend(combat.tick_player_effects())
                log.extend(combat.tick_enemy_effects())

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
                    log.extend(combat.tick_player_effects())
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
                log.extend(combat.tick_player_effects())

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
            # Play victory cutscene
            cutscene.play_victory(combat.enemy["name"])

            ui.print_header()
            ui.print_status(self.player)
            ui.success("\n>>> " + combat.enemy["name"] + " DEFEATED <<<")

            # Calculate loot but don't auto-apply - drop as corpse
            loot = combat.calculate_loot()
            self.player.add_corpse(
                self.player.location,
                combat.enemy["name"],
                loot["credits"],
                loot["items"],
            )
            ui.console.print(
                "\n[dim]The body lies at your feet. Type 'search' to loot it.[/dim]"
            )

            # Award XP based on enemy level
            xp_amount = self._enemy_xp_value(combat.enemy_id, combat.enemy)
            xp_events = self.player.gain_xp(xp_amount)
            for e in xp_events:
                ui.success(e)

            # Trigger level-up cutscene if any
            self._check_levelup_cutscene(xp_events)

            # Faction & NPC adjustments - check if tier changed
            def rep_adjust_with_cutscene(faction, delta):
                from game import relationships
                old_tier = relationships.get_tier_name(self.player.reputation.get(faction, 0))
                self.player.adjust_reputation(faction, delta)
                new_tier = relationships.get_tier_name(self.player.reputation.get(faction, 0))
                if old_tier != new_tier:
                    cutscene.play_faction_status_change(
                        faction, new_tier, delta > 0)

            if "corpo" in enemy_id or "tower" in enemy_id or "elite" in enemy_id or "ishikawa" in enemy_id:
                rep_adjust_with_cutscene("corpo", -8)
                rep_adjust_with_cutscene("gangs", +3)
                rep_adjust_with_cutscene("hackers", +2)
            elif "rail" in enemy_id:
                rep_adjust_with_cutscene("gangs", -5)
            elif "alley_ganger" in enemy_id:
                rep_adjust_with_cutscene("gangs", -5)
            elif "scavenger" in enemy_id:
                rep_adjust_with_cutscene("scavengers", -5)

        elif not self.player.is_alive():
            ui.error("\n>>> YOU HAVE BEEN KILLED <<<")

        self.player.in_combat = False
        ui.pause()

    def _check_levelup_cutscene(self, events: list):
        """If level-up events are present, play the cutscene."""
        for e in events:
            if "LEVEL UP" in e:
                cutscene.play_level_up(self.player.level)
                break

    def _enemy_xp_value(self, enemy_id: str, enemy_data: dict) -> int:
        """Calculate XP based on enemy level."""
        level = enemy_data.get("level", 3)
        if level <= 2:
            return XP_REWARDS["kill_low"]
        elif level <= 6:
            return XP_REWARDS["kill_mid"]
        else:
            return XP_REWARDS["kill_high"]

    # ============== END ==============

    def _game_over(self):
        cutscene.play_game_over(self.player)

