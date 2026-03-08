from Options import (
  DeathLink,
  StartInventoryPool,
  PerGameCommonOptions,
  Choice,
  Toggle,
  DefaultOnToggle,
  Range,
  OptionGroup
)
from dataclasses import dataclass

class StartingEpisode(Choice):
  """
  Select Which episode to start with.

  Flight of Fancy and Dead Men Tell No Tales require items to do the first
  jobs, meaning you'll only have ThiefNet locations in logic.
  A Cold Alliance also requires items to have even ThiefNet in logic, so if you
  start with that episode, you will start with no locations in logic.
  """

  display_name = "Starting Episode"
  option_An_Opera_of_Fear = 0
  option_Rumble_Down_Under = 1
  option_Flight_of_Fancy = 2
  option_A_Cold_Alliance = 3
  option_Dead_Men_Tell_No_Tales = 4
  default = 0

class Goal(Choice):
  """
  Which boss you must defeat to goal.
  """
  display_name = "Goal"
  option_Don_Octavio = 0
  option_Dark_Mask = 1
  option_Black_Baron = 2
  option_General_Tsao = 3
  option_Captain_LeFwee = 4
  option_Dr_M = 5
  option_All_Bosses = 6
  default = 5

class BonusCrewMember(Choice):
  """
  Which crew member, in addition to Sly, you start with.
  """
  display_name = "Bonus Crew Member"
  option_None = 0
  option_Bentley = 1
  option_Murray = 2
  option_Guru = 3
  option_Penelope = 4
  option_Panda_King = 5
  option_Dimitri = 6
  option_Carmelita = 7
  default = 1


class IncludeMegaJump(Toggle):
  """
  Add the Mega Jump ability to the pool.
  """

  display_name = "Include Mega Jump"


class StartWithBinocucom(DefaultOnToggle):
  """
  Start with the ability to use the binocucom, rather than shuffling it into
  the pool.
  """

  display_name = "Start with Binocucom"


class StartWithBombs(DefaultOnToggle):
  """
  Start with Bentley's bombs, rather than shuffling it into the pool.
  """

  display_name = "Start with Bombs"


class CoinsMinimum(Range):
  """
  The minimum number of coins you'll receive when you get a "Coins" filler
  item.
  """

  display_name = "Coins Minimum"
  range_start = 0
  range_end = 1000
  default = 50


class CoinsMaximum(Range):
  """
  The maximum number of coins you'll receive when you get a "Coins" filler
  item.
  """

  display_name = "Coins Maximum"
  range_start = 0
  range_end = 1000
  default = 200

class ThiefNetLocations(Range):
  """
  The number ThiefNet locations.
  """

  display_name = "ThiefNet Locations"
  range_start = 0
  range_end = 37
  default = 20

class ThiefNetCostMinimum(Range):
  """
  The minimum number of coins items on ThiefNet will cost.
  """

  display_name = "ThiefNet Cost Minimum"
  range_start = 0
  range_end = 9999
  default = 200


class ThiefNetCostMaximum(Range):
  """
  The maximum number of coins items on ThiefNet will cost.
  """

  display_name = "ThiefNet Cost Maximum"
  range_start = 0
  range_end = 9999
  default = 2000


class ScoutThiefnet(DefaultOnToggle):
    """
    Whether to scout/hint ThiefNet checks. They will still be displayed in game.
    """

    display_name = "Scout Thiefnet"

@dataclass
class Sly3Options(PerGameCommonOptions):
  start_inventory_from_pool: StartInventoryPool
  death_link: DeathLink
  starting_episode: StartingEpisode
  goal: Goal
  include_mega_jump: IncludeMegaJump
  coins_minimum: CoinsMinimum
  coins_maximum: CoinsMaximum
  thiefnet_locations: ThiefNetLocations
  thiefnet_minimum: ThiefNetCostMinimum
  thiefnet_maximum: ThiefNetCostMaximum
  bonus_crew_member: BonusCrewMember
  start_with_binocucom: StartWithBinocucom
  start_with_bombs: StartWithBombs
  scout_thiefnet: ScoutThiefnet

sly3_option_groups = [
  OptionGroup("Goal",[
    Goal
  ]),
  OptionGroup("Items",[
    BonusCrewMember,
    StartWithBinocucom,
    StartWithBombs,
    IncludeMegaJump,
    CoinsMinimum,
    CoinsMaximum
  ]),
  OptionGroup("Locations",[
    ThiefNetLocations,
    ThiefNetCostMinimum,
    ThiefNetCostMaximum,
    ScoutThiefnet
  ])
]