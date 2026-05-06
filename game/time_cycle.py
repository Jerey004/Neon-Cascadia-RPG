"""Day/night cycle system.

Tracks an in-game turn counter. Every N player actions = 1 hour of game time.

Day cycle: 24 hours
  0600-1800: Day   (normal encounter rates, all NPCs available)
  1800-2200: Dusk  (+5% encounters, some NPCs go off-duty)
  2200-0400: Night (+10% encounters, nocturnal NPCs available)
  0400-0600: Dawn  (+5% encounters, quiet before the storm)

Actions per hour: 4 (so 96 actions = full day)
"""

ACTIONS_PER_HOUR = 4
HOURS_PER_DAY = 24

# Time periods
PERIODS = [
    (6,  18, "Day",   "cyan",       "Overcast daylight. Chrome and neon."),
    (18, 22, "Dusk",  "yellow",     "The city shifts gears. More predators out."),
    (22,  4, "Night", "dim magenta","Neon burns bright. Danger doubles."),
    (4,   6, "Dawn",  "dim cyan",   "The quiet hour. Before the city wakes."),
]

# NPCs that only appear at certain times
NPC_SCHEDULES = {
    "Ghost (netrunner)":    {"night_only": True},
    "Vex (fixer)":          {"night_only": True},
    "Hooded Figure":        {"night_only": True},
    "Old Marta (food vendor)": {"day_only": True},
    "Synth Noodle Cook":    {"day_only": True},
    "Street Kid Riku":      {"day_only": True},
}


class DayCycle:
    """Tracks time and manages day/night state."""

    def __init__(self):
        self.total_turns = 0
        self.start_hour = 8   # Game starts at 0800

    def advance(self, turns: int = 1):
        self.total_turns += turns

    @property
    def hour(self) -> int:
        hours_passed = self.total_turns // ACTIONS_PER_HOUR
        return (self.start_hour + hours_passed) % HOURS_PER_DAY

    @property
    def day(self) -> int:
        return self.total_turns // (ACTIONS_PER_HOUR * HOURS_PER_DAY) + 1

    @property
    def is_night(self) -> bool:
        h = self.hour
        return h >= 22 or h < 6

    @property
    def is_day(self) -> bool:
        return 6 <= self.hour < 18

    @property
    def period_name(self) -> str:
        h = self.hour
        for start, end, name, color, desc in PERIODS:
            if start < end:
                if start <= h < end:
                    return name
            else:
                if h >= start or h < end:
                    return name
        return "Day"

    @property
    def period_color(self) -> str:
        h = self.hour
        for start, end, name, color, desc in PERIODS:
            if start < end:
                if start <= h < end:
                    return color
            else:
                if h >= start or h < end:
                    return color
        return "white"

    @property
    def period_desc(self) -> str:
        h = self.hour
        for start, end, name, color, desc in PERIODS:
            if start < end:
                if start <= h < end:
                    return desc
            else:
                if h >= start or h < end:
                    return desc
        return ""

    def time_string(self) -> str:
        h = self.hour
        return str(h).zfill(2) + "00  Day " + str(self.day) + "  [" + self.period_name + "]"

    def npc_available(self, npc_name: str) -> bool:
        """Check if NPC is on-duty at current time."""
        sched = NPC_SCHEDULES.get(npc_name, {})
        if sched.get("night_only") and self.is_day:
            return False
        if sched.get("day_only") and self.is_night:
            return False
        return True

    def to_dict(self) -> dict:
        return {"total_turns": self.total_turns, "start_hour": self.start_hour}

    @classmethod
    def from_dict(cls, data: dict) -> "DayCycle":
        dc = cls()
        dc.total_turns = data.get("total_turns", 0)
        dc.start_hour = data.get("start_hour", 8)
        return dc
