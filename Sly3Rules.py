import typing
from math import ceil

from BaseClasses import CollectionState

from worlds.generic.Rules import add_rule
from .data.Constants import EPISODES

if typing.TYPE_CHECKING:
    from . import Sly3World

def set_rules_sly3(world: "Sly3World"):
  player = world.player

  # Putting ThiefNet stuff out of logic, to make early game less slow.
  # Divides the items into 8 groups of 3. First groups requires 2 episodes
  # items to be in logic, second group requires 4, etc.
  for i in range(1,38):
    episode_items_n = ceil(i/4)*2
    add_rule(
      world.get_location(f"ThiefNet {i:02}"),
      lambda state, n=episode_items_n: (
        state.has_group("Episode", player, n)
      )
    )

  def require(location: str, item: str|list[str]):
    if isinstance(item,str):
      add_rule(
        world.get_location(location),
        lambda state, i=item: (
          state.has(i, player)
        )
      )
    else:
      add_rule(
        world.get_location(location),
        lambda state, i=item: (
          all(state.has(j, player) for j in i)
        )
      )

  ### Job requirements
  ## An Opera of fear
  # An Opera of Fear - Police HQ

  require("An Opera of Fear - Octavio Snap", "Binocucom")
  # An Opera of Fear - Into the Depths
  require("An Opera of Fear - Canal Chase", "Bentley")

  require("An Opera of Fear - Turf War!", "Carmelita")
  require("An Opera of Fear - Tar Ball", ["Murray", "Ball Form"])
  # An Opera of Fear - Run 'n Bomb
  require("An Opera of Fear - Guard Duty", "Disguise (Venice)")

  require("An Opera of Fear - Operation: Tar-Be Gone!", "Bombs")

  ## Rumble Down Under
  # Rumble Down Under - Search for the Guru

  require("Rumble Down Under - Spelunking", "Murray")
  # Rumble Down Under - Dark Caves
  # Rumble Down Under - Big Truck
  require("Rumble Down Under - Unleash the Guru", "Guru")

  # Rumble Down Under - The Claw
  require("Rumble Down Under - Lemon Rage", "Bentley")
  # Rumble Down Under - Hungry Croc

  # Rumble Down Under - Operation: Moon Crash

  ## Flight of Fancy
  # Flight of Fancy - Hidden Flight Roster

  require("Flight of Fancy - Frame Team Belgium", ["Murray", "Bentley", "Guru", "Fishing Pole"])
  require("Flight of Fancy - Frame Team Iceland", "Murray")
  require("Flight of Fancy - Cooper Hangar Defense", "Penelope")
  require("Flight of Fancy - ACES Semifinals", ["Murray", "Bentley", "Guru", "Fishing Pole", "Penelope"])

  require("Flight of Fancy - Giant Wolf Massacre", "Binocucom")
  require("Flight of Fancy - Windmill Firewall", "Hover Pack")
  require("Flight of Fancy - Beauty and the Beast", "Carmelita")

  require("Flight of Fancy - Operation: Turbo Dominant Eagle", "Paraglider")

  ## A Cold Alliance
  require("A Cold Alliance - King of Fire", ["Bentley", "Murray", "Guru", "Penelope", "Binocucom"])

  require("A Cold Alliance - Get a Job", "Disguise (Photographer)")
  require("A Cold Alliance - Tearful Reunion", "Panda King")
  require("A Cold Alliance - Grapple-Cam Break-In", "Grapple-Cam")
  require("A Cold Alliance - Laptop Retrieval", ["Disguise (Photographer)", "Panda King", "Grapple-Cam"])

  # A Cold Alliance - Vampiric Defense
  # A Cold Alliance - Down the Line
  require("A Cold Alliance - A Battery of Peril", "Carmelita")

  # A Cold Alliance - Operation: Wedding Crasher

  ## Dead Men Tell No Tales
  require("Dead Men Tell No Tales - The Talk of Pirates", "Disguise (Pirate)")

  require("Dead Men Tell No Tales - Dynamic Duo", ["Bentley", "Penelope", "Grapple-Cam"])
  require("Dead Men Tell No Tales - Jollyboat of Destruction", "Murray")
  require("Dead Men Tell No Tales - X Marks the Spot", ["Bentley", "Penelope", "Grapple-Cam", "Murray", "Silent Obliteration", "Treasure Map"])

  require("Dead Men Tell No Tales - Crusher from the Depths", "Panda King")
  require("Dead Men Tell No Tales - Deep Sea Danger", "Dimitri")
  # Dead Men Tell No Tales - Battle on the High Seas

  require("Dead Men Tell No Tales - Operation: Reverse Double-Cross", "Guru")

  ## Honor Among Thieves
  # Honor Among Thieves - Carmelita to the Rescue
  # Honor Among Thieves - A Deadly Bite
  # Honor Among Thieves - The Dark Current
  # Honor Among Thieves - Bump-Charge-Jump
  # Honor Among Thieves - Danger in the Skie
  # Honor Among Thieves - The Ancestors' Gauntlet
  # Honor Among Thieves - Stand your Ground
  # Honor Among Thieves - Final Legacy

  ### Challenge requirements
  ## An Opera of Fear
  require("An Opera of Fear - Canal Chase - Expert Course", "Bentley")
  require("An Opera of Fear - Air Time", ["Murray", "Ball Form"])
  # An Opera of Fear - Tower Scramble
  # An Opera of Fear - Coin Chase
  require("An Opera of Fear - Speed Bombing", "Bombs")
  # An Opera of Fear - Octavio Canal Challenge
  # An Opera of Fear - Octavio's Last Stand
  require("An Opera of Fear - Venice Treasure Hunt", "Treasure Map")

  ## Rumble Down Under
  # Rumble Down Under - Rock Run
  # Rumble Down Under - Cave Sprint
  # Rumble Down Under - Cave Mayhem
  # Rumble Down Under - Scaling the Drill
  require("Rumble Down Under - Guard Swappin'", "Guru")
  # Rumble Down Under - Quick Claw
  require("Rumble Down Under - Pressure Brawl", "Bentley")
  # Rumble Down Under - Croc and Coins
  # Rumble Down Under - Carmelita Climb
  require("Rumble Down Under - Outback Treasure Hunt", "Treasure Map")

  ## Flight of Fancy
  # Flight of Fancy - Castle Quick Climb
  require("Flight of Fancy - Muggshot Goon Attack", "Penelope")
  require("Flight of Fancy - Security Breach", "Penelope")
  require("Flight of Fancy - Defend the Hangar", "Penelope")
  require("Flight of Fancy - Precision Air Duel", ["Murray", "Bentley", "Guru", "Fishing Pole", "Penelope"])
  require("Flight of Fancy - Wolf Rampage", "Guru")
  require("Flight of Fancy - One Woman Army", "Carmelita")
  require("Flight of Fancy - Going Out On A Wing", "Paraglider")
  require("Flight of Fancy - Holland Treasure Hunt", "Treasure Map")

  ## A Cold Alliance
  require("A Cold Alliance - Big Air in China", ["Bentley", "Murray", "Guru", "Penelope", "Binocucom"])

  require("A Cold Alliance - Sharpshooter", "Panda King")
  # A Cold Alliance - Treetop Tangle
  # A Cold Alliance - Tsao Showdown
  require("A Cold Alliance - China Treasure Hunt", "Treasure Map")

  ## Dead Men Tell No Tales
  require("Dead Men Tell No Tales - Patch Grab", "Disguise (Pirate)")
  require("Dead Men Tell No Tales - Stealth Challenge", "Disguise (Pirate)")
  require("Dead Men Tell No Tales - Boat Bash", "Murray")
  require("Dead Men Tell No Tales - Last Ship Sailing", ["Bentley", "Penelope", "Grapple-Cam", "Murray", "Silent Obliteration", "Treasure Map"])
  # Dead Men Tell No Tales - Pirate Treasure Hunt

  ## Honor Among Thieves
  # Beauty versus the Beast
  # Road Rage
  # Dr. M Dogfight
  # Ultimate Gauntlet
  # Battle Against Time

  if world.options.goal.value < 6:
    victory_condition = [
      "An Opera of Fear - Operation: Tar-Be Gone!",
      "Rumble Down Under - Operation: Moon Crash",
      "Flight of Fancy - Operation: Turbo Dominant Eagle",
      "A Cold Alliance - Operation: Wedding Crasher",
      "Dead Men Tell No Tales - Operation: Reverse Double-Cross",
      "Honor Among Thieves - Final Legacy"
    ][world.options.goal.value]

    victory_location = world.multiworld.get_location(victory_condition, world.player)
    victory_location.address = None
    victory_location.place_locked_item(world.create_event("Victory"))
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
  elif world.options.goal.value == 6:
    def access_rule(state: CollectionState):
      victory_conditions = [
        "An Opera of Fear - Operation: Tar-Be Gone!",
        "Rumble Down Under - Operation: Moon Crash",
        "Flight of Fancy - Operation: Turbo Dominant Eagle",
        "A Cold Alliance - Operation: Wedding Crasher",
        "Dead Men Tell No Tales - Operation: Reverse Double-Cross",
        "Honor Among Thieves - Final Legacy"
      ]

      return all(
        world.multiworld.get_location(cond,world.player).access_rule(state)
        for cond in victory_conditions
      )

    world.multiworld.completion_condition[world.player] = access_rule
