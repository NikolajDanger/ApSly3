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
        ["Bombs"],
        ["Bentley"],
      ],
      [
        ["Carmelita"],
        ["Murray", "Ball Form"],
        [],
        ["Disguise (Venice)"],
      ],
      [
        []
      ]
    ],
    "Rumble Down Under" :[
      [[]],
      [
        ["Murray", "Ball Form"],
        [],
        ["Murray", "Ball Form"],
        ["Bentley", "Murray", "Ball Form", "Guru"],
      ],
      [
        [],
        ["Bombs"],
        []
      ],
      [
        ["Binocucom"]
      ]
    ],
    "Flight of Fancy": [
      [
        ["Bentley"]
      ],
      [
        ["Murray", "Guru", "Fishing Pole"],
        ["Murray", "Ball Form"],
        ["Murray","Penelope"],
        ["Murray", "Guru", "Fishing Pole", "Penelope"]
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
        ["Bentley", "Murray", "Guru", "Penelope", "Binocucom", "Ball Form"]
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
        ["Bentley", "Penelope", "Grapple-Cam", "Bombs"],
        ["Murray"],
        ["Bentley", "Penelope", "Grapple-Cam", "Bombs", "Murray", "Silent Obliteration", "Treasure Map"]
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
    "Honor Among Thieves": [
      [
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita", "Paraglider"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita", "Paraglider"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita", "Paraglider"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita", "Paraglider"],
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
        [],
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
        ["Murray", "Ball Form"],
        ["Murray", "Ball Form", "Guru"]
      ],
      [
        [],
        ["Bentley"],
        []
      ],
      [
        ["Binocucom"],
        ["Treasure Map"]
      ]
    ],
    "Flight of Fancy": [
      [
        ["Bentley"]
      ],
      [
        ["Murray", "Penelope"],
        ["Murray", "Penelope"],
        ["Murray", "Penelope"],
        ["Murray", "Guru", "Fishing Pole", "Penelope"],
      ],
      [
        [],
        ["Carmelita"]
      ],
      [
        ["Paraglider"],
        ["Paraglider", "Treasure Map"]
      ]
    ],
    "A Cold Alliance": [
      [
        ["Bentley", "Murray", "Ball Form", "Guru", "Penelope", "Binocucom"]
      ],
      [
        ["Panda King"],
        ["Disguise (Photographer)", "Panda King", "Grapple-Cam"],
        ["Disguise (Photographer)", "Panda King", "Grapple-Cam"]
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
      [
        ["Guru"]
      ]
    ],
    "Honor Among Thieves": [
      [
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita", "Paraglider"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita", "Paraglider"],
        ["Bentley", "Murray", "Guru", "Penelope", "Panda King", "Dimitri", "Carmelita", "Paraglider"],
      ]
    ],
  }
}

JOB_IDS = {
  "An Opera of Fear": [
    [2085],
    [2230,2283,2329],
    [2139,2168,2187,2352],
    [2419]
  ],
  "Rumble Down Under": [
    [2577],
    [2596,2805,2695,2663],
    [2623,2730,2780],
    [2843]
  ],
  "Flight of Fancy": [
    [2983],
    [3025,3061,3101,3140],
    [3202,3164,3225],
    [3259]
  ],
  "A Cold Alliance": [
    [3381],
    [3449,3509,3540,3584],
    [3629,3672,3684],
    [3712]
  ],
  "Dead Men Tell No Tales": [
    [3848],
    [3907,4038,3991],
    [4071,4101,4120],
    [4145]
  ],
  "Honor Among Thieves": [
    [4327,4369,4396,4412,4436,4479,4505,4544]
  ]
}

ADDRESSES = {
  "SCUS-97464" : {
    "bentley": 0x36B250,
    "items received": 0x46E250,
    "world id": 0x468D30,
    "map id": 0x47989C,
    "job id": 0x36DB98,
    "loading": 0x467B00,
    "reload": 0x4797C4,
    "reload values": 0x4797CC,
    "episode unlocks": 0x56AEC8,
    "frame counter": 0x389BE0,
    "x pressed": 0x36E78E,
    "skip cutscene": 0x389C20,
    "gadgets": 0x468DCC,
    "coins": 0x468DDC,
    "DAG root": 0x478C8C,
    "intro complete": 0x46E260,
    "grapple-cam weapon": 0x468DD8,
    "job completed": {
      "An Opera of Fear": [
        [
          0x468FEC,
        ],
        [
          0x468FAC,
          0x468FBC,
          0x468F7C,
        ],
        [
          0x46900C,
          0x468F6C,
          0x468FFC,
          0x468F9C,
        ],
        [
          0x468FCC,
        ],
      ],
      "Rumble Down Under": [
        [
          0x46909C,
        ],
        [
          0x46902C,
          0x46903C,
          0x46905C,
          0x4690AC,
        ],
        [
          0x46904C,
          0x46901C,
          0x46906C,
        ],
        [
          0x46907C,
        ],
      ],
      "Flight of Fancy": [
        [
          0x46916C,
        ],
        [
          0x4690EC,
          0x4690DC,
          0x46910C,
          0x46917C,
        ],
        [
          0x46919C,
          0x46918C,
          0x46914C,
        ],
        [
          0x46911C,
        ],
      ],
      "A Cold Alliance": [
        [
          0x46920C,
        ],
        [
          0x4691BC,
          0x46922C,
          0x46923C,
          0x46921C,
        ],
        [
          0x46925C,
          0x4691FC,
          0x4691AC,
        ],
        [
          0x4691CC,
        ],
      ],
      "Dead Men Tell No Tales": [
        [
          0x4692FC,
        ],
        [
          0x4692CC,
          0x4692BC,
          0x46931C,
        ],
        [
          0x46930C,
          0x46929C,
          0x46926C,
        ],
        [
          0x4692AC,
        ],
      ],
      "Honor Among Thieves": [
        [
          0x46936C,
          0x46938C,
          0x46935C,
          0x46934C,
          0x46932C,
          0x46937C,
          0x46939C,
          0x46933C,
        ]
      ],
    },
    "challenge completed": {
      "An Opera of Fear": [
        [],
        [
          0x46DF30
        ],
        [
          0x46DF20,
          0x46DF98,
          0x46DF90,
        ],
        [
          0x46DF60,
          0x46DF70,
          0x46DF68,
          0x46DF78
        ]
      ],
      "Rumble Down Under": [
        [
          0x46E028
        ],
        [
          0x46DFC8,
          0x46DFD0,
          0x46DFF0,
          0x46E038
        ],
        [
          0x46DFE0,
          0x46DFB0,
          0x46E000
        ],
        [
          0x46E010,
          0x46E018
        ]
      ],
      "Flight of Fancy": [
        [
          0x46E0B0
        ],
        [
          0x46E068,
          0x46E078,
          0x46E070,
          0x46E0C0
        ],
        [
          0x46E0D8,
          0x46E0A0,
        ],
        [
          0x46E088,
          0x46E090
        ]
      ],
      "A Cold Alliance": [
        [
          0x46E100
        ],
        [
          0x46E138,
          0x46E128,
          0x46E120
        ],
        [],
        [
          0x46E0F8
        ]
      ],
      "Dead Men Tell No Tales": [
        [
          0x46E1B0,
          0x46E1B8
        ],
        [
          0x46E190,
          0x46E160
        ],
        [],
        [
          0x46E1A0
        ]
      ],
      "Honor Among Thieves": [
        [
          0x46E210,
          0x46E1F8,
          0x46E1D8,
          0x46E220,
          0x46E1E8
        ]
      ]
    },
    "job markers": {
      2085: 0x1335d10,
      2230: 0x1350560,
      2283: 0x1357f80,
      2329: 0x135aba0,
      2139: 0x1330c40,
      2168: 0x1335dc0,
      2187: 0x133e9b0,
      2352: 0x1351520,
      2419: 0x135e550,

      2577: 0x6b4250,
      2596: 0x6b80f0,
      2805: 0x6d0770,
      2695: 0x6c3eb0,
      2663: 0x6bdaf0,
      2623: 0x6bb070,
      2730: 0x6c5fb0,
      2780: 0x6ca1c0,
      2843: 0x6d4330,

      2983: 0x794360,
      3025: 0x627a60,
      3061: 0x62c7b0,
      3101: 0x630220,
      3140: 0xecb450,
      3202: 0x642a90,
      3164: 0x63b4d0,
      3225: 0x7adf50,
      3259: 0x651eb0,

      3381: 0x1614110,
      3449: 0x1618740,
      3509: 0x16200f0,
      3540: 0x1625780,
      3584: 0x162b770,
      3629: 0x1630060,
      3672: 0x16377e0,
      3684: 0x163a930,
      3712: 0x1641a30,

      3848: 0x7672e0,
      3907: 0x7743d0,
      4038: 0x78d440,
      3991: 0x788780,
      4071: 0x602a30,
      4101: 0x60e0c0,
      4120: 0x60fa80,
      4145: 0x6126c0,
    },
    "job states": {
      2085: 0x46A688,
      2230: 0x46A0E8,
      2283: 0x46A2B4,
      2329: 0x469E54,
      2139: 0x46A8E0,
      2168: 0x469DF0,
      2187: 0x46A7B4,
      2352: 0x46A098,
      2419: 0x46A50C,

      2577: 0x46B150,
      2596: 0x46AA5C,
      2805: 0x46AB88,
      2695: 0x46AD54,
      2663: 0x46B204,
      2623: 0x46ABEC,
      2730: 0x46A980,
      2780: 0x46AE58,
      2843: 0x46AFC0,

      2983: 0x46BB3C,
      3025: 0x46B5B0,
      3061: 0x46B3D0,
      3101: 0x46B718,
      3140: 0x46BC04,
      3202: 0x46BE34,
      3164: 0x46BDBC,
      3225: 0x46BA74,
      3259: 0x46B920,

      3381: 0x46C5B4,
      3449: 0x46BF60,
      3509: 0x46C938,
      3540: 0x46CA00,
      3584: 0x46C80C,
      3629: 0x46CB7C,
      3672: 0x46C4EC,
      3684: 0x46BEC0,
      3712: 0x46C370,

      3848: 0x46D590,
      3907: 0x46D158,
      4038: 0x46D0CC,
      3991: 0x46D770,
      4071: 0x46D694,
      4101: 0x46CE38,
      4120: 0x46CCD0,
      4145: 0x46CEC4,
    },
    "active character pointer": 0x36F84C,
    "infobox scrolling": 0x46F780,
    "infobox string": 0x46F788,
    "infobox duration": 0x46F78C,
    "infobox": 0x46F798,
    # "infobox": 0x47671C,
    # "infobox": 0x479758,
    "thiefnet start": 0x343208,
    "string table": 0x47A2D8,
    "text": {
      "Press START (start)": 0x5639b0,
      "Press START (resume)": 0x563bd0,
      "Press SELECT": 0x564380,
      "An Opera of Fear": 0x53b380,
      "Rumble Down Under": 0x53b4e0,
      "Flight of Fancy": 0x53b5a0,
      "A Cold Alliance": 0x53b710,
      "Dead Men Tell No Tales": 0x53b7b0,
      "Honor Among Thieves": 0x53b900,
      "infobox": {
        3: 0x5765d0,
        8: 0x564170,
        15: 0x579ec0,
        23: 0x56fa80,
        31: 0x57a860,
        32: 0x57a470,
        35: 0x561a40,
      },
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

# TODO: Death Messages
DEATH_TYPES = {}

POWER_UP_TEXT = [
  ("Trigger Bomb","Throwable bomb with remote detonation"),
  ("Fishing Pole","Fish loot out of guards' pockets"),
  ("Alarm Clock","Confuse your enemies with this distracting alarm clock"),
  ("Adrenaline Burst","Move like no turtle has moved before"),
  ("Health Extractor","Capture guards and extract medicine from them"),
  ("Hover Pack","Extend your jumps by hovering in the air"),
  ("Insanity Strike","Make enemies attack each other with the wheelchair spin attack"),
  ("Grapple-Cam","A remote camera with amazing abilities"),
  ("Size Destabilizer","Shrink guards by whacking them with your wheelchair"),
  ("Rage Bomb","Confuse all enemies in the area into attacking each other"),
  ("Reduction Bomb","Shrink enemies in the area"),
  ("Be The Ball","Roll around like a ball"),
  ("Berserker Charge","Scatter enemies with this powerful run"),
  ("Juggernaut Throw","Thrown enemies explode on impact"),
  ("Guttural Roar","Terrify your foes"),
  ("Fists of Flame","Turn ordinary punches into fiery ones"),
  ("Temporal Lock","Freeze time around the guards…temporarily, at least"),
  ("Raging Inferno Flop","Use while jumping to create a wall of flame on impact"),
  ("Diablo Fire Slam","Use while carrying an enemy to create a deadly firestorm"),
  ("Smoke Bomb","Obscure the vision of your enemies for a hasty getaway"),
  ("Combat Dodge","Sidestep enemies in combat"),
  ("Paraglide","Fly through the air with this quick-deploy paraglider"),
  ("Silent Obliteration","Juggle an unaware enemy with &2T&."),
  ("Feral Pounce","Jump over vast distances"),
  ("Mega Jump","Jump to impressive heights"),
  ("Knockout Dive","Leap at enemies, leaving them stunned on the ground"),
  ("Shadow Power Level 1","Move without being seen"),
  ("Thief Reflexes","Slow time to a crawl"),
  ("Shadow Power Level 2","Attack foes while invisible"),
  ("Rocket Boots","Zoom through the world with these speedy boots"),
  ("Treasure Map","Follow the trail to find buried treasure"),
  ("ENGLISHpowerup_shield_name","ENGLISHpowerup_shield_desc"),
  ("Venice Disguise","Fool guards in Venice with this disguise"),
  ("Photographer Disguise","Fool guards in China with this disguise"),
  ("Pirate Disguise","Fool Guards in Blood Bath Bay with this disguise"),
  ("Spin Attack Level 1","Press &2T&. and &2S&. to do a spin attack"),
  ("Spin Attack Level 2","Press &2T&., &2T&. and &2S&. to do a powerful spin attack"),
  ("Spin Attack Level 3","Press &2T&., &2T&., &2T&. and &2S&. to do a devastating spin attack"),
  ("Jump Attack Level 1","Press &2T&. and &2X&. to do a jump attack"),
  ("Jump Attack Level 2","Press &2T&., &2T&. and &2X&. to do a powerful jump attack"),
  ("Jump Attack Level 3","Press &2T&., &2T&., &2T&. and &2X&. to do a devastating jump attack"),
  ("Push Attack Level 1","Press &2T&. then &2O&. to do a push attack"),
  ("Push Attack Level 2","Press &2T&., &2T&. and &2O&. to do a powerful push attack"),
  ("Push Attack Level 3","Press &2T&., &2T&., &2T&. and &2O&. to do a devastating push attack"),
]
