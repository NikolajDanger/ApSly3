from typing import Optional, Dict, NamedTuple
import struct
from logging import Logger
from enum import IntEnum

from .pcsx2_interface.pine import Pine
from .data.Constants import ADDRESSES, MENU_RETURN_DATA

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

  def _write8(self, address: int, value: int):
    self.pcsx2_interface.write_int8(address, value)

  def _write16(self, address: int, value: int):
    self.pcsx2_interface.write_int16(address, value)

  def _write32(self, address: int, value: int):
    self.pcsx2_interface.write_int32(address, value)

  def _write_bytes(self, address: int, value: bytes):
    self.pcsx2_interface.write_bytes(address, value)

  def _write_float(self, address: int, value: float):
    self.pcsx2_interface.write_bytes(address, struct.pack("f", value))

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
      if game_id in ADDRESSES.keys():
        self.current_game = game_id
        self.addresses = ADDRESSES[game_id]
      if self.current_game is None and self.game_id_error != game_id and game_id != b'\x00\x00\x00\x00\x00\x00':
        self.logger.warning(
          f"Connected to the wrong game ({game_id})")
        self.game_id_error = game_id
    except RuntimeError:
      pass
    except ConnectionError:
      pass

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

  def get_current_map(self) -> int:
    return self._read32(self.addresses["map id"])

  def get_current_job(self) -> int:
    return self._read32(self.addresses["job id"])

  def set_current_job(self, job: int) -> None:
    self._write32(self.addresses["job id"], job)

  def set_items_received(self, n:int) -> None:
    self._write32(self.addresses["items received"], n)

  def to_episode_menu(self) -> None:
    self.logger.info("Skipping to episode menu")
    if (
      self.get_current_map() == 35 and
      self.get_current_job() == 1797
    ):
      self.set_current_job(0xffffffff)
      # self.set_items_received(0)

    self._reload(bytes.fromhex(MENU_RETURN_DATA))

  def unlock_episodes(self) -> None:
    self._write8(self.addresses["episode unlocks"], 8)

  def in_cutscene(self) -> bool:
    frame_counter = self._read16(self.addresses["frame counter"])
    return frame_counter > 10

  def skip_cutscene(self) -> None:
    pressing_x = self._read8(self.addresses["x pressed"]) == 255

    if self.in_cutscene() and pressing_x:
      self._write32(self.addresses["skip cutscene"],0)

  def load_powerups(self, powerups: PowerUps):
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

  def read_powerups(self):
    data = self._read_bytes(self.addresses["gadgets"], 8)
    bits = [
      bool(int(b))
      for byte in data
      for b in f"{byte:08b}"[::-1]
    ]

    relevant_bits = bits[2:48]
    return PowerUps(*relevant_bits)

  def add_coins(self, to_add: int):
    current_amount = self._read32(self.addresses["coins"])
    new_amount = max(current_amount + to_add,0)
    self._write32(self.addresses["coins"],new_amount)

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
  power_ups = PowerUps(True, True, True, False, *[True]*44)
  interf.load_powerups(power_ups)

  # Adding 10000 coins
  #interf.add_coins(10000)

  # === Testing Zone ===

 # print_thiefnet_addresses(interf)

  # disabling first job of episode 1 (0 = disabled, 1 = available, 2 = in progress, 3 = complete)
  # interf._write32(0x1335d10+0x44, 0)

  current_job_info(interf)
