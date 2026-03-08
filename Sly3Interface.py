from typing import Optional, Dict, NamedTuple
import struct
from logging import Logger
from enum import IntEnum
import traceback
from time import sleep

from .pcsx2_interface.pine import Pine
from .data.Constants import ADDRESSES, MENU_RETURN_DATA, POWER_UP_TEXT, JOB_IDS, EPISODES

class Sly3Episode(IntEnum):
  Title_Screen = 0
  An_Opera_of_Fear = 1
  Rumble_Down_Under = 2
  Flight_of_Fancy = 3
  A_Cold_Alliance = 4
  Dead_Men_Tell_No_Tales = 5
  Honor_Among_Thieves = 6

class PowerUps(NamedTuple):
  attack: bool = False
  binocucom: bool = False
  bombs: bool = False
  unknown: bool = False
  trigger_Bomb: bool = False
  fishing_pole: bool = False

  alarm_clock: bool = False
  adrenaline_burst: bool = False
  health_extractor: bool = False
  hover_pack: bool = False
  insanity_strike: bool = False
  grapple_cam: bool = False
  size_destabilizer: bool = False
  rage_bomb: bool = False

  reduction_bomb: bool = False
  ball_form: bool = False
  berserker_charge: bool = False
  juggernaut_throw: bool = False
  guttural_roar: bool = False
  fists_of_flame: bool = False
  temporal_lock: bool = False
  raging_inferno_flop: bool = False

  diablo_fire_slam: bool = False
  smoke_bomb: bool = False
  combat_dodge: bool = False
  paraglider: bool = False
  silent_obliteration: bool = False
  feral_pounce: bool = False
  mega_jump: bool = False
  knockout_dive: bool = False

  shadow_power_1: bool = False
  thief_reflexes: bool = False
  shadow_power_2: bool = False
  rocket_boots: bool = False
  treasure_map: bool = False
  shield: bool = False
  disguise_venice: bool = False
  disguise_photographer: bool = False

  disguise_pirate: bool = False
  spin_1: bool = False
  spin_2: bool = False
  spin_3: bool = False
  jump_1: bool = False
  jump_2: bool = False
  jump_3: bool = False
  push_1: bool = False

  push_2: bool = False
  push_3: bool = False

class GameInterface():
  """
  Base class for connecting with a pcsx2 game
  """

  pcsx2_interface: Pine = Pine()
  logger: Logger
  game_id_error: Optional[str] = None
  current_game: Optional[str] = None
  addresses: Dict = {}

  def __init__(self, logger) -> None:
    self.logger = logger

  def _read8(self, address: int):
    return self.pcsx2_interface.read_int8(address)

  def _read16(self, address: int):
    return self.pcsx2_interface.read_int16(address)

  def _read32(self, address: int):
    return self.pcsx2_interface.read_int32(address)

  def _read_bytes(self, address: int, n: int):
    return self.pcsx2_interface.read_bytes(address, n)

  def _read_float(self, address: int):
    return struct.unpack("f",self.pcsx2_interface.read_bytes(address, 4))[0]

  def _batch_read8(self, addresses: list[int]) -> list[int]:
    return self.pcsx2_interface.batch_read_int8(addresses)

  def _batch_read16(self, addresses: list[int]) -> list[int]:
    return self.pcsx2_interface.batch_read_int16(addresses)

  def _batch_read32(self, addresses: list[int]) -> list[int]:
    return self.pcsx2_interface.batch_read_int32(addresses)

  def _write8(self, address: int, value: int):
    self.pcsx2_interface.write_int8(address, value)

  def _write16(self, address: int, value: int):
    self.pcsx2_interface.write_int16(address, value)

  def _write32(self, address: int, value: int):
    self.pcsx2_interface.write_int32(address, value)

  def _write_bytes(self, address: int, value: bytes):
    self.pcsx2_interface.write_bytes(address, value)

  def _write_float(self, address: int, value: float):
    self.pcsx2_interface.write_float(address, value)

  def _batch_write32(self, operations: list[tuple[int,int]]):
    self.pcsx2_interface.batch_write_int32(operations)
    # for address, data in operations:
    #   self._write32(address, data)

  def connect_to_game(self):
    """
    Initializes the connection to PCSX2 and verifies it is connected to the
    right game
    """
    if not self.pcsx2_interface.is_connected():
      self.pcsx2_interface.connect()
      if not self.pcsx2_interface.is_connected():
        return
      self.logger.info("Connected to PCSX2 Emulator")
    try:
      game_id = self.pcsx2_interface.get_game_id()
      # The first read of the address will be null if the client is faster than the emulator
      self.current_game = None
      if game_id == "":
        self.logger.debug("No game connected")
        return

      if game_id in ADDRESSES.keys():
        self.current_game = game_id
        self.addresses = ADDRESSES[game_id]
      if self.current_game is None and self.game_id_error != game_id and game_id != b'\x00\x00\x00\x00\x00\x00':
        self.logger.warning(
          f"Connected to the wrong game ({game_id})")
        self.game_id_error = game_id
    except RuntimeError:
      self.logger.debug(traceback.format_exc())
    except ConnectionError:
      self.logger.debug(traceback.format_exc())

  def disconnect_from_game(self):
    self.pcsx2_interface.disconnect()
    self.current_game = None
    self.logger.info("Disconnected from PCSX2 Emulator")

  def get_connection_state(self) -> bool:
    try:
      connected = self.pcsx2_interface.is_connected()
      return connected and self.current_game is not None
    except RuntimeError:
      return False

class Sly3Interface(GameInterface):
  ############################
  ## Private Helper Methods ##
  ############################
  def _reload(self, reload_data: bytes = b""):
    if reload_data != b"":
      self._write_bytes(
        self.addresses["reload values"],
        reload_data
      )
    self._write32(self.addresses["reload"], 1)

  def _find_string_address(self, _id: int) -> int:
    # Each entry in the string table has 4 bytes of its ID and then 4 bytes of an
    # address to the string

    string_table_address = self._read32(self.addresses["string table"])
    i = 0
    while True:
      string_id = self._read32(string_table_address+i*8)
      if string_id == _id:
        return self._read32(string_table_address+i*8+4)
      i += 1

  def _get_task_parents(self, job: int) -> list[int]:
    address = self.addresses["job markers"][job]
    parents_n = self._read32(address+0x84)
    parents_list = self._read32(address+0x88)
    parent_pointers = [parents_list+4*i for i in range(parents_n)]
    return self._batch_read32(parent_pointers)

  def _job_parents_finished(self, job: int) -> bool:
    parents = self._get_task_parents(job)
    return all([
      s == 3 for s in self._batch_read32([p+0x44 for p in parents])
    ])

  ###################
  ## Current State ##
  ###################
  def in_cutscene(self) -> bool:
    frame_counter = self._read16(self.addresses["frame counter"])
    return frame_counter > 10

  def is_loading(self) -> bool:
    return self._read32(self.addresses["loading"]) == 2

  def in_safehouse(self) -> bool:
    return (
      not self.is_loading() and
      self.in_hub() and
      self.current_infobox() in [
        5345,5346,5347,5348,5349,5350,5351
      ]
    )

  def in_hub(self) -> bool:
    return self.get_current_map() in [3,8,15,23,31,32,35]

  def is_goaled(self, goal: int) -> bool:
    goal_jobs = [ep[-1][-1] for ep in self.addresses["job completed"].values()]
    if goal < 6:
      return self._read32(goal_jobs[goal]) != 0
    elif goal == 6:
      return all([s != 0 for s in self._batch_read32(goal_jobs)])
    return False

  def is_game_started(self) -> bool:
    # world_id = self.get_current_episode()
    # map_id = self.get_current_map()
    return self.intro_done()

  def showing_infobox(self) -> bool:
    infobox_pointer = self._read32(self.addresses["infobox"])
    return self._read32(infobox_pointer+0x64) == 2

  def alive(self) -> bool:
    active_character = self._read32(self.addresses["active character pointer"])
    if active_character == 0:
      return True

    health_gui_pointer = self._read32(active_character+0x168)
    health = self._read32(active_character+0x16c)
    return health_gui_pointer == 0 or health != 0

  #######################
  ## Getters & Setters ##
  #######################
  def set_thiefnet(self, data: list[tuple[int,str]]) -> None:
    thiefnet_indices = set([
      i for i in range(44)
      if i not in [28,36,37,39,40,42,43]
    ][:len(data)])
    addresses = [
      self.addresses["thiefnet start"]+i*0x3c
      for i in thiefnet_indices
    ][:len(data)]
    not_thiefnet = set(range(44)) - thiefnet_indices

    operations = []

    for i, address in enumerate(addresses):
      operations.append((address,data[i][0]))
      operations.append((address+0xC,0))
      name_id = self._read32(address+0x14)
      name_address = self._find_string_address(name_id)
      self.set_text(name_address, f"Check #{i+1}")

      description_id = self._read32(address+0x18)
      description_address = self._find_string_address(description_id)
      self.set_text(description_address, data[i][1])

    for i in not_thiefnet:
      address = self.addresses["thiefnet start"]+i*0x3c
      operations.append((address+0xC,10))

    self._batch_write32(operations)

  def reset_thiefnet(self) -> None:
    for i in range(44):
      address = self.addresses["thiefnet start"]+i*0x3c
      name_id = self._read32(address+0x14)
      name_address = self._find_string_address(name_id)
      self.set_text(name_address, POWER_UP_TEXT[i][0])

      description_id = self._read32(address+0x18)
      description_address = self._find_string_address(description_id)
      self.set_text(description_address, POWER_UP_TEXT[i][1])

  def set_text(self, text: int|str, replacement: str) -> None:
    if isinstance(text,str):
      text_pointer = self.addresses["text"].get(text, None)
      if isinstance(text_pointer, dict):
        text_pointer = text_pointer.get(self.get_current_map(), None)

      if not isinstance(text_pointer,int):
        return
    else:
      text_pointer = text

    replacement_string = replacement.encode("utf-16-le")+b"\x00\x00"
    self._write_bytes(text_pointer,replacement_string)

  def get_current_episode(self) -> Sly3Episode:
    episode_num = self._read32(self.addresses["world id"]) - 2
    return Sly3Episode(max(0,episode_num))

  def get_current_map(self) -> int:
    return self._read32(self.addresses["map id"])

  def get_current_job(self) -> int:
    return self._read32(self.addresses["job id"])

  def set_current_job(self, job: int) -> None:
    self._write32(self.addresses["job id"], job)

  def get_items_received(self) -> int:
    return self._read32(self.addresses["items received"])

  def set_items_received(self, n:int) -> None:
    self._write32(self.addresses["items received"], n)

  def set_powerups(self, powerups: PowerUps):
    booleans = list(powerups)
    byte_list = [
      [False]*2+booleans[0:6],
      booleans[6:14],
      booleans[14:22],
      booleans[22:30],
      booleans[30:38],
      booleans[38:46],
      booleans[46:48]+[False]*2,
      [False]*8
    ]
    data = b''.join(
      int(''.join(str(int(i)) for i in byte[::-1]),2).to_bytes(1,"big")
      for byte in byte_list
    )

    self._write_bytes(self.addresses["gadgets"], data)
    self._write32(self.addresses["grapple-cam weapon"],1)

    if powerups.hover_pack:
      bentley = self._read32(self.addresses["bentley"])
      self._write32(bentley+0x4b0,3)

  def get_powerups(self):
    data = self._read_bytes(self.addresses["gadgets"], 8)
    bits = [
      bool(int(b))
      for byte in data
      for b in f"{byte:08b}"[::-1]
    ]

    relevant_bits = bits[2:48]
    return PowerUps(*relevant_bits)

  def activate_jobs(self, job_ids: int|list[int]):
    if isinstance(job_ids, int):
      job_ids = [job_ids]

    markers = self.addresses["job markers"]
    memory_states = self.addresses["job states"]
    to_read = []
    for job in job_ids:
      if job not in markers:
        self.logger.debug(f"Job {job} not able to be activated")
        continue

      to_read.append(job)

    statuses = self._batch_read32([markers[j]+0x44 for j in to_read])
    to_write = [j for i,j in enumerate(to_read) if statuses[i] == 0 and self._job_parents_finished(j)]
    operations = [(markers[j]+0x44,1) for j in to_write]+[(memory_states[j],1) for j in to_write]
    self._batch_write32(operations)

  def deactivate_jobs(self, job_ids: int|list[int]):
    if isinstance(job_ids, int):
      job_ids = [job_ids]

    markers = self.addresses["job markers"]
    memory_states = self.addresses["job states"]
    to_read = []
    for job in job_ids:
      if job not in markers:
        self.logger.debug(f"Job {job} not able to be deactivated")
        continue

      to_read.append(job)

    statuses = self._batch_read32([markers[j]+0x44 for j in to_read])
    to_write = [j for i,j in enumerate(to_read) if statuses[i] == 1]
    operations = [(markers[j]+0x44,0) for j in to_write]+[(memory_states[j],0) for j in to_write]
    self._batch_write32(operations)

  def complete_jobs(self, job_ids: int|list[int]):
    if isinstance(job_ids, int):
      job_ids = [job_ids]

    markers = self.addresses["job markers"]
    memory_states = self.addresses["job states"]
    to_read = []
    for job in job_ids:
      if job not in markers:
        self.logger.debug(f"Job {job} not able to be completed")
        continue

      to_read.append(job)

    statuses = self._batch_read32([markers[j]+0x44 for j in to_read])
    to_write = [j for i,j in enumerate(to_read) if statuses[i] != 3]
    operations = [(markers[j]+0x44,3) for j in to_write]+[(memory_states[j],3) for j in to_write]
    self._batch_write32(operations)

  def jobs_completed(self) -> list[bool]:
    addresses = [a for ep in self.addresses["job completed"].values() for c in ep for a in c]
    states = self._batch_read32(addresses)

    return [s != 0 for s in states]

  def challenges_completed(self) -> list[bool]:
    addresses = [a for ep in self.addresses["challenge completed"].values() for c in ep for a in c]
    states = self._batch_read32(addresses)

    return [s != 0 for s in states]

  def current_infobox(self) -> int:
    return self._read32(self.addresses["infobox string"])

  def get_damage_type(self) -> int:
    # TODO: Death Messages
    return 0

  #################
  ## Other Utils ##
  #################
  def fix_jobs(self):
    current_job = self.get_current_job()
    if current_job != 0xffffffff:
      return

    current_map = self.get_current_map()

    if current_map == 31:
      job_ids = [3848,3907,4038,3991]
    elif current_map == 32:
      job_ids = [4071,4101,4120,4145]
    else:
      job_ids = [
        job
        for chapter in JOB_IDS[self.get_current_episode().name.replace("_", " ")]
        for job in chapter
      ]

    markers = [self.addresses["job markers"][j]+0x44 for j in job_ids if j in self.addresses["job markers"]]
    statuses = self._batch_read32(markers)
    messed_up_jobs = [job_ids[i] for i,s in enumerate(statuses) if s == 2]

    for job in messed_up_jobs:
      self.logger.info(f"Fixing job {job}")
      job_address = self.addresses["job markers"][job]
      mission = self._read32(job_address+0x6c)

      addresses = [job_address]

      # Fixing all tasks in the job
      while True:
        if len(addresses) == 0:
          break

        address = addresses.pop(0)
        task_mission = self._read32(address+0x6c)
        if task_mission != mission:
          break

        self._write32(address+0x44,1)
        n_children = self._read32(address+0x90)
        children_list = self._read32(address+0x94)
        addresses += [children_list+4*i for i in range(n_children)]

  def intro_done(self) -> bool:
    return self._read32(self.addresses["intro complete"]) == 1

  def to_episode_menu(self) -> None:
    self.logger.info("Skipping to episode menu")
    if (
      self.get_current_map() == 35 and
      self.get_current_job() == 1797 and
      not self.intro_done()
    ):
      self.set_current_job(0xffffffff)
      self.set_items_received(0)

    self._reload(bytes.fromhex(MENU_RETURN_DATA))

  def unlock_episodes(self) -> None:
    self._write32(self.addresses["intro complete"],1)
    self._write8(self.addresses["episode unlocks"], 8)

  def skip_cutscene(self) -> None:
    pressing_x = self._read8(self.addresses["x pressed"]) == 255

    if self.in_cutscene() and pressing_x:
      self._write32(self.addresses["skip cutscene"],0)

  def add_coins(self, to_add: int):
    current_amount = self._read32(self.addresses["coins"])
    new_amount = max(current_amount + to_add,0)
    self._write32(self.addresses["coins"],new_amount)

  def disable_infobox(self):
    infobox_pointer = self._read32(self.addresses["infobox"])
    if self._read32(infobox_pointer+0x54) != 1:
      self._write32(infobox_pointer+0x54,2)
      self._write32(infobox_pointer+0x54,1)

  def set_infobox(self, text: str):
    ep = self.get_current_episode()
    if ep == 0 or self.in_safehouse():
      return

    infobox_pointer = self._read32(self.addresses["infobox"])
    self._write32(self.addresses["infobox scrolling"],1)
    self.set_text("infobox"," "*10+text)
    self._write32(self.addresses["infobox string"],1)
    self._write32(infobox_pointer+0x54,2)
    self._write32(self.addresses["infobox duration"],0xffffffff)

  def kill_player(self):
    if self.in_safehouse() or self.get_current_episode() == Sly3Episode.Title_Screen:
      return

    self._write32(self.addresses["reload"],1)
