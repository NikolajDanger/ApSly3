from typing import Dict, List, Any, Optional, Mapping
import logging
import inspect
import os.path

from BaseClasses import Item, ItemClassification
from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import (
  Component,
  Type,
  components,
  launch,
  icon_paths,
)

from .Sly3Options import sly3_option_groups, Sly3Options
from .Sly3Regions import create_regions_sly3
from .Sly3Pool import gen_pool_sly3
from .Sly3Rules import (
  set_rules_sly3,
  THIEFNET_GATED_EPISODES,
  THIEFNET_FREE_EPISODES,
)
from .data.Items import item_dict, item_groups, Sly3Item
from .data.Locations import location_dict, location_groups
from .data.Constants import EPISODES, REQUIREMENTS

## Client stuff
def run_client():
  from .Sly3Client import launch_client
  launch(launch_client, name="Sly3Client")

icon_paths["sly3_ico"] = f"ap:{__name__}/icon.png"
components.append(
  Component("Sly 3 Client", func=run_client, component_type=Type.CLIENT, icon="sly3_ico")
)


## UT Stuff
def map_page_index(episode: str) -> int:
  mapping = {k: i for i,k in enumerate(EPISODES.keys())}

  return mapping.get(episode,0)

## The world
class Sly3Web(WebWorld):
  game = "Sly 3: Honor Among Thieves"
  option_groups = sly3_option_groups

class Sly3World(World):
  """
  Sly 3: Honor Among Thieves is a 2004 stealth action video game developed by
  Sucker Punch Productions and published by Sony Computer Entertainment for
  the PlayStation 2.
  """

  game = "Sly 3: Honor Among Thieves"
  web = Sly3Web()

  options_dataclass = Sly3Options
  options: Sly3Options
  topology_present = True

  item_name_to_id = {item.name: item.code for item in item_dict.values()}
  item_name_groups = item_groups
  location_name_to_id = {
    location.name: location.code for location in location_dict.values()
  }
  location_name_groups = location_groups

  thiefnet_costs: List[int] = []

  # this is how we tell the Universal Tracker we want to use re_gen_passthrough
  @staticmethod
  def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
    return slot_data

  # and this is how we tell Universal Tracker we don't need the yaml
  ut_can_gen_without_yaml = True

  def starting_episode_viable(self, opt: Sly3Options, episode_index: int) -> bool:
    episode = list(EPISODES.keys())[episode_index]
    if self.multiworld.players != 1:
      return True
    starting_items = self.get_starting_items(opt)
    def has_req(req) -> bool:
      if isinstance(req, tuple):
        return starting_items.get(req[0], 0) >= req[1]
      return starting_items.get(req, 0) >= 1
    first_job_doable = any(
      all(has_req(req) for req in job_reqs)
      for job_reqs in REQUIREMENTS["Jobs"][episode][0]
    )
    if episode in THIEFNET_FREE_EPISODES:
      # ThiefNet is open at episode start. A doable first job anchors sphere 1
      # on its own; without one (Dead Men Tell No Tales' first job needs an
      # item), the start relies entirely on the ThiefNet fill bootstrap, which
      # needs enough shops to seed generation reliably (see Sly3Rules). An Opera
      # and Rumble always have a free first job, so they stay viable fallbacks.
      if first_job_doable:
        return True
      return opt.thiefnet_locations.value >= 3
    if episode in THIEFNET_GATED_EPISODES:
      # ThiefNet only opens after the first job, so the first job has to be
      # doable from the starting items for anything to be in logic.
      return first_job_doable
    return True

  def validate_options(self, opt: Sly3Options):
    # The fuzzer should run with permissive yaml on so random-value yamls
    # produce a representative sample instead of halting on OptionErrors.
    if any(
      frame.function == "call_generate"
      and os.path.basename(frame.filename) == "fuzz.py"
      for frame in inspect.stack()
    ):
      opt.permissive_yaml.value = True

    if opt.coins_maximum < opt.coins_minimum:
      if not opt.permissive_yaml:
        raise OptionError(
          f"{self.player_name}: Coins minimum cannot be larger than maximum "
          f"(min: {opt.coins_minimum}, max: {opt.coins_maximum})."
        )
      logging.warning(
        f"{self.player_name}: " +
        f"Coins minimum cannot be larger than maximum (min: {opt.coins_minimum}, max: {opt.coins_maximum}). Swapping values."
      )
      temp = opt.coins_minimum.value
      opt.coins_minimum.value = opt.coins_maximum.value
      opt.coins_maximum.value = temp

    if opt.thiefnet_maximum < opt.thiefnet_minimum:
      if not opt.permissive_yaml:
        raise OptionError(
          f"{self.player_name}: Thiefnet minimum cannot be larger than maximum "
          f"(min: {opt.thiefnet_minimum}, max: {opt.thiefnet_maximum})."
        )
      logging.warning(
        f"{self.player_name}: " +
        f"Thiefnet minimum cannot be larger than maximum (min: {opt.thiefnet_minimum}, max: {opt.thiefnet_maximum}). Swapping values."
      )
      temp = opt.thiefnet_minimum.value
      opt.thiefnet_minimum.value = opt.thiefnet_maximum.value
      opt.thiefnet_maximum.value = temp

    if not self.starting_episode_viable(opt, opt.starting_episode.value):
      starting_episode = list(EPISODES.keys())[opt.starting_episode.value]
      if not opt.permissive_yaml:
        raise OptionError(
          f"{self.player_name}: Starting in {starting_episode} as the only slot "
          "leaves no locations in logic, because its first job requires items "
          "you don't start with and no other slot can send them. Either change "
          "your starting episode, add the required items via start_inventory, "
          "or play in a multiworld with other slots."
        )
      new_index = self.random.choice([
        i for i in range(len(EPISODES) - 1)
        if self.starting_episode_viable(opt, i)
      ])
      opt.starting_episode.value = new_index
      logging.warning(
        f"{self.player_name}: " +
        f"Starting in {starting_episode} as the only slot leaves no locations "
        f"in logic. Changing starting episode to "
        f"{list(EPISODES.keys())[new_index]}."
      )

  def get_starting_items(self, opt: Sly3Options) -> Dict[str, int]:
    items: Dict[str, int] = {}
    def add(name: str, count: int = 1) -> None:
      items[name] = items.get(name, 0) + count
    if opt.bonus_crew_member.value != 0:
      # current_key is lowercased; crew item names are Title Case.
      add(opt.bonus_crew_member.current_key.replace("_", " ").title())
    if opt.start_with_binocucom:
      add("Binocucom")
    if opt.start_with_bombs:
      add("Bombs")
    if opt.start_with_double_jump:
      add("Progressive Hover Pack")
    for name, count in opt.start_inventory.value.items():
      add(name, count)
    for name, count in opt.start_inventory_from_pool.value.items():
      add(name, count)
    return items

  def generate_early(self) -> None:
    # implement .yaml-less Universal Tracker support
    if hasattr(self.multiworld, "generation_is_fake"):
      if hasattr(self.multiworld, "re_gen_passthrough"):
        # I'm doing getattr purely so pylance stops being mad at me
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough")

        if "Sly 3: Honor Among Thieves" in re_gen_passthrough:
          slot_data = re_gen_passthrough["Sly 3: Honor Among Thieves"]
          self.thiefnet_costs = slot_data["thiefnet_costs"]
          self.options.starting_episode.value = slot_data["starting_episode"]
          self.options.goal.value = slot_data["goal"]
          self.options.include_mega_jump.value = slot_data["include_mega_jump"]
          self.options.mega_jump_energy_cost.value = slot_data["mega_jump_energy_cost"]
          self.options.coins_minimum.value = slot_data["coins_minimum"]
          self.options.coins_maximum.value = slot_data["coins_maximum"]
          self.options.thiefnet_locations.value = slot_data["thiefnet_locations"]
          self.options.thiefnet_minimum.value = slot_data["thiefnet_minimum"]
          self.options.thiefnet_maximum.value = slot_data["thiefnet_maximum"]
          self.options.bonus_crew_member.value = slot_data["bonus_crew_member"]
          self.options.start_with_binocucom.value = slot_data["start_with_binocucom"]
          self.options.start_with_bombs.value = slot_data["start_with_bombs"]
          self.options.start_with_double_jump.value = slot_data["start_with_double_jump"]
          self.options.scout_thiefnet.value = slot_data["scout_thiefnet"]
          self.options.permissive_yaml.value = slot_data["permissive_yaml"]
      return

    self.validate_options(self.options)

    thiefnet_min = self.options.thiefnet_minimum.value
    thiefnet_max = self.options.thiefnet_maximum.value
    self.thiefnet_costs = sorted([
      self.random.randint(thiefnet_min,thiefnet_max)
      for _ in range(37)
    ])

  def create_regions(self) -> None:
    create_regions_sly3(self)

  def get_filler_item_name(self) -> str:
    # Currently just coins
    return self.random.choice(list(self.item_name_groups["Filler"]))

  def create_item(
    self, name: str, override: Optional[ItemClassification] = None
  ) -> Item:
    item = item_dict[name]

    if override is not None:
      return Sly3Item(name, override, item.code, self.player)

    return Sly3Item(name, item.classification, item.code, self.player)

  def create_event(self, name: str):
    return Sly3Item(name, ItemClassification.progression, None, self.player)

  def create_items(self) -> None:
    items_to_add = gen_pool_sly3(self)

    self.multiworld.itempool += items_to_add

  def set_rules(self) -> None:
    set_rules_sly3(self)

  def get_options_as_dict(self) -> Dict[str, Any]:
    return self.options.as_dict(
      "death_link",
      "starting_episode",
      "goal",
      "include_mega_jump",
      "mega_jump_energy_cost",
      "coins_minimum",
      "coins_maximum",
      "thiefnet_locations",
      "thiefnet_minimum",
      "thiefnet_maximum",
      "bonus_crew_member",
      "start_with_binocucom",
      "start_with_bombs",
      "start_with_double_jump",
      "scout_thiefnet",
      "permissive_yaml",
    )

  def fill_slot_data(self) -> Mapping[str, Any]:
    slot_data = self.get_options_as_dict()
    slot_data["thiefnet_costs"] = self.thiefnet_costs
    slot_data["world_version"] = self.world_version

    return slot_data

