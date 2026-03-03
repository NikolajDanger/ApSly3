import typing

from BaseClasses import Region, CollectionState

from .data.Locations import location_dict
from .data.Constants import EPISODES, CHALLENGES, REQUIREMENTS

if typing.TYPE_CHECKING:
  from . import Sly3World
  from .Sly3Options import Sly3Options

def create_access_rule(episode: str, n: int, options: "Sly3Options", player: int):
  """Returns a function that checks if the player has access to a specific region"""
  def rule(state: CollectionState):
    access = True
    if episode == "Honor Among Thieves":
      access = access and state.count_group("Crew", player) == 7
    else:
      access = access and state.count(episode, player) == 1

      if n > 1:
        section_requirements = [
          sum(
            ep_reqs,
            []
          )
          for ep_reqs
          in REQUIREMENTS["Jobs"][episode][:n-1]
        ]
        requirements = list(set(sum(section_requirements, [])))
        access = access and all(state.has(i, player) for i in requirements)

    return access

  return rule

def create_regions_sly3(world: "Sly3World"):
    """Creates a region for each chapter of each episode"""

    menu = Region("Menu", world.player, world.multiworld)
    menu.add_locations({
      f"ThiefNet {i+1:02}": location_dict[f"ThiefNet {i+1:02}"].code
      for i in range(world.options.thiefnet_locations)
    })

    world.multiworld.regions.append(menu)

    for i, episode in enumerate(EPISODES.keys()):
      for n in range(1,5):
        if n == 2 and episode == "Honor Among Thieves":
          break

        region = Region(f"Episode {i+1} ({n})", world.player, world.multiworld)
        region.add_locations({
          f"{episode} - {job}": location_dict[f"{episode} - {job}"].code
          for job in EPISODES[episode][n-1]
        })
        region.add_locations({
          f"{episode} - {challenge}": location_dict[f"{episode} - {challenge}"].code
          for challenge in CHALLENGES[episode][n-1]
        })

        world.multiworld.regions.append(region)

        menu.connect(
          region,
          None,
          create_access_rule(episode, n, world.options, world.player)
        )

