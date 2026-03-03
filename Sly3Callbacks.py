from typing import TYPE_CHECKING, Dict, List
from time import time

from NetUtils import ClientStatus
from BaseClasses import ItemClassification

from .data.Constants import REQUIREMENTS, DEATH_TYPES, EPISODES, CHALLENGES
from .data import Items, Locations

if TYPE_CHECKING:
  from .Sly3Client import Sly3Context

###########
# Helpers #
###########

def accessibility(ctx: "Sly3Context") -> Dict[str, Dict[str, List[List[bool]]]]:
  section_requirements = {
    episode_name: [
      list(set(sum([
        sum(
          ep_reqs,
          []
        )
        for ep_reqs
        in episode[:i-1]
      ], [])))
      for i in range(1,5)
    ]
    for episode_name, episode in REQUIREMENTS["Jobs"].items()
  }

  job_requirements = {
    episode_name: [
      [
        list(set(reqs + section_requirements[episode_name][section_idx]))
        for reqs in section
      ]
      for section_idx, section in enumerate(episode)
    ]
    for episode_name, episode in REQUIREMENTS["Jobs"].items()
  }

  job_requirements["Honor Among Thieves"] = [[
    [
      "Bentley",
      "Murray",
      "Guru",
      "Penelope",
      "Panda King",
      "Dimitri",
      "Carmelita"
    ]
    for _ in range(8)
  ]]

  challenge_requirements = {
    episode_name: [
      [
        list(set(reqs + section_requirements[episode_name][section_idx]))
        for reqs in section
      ]
      for section_idx, section in enumerate(episode)
    ]
    for episode_name, episode in REQUIREMENTS["Challenges"].items()
  }

  challenge_requirements["Honor Among Thieves"] = [[
    [
      "Bentley",
      "Murray",
      "Guru",
      "Penelope",
      "Panda King",
      "Dimitri",
      "Carmelita"
    ]
    for _ in range(5)
  ]]

  items_received = [
    Items.from_id(i.item)
    for i in ctx.items_received
  ]

  progression_item_names = set([
    i.name
    for i in items_received
    if i.classification == ItemClassification.progression
  ])

  job_accessibility = {
    episode_name: [
      [
        all(r in progression_item_names for r in reqs)
        for reqs in section
      ]
      for section in episode
    ]
    for episode_name, episode in job_requirements.items()
  }

  challenge_accessibility = {
    episode_name: [
      [
        all(r in progression_item_names for r in reqs)
        for reqs in section
      ]
      for section in episode
    ]
    for episode_name, episode in challenge_requirements.items()
  }

  return {
    "Jobs": job_accessibility,
    "Challenges": challenge_accessibility
  }

def set_thiefnet(ctx: "Sly3Context"):
  # TODO
  pass

def unset_thiefnet(ctx: "Sly3Context"):
  # TODO
  pass

def check_jobs(ctx: "Sly3Context"):
  # TODO
  pass

def check_challenges(ctx: "Sly3Context"):
  # TODO
  pass

def set_powerups(ctx: "Sly3Context"):
  if not ctx.in_safehouse():
    ctx.game_interface.set_powerups(ctx.powerups)

#########
# Steps #
#########

async def update_in_safehouse(ctx: "Sly3Context"):
  in_safehouse = ctx.game_interface.in_safehouse()
  if in_safehouse and not ctx.in_safehouse:
    ctx.in_safehouse = True
    set_thiefnet(ctx)
  elif ctx.in_safehouse and not in_safehouse:
    ctx.in_safehouse = False
    unset_thiefnet(ctx)

async def replace_text(ctx: "Sly3Context"):
  # TODO
  # I'm not totally sure yet which text I'm replacing
  pass

async def kick_from_episode(ctx: "Sly3Context", availability: Dict):
  # TODO
  not_connected = ctx.current_map == 0 and not ctx.is_connected_to_server
  current_episode = ctx.game_interface.get_current_episode()
  ep_not_unlocked = current_episode == 0 or ctx.available_episodes[current_episode-1]
  job_not_available = False # if current job/challenge not available

  if not_connected or ep_not_unlocked or job_not_available:
    ctx.game_interface.to_episode_menu()

async def check_jobs_and_challenges(ctx: "Sly3Context"):
  check_jobs()
  check_challenges()

async def send_checks(ctx: "Sly3Context"):
  if ctx.slot_data is None:
    return

  # ThiefNet purchases
  if ctx.in_safehouse:
    ctx.thiefnet_purchases = ctx.game_interface.read_powerups()
  purchases = list(ctx.thiefnet_purchases)
  purchases = (
    purchases[4:32] +
    purchases[33:40] +
    purchases[42:43] +
    purchases[45:46]
  )

  thiefnet_n = ctx.slot_data["thiefnet_locations"]
  purchases = purchases[:thiefnet_n]
  for i, purchased in enumerate(purchases):
    if purchased:
      location_name = f"ThiefNet {i+1:02}"
      location_code = Locations.location_dict[location_name].code
      ctx.locations_checked.add(location_code)

  # Jobs
  for i, episode in enumerate(ctx.jobs_completed):
    episode_name = list(EPISODES.keys())[i]
    for j, chapter in enumerate(episode):
      for k, job in enumerate(chapter):
        if job:
          job_name = EPISODES[episode_name][j][k]
          location_name = f"{episode_name} - {job_name}"
          location_code = Locations.location_dict[location_name].code
          ctx.locations_checked.add(location_code)

  # Challenges
  for i, episode in enumerate(ctx.challenges_completed):
    episode_name = list(CHALLENGES.keys())[i]
    for j, chapter in enumerate(episode):
      for k, job in enumerate(chapter):
        if job:
          job_name = CHALLENGES[episode_name][j][k]
          location_name = f"{episode_name} - {job_name}"
          location_code = Locations.location_dict[location_name].code
          ctx.locations_checked.add(location_code)

  await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": ctx.locations_checked}])

async def receive_items(ctx: "Sly3Context"):
  # TODO
  pass

async def check_goal(ctx: "Sly3Context"):
  if ctx.slot_data is None:
    return

  goal = ctx.slot_data["goal"]
  goaled = ctx.game_interface.is_goaled(goal)

  if goaled:
    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

async def handle_job_markers(ctx: "Sly3Context", availability: Dict):
  # TODO
  pass

async def handle_notifications(ctx: "Sly3Context"):
  if (
    (ctx.showing_notification and time() - ctx.notification_timestamp < 10) or
    (
      (not ctx.showing_notification) and
      ctx.game_interface.showing_infobox() and
      ctx.game_interface.current_infobox() != 0xffffffff
    ) or
    ctx.game_interface.in_cutscene()
  ):
    return

  ctx.game_interface.disable_infobox()
  ctx.showing_notification = False
  if len(ctx.notification_queue) > 0 and ctx.game_interface.in_hub():
    new_notification = ctx.notification_queue.pop(0)
    ctx.notification_timestamp = time()
    ctx.showing_notification = True
    ctx.game_interface.set_infobox(new_notification)

async def handle_deathlink(ctx: "Sly3Context"):
  if not ctx.death_link_enabled:
    return

  if time()-ctx.deathlink_timestamp <= 20:
    return

  if ctx.game_interface.alive():
    if ctx.queued_deaths > 0:
      ctx.game_interface.kill_player()
      ctx.queued_deaths = 0
      ctx.deathlink_timestamp = time()
  else:
    damage_type = ctx.game_interface.get_damage_type()
    player_name = ctx.player_names[ctx.slot if ctx.slot else 0]
    death_message = DEATH_TYPES.get(damage_type, "{player} died").format(player=player_name)

    await ctx.send_death(death_message)
    ctx.deathlink_timestamp = time()

##################
# Main Functions #
##################

async def init(ctx: "Sly3Context") -> None:
  """Called when the player connects to the AP server or changes map"""
  if ctx.current_map is None or not ctx.is_connected_to_server:
    return

  if ctx.current_map == 0:
    ctx.game_interface.unlock_episodes()

  await replace_text(ctx)
  # Maybe fix jobs if they break?

async def update(ctx: "Sly3Context") -> None:
  """Called continuously"""
  if ctx.current_map is None:
    return

  availability = accessibility(ctx)
  kick_from_episode(ctx, availability)

  if not ctx.is_connected_to_server:
    return

  await update_in_safehouse(ctx)
  await check_jobs_and_challenges(ctx)
  await send_checks(ctx)
  await receive_items(ctx)
  await check_goal(ctx)
  await handle_job_markers(ctx, availability["Jobs"])

  if ctx.in_safehouse:
    await handle_notifications(ctx)
    await handle_deathlink(ctx)
