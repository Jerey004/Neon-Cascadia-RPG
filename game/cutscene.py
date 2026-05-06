"""Cutscene playback engine.

A cutscene is a sequence of beats - ART, TEXT, PAUSE, CLEAR, or INPUT.
Timing is tuned for Termux mobile (phone screen, slower reading).

TIMING GUIDE:
  typewriter delay 0.03 = comfortable reading pace on mobile
  end_pause 0.9-1.2     = enough time to read a full line before next
  district pause 2.5    = long enough to see the art, not feel stuck
  title pause 1.0       = renders, settles, then waits for input
"""
import time
import sys
from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich import box
from game.art import ascii_art

console = Console()


# ============================================================
# CORE RENDER PRIMITIVES
# ============================================================

def render_art(art: str, color: str = "cyan", center: bool = True, glow: bool = False):
    """Render an ASCII art block in the given color."""
    console.print()
    text = Text(art, style=color)
    if glow:
        console.print(Panel(text, border_style=color, box=box.HEAVY, padding=(0, 1)))
    elif center:
        console.print(Align.center(text))
    else:
        console.print(text)
    console.print()


def typewriter(text: str, color: str = "white", delay: float = 0.03,
               end_pause: float = 1.0):
    """Print text character by character.

    delay=0.03 feels natural on mobile without being annoying.
    end_pause should be at least 0.9 so the reader can finish the line.
    """
    for char in text:
        console.print("[" + color + "]" + char + "[/" + color + "]", end="")
        sys.stdout.flush()
        time.sleep(delay)
    console.print()
    if end_pause > 0:
        time.sleep(end_pause)


def pause_for(seconds: float):
    time.sleep(seconds)


def wait_for_input(prompt: str = "[ press ENTER to continue ]"):
    console.input("\n[dim]" + prompt + "[/dim]")


# ============================================================
# SCENE PLAYER
# ============================================================

def play_scene(beats: list, allow_skip: bool = True):
    """Play a list of cutscene beats.

    Beat types:
      {"type": "clear"}
      {"type": "art",   "art": str,  "color": str, "glow": bool}
      {"type": "text",  "text": str, "color": str, "delay": float, "end_pause": float}
      {"type": "pause", "seconds": float}
      {"type": "input", "prompt": str}
    """
    console.clear()

    if allow_skip:
        console.print("[dim](Ctrl+C to skip)[/dim]\n")
        time.sleep(0.3)

    try:
        for beat in beats:
            kind = beat.get("type", "text")

            if kind == "clear":
                console.clear()

            elif kind == "art":
                render_art(
                    beat["art"],
                    color=beat.get("color", "cyan"),
                    center=beat.get("center", True),
                    glow=beat.get("glow", False),
                )

            elif kind == "text":
                typewriter(
                    beat["text"],
                    color=beat.get("color", "white"),
                    delay=beat.get("delay", 0.03),
                    end_pause=beat.get("end_pause", 1.0),
                )

            elif kind == "pause":
                pause_for(beat.get("seconds", 1.0))

            elif kind == "input":
                wait_for_input(beat.get("prompt", "[ press ENTER to continue ]"))

    except KeyboardInterrupt:
        console.print("\n\n[dim](skipped)[/dim]\n")
        time.sleep(0.2)


# ============================================================
# PRESET CUTSCENES
# ============================================================

def play_title_screen():
    """Initial title screen - renders and waits for input."""
    console.clear()
    render_art(ascii_art.TITLE, color="bold cyan", glow=False)
    time.sleep(1.0)   # Let title settle before showing prompt
    console.print(Align.center(Text("press ENTER to begin", style="dim yellow")))
    console.input("")


def play_intro_cutscene(player):
    """Cinematic intro after character creation."""
    portrait = ascii_art.get_class_portrait(player.class_id)

    # Class-specific opening lines - kept short for readability on mobile
    intro_lines = {
        "street_samurai": [
            "Steel and rain.",
            "The slums never sleep.",
            "Your blade hangs ready, " + player.name + ".",
            "Time to make some history.",
        ],
        "netrunner": [
            "The grid hums in your skull.",
            "Three days off-net. Too long.",
            "You jack in, " + player.name + ".",
            "The wires welcome you home.",
        ],
        "fixer": [
            "Three jobs. Two debts. One enemy.",
            "Just another Tuesday in the city.",
            "You step into the rain, " + player.name + ".",
            "Time to do business.",
        ],
        "tech": [
            "Your hands smell of solder.",
            "Three half-built drones on the bench.",
            "You crack your knuckles, " + player.name + ".",
            "Time to get to work.",
        ],
        "medic": [
            "Blood under your fingernails.",
            "Six patients last night. Four lived.",
            "Decent odds for the slums, " + player.name + ".",
            "The sirens never stop.",
        ],
        "ex_corpo": [
            "Six months out. They're still hunting.",
            "You touch the old badge in your pocket.",
            "Time to use what you stole, " + player.name + ".",
            "Before they catch up.",
        ],
    }
    lines = intro_lines.get(player.class_id,
                            ["Welcome to Neon Cascadia, " + player.name + "."])

    beats = [
        {"type": "clear"},
        # Skyline + city reveal
        {"type": "art", "art": ascii_art.SKYLINE, "color": "cyan"},
        {"type": "pause", "seconds": 1.2},
        {"type": "text", "text": "Year 2087.  Neon Cascadia.",
         "color": "bold magenta", "delay": 0.05, "end_pause": 1.4},
        {"type": "text", "text": "Population: too many.  Hope: too little.",
         "color": "magenta", "delay": 0.04, "end_pause": 1.6},
        {"type": "text", "text": "The megacorps own the sky.  The gangs own the streets.",
         "color": "dim magenta", "delay": 0.03, "end_pause": 1.8},
        # Jack-in animation
        {"type": "clear"},
        {"type": "art", "art": ascii_art.JACK_IN, "color": "green"},
        {"type": "pause", "seconds": 1.2},
        # Character portrait
        {"type": "clear"},
        {"type": "art", "art": portrait, "color": "bold cyan", "glow": True},
        {"type": "pause", "seconds": 0.8},
    ]

    # Class intro lines - 1.1s each so they're readable
    for line in lines:
        beats.append({"type": "text", "text": line,
                      "color": "white", "delay": 0.035, "end_pause": 1.1})

    beats.append({"type": "pause", "seconds": 0.5})
    beats.append({"type": "input",
                  "prompt": "[ press ENTER to enter the city ]"})

    play_scene(beats, allow_skip=True)


def play_district_transition(district_name: str):
    """Brief banner when entering a new district for the first time."""
    art = ascii_art.get_district_art(district_name)
    if not art:
        return
    beats = [
        {"type": "clear"},
        {"type": "art", "art": art, "color": "bold magenta"},
        {"type": "pause", "seconds": 2.5},   # Long enough to read on mobile
        {"type": "text", "text": "Entering: " + district_name,
         "color": "dim cyan", "delay": 0.025, "end_pause": 0.6},
    ]
    play_scene(beats, allow_skip=True)


def play_combat_intro(enemy_name: str):
    """Brief banner before combat begins."""
    beats = [
        {"type": "art", "art": ascii_art.COMBAT_BANNER, "color": "bold red"},
        {"type": "text", "text": "Target acquired:  " + enemy_name,
         "color": "red", "delay": 0.04, "end_pause": 0.8},
        {"type": "pause", "seconds": 0.5},
    ]
    play_scene(beats, allow_skip=True)


def play_victory(enemy_name: str):
    """Played when an enemy is defeated."""
    beats = [
        {"type": "art", "art": ascii_art.VICTORY, "color": "bold green"},
        {"type": "text", "text": enemy_name + " is down.",
         "color": "green", "delay": 0.04, "end_pause": 0.8},
    ]
    play_scene(beats, allow_skip=True)


def play_level_up(new_level: int):
    """Played on level up."""
    beats = [
        {"type": "art", "art": ascii_art.LEVEL_UP, "color": "bold yellow", "glow": True},
        {"type": "text", "text": ">>> NOW LEVEL " + str(new_level) + " <<<",
         "color": "bold yellow", "delay": 0.05, "end_pause": 1.0},
        {"type": "text", "text": "New stat and skill points available.",
         "color": "cyan", "delay": 0.03, "end_pause": 0.8},
        {"type": "text", "text": "Type 'levelup' to spend them.",
         "color": "dim cyan", "delay": 0.025, "end_pause": 0.5},
        {"type": "pause", "seconds": 0.4},
    ]
    play_scene(beats, allow_skip=True)


def play_game_over(player):
    """Cinematic death screen."""
    beats = [
        {"type": "clear"},
        {"type": "pause", "seconds": 0.8},
        {"type": "art", "art": ascii_art.GAME_OVER, "color": "bold red"},
        {"type": "pause", "seconds": 1.2},
        {"type": "text",
         "text": player.name + "  -  Level " + str(player.level) +
                 "  " + (player.class_name or "Runner"),
         "color": "red", "delay": 0.05, "end_pause": 1.0},
        {"type": "text",
         "text": "XP: " + str(player.xp) +
                 "   Locations visited: " + str(len(player.visited)) +
                 "   Credits: " + str(player.credits),
         "color": "dim red", "delay": 0.03, "end_pause": 1.2},
        {"type": "text",
         "text": "The grid forgets you in three seconds.",
         "color": "dim white", "delay": 0.04, "end_pause": 1.5},
    ]
    play_scene(beats, allow_skip=False)


def play_quest_accepted(quest_title: str):
    """Flash when accepting a quest."""
    art = r"""
    + - - - - - - - - - - - - - - - - +
    |     * QUEST ACCEPTED *           |
    + - - - - - - - - - - - - - - - - +
    """
    beats = [
        {"type": "art", "art": art, "color": "bold yellow"},
        {"type": "text", "text": quest_title,
         "color": "yellow", "delay": 0.04, "end_pause": 0.8},
    ]
    play_scene(beats, allow_skip=True)


def play_quest_completed(quest_title: str, xp_reward: int = 100):
    """Played when a quest is completed."""
    art = r"""
    + - - - - - - - - - - - - - - - - - +
    |     * OBJECTIVE COMPLETE *         |
    + - - - - - - - - - - - - - - - - - +
    """
    beats = [
        {"type": "art", "art": art, "color": "bold green"},
        {"type": "text", "text": quest_title + " - complete.",
         "color": "green", "delay": 0.04, "end_pause": 0.8},
        {"type": "text", "text": "+" + str(xp_reward) + " XP",
         "color": "bold yellow", "delay": 0.05, "end_pause": 0.8},
    ]
    play_scene(beats, allow_skip=True)


def play_first_blackwire():
    """Story cutscene: player first encounters BLACKWIRE evidence."""
    art = r"""
     |||||||||||||||||||||||||||||||||||||||||
     |  WARNING: UNKNOWN PATHOGEN DETECTED  |
     |  NEURAL INTERFACE COMPROMISED        |
     |  CONTAMINANT:   B L A C K W I R E   |
     |||||||||||||||||||||||||||||||||||||||||
    """
    beats = [
        {"type": "clear"},
        {"type": "art", "art": art, "color": "bold red", "glow": True},
        {"type": "pause", "seconds": 1.0},
        {"type": "text", "text": "Someone is killing people from the inside.",
         "color": "red", "delay": 0.04, "end_pause": 1.2},
        {"type": "text", "text": "Through their own cyberware.",
         "color": "red", "delay": 0.04, "end_pause": 1.5},
        {"type": "text", "text": "This isn't random.",
         "color": "bold red", "delay": 0.05, "end_pause": 1.8},
        {"type": "input", "prompt": "[ press ENTER ]"},
    ]
    play_scene(beats, allow_skip=True)


def play_enter_omnicorp():
    """Story cutscene: player enters OmniCorp territory."""
    art = r"""
      ____  __  __ _   _ ___ ____  ___  ____  ____
     / __ \|  \/  | \ | |_ _/ ___|/ _ \|  _ \|  _ \\
    | |  | | |\/| |  \| || || |   | | | | |_) | |_) |
    | |__| | |  | | |\  || || |___| |_| |  _ <|  __/
     \____/|_|  |_|_| \_|___\____|\___/|_| \_\_|

           [ AUTHORIZED PERSONNEL ONLY ]
           [ ALL ACTIVITY MONITORED    ]
           [ TRESPASSERS WILL BE ENDED ]
    """
    beats = [
        {"type": "clear"},
        {"type": "art", "art": art, "color": "bold cyan"},
        {"type": "pause", "seconds": 1.2},
        {"type": "text", "text": "You don't belong here.",
         "color": "yellow", "delay": 0.04, "end_pause": 1.0},
        {"type": "text", "text": "Everyone in this building knows it.",
         "color": "yellow", "delay": 0.03, "end_pause": 1.2},
        {"type": "text", "text": "Act like you do.",
         "color": "bold white", "delay": 0.05, "end_pause": 1.5},
        {"type": "input", "prompt": "[ press ENTER ]"},
    ]
    play_scene(beats, allow_skip=True)


def play_discover_underground():
    """Story cutscene: player goes underground / sewers for first time."""
    art = r"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . ~
    ~  .  d  e  e  p  e  r  .  d  o  w  n  .  .  . ~
    ~  .  .  .  .  .  .  .  .  .  .  .  .  .  .  . ~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         [something lives down here]
         [it has been waiting]
    """
    beats = [
        {"type": "clear"},
        {"type": "art", "art": art, "color": "dim cyan"},
        {"type": "pause", "seconds": 1.5},
        {"type": "text", "text": "The city above doesn't know this exists.",
         "color": "dim white", "delay": 0.035, "end_pause": 1.2},
        {"type": "text", "text": "Whatever happened here — it wasn't an accident.",
         "color": "dim white", "delay": 0.035, "end_pause": 1.5},
        {"type": "input", "prompt": "[ press ENTER ]"},
    ]
    play_scene(beats, allow_skip=True)


def play_found_legendary(item_name: str):
    """Flash when a legendary item is discovered."""
    art = r"""
     * * * * * * * * * * * * * * * * * * *
     *   L E G E N D A R Y   F I N D    *
     * * * * * * * * * * * * * * * * * * *
    """
    beats = [
        {"type": "art", "art": art, "color": "bold yellow", "glow": True},
        {"type": "text", "text": item_name,
         "color": "bold yellow", "delay": 0.05, "end_pause": 1.2},
        {"type": "text", "text": "They say only a handful exist in the city.",
         "color": "dim yellow", "delay": 0.03, "end_pause": 1.0},
    ]
    play_scene(beats, allow_skip=True)


def play_faction_status_change(faction: str, new_tier: str, positive: bool):
    """Brief flash when faction relationship changes tier."""
    color = "green" if positive else "red"
    direction = "improved" if positive else "worsened"
    art = r"""
     + - - - - - - - - - - - - - - +
     |   FACTION STATUS CHANGED    |
     + - - - - - - - - - - - - - - +
    """
    beats = [
        {"type": "art", "art": art, "color": color},
        {"type": "text", "text": faction + " standing " + direction + ".",
         "color": color, "delay": 0.04, "end_pause": 0.8},
        {"type": "text", "text": "New status: " + new_tier,
         "color": "bold " + color, "delay": 0.04, "end_pause": 0.8},
    ]
    play_scene(beats, allow_skip=True)


def play_first_shop():
    """Brief tutorial hint the first time a shop is opened."""
    beats = [
        {"type": "text",
         "text": "TIP: Your relationship with a faction changes prices.",
         "color": "dim cyan", "delay": 0.02, "end_pause": 1.0},
        {"type": "text",
         "text": "Friends give discounts. Enemies gouge. Barter skill helps too.",
         "color": "dim cyan", "delay": 0.02, "end_pause": 1.2},
    ]
    play_scene(beats, allow_skip=True)


def play_intro_rain():
    """Ambient rain scene for between-scene pauses."""
    beats = [
        {"type": "art", "art": ascii_art.RAIN_SCENE, "color": "dim cyan"},
        {"type": "pause", "seconds": 1.5},
    ]
    play_scene(beats, allow_skip=True)
