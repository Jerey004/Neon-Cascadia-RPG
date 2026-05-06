"""ASCII/ANSI art library.

Each piece is a string. The cutscene engine handles colored rendering.
Width is kept under ~70 chars to fit Termux portrait mode comfortably.
"""

# ============================================================
# TITLE SCREEN
# ============================================================
TITLE = r"""
   _   _ ___ ___  _   _    ___   _   ___  ___   _   ___ ___ _
  | \ | | __/ _ \| \ | |  / __| /_\ / __|/ __| /_\ |   \_ _/_\
  | .` | _| (_) | .` | | (__ / _ \\__ \ (__ / _ \| |) | |/ _ \
  |_|\_|___\___/|_|\_|  \___/_/ \_\___/\___/_/ \_\___/___/_/ \_\

         + + + + + + + + + + + + + + + + + + + + + + +
                       v 2 0 8 7
         + + + + + + + + + + + + + + + + + + + + + + +

              [ THE GRID NEVER SLEEPS ]
"""


# ============================================================
# CITY SKYLINE (used at intro & district transitions)
# ============================================================
SKYLINE = r"""
                                            .
                  .             |       .   |    .
        |    |    |       .    |||      |   |   ||
       |||  |||  |||      |   |||||    |||  |  ||||
      |||||||||| |||  .  ||  |||||||  |||||| |||||| .
   __||||||||||| |||___||||__||||||||_||||||||||||||||___
  /   |||||||||||||| ||||||| |||||||| |||||||||||||| |||\
  |[]| |||  ||| |||| |||  || |||  ||| |||| ||| |||||| []|
  | |##|||##|||#||||#||| ## |||## ||| ||||#||| ||||||##| |
  | | _||| ||| ||||  | _ ||  | _ ||| |||| ||| ||||||  | |
  |_|/_|||_|||_||||__|/_||___|/_|||__||||_|||_||||||__|_|
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
       N E O - C A S C A D I A      [ rain on chrome ]
"""


# ============================================================
# DEATH / GAME OVER
# ============================================================
GAME_OVER = r"""
   ____    _    __  __ _____    _____     _______ ____
  / ___|  / \  |  \/  | ____|  / _ \ \   / / ____|  _ \
 | |  _  / _ \ | |\/| |  _|   | | | \ \ / /|  _| | |_) |
 | |_| |/ ___ \| |  | | |___  | |_| |\ V / | |___|  _ <
  \____/_/   \_\_|  |_|_____|  \___/  \_/  |_____|_| \_\

         + - - - - - - - - - - - - - - - - +
         |   The neon flickers on without you. |
         |   Your story ends in the static.    |
         + - - - - - - - - - - - - - - - - +
"""


# ============================================================
# LEVEL UP
# ============================================================
LEVEL_UP = r"""
       _______________________________________
      |                                       |
      |   * * *   L E V E L   U P   * * *   |
      |                                       |
      |          [SYSTEM UPGRADE OK]          |
      |       New abilities unlocked.         |
      |_______________________________________|

           //   \\   //   \\   //   \\
          (( + ))  (( + ))  (( + ))
           \\   //   \\   //   \\   //
"""


# ============================================================
# COMBAT BANNER
# ============================================================
COMBAT_BANNER = r"""
   ___ ___  __  __ ___    _  _____   ___ _  _ ___ _____ _   _____ ___
  / __/ _ \|  \/  | _ )  /_\|_   _| |_ _| \| |_ _|_   _(_) /_\_ _|   \
 | (_| (_) | |\/| | _ \ / _ \ | |    | || .` || |  | | _ / _ \| || |) |
  \___\___/|_|  |_|___//_/ \_\|_|   |___|_|\_|___| |_|(_)_/ \_\___|___/

                ~~~  weapons hot. stay sharp.  ~~~
"""


# ============================================================
# VICTORY (combat win)
# ============================================================
VICTORY = r"""
        + - - - - - - - - - - - - - - - - +
        |     T A R G E T   D O W N        |
        + - - - - - - - - - - - - - - - - +
              [ scanning for loot... ]
"""


# ============================================================
# CHARACTER CREATION INTRO
# ============================================================
JACK_IN = r"""
        .-----------------------------.
        |                             |
        |   J A C K I N G   I N . . . |
        |                             |
        |     [||||||||||||||||]      |
        |     neural link: OK         |
        |     uplink:      OK         |
        |     wetware:     OK         |
        |                             |
        '-----------------------------'

           Welcome to the grid, runner.
"""


# ============================================================
# DISTRICT BANNERS (shown when entering a new district)
# ============================================================
DISTRICT_SLUMS = r"""
   ___ _   _   _ __  __ ___
  / __| | | | | |  \/  / __|     Block 9 - Where you started.
  \__ \ |_| |_| | |\/| \__ \     Where most of you will end.
  |___/____\___/|_|  |_|___/
"""

DISTRICT_MARKET = r"""
  __  __   _   ___ _  _____ _____
 |  \/  | /_\ | _ \ |/ / __|_   _|     Anything sold. Anyone bought.
 | |\/| |/ _ \|   / ' <| _|  | |
 |_|  |_/_/ \_\_|_\_|\_\___| |_|
"""

DISTRICT_CORPO = r"""
   ___ ___  ___ ___  ___
  / __/ _ \| _ \ _ \/ _ \      Polished hell. Smile for the cameras.
 | (_| (_) |   /  _/ (_) |
  \___\___/|_|_\_|  \___/
"""

DISTRICT_NET = r"""
  _   _ ___ _____
 | \ | | __|_   _|     The wires hum. The ghosts watch.
 |  \| | _|  | |
 |_|\_|___| |_|
"""

DISTRICT_INDUSTRIAL = r"""
  ___ _  _ ___  _   _ ___ _____ ___ ___   _ _
 |_ _| \| |   \| | | / __|_   _| _ \_ _| /_\ |        Rust and ruin.
  | || .` | |) | |_| \__ \ | | |   /| | / _ \|_       Where machines die.
 |___|_|\_|___/ \___/|___/ |_| |_|_\___/_/ \_\
"""

DISTRICT_UNDERGROUND = r"""
  _   _ _  _ ___  ___ ___ ___ ___  ___  _   _ _  _ ___
 | | | | \| |   \| __| _ \ __| _ \/ _ \| | | | \| |   \    Don't go alone.
 | |_| | .` | |) | _||   / _||   / (_) | |_| | .` | |) |
  \___/|_|\_|___/|___|_|_\___|_|_\\___/ \___/|_|\_|___/
"""


# ============================================================
# CHARACTER CLASS PORTRAITS
# ============================================================
PORTRAIT_SAMURAI = r"""
        ___
       /   \
      | o o |     STREET SAMURAI
      |  ^  |     "All problems have edges."
       \___/
      __|||__
     /  | |  \
    |   | |   |
    |   |/|   |
    |   /\ \  |     [katana glints]
    |  /  \ \ |
    | /    \ \|
"""

PORTRAIT_NETRUNNER = r"""
       ____
      / [] \
     | /\/\ |     NETRUNNER
     | \--/ |     "I am the wires."
      \____/
       /||\
      / || \
     /  || (((
    [(  ||  )]    [neural data stream]
     \  ||  /
      \_||_/
"""

PORTRAIT_FIXER = r"""
        ___
       / _ \
      |(o o)|     FIXER
      | --- |     "Everything has a price."
       \___/
       /||\
      / [|]\
     |  $$$ |
     |  ||| |     [carries credstick]
     |  /|\ |
     | / | \|
"""

PORTRAIT_TECH = r"""
        ___
       /[+]\
      | -.- |     TECH
      |  o  |     "Built different."
       \___/
       /|@|\
      / |X| \
     {  >|<  }
     |  / \  |    [tools and chrome]
     | (   ) |
     |__| |__|
"""

PORTRAIT_MEDIC = r"""
        ___
       /+++\
      | =.= |     STREET MEDIC
      |  -  |     "Hold still. Bite this."
       \___/
       /|+|\
      / |+| \
     |  |+|  |    [med-bag]
     | =====|
     | [+++] |
     |__| |__|
"""

PORTRAIT_EXCORPO = r"""
        ___
       /\\\\\
      | --- |     EX-CORPORATE
      | === |     "I know where the bodies are."
       \___/
        |||
      _/[$]\_
     |  / \  |
     | |   | |    [tailored coat, hidden gun]
     | |   | |
     |_|   |_|
"""


PORTRAITS = {
    "street_samurai": PORTRAIT_SAMURAI,
    "netrunner": PORTRAIT_NETRUNNER,
    "fixer": PORTRAIT_FIXER,
    "tech": PORTRAIT_TECH,
    "medic": PORTRAIT_MEDIC,
    "ex_corpo": PORTRAIT_EXCORPO,
}


# ============================================================
# SCENE: Rain on the streets (used in transitions)
# ============================================================
RAIN_SCENE = r"""
   ' . ' . ' . ' . ' . ' . ' . ' . ' . ' . ' . ' . ' . '
    .  '  .  '  .  '  .  '  .  '  .  '  .  '  .  '  .
   ' . ' . ' . ' . ' . ' . ' . ' . ' . ' . ' . ' . ' . '
        |  |  |   |   |  |   |   |  |   |  |   |
       _|__|__|___|___|__|___|___|__|___|__|___|_
        ___      ___      ___      ___      ___
       |   |    |   |    |   |    |   |    |   |
       | o |____| o |____| o |____| o |____| o |
       |___|####|___|####|___|####|___|####|___|

         the city breathes static and rain
"""


# ============================================================
# DISTRICT MAPPING
# ============================================================
DISTRICT_ART = {
    "Slums": DISTRICT_SLUMS,
    "Market": DISTRICT_MARKET,
    "Corpo": DISTRICT_CORPO,
    "Net": DISTRICT_NET,
    "Industrial": DISTRICT_INDUSTRIAL,
    "Underground": DISTRICT_UNDERGROUND,
    "Transit": DISTRICT_NET,  # reuse for now
}


def get_district_art(district_name: str) -> str:
    """Return ASCII art for a district name, or empty string."""
    return DISTRICT_ART.get(district_name, "")


def get_class_portrait(class_id: str) -> str:
    """Return portrait for a character class."""
    return PORTRAITS.get(class_id, "")
