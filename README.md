# Neon Cascadia v2087

A cyberpunk text-based RPG with full character creation, leveling, and AI-driven storytelling. Runs on Termux (Android), connects to your Ollama server over Tailscale.

## Features

- **6 character classes** - Street Samurai, Netrunner, Fixer, Tech, Street Medic, Ex-Corporate
- **13 skills** - Combat, hacking, first aid, stealth, persuasion, intimidation, streetwise, barter, tech repair, engineering, biology, corporate lore, perception
- **Leveling system** - XP from kills, exploration, quests, and skill checks. Level up grants stat & skill points
- **Skill checks** - d20 + skill + stat modifiers vs DC. Results feed back to AI for narration
- **Open world** - 16 locations across 6 districts
- **AI-driven NPCs** - Local LLM handles all dialogue and dynamic events
- **Combat system** - Turn-based, with crits, fleeing, equipment stats
- **Inventory & equipment** - 22 items: weapons, armor, consumables, cyberware
- **Cyberware** - Permanent stat bonuses when installed
- **Faction reputation** - 5 factions react to your standing
- **Save/load** - Full state persistence

## Quick Setup on Termux

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/YOUR_USER/neon-cascadia-rpg.git
cd neon-cascadia-rpg
pip install -r requirements.txt
nano game/config.py    # set OLLAMA_HOST to your Tailscale IP
python main.py
```

## Setup on your Ollama server

```bash
OLLAMA_HOST=0.0.0.0 ollama serve
ollama pull llama3      # or mistral, qwen2.5, phi3
```

## Character Classes

| Class | Style | Strong In | Starting Gear |
|---|---|---|---|
| **Street Samurai** | Combat focused | Combat, intimidation | Monoblade + leather jacket |
| **Netrunner** | Hacker | Hacking, stealth | Pistol + neural jack |
| **Fixer** | Social manipulator | Persuasion, barter, streetwise | Pistol + credits |
| **Tech** | Builder/repair | Tech repair, engineering | Stun baton + cyber eye |
| **Street Medic** | Healer | First aid, biology | Pistol + trauma kits |
| **Ex-Corporate** | Insider | Corp lore, persuasion | Smartgun + kevlar |

## Leveling

- Earn XP from: kills (25-200), discovering locations (15), completing quests (100-500), passing skill checks (5)
- Each level gives **3 skill points** and **+10 max HP** (with full heal)
- Every other level gives **1 stat point**
- XP curve: Lv2=100, Lv3=250, Lv4=450, Lv5=700, etc.
- Spend points with `levelup` command

## Skill System

When you take an action like "hack the door" or "convince the guard," the engine detects it's a skill check and rolls behind the scenes:

```
roll = d20 + skill_level + (stat_bonus)
```

Result tier is included in the AI prompt:

- **Critical Success** (nat 20) - Action goes spectacularly well
- **Success** (margin +5) - Works as intended
- **Partial Success** (margin 0-4) - Works with complications
- **Failure** (negative margin) - Doesn't work
- **Critical Failure** (nat 1) - Fails badly with consequence

The AI then narrates the outcome accordingly. So a Netrunner with hacking 8 will glide through ICE that destroys an untrained Street Samurai.

## Commands

| Command | Effect |
|---|---|
| `go <dir>` | Move (north/south/east/west/up/down) |
| `look` | Re-examine surroundings |
| `take <item>` | Pick up an item |
| `inv` | Inventory |
| `stats` | Full character sheet |
| `skills` | Show all skills |
| `levelup` | Spend stat/skill points |
| `equip <item>` | Equip weapon/armor |
| `use <item>` | Consumable / install cyberware |
| `quests` | Active quests |
| `save` / `load` | Persistence |
| `help` | Command list |
| `quit` | Exit (offers save) |
| anything else | Sent to AI - talk, hack, persuade, search... |

### Combat

| Command | Effect |
|---|---|
| `attack` | Strike with equipped weapon |
| `use <item>` | Heal mid-combat |
| `flee` | Try to escape (agility-based) |
| `inv` | Check inventory |

## How AI integration works

The game sends Ollama a structured prompt with **everything** about the player: class, level, stats, skills, inventory, faction standings, current location, NPCs present, and the action. The AI responds with narrative plus bracketed tags the engine parses:

```
The fixer studies you. "I heard about your work in the slums. 
Got a job. 500 creds, no questions." [QUEST_OFFER: Data Heist | 
Steal a shard from OmniCorp courier]
[ACTION_OPTIONS: accept | refuse | negotiate price]
```

Tags supported:
- `[COMBAT_START: enemy_id]` - triggers combat
- `[ITEM_GAIN: item_name]` - adds to inventory
- `[ITEM_LOSE: item_name]` - removes from inventory
- `[CREDITS: +50]` / `[CREDITS: -20]` - changes money
- `[QUEST_OFFER: title | description]` - adds quest
- `[ACTION_OPTIONS: opt1 | opt2 | opt3]` - suggested next moves

Skill check results are also injected into the prompt so the AI knows whether your hacking attempt succeeded or failed and narrates accordingly.

## Project structure

```
neon-cascadia-rpg/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── game/
│   ├── __init__.py
│   ├── config.py          # Ollama, prompts, balance
│   ├── engine.py          # Main loop & dispatch
│   ├── character.py       # Classes, skills, XP curves
│   ├── skills.py          # Skill check resolution
│   ├── ai_engine.py       # Ollama client + tag parser
│   ├── player.py          # Player state w/ class/level/skills
│   ├── combat.py          # Combat system
│   ├── world.py           # Locations
│   ├── enemies.py         # Enemy stats
│   ├── items.py           # Item DB
│   └── ui.py              # Rich rendering & screens
└── saves/                 # JSON saves (gitignored)
```

## Extending

- **Add classes** - edit `CLASSES` in `game/character.py`
- **Add skills** - edit `SKILL_DEFINITIONS` and add detection keywords in `game/skills.py`
- **Add locations** - `WORLD` in `game/world.py`
- **Add items** - `ITEMS` in `game/items.py`
- **Add enemies** - `ENEMIES` in `game/enemies.py`
- **Tune XP** - `XP_REWARDS` in `game/character.py`
- **Tune AI tone** - `GAME_SYSTEM_PROMPT` in `game/config.py`

## Troubleshooting

| Problem | Fix |
|---|---|
| `Cannot reach Ollama` | Verify `tailscale status` & `OLLAMA_HOST=0.0.0.0` |
| Ollama timeout | Smaller model or raise `OLLAMA_TIMEOUT` |
| Want to start over | Delete `saves/autosave.json` |
| New skill not recognized | Add keywords to `detect_skill_check` in `skills.py` |
