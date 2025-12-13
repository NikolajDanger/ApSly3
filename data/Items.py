from typing import NamedTuple

from BaseClasses import Item, ItemClassification

from .Constants import EPISODES

class Sly3Item(Item):
  game: str = "Sly 3: Honor Among Thieves"

class Sly3ItemData(NamedTuple):
  name: str
  code: int
  category: str
  classification: ItemClassification

filler_list = [
  ("Coins",                     ItemClassification.filler,      "Filler"),
]

powerup_list = [
  ("Binocucom",                 ItemClassification.progression, "Power-Up"),
  ("Smoke Bomb",                ItemClassification.useful,      "Power-Up"),
  ("Knockout Dive",             ItemClassification.useful,      "Power-Up"),
  ("Combat Dodge",              ItemClassification.useful,      "Power-Up"),
  ("Paraglider",                ItemClassification.progression, "Power-Up"),
  ("Rocket Boots",              ItemClassification.useful,      "Power-Up"),
  ("Silent Obliteration",       ItemClassification.progression, "Power-Up"),
  ("Feral Pounce",              ItemClassification.useful,      "Power-Up"),
  ("Thief Reflexes",            ItemClassification.useful,      "Power-Up"),
  ("Progressive Shadow Power",  ItemClassification.useful,      "Power-Up"),
  ("Treasure Map",              ItemClassification.progression, "Power-Up"),
  ("Disguise (Venice)",         ItemClassification.progression, "Power-Up"),
  ("Disguise (Photographer)",   ItemClassification.progression, "Power-Up"),
  ("Disguise (Pirate)",         ItemClassification.progression, "Power-Up"),
  ("Progressive Spin Attack",   ItemClassification.useful,      "Power-Up"),
  ("Progressive Jump Attack",   ItemClassification.useful,      "Power-Up"),
  ("Progressive Push Attack",   ItemClassification.useful,      "Power-Up"),
  ("Mega Jump",                 ItemClassification.useful,      "Power-Up"),

  ("Bombs",                     ItemClassification.progression, "Power-Up"),
  ("Trigger Bomb",              ItemClassification.useful,      "Power-Up"),
  ("Fishing Pole",              ItemClassification.progression, "Power-Up"),
  ("Alarm Clock",               ItemClassification.useful,      "Power-Up"),
  ("Adrenaline Burst",          ItemClassification.useful,      "Power-Up"),
  ("Health Extractor",          ItemClassification.useful,      "Power-Up"),
  ("Insanity Strike",           ItemClassification.useful,      "Power-Up"),
  ("Grapple-Cam",               ItemClassification.progression, "Power-Up"),
  ("Size Destabilizer",         ItemClassification.useful,      "Power-Up"),
  ("Rage Bomb",                 ItemClassification.useful,      "Power-Up"),
  ("Reduction Bomb",            ItemClassification.useful,      "Power-Up"),
  ("Hover Pack",                ItemClassification.progression, "Power-Up"),

  ("Ball Form",                 ItemClassification.progression, "Power-Up"),
  ("Berserker Charge",          ItemClassification.useful,      "Power-Up"),
  ("Juggernaut Throw",          ItemClassification.useful,      "Power-Up"),
  ("Guttural Roar",             ItemClassification.useful,      "Power-Up"),
  ("Fists of Flame",            ItemClassification.useful,      "Power-Up"),
  ("Temporal Lock",             ItemClassification.useful,      "Power-Up"),
  ("Raging Inferno Flop",       ItemClassification.useful,      "Power-Up"),
  ("Diablo Fire Slam",          ItemClassification.useful,      "Power-Up")
]

crew_list = [
  ("Bentley",                   ItemClassification.progression, "Crew"),
  ("Murray",                    ItemClassification.progression, "Crew"),
  ("Guru",                      ItemClassification.progression, "Crew"),
  ("Penelope",                  ItemClassification.progression, "Crew"),
  ("Panda King",                ItemClassification.progression, "Crew"),
  ("Dimitri",                   ItemClassification.progression, "Crew"),
  ("Carmelita",                 ItemClassification.progression, "Crew")
]

episode_list = [
  (episode,                     ItemClassification.progression, "Episode")
  for episode in list(EPISODES.keys())[:-1]
]

item_list = (
  filler_list +
  powerup_list +
  crew_list +
  episode_list
)

base_code = 5318008

item_dict = {
  name: Sly3ItemData(name, base_code+code, category, classification)
  for code, (name, classification, category) in enumerate(item_list)
}

item_groups = {
  key: {item.name for item in item_dict.values() if item.category == key}
  for key in [
    "Filler",
    "Power-Up",
    "Episode",
    "Crew"
  ]
}

def from_id(item_id: int) -> Sly3ItemData:
  matching = [item for item in item_dict.values() if item.code == item_id]
  if len(matching) == 0:
    raise ValueError(f"No item data for item id '{item_id}'")
  assert len(matching) < 2, f"Multiple item data with id '{item_id}'. Please report."
  return matching[0]