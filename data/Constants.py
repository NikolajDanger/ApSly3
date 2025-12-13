EPISODES = {
  "An Opera of Fear": [
    [
      "Police HQ"
    ],
    [
      "Octavio Snap",
      "Into the Depths",
      "Canal Chase"
    ],
    [
      "Turf War!",
      "Tar Ball",
      "Run 'n Bomb",
      "Guard Duty",
    ],
    [
      "Operation: Tar-Be Gone!"
    ]
  ],
  "Rumble Down Under": [
    [
      "Search for the Guru"
    ],
    [
      "Spelunking",
      "Dark Caves",
      "Big Truck",
      "Unleash the Guru"
    ],
    [
      "The Claw",
      "Lemon Rage",
      "Hungry Croc"
    ],
    [
      "Operation: Moon Crash"
    ]
  ],
  "Flight of Fancy": [
    [
      "Hidden Flight Roster"
    ],
    [
      "Frame Team Belgium",
      "Frame Team Iceland",
      "Cooper Hangar Defense",
      "ACES Semifinals"
    ],
    [
      "Giant Wolf Massacre",
      "Windmill Firewall",
      "Beauty and the Beast"
    ],
    [
      "Operation: Turbo Dominant Eagle"
    ]
  ],
  "A Cold Alliance": [
    [
      "King of Fire"
    ],
    [
      "Get a Job",
      "Tearful Reunion",
      "Grapple-Cam Break-In",
      "Laptop Retrieval"
    ],
    [
      "Vampiric Demise",
      "Down the Line",
      "A Battery of Peril"
    ],
    [
      "Operation: Wedding Crasher"
    ]
  ],
  "Dead Men Tell No Tales": [
    [
      "The Talk of Pirates"
    ],
    [
      "Dynamic Duo",
      "Jollyboat of Destruction",
      "X Marks the Spot"
    ],
    [
      "Crusher from the Depths",
      "Deep Sea Danger",
      "Battle on the High Seas"
    ],
    [
      "Operation: Reverse Double-Cross"
    ]
  ],
  "Honor Among Thieves": [
    [
      "Carmelita to the Rescue",
      "A Deadly Bite",
      "The Dark Current",
      "Bump-Charge-Jump",
      "Danger in the Skies",
      "The Ancestor's Gauntlet",
      "Stand Your Ground",
      "Final Legacy"
    ]
  ]
}

CHALLENGES = {
  "An Opera of Fear": [
    [],
    [
      "Canal Chase - Expert Course"
    ],
    [
      "Air Time",
      "Tower Scramble",
      "Coin Chase",
    ],
    [
      "Speed Bombing",
      "Octavio Canal Challenge",
      "Octavio's Last Stand",
      "Venice Treasure Hunt"
    ]
  ],
  "Rumble Down Under": [
    [
      "Rock Run"
    ],
    [
      "Cave Sprint",
      "Cave Mayhem",
      "Scaling the Drill",
      "Guard Swappin'"
    ],
    [
      "Quick Claw",
      "Pressure Brawl",
      "Croc and Coins"
    ],
    [
      "Carmelita Climb",
      "Outback Treasure Hunt"
    ]
  ],
  "Flight of Fancy": [
    [
      "Castle Quick Climb"
    ],
    [
      "Muggshot Goon Attack",
      "Security Breach",
      "Defend the Hangar",
      "Precision Air Duel"
    ],
    [
      "Wolf Rampage",
      "One Woman Army",
    ],
    [
      "Going Out On A Wing",
      "Holland Treasure Hunt"
    ]
  ],
  "A Cold Alliance": [
    [
      "Big Air in China"
    ],
    [
      "Sharpshooter",
      "Treetop Tangle",
      "Tsao Showdown"
    ],
    [],
    [
      "China Treasure Hunt"
    ]
  ],
  "Dead Men Tell No Tales": [
    [
      "Patch Grab",
      "Stealth Challenge"
    ],
    [
      "Boat Bash",
      "Last Ship Sailing"
    ],
    [],
    [
      "Pirate Treasure Hunt"
    ]
  ],
  "Honor Among Thieves": [
    [
      "Beauty versus the Beast",
      "Road Rage",
      "Dr. M Dogfight",
      "Ultimate Gauntlet",
      "Battle Against Time"
    ]
  ]
}

# Jobs/Challenges -> episode -> section -> job
#            dict[      list[      list[  list[]]]]
REQUIREMENTS = {
  "Jobs": {
    "An Opera of Fear": [
      [[]],
      [
        ["Binocucom"],
        [],
        ["Bentley"],
      ],
      [
        ["Carmelita"],
        ["Murray", "Ball Form"],
        [],
        ["Disguise (Venice)"],
      ],
      [
        ["Bombs"]
      ]
    ],
    "Rumble Down Under" :[
      [[]],
      [
        ["Murray"],
        [],
        [],
        ["Guru"],
      ],
      [
        [],
        ["Bentley"],
        []
      ],
      [[]]
    ],
    "Flight of Fancy": [
      [[]],
      [
        ["Murray", "Bentley", "Guru", "Fishing Pole"],
        ["Murray"],
        ["Penelope"],
        ["Murray", "Bentley", "Guru", "Fishing Pole", "Penelope"]
      ],
      [
        ["Binocucom"],
        ["Hover Pack"],
        ["Carmelita"]
      ],
      [
        ["Paraglider"]
      ]
    ],
    "A Cold Alliance": [
      [
        ["Bentley", "Murray", "Guru", "Penelope", "Binocucom"]
      ],
      [
        ["Disguise (Photographer)"],
        ["Panda King"],
        ["Grapple-Cam"],
        ["Disguise (Photographer)", "Panda King", "Grapple-Cam"]
      ],
      [
        [],
        [],
        ["Carmelita"]
      ],
      [[]]
    ],
    "Dead Men Tell No Tales": [
      [
        ["Disguise (Pirate)"]
      ],
      [
        ["Bentley", "Penelope", "Grapple-Cam"],
        ["Murray"],
        ["Bentley", "Penelope", "Grapple-Cam", "Murray", "Silent Obliteration", "Treasure Map"]
      ],
      [
        ["Panda King"],
        ["Dimitri"],
        []
      ],
      [
        ["Guru"]
      ]
    ],
  },
  "Challenges": {
    "An Opera of Fear": [
      [],
      [
        ["Bentley"]
      ],
      [
        ["Murray", "Ball Form"],
        [],
        []
      ],
      [
        ["Bombs"],
        [],
        [],
        ["Treasure Map"]
      ]
    ],
    "Rumble Down Under" :[
      [[]],
      [
        [],
        [],
        [],
        ["Guru"]
      ],
      [
        [],
        ["Bentley"],
        []
      ],
      [
        [],
        ["Treasure Map"]
      ]
    ],
    "Flight of Fancy": [
      [[]],
      [
        ["Penelope"],
        ["Penelope"],
        ["Penelope"],
        ["Murray", "Bentley", "Guru", "Fishing Pole", "Penelope"],
      ],
      [
        [],
        ["Carmelita"]
      ],
      [
        ["Paraglider"],
        ["Treasure Map"]
      ]
    ],
    "A Cold Alliance": [
      [
        ["Bentley", "Murray", "Guru", "Penelope", "Binocucom"]
      ],
      [
        ["Panda King"],
        [],
        [],
        []
      ],
      [],
      [
        ["Treasure Map"]
      ]
    ],
    "Dead Men Tell No Tales": [
      [
        ["Disguise (Pirate)"],
        ["Disguise (Pirate)"]
      ],
      [
        ["Murray"],
        ["Bentley", "Penelope", "Grapple-Cam", "Murray", "Silent Obliteration", "Treasure Map"]
      ],
      [],
      [[]]
    ],
  }
}

ADDRESSES = {
  "SCUS-97464" : {
    "map id": 0x47989C,
    "job id": 0x36DB98,
    "reload": 0x4797C4,
    "reload values": 0x4797CC,
    "episode unlocks": 0x56AEC8,
    "frame counter": 0x389BE0,
    "x pressed": 0x36E78E,
    "skip cutscene": 0x389C20,
    "gadgets": 0x468DCC,
    "coins": 0x468DDC,
    "DAG root": 0x478C8C,
    "jobs": [
      [
        [0x1335d10]
      ],
      [
        [0x1350560,0x1357f80,0x135aba0]
      ],
      [],
      [],
      [],
      []
    ],
    "text": {
      "powerups": [
        {
          "Trigger Bomb": (0x58db60,0x58dcf0),
          "Fishing Pole": (0x595da0,0x595fc0),
          "Alarm Clock": (0x591db0,0x591f40),
          "Adrenaline Burst": (0x58e800,0x58e9c0),
          "Health Extractor": (0x58ebe0,0x58ee00),
          "Hover Pack": (0x58ef90,0x58f1b0),
          "Insanity Strike": (0x593a40,0x593b70),
          "Grapple-Cam": (0x5957d0,0x595ae0),
          "Size Destabilizer": (0x58df70,0x58e170),
          "Rage Bomb": (0x594160,0x5942d0),
          "Reduction Bomb": (0x58f260,0x58f390),
          "Be The Ball": (0x5955c0,0x595730),
          "Berserker Charge": (0x5912d0,0x591380),
          "Juggernaut Throw": (0x590730,0x590850),
          "Guttural Roar": (0x5914e0,0x591610),
          "Fists of Flame": (0x58f960,0x5900b0),
          "Temporal Lock": (0x58f440,0x58f5a0),
          "Raging Inferno Flop": (0x5916c0,0x5917f0),
          "Diablo Fire Slam": (0x590fa0,0x591090),
          "Smoke Bomb": (0x5918f0,0x591a00),
          "Combat Dodge": (0x591b40,0x591c90),
          "Paraglide": (0x5921f0,0x5924c0),
          "Silent Obliteration": (0x592690,0x592870),
          "Feral Pounce": (0x592c50,0x592de0),
          "Mega Jump": (0x592fc0,0x593180),
          "Knockout Dive": (0x5936d0,0x5938e0),
          "Shadow Power Level 1": (0x594770,0x594880),
          "Thief Reflexes": (0x592a10,0x592b50),
          "Shadow Power Level 2": (0x5949e0,0x594d00),
          "Rocket Boots": (0x577060,0x577300),
          "Treasure Map": (0x576af0,0x576dc0),
          "ENGLISHpowerup_shield_name": (0x596280,0x576450),
          "Venice Disguise": (0x577510,0x577670),
          "Photographer Disguise": (0x5778f0,0x577ac0),
          "Pirate Disguise": (0x577ca0,0x577e20),
          "Spin Attack Level 1": (0x577fe0,0x5781b0),
          "Spin Attack Level 2": (0x578350,0x578500),
          "Spin Attack Level 3": (0x578770,0x578af0),
          "Jump Attack Level 1": (0x578d80,0x579070),
          "Jump Attack Level 2": (0x579390,0x579620),
          "Jump Attack Level 3": (0x5797b0,0x579950),
          "Push Attack Level 1": (0x579ae0,0x579d70),
          "Push Attack Level 2": (0x579f70,0x57a1f0),
          "Push Attack Level 3": (0x57a670,0x57a940),
        },
        {},
        {
          "Trigger Bomb": (0x592c40,0x592e00),
          "Fishing Pole": (0x59b000,0x59b2d0),
          "Alarm Clock": (0x5962b0,0x5964c0),
          "Adrenaline Burst": (0x593410,0x5934f0),
          "Health Extractor": (0x5935c0,0x593660),
          "Hover Pack": (0x593750,0x593840),
          "Insanity Strike": (0x598480,0x598690),
          "Grapple-Cam": (0x59acd0,0x59ae50),
          "Size Destabilizer": (0x592f30,0x593010),
          "Rage Bomb": (0x599250,0x599420),
          "Reduction Bomb": (0x5939b0,0x593b00),
          "Be The Ball": (0x59a9c0,0x59ab70),
          "Berserker Charge": (0x5955a0,0x595700),
          "Juggernaut Throw": (0x594c50,0x594dd0),
          "Guttural Roar": (0x595830,0x595920),
          "Fists of Flame": (0x5944a0,0x594610),
          "Temporal Lock": (0x593c40,0x593e60),
          "Raging Inferno Flop": (0x595a50,0x595bd0),
          "Diablo Fire Slam": (0x595260,0x595450),
          "Smoke Bomb": (0x595d60,0x595ee0),
          "Combat Dodge": (0x596050,0x596190),
          "Paraglide": (0x5966d0,0x5968d0),
          "Silent Obliteration": (0x596ba0,0x596df0),
          "Feral Pounce": (0x597290,0x5973f0),
          "Mega Jump": (0x5975f0,0x597780),
          "Knockout Dive": (0x597e10,0x598130),
          "Shadow Power Level 1": (0x599c30,0x599eb0),
          "Thief Reflexes": (0x596f70,0x597110),
          "Shadow Power Level 2": (0x59a140,0x59a310),
          "Rocket Boots": (0x57aa00,0x57ace0),
          "Treasure Map": (0x57a3e0,0x57a780),
          "ENGLISHpowerup_shield_name": (0x59b550,0x579c50),
          "Venice Disguise": (0x57ae40,0x57b040),
          "Photographer Disguise": (0x57b220,0x57b3b0),
          "Pirate Disguise": (0x57b5d0,0x57b7b0),
          "Spin Attack Level 1": (0x57b9e0,0x57bc40),
          "Spin Attack Level 2": (0x57be80,0x57c130),
          "Spin Attack Level 3": (0x57c300,0x57c5b0),
          "Jump Attack Level 1": (0x57c7c0,0x57c970),
          "Jump Attack Level 2": (0x57cb00,0x57cc30),
          "Jump Attack Level 3": (0x57cdf0,0x57d010),
          "Push Attack Level 1": (0x57d370,0x57d680),
          "Push Attack Level 2": (0x57d940,0x57dc80),
          "Push Attack Level 3": (0x57e070,0x57e3b0),
        },
        {},
        {},
        {}
      ]
    }
  }
}

MENU_RETURN_DATA = (
  "794C15EE"+
  "419A69B1"+
  "FA2319BC"+
  "FF2E5E8A"+
  "ACD1E787"+
  "3A2B7DB0"+
  "B94681B3"+
  "95777951"+
  "CE8FEAA9"+
  "07FB6D94"+
  "F890094F"+
  "3BFA55F6"+
  "A0310D22"+
  "F93E1EEE"+
  "7F2319BC"+
  "7B8274B1"
)