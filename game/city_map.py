"""City map system - shows the player's location and connections."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from game.world import WORLD

console = Console()


# ============================================================
# ASCII CITY MAP
# ============================================================
# Shows the layout of the entire city as connected districts.
# {YOU} marker is replaced with the player's location.

CITY_MAP_TEMPLATE = r"""
                    ====[ NEO-CASCADIA  2087 ]====


   +----------------+        +-----------------+
   |  EXEC TOWER    |        |   OMNICORP      |
   |  {executive_tower}      |---|   PLAZA         |
   +----------------+        |   {corpo_plaza}            |
                              +--------+--------+
                                       |
                                       |
                              +--------+--------+
                              |  UNDERCITY      |
                +-------------|  RAIL STATION   |---------+
                |             |  {undercity_rail}             |         |
                |             +-----+------+----+         |
                |                   |      |              |
        +-------+-------+           |      |       +------+--------+
        |  FACTORY      |           |      |       |  HACKER DEN   |
        |  RUINS        |           |      |       |  {hacker_den}    |
        |  {factory_ruins}        |           |      |       +-------+-------+
        +---+---------+-+           |      |               |
            |         |             |      |               |
   +--------+----+    |             |      |       +-------+-------+
   |  ROBOT PIT  |    |             |      |       |  UNDERGROUND  |
   |  {robot_pit}    |    |             |      |       |  LAB  {underground_lab}    |
   +-------------+    |             |      |       +-------+-------+
                      |             |      |               |
              +-------+-----+       |      |               |
              |  ALLEYS     |       |      |       +-------+-------+
              |  {alley_network}     |---+   |       |    SEWERS     |
              +-+---------+-+       |   |   |       |    {sewers}      |
                |         |         |   |   |       +---+-----------+
        +-------+----+    |         |   |   |           |
        |  ARCADE    |    |         |   |   |   +-------+-------+
        |  {abandoned_arcade}    |    |         |   |   |   |  CHOKEPOINT   |
        +------------+    |         |   |   |   |   {sewer_chokepoint}  |
                          |         |   |   |   +---------------+
                  +-------+---+     |   |   |
                  |  NEON     |     |   |   |
                  |  MARKET   |-----+   |   |
                  |  {neon_market}|         |   |
                  +-+--------++         |   |
                    |        |          |   |
            +-------+--+   +-+--------+ |   |
            |  BACK    |   |  CLINIC  | |   |
            |  ALLEY   |   |  {clinic}    | |   |
            |  {back_alley}|   +----------+ |   |
            +-----+----+                  |   |
                  |                       |   |
          +-------+------+        +-------+---+
          |  FIXER OFFICE|        |   SLUMS   |
          |  {fixer_office}      |        |   {slums}    |---+
          +--------------+        +-----------+


   LEGEND:  [Y] = your location    {___} = district codes
"""


def render_city_map(player) -> str:
    """Build the ASCII map with the player's location marked."""
    # Build a marker for each location
    markers = {}
    for loc_id in WORLD:
        if loc_id == player.location:
            marker = "[Y]"
        elif loc_id in player.visited:
            marker = " * "
        else:
            marker = " ? "
        markers[loc_id] = marker

    # Substitute markers into the template
    text = CITY_MAP_TEMPLATE
    for loc_id, marker in markers.items():
        # Pad marker to 3 chars
        padded = marker.ljust(3)
        text = text.replace("{" + loc_id + "}", padded)

    return text


def print_map(player):
    """Print the city map with player location."""
    art = render_city_map(player)
    console.print(Panel(art, title="[bold cyan]NEO-CASCADIA STREET MAP[/bold cyan]",
                        border_style="cyan", box=box.DOUBLE, padding=(0, 1)))

    # Legend
    console.print("\n[bold]LEGEND:[/bold]")
    console.print("  [bold yellow][Y][/bold yellow] You are here")
    console.print("  [green] * [/green] Visited")
    console.print("  [dim] ? [/dim] Unknown / unexplored")

    # Current district info
    location = WORLD[player.location]
    console.print("\n[bold magenta]Current Location:[/bold magenta] " + location["name"])
    console.print("[bold magenta]District:[/bold magenta] " + location.get("district", "?"))

    # Show exits with destination names
    console.print("\n[bold cyan]Exits from here:[/bold cyan]")
    for direction, dest in location.get("exits", {}).items():
        dest_loc = WORLD.get(dest, {})
        dest_name = dest_loc.get("name", dest)
        visited = " [green](visited)[/green]" if dest in player.visited else " [dim](unknown)[/dim]"
        console.print("  [yellow]" + direction + "[/yellow] -> " + dest_name + visited)


def print_district_summary(player):
    """Show a table of districts and how many locations the player has explored in each."""
    # Group locations by district
    districts = {}
    for loc_id, loc in WORLD.items():
        d = loc.get("district", "Unknown")
        districts.setdefault(d, []).append(loc_id)

    table = Table(title="DISTRICTS DISCOVERED", box=box.SIMPLE_HEAVY, border_style="magenta")
    table.add_column("District", style="magenta")
    table.add_column("Explored", style="green", justify="right")
    table.add_column("Total", style="cyan", justify="right")
    table.add_column("Locations", style="white")

    for district, locs in sorted(districts.items()):
        visited_count = sum(1 for l in locs if l in player.visited)
        loc_names = ", ".join(
            WORLD[l]["name"] if l in player.visited else "[dim]???[/dim]"
            for l in locs
        )
        table.add_row(district, str(visited_count), str(len(locs)), loc_names)

    console.print(table)
