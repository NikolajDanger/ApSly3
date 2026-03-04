from typing import Optional, Dict, NamedTuple
import struct
from logging import Logger
from enum import IntEnum
import traceback

from .pcsx2_interface.pine import Pine
from .data.Constants import ADDRESSES, MENU_RETURN_DATA, POWER_UP_TEXT

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
  venice_disguise: bool = False
  photographer_disguise: bool = False

  pirate_disguise: bool = False
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
  def _reload(self, reload_data: bytes):
    self._write_bytes(
      self.addresses["reload values"],
      reload_data
    )
    self._write32(self.addresses["reload"], 1)

  def _get_job_address(self, task: int) -> int:
    pointer = self._read32(self.addresses["DAG root"])
    for _ in range(task):
      pointer = self._read32(pointer+0x20)

    return pointer

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
      self._read32(self.addresses["infobox string"]) in [
        5345,5346,5347,5348,5349,5350,5351
      ]
    )

  def in_hub(self) -> bool:
    return self.get_current_map() in [3,8,15,23,31,35]

  def is_goaled(self, goal: int) -> bool:
    # TODO: Goal
    return False

  def is_game_started(self) -> bool:
    world_id = self.get_current_episode()
    map_id = self.get_current_map()
    return not (
      world_id == 0 and
      map_id in [35,0xffffffff]
    )

  def showing_infobox(self) -> bool:
    # TODO: Notifications
    return False

  def alive(self) -> bool:
    active_character = self._read32(self.addresses["active character pointer"])
    if active_character == 0:
      return True

    health_gui = self._read32(active_character+0x16c)
    health = self._read32(active_character+0x16c)
    return health_gui != 2 or health != 0

  #######################
  ## Getters & Setters ##
  #######################
  def set_thiefnet(self, data: list[tuple[int,str]]) -> None:
    addresses = [
      self.addresses["thiefnet start"]+i*0x3c
      for i in range(44)
      if i not in [28,36,37,39,40,42,43]
    ][:len(data)]

    for i, address in enumerate(addresses):
      self._write32(address,data[i][0])
      self._write32(address+0xC,0)
      name_id = self._read32(address+0x14)
      name_address = self._find_string_address(name_id)
      self.set_text(name_address, f"Check #{i+1}")

      description_id = self._read32(address+0x18)
      description_address = self._find_string_address(description_id)
      self.set_text(description_address, data[i][1])

    for i in [28,36,37,39,40,42,43]+list(range(len(data),44)):
      address = self.addresses["thiefnet start"]+i*0x3c
      self._write32(address+0xC,10)

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
    # TODO: Job Markers
    pass

  def deactivate_jobs(self, job_ids: int|list[int]):
    # TODO: Job Markers
    pass

  def jobs_completed(self) -> list[bool]:
    addresses = [a for ep in self.addresses["job completed"].values() for c in ep for a in c]
    states = self._batch_read32(addresses)

    return [s != 0 for s in states]

  def current_infobox(self) -> int:
    # TODO: Notifications
    return 0

  def get_damage_type(self) -> int:
    # TODO: Death Messages
    return 0

  #################
  ## Other Utils ##
  #################
  def to_episode_menu(self) -> None:
    self.logger.info("Skipping to episode menu")
    if (
      self.get_current_map() == 35 and
      self.get_current_job() == 1797
    ):
      self.set_current_job(0xffffffff)
      self.set_items_received(0)

    self._reload(bytes.fromhex(MENU_RETURN_DATA))

  def unlock_episodes(self) -> None:
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
    # TODO: Notifications
    pass

  def set_infobox(self, text: str):
    # TODO: Notifications
    pass

  def kill_player(self):
    if self.in_safehouse() or self.get_current_episode() == Sly3Episode.Title_Screen:
      return

    self._write32(self.addresses["reload"],1)

#### TESTING ZONE ####

def read_text(interf: Sly3Interface, address: int):
  """Reads text at a specific address"""
  text = ""

  while True:
    character = interf._read_bytes(address,2)

    if character == b"\x00\x00":
      break

    text += character.decode("utf-16-le")

    address += 2

  return text

def find_string_id(interf: Sly3Interface, _id: int):
  """Searches for a specific string by ID"""

  # String table starts at 0x47A2D8

  # Each entry in the string table has 4 bytes of its ID and then 4 bytes of an
  # address to the string

  string_table_address = interf._read32(0x47A2D8)
  i = 0
  while True:
    string_id = interf._read32(string_table_address+i*8)
    if string_id == _id:
      return interf._read32(string_table_address+i*8+4)
    i += 1

def find_string_address(interf: Sly3Interface, address: int):
  """Searches for a specific string by ID"""

  # String table starts at 0x47A2D8

  # Each entry in the string table has 4 bytes of its ID and then 4 bytes of an
  # address to the string

  string_table_address = interf._read32(0x47A2D8)
  i = 0
  while True:
    string_address = interf._read32(string_table_address+i*8+4)
    if string_address == address:
      return interf._read32(string_table_address+i*8)
    i += 1

def print_string_table(interf: Sly3Interface, n: int):
  """Prints n entries in the string table"""

  # String table starts at 0x47A2D8

  # Each entry in the string table has 4 bytes of its ID and then 4 bytes of an
  # address to the string

  string_table_address = interf._read32(0x47A2D8)
  for i in range(n):
    address = interf._read32(string_table_address+i*8+4)
    print(read_text(interf, address), i)

def find_text(interf: Sly3Interface, text: str):
  """Prints n entries in the string table"""

  # String table starts at 0x47A2D8

  # Each entry in the string table has 4 bytes of its ID and then 4 bytes of an
  # address to the string

  string_table_address = interf._read32(0x47A2D8)
  results = []
  for i in range(2000):
    address = interf._read32(string_table_address+i*8+4)
    try:
      if text in read_text(interf, address):
        results.append(address)
    except:
      return results

  return results

def print_thiefnet_addresses(interf: Sly3Interface):
  print("        {")
  for i in range(44):
    address = 0x343208+i*0x3c
    interf._write32(address,i+1)
    interf._write32(address+0xC,0)

    name_id = interf._read32(address+0x14)
    name_address = find_string_id(interf, name_id)
    name_text = read_text(interf, name_address)

    description_id = interf._read32(address+0x18)
    description_address = find_string_id(interf, description_id)

    print(
      "          " +
      f"\"{name_text}\": "+
      f"({hex(name_address)},{hex(description_address)}),"
    )

  print("        }")

def print_thiefnet_text(interf: Sly3Interface):
  print("[")
  for i in range(44):
    address = 0x343208+i*0x3c
    interf._write32(address,i+1)
    interf._write32(address+0xC,0)

    name_id = interf._read32(address+0x14)
    name_address = find_string_id(interf, name_id)
    name_text = read_text(interf, name_address)

    description_id = interf._read32(address+0x18)
    description_address = find_string_id(interf, description_id)
    description_text = read_text(interf, description_address)

    print(
      "  " +
      f"(\"{name_text}\",\"{description_text}\"),"
    )

  print("]")

def current_job_info(interf: Sly3Interface):
  current_job = interf._read32(0x36DB98)

  address = interf._read32(interf.addresses["DAG root"])
  i = 0
  while address != 0:
    job_pointer = interf._read32(address+0x6c)
    job_id = interf._read32(job_pointer+0x18)
    if job_id == current_job:
      break

    address = interf._read32(address+0x20)
    i += 1

  print("Job ID:", current_job)
  print("Job address:", hex(address))
  print("Job index:", i)
  print("Job state (should be 2):", interf._read32(address+0x44))

if __name__ == "__main__":
  interf = Sly3Interface(Logger("test"))
  interf.connect_to_game()
  #interf.to_episode_menu()
  #interf.unlock_episodes()
  # interf.skip_cutscene()

  # Loading all power-ups (except the one I don't know)
  # power_ups = PowerUps(True, True, True, False, *[True]*44)
  # interf.set_powerups(power_ups)

  # Adding 10000 coins
  #interf.add_coins(10000)

  # === Testing Zone ===

  # print_thiefnet_addresses(interf)

  # disabling first job of episode 1 (0 = disabled, 1 = available, 2 = in progress, 3 = complete)
  # interf._write32(0x1335d10+0x44, 0)

  # current_job_info(interf)
  # find_string_id

  # print_string_table(interf, 500)

  # addresses = find_text(interf, "Press &2X&. to ")
  # print("======")
  # for address in addresses:
  #   print(hex(address))
  #   print(read_text(interf, address))
  #   print(find_string_address(interf, address))
  #   print("======")

  print_thiefnet_text(interf)