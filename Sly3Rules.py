import typing

from BaseClasses import CollectionState

from worlds.generic.Rules import add_rule
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


THIEFNET_FREE_EPISODES = (
  "An Opera of Fear",
  "Rumble Down Under",
  "Dead Men Tell No Tales",
)
THIEFNET_GATED_EPISODES = ("Flight of Fancy", "A Cold Alliance")

def thiefnet_accessible(state: CollectionState, player: int) -> bool:
  """Whether the player can open ThiefNet in-game at all."""
  if any(state.has(ep, player) for ep in THIEFNET_FREE_EPISODES):
    return True
  return any(
    state.has(ep, player) and
    all(has_req(state, req, player) for req in REQUIREMENTS["Jobs"][ep][0][0])
    for ep in THIEFNET_GATED_EPISODES
  )

def make_thiefnet_rule(non_shop_locations, required: int, player: int):
  def new_rule(state: CollectionState):
    if not thiefnet_accessible(state, player):
      return False
    if required <= 0:
      return True
    count = 0
    for loc in non_shop_locations:
      if loc.can_reach(state):
        count += 1
        if count >= required:
          return True
    return False

  return new_rule

def set_rules_sly3(world: "Sly3World"):
  player = world.player
  thiefnet_items = world.options.thiefnet_locations.value

  non_shop_locations = []

  ### Job requirements
  for episode, sections in EPISODES.items():
    for i, s in enumerate(sections):
      for j, job in enumerate(s):
        reqs = REQUIREMENTS["Jobs"][episode][i][j]
        location = world.get_location(f"{episode} - {job}")
        add_rule(
          location,
          lambda state, items=reqs: (
            all(has_req(state, item, player) for item in items)
          )
        )
        non_shop_locations.append(location)

  ### Challenge requirements
  for episode, sections in CHALLENGES.items():
    for i, s in enumerate(sections):
      for j, challenge in enumerate(s):
        reqs = REQUIREMENTS["Challenges"][episode][i][j]
        location = world.get_location(f"{episode} - {challenge} (MTC)")
        add_rule(
          location,
          lambda state, items=reqs: (
            all(has_req(state, item, player) for item in items)
          )
        )
        non_shop_locations.append(location)

  if not hasattr(world.multiworld, "generation_is_fake") and thiefnet_items > 0: # (unless tracking)
    start_state = CollectionState(world.multiworld)
    needs_bootstrap = thiefnet_accessible(start_state, player)
    BOOTSTRAP = min(3, thiefnet_items) if needs_bootstrap else 0
    CEILING = 40
    span = max(thiefnet_items - BOOTSTRAP, 1)

    for i in range(1, thiefnet_items + 1):
      location = world.get_location(f"ThiefNet {i:02}")

      required = round((i - BOOTSTRAP) / span * CEILING) if i > BOOTSTRAP else 0
      add_rule(location, make_thiefnet_rule(non_shop_locations, required, player))

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
