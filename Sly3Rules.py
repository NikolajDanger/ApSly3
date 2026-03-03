import typing
from math import ceil

from BaseClasses import CollectionState

from worlds.generic.Rules import add_rule
from .data.Constants import EPISODES, CHALLENGES, REQUIREMENTS
from .data.Locations import location_dict

if typing.TYPE_CHECKING:
    from . import Sly3World

def set_rules_sly3(world: "Sly3World"):
  player = world.player
  thiefnet_items = world.options.thiefnet_locations.value

  # Putting ThiefNet stuff out of logic, to make early game less slow.
  # Divides the items into groups that require a number of episode and crew
  # items to be in logic
  for i in range(1,thiefnet_items):
    divisor = ceil(thiefnet_items/12)
    episode_items_n = ceil(i/divisor)
    add_rule(
      world.get_location(f"ThiefNet {i:02}"),
      lambda state, n=episode_items_n: (
        (
          state.count_group("Episode", player) +
          state.count_group("Crew", player)
        ) >= n
      )
    )

  def require(location: str, item: str|list[str]):
    add_rule(
      world.get_location(location),
      lambda state, i=item: (
        all(state.has(j, player) for j in i)
      )
    )

  ### Job requirements
  for episode, sections in EPISODES.items():
    if episode == "Honor Among Thieves":
      continue

    for i, s in enumerate(sections):
      for j, job in enumerate(s):
        reqs = REQUIREMENTS["Jobs"][episode][i][j]
        add_rule(
          world.get_location(f"{episode} - {job}"),
          lambda state, items=reqs: (
            all(state.has(item, player) for item in items)
          )
        )

  ### Challenge requirements
  for episode, sections in CHALLENGES.items():
    if episode == "Honor Among Thieves":
      continue

    for i, s in enumerate(sections):
      for j, challenge in enumerate(s):
        reqs = REQUIREMENTS["Challenges"][episode][i][j]
        add_rule(
          world.get_location(f"{episode} - {challenge}"),
          lambda state, items=reqs: (
            all(state.has(item, player) for item in items)
          )
        )

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
  elif world.options.goal.value == 6:
    all_requirements = list(set(sum([sum(sum(ep,[]),[]) for ep in REQUIREMENTS["Jobs"].values()],[])))
    menu_region = world.multiworld.get_region("Menu", world.player)
    menu_region.add_locations({"All Bosses": location_dict["All Bosses"].code})

    victory_location = world.multiworld.get_location("All Bosses", world.player)
    add_rule(
      victory_location,
      lambda state, items=reqs: (
        all(state.has(item, player) for item in all_requirements)
      )
    )

  victory_location.address = None
  victory_location.place_locked_item(world.create_event("Victory"))
  world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
