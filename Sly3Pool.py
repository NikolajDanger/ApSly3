import typing

from BaseClasses import Item

from .data.Constants import EPISODES
from .data.Items import item_groups

if typing.TYPE_CHECKING:
    from . import Sly3World

def gen_powerups(world: "Sly3World") -> list[Item]:
  """Generate the power-ups for the item pool"""
  powerups = []
  for item_name in item_groups["Power-Up"]:
    if item_name == "Mega Jump" and not world.options.include_mega_jump:
      continue
    elif item_name == "Progressive Shadow Power":
      powerups.append(item_name)
      powerups.append(item_name)
    elif item_name[:11] == "Progressive":
      powerups.append(item_name)
      powerups.append(item_name)
      powerups.append(item_name)
    else:
      powerups.append(item_name)

  if world.options.start_with_binocucom:
    powerups.remove("Binocucom")
    world.multiworld.push_precollected(world.create_item("Binocucom"))

  if world.options.start_with_bombs:
    powerups.remove("Bombs")
    world.multiworld.push_precollected(world.create_item("Bombs"))

  return [world.create_item(c) for c in powerups]

def gen_crew(world: "Sly3World") -> list[Item]:
  """Generate the crew for the item pool"""
  crew = list(item_groups["Crew"])

  bonus_crew_n = world.options.bonus_crew_member.value
  if bonus_crew_n != 0:
    bonus_crew = [
      "Bentley",
      "Murray",
      "Guru",
      "Penelope",
      "Panda King",
      "Dimitri",
      "Carmelita"
    ][bonus_crew_n-1]
    crew.remove(bonus_crew)
    world.multiworld.push_precollected(world.create_item(bonus_crew))

  return [world.create_item(c) for c in crew]

def gen_episodes(world: "Sly3World") -> list[Item]:
  """Generate the episodes items for the item pool"""
  all_episodes = [
    item_name for item_name in item_groups["Episode"]
  ]

  # Make sure the starting episode is precollected
  starting_episode_n = world.options.starting_episode.value
  starting_episode = list(EPISODES.keys())[starting_episode_n]
  all_episodes.remove(starting_episode)
  world.multiworld.push_precollected(world.create_item(starting_episode))

  return [world.create_item(e) for e in all_episodes]



def gen_pool_sly3(world: "Sly3World") -> list[Item]:
  """Generate the item pool for the world"""
  item_pool = []
  item_pool += gen_powerups(world)
  item_pool += gen_episodes(world)
  item_pool += gen_crew(world)

  unfilled_locations = world.multiworld.get_unfilled_locations(world.player)
  remaining = len(unfilled_locations)-len(item_pool)
  if world.options.goal.value < 6:
      remaining -= 1
  assert remaining >= 0, f"There are more items than locations ({len(item_pool)} items; {len(unfilled_locations)} locations)"
  item_pool += [world.create_item(world.get_filler_item_name()) for _ in range(remaining)]

  return item_pool
