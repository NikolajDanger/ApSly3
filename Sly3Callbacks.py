from typing import TYPE_CHECKING, Dict, List
from time import time
from random import randint
import asyncio
import re

from NetUtils import ClientStatus
from BaseClasses import ItemClassification

from .Sly3Interface import Sly3Episode, PowerUps
from .data.Constants import REQUIREMENTS, DEATH_TYPES, EPISODES, CHALLENGES, JOB_IDS
from .data import Items, Locations

if TYPE_CHECKING:
  from .Sly3Client import Sly3Context

###########
# Helpers #
###########

def accessibility(ctx: "Sly3Context") -> Dict[int, bool]:
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

  # challenge_requirements = {
  #   episode_name: [
  #     [
  #       list(set(reqs + section_requirements[episode_name][section_idx]))
  #       for reqs in section
  #     ]
  #     for section_idx, section in enumerate(episode)
  #   ]
  #   for episode_name, episode in REQUIREMENTS["Challenges"].items()
  # }

  # challenge_requirements["Honor Among Thieves"] = [[
  #   [
  #     "Bentley",
  #     "Murray",
  #     "Guru",
  #     "Penelope",
  #     "Panda King",
  #     "Dimitri",
  #     "Carmelita"
  #   ]
  #   for _ in range(5)
  # ]]

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

  # challenge_accessibility = {
  #   episode_name: [
  #     [
  #       all(r in progression_item_names for r in reqs)
  #       for reqs in section
  #     ]
  #     for section in episode
  #   ]
  #   for episode_name, episode in challenge_requirements.items()
  # }

  # I don't think we need to also do challenges
  return {
    JOB_IDS[ep][i][j]: avail
    for ep, ep_avail in job_accessibility.items()
    for i, section_avail in enumerate(ep_avail)
    for j, avail in enumerate(section_avail)
  }

async def set_thiefnet(ctx: "Sly3Context"):
  if ctx.slot_data is None:
    return

  thiefnet_n = ctx.slot_data["thiefnet_locations"]

  if ctx.thiefnet_items is None:
    info = ctx.locations_info
    ctx.thiefnet_items = []
    for i in range(thiefnet_n):
      location_info = info[Locations.location_dict[f"ThiefNet {i+1:02}"].code]

      player_name = ctx.player_names[location_info.player]
      item_name = ctx.item_names.lookup_in_slot(location_info.item,location_info.player)
      string = f"{player_name}'s {item_name}"

      ctx.thiefnet_items.append(string)

  skipped_indices = set([28,36,37,39,40,42,43])
  total_length = thiefnet_n+len(skipped_indices)
  val_iter = iter([
    Locations.location_dict[f"ThiefNet {i+1:02}"].code in ctx.checked_locations
    for i in range(thiefnet_n)
  ])
  ctx.thiefnet_purchases = PowerUps(*[False]*4+[
    False if i in skipped_indices else next(val_iter)
    for i in range(total_length)
  ])

  if ctx.slot_data["scout_thiefnet"]:
    await ctx.send_msgs([{
      "cmd": "LocationScouts",
      "locations": [
          Locations.location_dict[f"ThiefNet {i+1:02}"].code
          for i in range(thiefnet_n)
      ],
      "create_as_hint": 2
  }])

  ctx.game_interface.set_powerups(ctx.thiefnet_purchases)
  thiefnet_data = [
    (ctx.slot_data["thiefnet_costs"][i], ctx.thiefnet_items[i])
    for i in range(thiefnet_n)
  ]
  ctx.game_interface.set_thiefnet(thiefnet_data)

async def reset_thiefnet(ctx: "Sly3Context"):
  if ctx.game_interface.in_hub():
    ctx.thiefnet_purchases = ctx.game_interface.get_powerups()
  set_powerups(ctx)
  ctx.game_interface.reset_thiefnet()

def check_jobs(ctx: "Sly3Context"):
  ctx.jobs_completed = ctx.game_interface.jobs_completed()

def check_challenges(ctx: "Sly3Context"):
  ctx.challenges_completed = ctx.game_interface.challenges_completed()

def set_powerups(ctx: "Sly3Context"):
  if not ctx.in_safehouse:
    ctx.game_interface.set_powerups(ctx.powerups)

async def unlock_episodes(ctx):
  await asyncio.sleep(1)
  ctx.game_interface.unlock_episodes()

#########
# Steps #
#########

async def update_in_safehouse(ctx: "Sly3Context"):
  in_safehouse = ctx.game_interface.in_safehouse()
  if in_safehouse and not ctx.in_safehouse:
    ctx.in_safehouse = True
    await set_thiefnet(ctx)
  elif ctx.in_safehouse and not in_safehouse:
    ctx.in_safehouse = False
    await reset_thiefnet(ctx)

async def replace_text(ctx: "Sly3Context"):
  if ctx.current_episode != Sly3Episode.Title_Screen:
    return

  if ctx.current_map == 35:
    ctx.game_interface.set_text(
      "Press START (start)",
      "Connected to Archipelago"
    )
    ctx.game_interface.set_text(
      "Press START (resume)",
      "Connected to Archipelago"
    )

  elif ctx.current_map == 0:
    for i in range(1,7):
      ep_name = Sly3Episode(i).name.replace("_"," ")

      if ctx.available_episodes[Sly3Episode(i)]:
        rep_text = ep_name
      elif i == 6:
        obtained_crew = len([
          i for i in ctx.items_received
          if Items.from_id(i.item).category == "Crew"
        ])
        rep_text = f"{obtained_crew}/7 crew members"
      else:
        rep_text = "Locked"

      ctx.game_interface.set_text(
        ep_name,
        rep_text
      )


async def kick_from_episode(ctx: "Sly3Context", availability: Dict):
  not_connected = (
    ctx.current_episode != 0 and
    not ctx.is_connected_to_server and
    ctx.current_job == 0xffffffff
  )

  ep_not_unlocked = (
    ctx.is_connected_to_server and
    not ctx.available_episodes[Sly3Episode(ctx.current_episode)] and
    ctx.current_job == 0xffffffff
  )

  try:
    job_not_available = ctx.is_connected_to_server and not availability[ctx.current_job]
  except:
    # if ctx.current_job != 0xffffffff:
    #   print(f"Job ID not accounted for: {ctx.current_job}")
    job_not_available = False

  if not_connected or ep_not_unlocked or job_not_available:
    ctx.game_interface.logger.debug(
      f"\nNot connected: {not_connected}"+
      f"\nEpisode not unlocked: {ep_not_unlocked}"+
      f"\nJob not available: {job_not_available}"
    )
    ctx.game_interface.to_episode_menu()

async def check_locations(ctx: "Sly3Context"):
  check_jobs(ctx)
  check_challenges(ctx)

async def send_checks(ctx: "Sly3Context"):
  if ctx.slot_data is None:
    return

  # ThiefNet purchases
  if ctx.in_safehouse:
    ctx.thiefnet_purchases = ctx.game_interface.get_powerups()
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
  i = 0
  for episode_name, episode in EPISODES.items():
    for chapter in episode:
      for job_name in chapter:
        if ctx.jobs_completed[i]:
          location_name = f"{episode_name} - {job_name}"
          location_code = Locations.location_dict[location_name].code
          ctx.locations_checked.add(location_code)
        i += 1

  # Challenges
  i = 0
  for episode_name, episode in CHALLENGES.items():
    for chapter in episode:
      for challenge_name in chapter:
        if ctx.challenges_completed[i]:
          location_name = f"{episode_name} - {challenge_name}"
          location_code = Locations.location_dict[location_name].code
          ctx.locations_checked.add(location_code)
        i += 1

  await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": ctx.locations_checked}])

async def receive_items(ctx: "Sly3Context"):
  if ctx.slot_data is None:
    return

  items_n = ctx.game_interface.get_items_received()

  network_items = ctx.items_received
  available_episodes = {e: False for e in Sly3Episode}
  available_episodes[Sly3Episode.Title_Screen] = True
  available_episodes[Sly3Episode.Honor_Among_Thieves] = len([
    i for i in network_items
    if Items.from_id(i.item).category == "Crew"
  ]) == 7

  new_powerups = list(PowerUps(True))
  powerup_fields = PowerUps._fields

  for i, network_item in enumerate(network_items):
    item = Items.from_id(network_item.item)
    player = ctx.player_names[network_item.player]

    if i >= items_n:
      ctx.inventory[network_item.item] += 1
      ctx.notification(f"Received {item.name} from {player}")

    if item.category == "Episode":
      episode = Sly3Episode[
        item.name.replace(" ","_")
      ]

      available_episodes[episode] = True
    elif item.category == "Power-Up":
      item_name = item.name.lower().replace(" ","_").replace("-","_").replace("(","").replace(")","")
      if item_name == "progressive_shadow_power":
        if new_powerups[30]:
          idx = 32
        else:
          idx = 30
      elif item_name == "progressive_spin_attack":
        if new_powerups[40]:
          idx = 41
        elif new_powerups[39]:
          idx = 40
        else:
          idx = 39
      elif item_name == "progressive_jump_attack":
        if new_powerups[43]:
          idx = 44
        elif new_powerups[42]:
          idx = 43
        else:
          idx = 42
      elif item_name == "progressive_push_attack":
        if new_powerups[46]:
          idx = 47
        elif new_powerups[45]:
          idx = 46
        else:
          idx = 45
      else:
        idx = powerup_fields.index(item_name)

      new_powerups[idx] = True
    elif item.name == "Coins" and i >= items_n:
      amount = randint(
        ctx.slot_data["coins_minimum"],
        ctx.slot_data["coins_maximum"]
      )
      ctx.game_interface.add_coins(amount)

  if ctx.current_episode != 0 and not ctx.in_safehouse:
      set_powerups(ctx)

  ctx.game_interface.set_items_received(len(network_items))
  if available_episodes != ctx.available_episodes:
    ctx.available_episodes = available_episodes
    await replace_text(ctx)

  ctx.powerups = PowerUps(*new_powerups)


async def check_goal(ctx: "Sly3Context"):
  if ctx.slot_data is None:
    return

  goal = ctx.slot_data["goal"]
  goaled = ctx.game_interface.is_goaled(goal)

  if goaled:
    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

async def handle_job_markers(ctx: "Sly3Context", availability: Dict):
  episode = ctx.current_episode.name.replace("_"," ")
  all_ids = [j for e in JOB_IDS.values() for c in e for j in c]

  if ctx.current_map == 31:
    # job_ids = []
    job_ids = [[3848],[3907,4038,3991]]
  elif ctx.current_map == 32:
    # job_ids = []
    job_ids = [[4071,4101,4120],[4145]]
  else:
    job_ids = JOB_IDS[episode]

  completed_jobs = []
  active_jobs = []
  inactive_jobs = []
  for section in job_ids:
    for job_id in section:
      idx = all_ids.index(job_id)
      if ctx.jobs_completed[idx]:
        completed_jobs.append(job_id)
      elif availability[job_id]:
        active_jobs.append(job_id)
      else:
        inactive_jobs.append(job_id)

  ctx.game_interface.complete_jobs(completed_jobs)
  ctx.game_interface.activate_jobs(active_jobs)
  ctx.game_interface.deactivate_jobs(inactive_jobs)

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
    asyncio.create_task(unlock_episodes(ctx))
  elif ctx.game_interface.is_game_started() and ctx.in_hub:
    ctx.game_interface.fix_jobs()

  await replace_text(ctx)

  if ctx.game_interface.is_game_started():
    await receive_items(ctx)

async def update(ctx: "Sly3Context") -> None:
  """Called continuously"""
  if ctx.current_map is None:
    return

  if not ctx.game_interface.is_game_started():
    return

  if ctx.current_episode == Sly3Episode.Title_Screen and ctx.current_map == 35:
    ctx.game_interface.to_episode_menu()

  availability = accessibility(ctx)
  await kick_from_episode(ctx, availability)

  if not ctx.is_connected_to_server:
    return

  await update_in_safehouse(ctx)
  await check_locations(ctx)
  await send_checks(ctx)
  await receive_items(ctx)
  await check_goal(ctx)

  if ctx.current_episode != 0 and ctx.in_hub:
    await handle_job_markers(ctx, availability)

  if ctx.current_map != 0 and not ctx.in_safehouse:
    await handle_notifications(ctx)
    await handle_deathlink(ctx)
