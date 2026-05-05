"""Neo-Cascadia world map.

The world is structured in districts. Each location has:
- name, description: shown to player
- exits: dict of direction -> location_id
- npcs: list of NPC names present (AI handles them)
- items: items that can be picked up (one-time)
- shops: list of NPCs who can buy/sell (AI roleplays the trade)
- danger: 0-5, affects encounter chance
- district: for grouping/map display
- enemies: list of possible enemy types here
"""

WORLD = {
    # ============== SLUMS DISTRICT ==============
    "slums": {
        "name": "The Slums - Block 9",
        "description": "Your home turf. Crumbling arcologies pierce the smog. Kids with cybereyes "
                       "scrape by selling stolen data. The neon glow paints everything sick green.",
        "exits": {"north": "neon_market", "east": "clinic", "south": "alley_network", "down": "sewers"},
        "npcs": ["Old Marta (food vendor)", "Street Kid Riku"],
        "items": ["crowbar", "ration_pack"],
        "shops": ["Old Marta"],
        "danger": 1,
        "district": "Slums",
        "enemies": ["junkie", "lowlife_thug"],
    },
    "alley_network": {
        "name": "Alley Network",
        "description": "A maze of narrow passages between slum towers. Steam vents hiss. "
                       "Something scuttles in the dark. You smell copper and rot.",
        "exits": {"north": "slums", "east": "abandoned_arcade", "west": "factory_ruins"},
        "npcs": ["Hooded Figure"],
        "items": ["rusty_pipe"],
        "shops": [],
        "danger": 3,
        "district": "Slums",
        "enemies": ["alley_ganger", "feral_dog"],
    },
    "clinic": {
        "name": "Doc Sato's Clinic",
        "description": "A back-alley ripperdoc. Sterile only by slum standards. The smell of "
                       "antiseptic fights with old blood. Patients wait on plastic chairs.",
        "exits": {"west": "slums"},
        "npcs": ["Doc Sato (ripperdoc)", "Wounded Patient"],
        "items": [],
        "shops": ["Doc Sato"],
        "danger": 0,
        "district": "Slums",
        "enemies": [],
    },
    "sewers": {
        "name": "Maintenance Tunnels",
        "description": "Knee-deep in runoff. The walls are tagged with gang glyphs. "
                       "Distant echoes suggest you are not alone down here.",
        "exits": {"up": "slums", "north": "underground_lab", "east": "sewer_chokepoint"},
        "npcs": [],
        "items": ["transit_card"],
        "shops": [],
        "danger": 4,
        "district": "Underground",
        "enemies": ["mutant_rat", "scavenger", "rogue_drone"],
    },

    # ============== MARKET / COMMERCIAL ==============
    "neon_market": {
        "name": "Neon Dragon Market",
        "description": "A labyrinth of stalls. Black-market implants, stolen data, synth-noodles. "
                       "Everyone is selling, everyone is watching. Cameras hum overhead.",
        "exits": {"north": "undercity_rail", "east": "corpo_plaza", "south": "slums", "west": "back_alley"},
        "npcs": ["Zhen the Ripperdoc", "Information Broker", "Synth Noodle Cook"],
        "items": ["stim_pack", "smokes"],
        "shops": ["Zhen", "Information Broker", "Synth Noodle Cook"],
        "danger": 2,
        "district": "Market",
        "enemies": ["pickpocket"],
    },
    "back_alley": {
        "name": "Market Back Alley",
        "description": "Behind the stalls. Dumpsters overflow with synth-flesh. "
                       "A flickering sign reads CLOSED. The door is unlocked.",
        "exits": {"east": "neon_market", "north": "fixer_office"},
        "npcs": ["Suspicious Vendor"],
        "items": ["leather_jacket"],
        "shops": ["Suspicious Vendor"],
        "danger": 2,
        "district": "Market",
        "enemies": ["mugger"],
    },
    "fixer_office": {
        "name": "Vex's Office",
        "description": "Vex runs jobs out of this rented room. Three monitors. A pet rat. "
                       "A wall of guns behind a sliding panel. She trusts no one.",
        "exits": {"south": "back_alley"},
        "npcs": ["Vex (fixer)"],
        "items": [],
        "shops": ["Vex"],
        "danger": 0,
        "district": "Market",
        "enemies": [],
    },

    # ============== TRANSIT ==============
    "undercity_rail": {
        "name": "Undercity Rail Station",
        "description": "An abandoned mag-rail hub. Gangers use it as neutral ground. "
                       "Ozone, blood, and someone's bad cologne hang in the recycled air.",
        "exits": {"south": "neon_market", "west": "factory_ruins", "east": "hacker_den", "north": "corpo_plaza"},
        "npcs": ["Rail Rat Smuggler", "Drunk Conductor"],
        "items": [],
        "shops": ["Rail Rat Smuggler"],
        "danger": 3,
        "district": "Transit",
        "enemies": ["rail_ganger", "rogue_drone"],
    },

    # ============== FACTORY / INDUSTRIAL ==============
    "factory_ruins": {
        "name": "Old Kazumi Factory",
        "description": "Skeleton of an old assembly plant. Robots still patrol on broken routines. "
                       "Useful parts buried under rubble - if you don't get crushed.",
        "exits": {"east": "undercity_rail", "south": "alley_network", "north": "robot_pit"},
        "npcs": ["Scrap Boss"],
        "items": ["rusty_pipe", "ration_pack"],
        "shops": ["Scrap Boss"],
        "danger": 4,
        "district": "Industrial",
        "enemies": ["broken_servitor", "scavenger"],
    },
    "robot_pit": {
        "name": "Decommissioning Pit",
        "description": "Where dead machines are dumped. Eyes still glow in the dark mountain "
                       "of metal. Some of them shouldn't be glowing at all.",
        "exits": {"south": "factory_ruins"},
        "npcs": [],
        "items": ["smartgun"],
        "shops": [],
        "danger": 5,
        "district": "Industrial",
        "enemies": ["rogue_drone", "broken_servitor", "war_machine"],
    },
    "abandoned_arcade": {
        "name": "Neon Arcade (closed)",
        "description": "Once a kid's paradise. Now squatters and dealers. Cabinets still flicker, "
                       "playing ghost games to no one. Music loops from a busted speaker.",
        "exits": {"west": "alley_network"},
        "npcs": ["Arcade Squatter", "Dealer"],
        "items": ["virus_chip"],
        "shops": ["Dealer"],
        "danger": 2,
        "district": "Slums",
        "enemies": ["junkie", "alley_ganger"],
    },

    # ============== HACKER / NET ==============
    "hacker_den": {
        "name": "The Null Pointer",
        "description": "Underground hacker collective. Every surface is a screen. The air buzzes "
                       "with overclocked rigs. Trust is currency. Names are weapons.",
        "exits": {"west": "undercity_rail", "down": "underground_lab"},
        "npcs": ["Ghost (netrunner)", "Cipher", "Static (sysop)"],
        "items": ["data_shard"],
        "shops": ["Cipher"],
        "danger": 1,
        "district": "Net",
        "enemies": [],
    },
    "underground_lab": {
        "name": "Secret R&D Lab",
        "description": "Hidden beneath the hacker den. Experimental cyberware on the benches. "
                       "Tanks of green fluid. Something inside one of them moves.",
        "exits": {"up": "hacker_den", "south": "sewers"},
        "npcs": ["Dr. Vance (reclusive scientist)"],
        "items": ["reflex_booster", "cyber_eye"],
        "shops": ["Dr. Vance"],
        "danger": 2,
        "district": "Net",
        "enemies": ["security_drone"],
    },
    "sewer_chokepoint": {
        "name": "Sewer Junction",
        "description": "A flooded chamber where four tunnels meet. Gang territory. Old graffiti "
                       "warns of what hunts here. The water moves wrong.",
        "exits": {"west": "sewers"},
        "npcs": [],
        "items": ["monoblade"],
        "shops": [],
        "danger": 5,
        "district": "Underground",
        "enemies": ["sewer_horror", "mutant_rat", "scavenger"],
    },

    # ============== CORPO ==============
    "corpo_plaza": {
        "name": "OmniCorp Plaza",
        "description": "Gleaming towers of glass and surveillance. Polished concrete. Suits move "
                       "with purpose. Security drones patrol endlessly. You don't belong here.",
        "exits": {"west": "neon_market", "south": "undercity_rail", "north": "executive_tower"},
        "npcs": ["OmniCorp Guard", "Street Preacher", "Corporate Suit"],
        "items": [],
        "shops": [],
        "danger": 4,
        "district": "Corpo",
        "enemies": ["corpo_security", "security_drone"],
    },
    "executive_tower": {
        "name": "OmniCorp Tower (Lobby)",
        "description": "Marble floors. Holographic receptionist. Armed guards politely watching. "
                       "The elevator requires biometric clearance. This is the lion's den.",
        "exits": {"south": "corpo_plaza"},
        "npcs": ["Executive Receptionist", "Tower Guard"],
        "items": [],
        "shops": [],
        "danger": 5,
        "district": "Corpo",
        "enemies": ["corpo_security", "elite_guard"],
    },
}

START_LOCATION = "slums"
