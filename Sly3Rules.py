import typing

from BaseClasses import CollectionState

from worlds.generic.Rules import add_rule, add_item_rule
from .data.Constants import EPISODES, CHALLENGES, REQUIREMENTS
from .data.Locations import location_dict

if typing.TYPE_CHECKING:
    from . import Sly3World

def has_req(state: CollectionState, req, player: int) -> bool:
  """Check a single requirement, which may be an item name or a
  (item_name, count) tuple for progressive items."""
  if isinstance(req, tuple):
    return state.has(req[0], player, req[1])
  return state.has(req, player)

def make_thiefnet_rule(player: int, n: int):
  def new_rule(state: CollectionState):
    if (
      state.count_group("Episode", player) == 1 and
      state.has("Flight of Fancy", player) and
      not state.has("Bentley", player)
    ):
      return False

    if (
      state.count_group("Episode", player) == 1 and
      state.has("A Cold Alliance", player) and
      not all(
        state.has(item, player)
        for item in ["Bentley", "Murray", "Guru", "Penelope", "Binocucom"]
      )
    ):
      return False

    progression_items = (
      state.count_group("Episode", player) +
      state.count_group("Crew", player)
    )

    return progression_items >= n

  return new_rule

def set_rules_sly3(world: "Sly3World"):
  player = world.player
  thiefnet_items = world.options.thiefnet_locations.value

  # Putting ThiefNet stuff out of logic, to make early game less slow.
  if not hasattr(world.multiworld, "generation_is_fake") and thiefnet_items > 0: # (unless tracking)
    FLOOR = 6
    if world.options.starting_episode.value > 1:
      FLOOR = 1
    CEILING = 10

    span = max(thiefnet_items - 1, 1)

    for i in range(1, thiefnet_items + 1):
      location = world.get_location(f"ThiefNet {i:02}")

      required = FLOOR + round((i - 1) / span * (CEILING - FLOOR))
      add_rule(location, make_thiefnet_rule(player, required))

  ### Job requirements
  for episode, sections in EPISODES.items():
    for i, s in enumerate(sections):
      for j, job in enumerate(s):
        reqs = REQUIREMENTS["Jobs"][episode][i][j]
        add_rule(
          world.get_location(f"{episode} - {job}"),
          lambda state, items=reqs: (
            all(has_req(state, item, player) for item in items)
          )
        )

  ### Challenge requirements
  for episode, sections in CHALLENGES.items():
    for i, s in enumerate(sections):
      for j, challenge in enumerate(s):
        reqs = REQUIREMENTS["Challenges"][episode][i][j]
        add_rule(
          world.get_location(f"{episode} - {challenge} (MTC)"),
          lambda state, items=reqs: (
            all(has_req(state, item, player) for item in items)
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
        all(has_req(state, item, player) for item in all_requirements)
      )
    )

  victory_location.address = None
  victory_location.place_locked_item(world.create_event("Victory"))
  world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
