from typing import TYPE_CHECKING, Dict, List

from BaseClasses import ItemClassification

from .data.Constants import REQUIREMENTS
from .data import Items

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

#########
# Steps #
#########

##################
# Main Functions #
##################

async def init(ctx: "Sly3Context", ap_connected: bool) -> None:
  """Called when the player connects to the AP server or changes map"""
  pass

async def update(ctx: "Sly3Context", ap_connected: bool) -> None:
  """Called continuously"""
  pass
