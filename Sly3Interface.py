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
  attack = False
  binocucom = False
  bombs = False
  unknown = False
  trigger_Bomb = False
  fishing_pole = False

  alarm_clock = False
  adrenaline_burst = False
  health_extractor = False
  hover_pack = False
  insanity_strike = False
  grapple_cam = False
  size_destabilizer = False
  rage_bomb = False

  reduction_bomb = False
  ball_form = False
  berserker_charge = False
  juggernaut_throw = False
  guttural_roar = False
  fists_of_flame = False
  temporal_lock = False
  raging_inferno_flop = False

  diablo_fire_slam = False
  smoke_bomb = False
  combat_dodge = False
  paraglider = False
  silent_obliteration = False
  feral_pounce = False
  mega_jump = False
  knockout_dive = False

  shadow_power_1 = False
  thief_reflexes = False
  shadow_power_2 = False
  rocket_boots = False
  treasure_map = False
  shield = False
  venice_disguise = False
  photographer_disguise = False

  pirate_disguise = False
  spin_1 = False
  spin_2 = False
  spin_3 = False
  jump_1 = False
  jump_2 = False
  jump_3 = False
  push_1 = False

  push_2 = False
  push_3 = False

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

if __name__ == "__main__":
  interf = Sly3Interface(Logger("test"))
  interf.connect_to_game()

  byte_list = [
    [
      False,  # ???
      False,  # ???
      True,   # Sly/Bentley square attack
      True,   # Binocucom
      True,   # Bentley's bombs
      False,  # ???
      True,   # Trigger Bomb
      True    # Fishing Pole
    ],
    [
      True,   # Alarm Clock
      True,   # Adrenaline Burst
      True,   # Health Extractor
      True,   # Hover Pack (Doesn't activate until you reload)
      True,   # Insanity Strike
      True,   # Grapple Came
      True,   # Size Destabilizer
      True    # Rage Bomb
    ],
    [
      True,   # Reduction Bomb
      True,   # Ball Form
      True,   # Berskerker Charge
      True,   # Juggernaut Throw
      True,   # Gutteral Roar
      True,   # Fists of Flame
      True,   # Temporal Lock
      True    # Raging Inferno Flop
    ],
    [
      True,   # Diablo Fire Slam
      True,   # Smoke Bomb
      True,   # Combat Dodge
      True,   # Paraglider
      True,   # Silent Obliteration
      True,   # Feral Pounce
      True,   # Mega Jump
      True    # Knockout Dive
    ],
    [
      True,   # Shadow Power Lvl 1
      True,   # Thief Reflexes
      True,   # Shadow Power Lvl 2
      True,   # Rocket Boots
      True,   # Treasure Map
      False,  # ???
      True,   # Venice Disguise
      True    # Photographer Disguise
    ],
    [
      True,   # Pirate Disguise
      True,   # Spin Attack lvl 1
      True,   # Spin Attack lvl 2
      True,   # Spin Attack lvl 3
      True,   # Jump Attack lvl 1
      True,   # Jump Attack lvl 2
      True,   # Jump Attack lvl 3
      True    # Push Attack lvl 1
    ],
    [
      True,   # Push Attack lvl 1
      True,   # Push Attack lvl 1
      False,
      False,
      False,
      False,
      False,
      False
    ],
    [
      False,
      False,
      False,
      False,
      False,
      False,
      False,
      False
    ],
  ]

  # byte_list = [[False for _ in range(8)] for _ in range(8)]

  data = b''.join(
    int(''.join(str(int(i)) for i in byte[::-1]),2).to_bytes(1,"big")
    for byte in byte_list
  )

  interf._write_bytes(0x468DCC,data)

  # data = interf._read_bytes(0x468DCC, 8)
  # bits = [
  #     bool(int(b))
  #     for byte in data
  #     for b in f"{byte:08b}"[::-1]
  # ]

  # print(bits)

  interf._write32(0x468DDC, 10000)

  # thiefnet_values = list(range(9)) + list(range(10,))


  # def read_text(address: int):
  #   text = ""

  #   while True:
  #     character = interf._read_bytes(address,2)

  #     if character == b"\x00\x00":
  #       break

  #     text += character.decode("utf-16-le")

  #     address += 2

  #   return text

  # def find_string_id(_id: int):
  #   string_table_address = interf._read32(0x47A2D8)
  #   i = 0
  #   while True:
  #     string_id = interf._read32(string_table_address+i*8)
  #     if string_id == _id:
  #       return interf._read32(string_table_address+i*8+4)
  #     i += 1


  # print("      {")
  # for i in range(44):
  #   address = 0x343208+i*0x3c
  #   interf._write32(address,i+1)
  #   interf._write32(address+0xC,0)

  #   name_id = interf._read32(address+0x14)
  #   name_address = find_string_id(name_id)
  #   name_text = read_text(name_address)

  #   description_id = interf._read32(address+0x18)
  #   description_address = find_string_id(description_id)

  #   print(
  #     "        " +
  #     f"\"{name_text}\": "+
  #     f"({hex(name_address)},{hex(description_address)}),"
  #   )

  # print("      }")

  # string_table_address = interf._read32(0x47A2D8)
  # for i in range(10):
  #   print("----")
  #   string_id = interf._read32(string_table_address+i*8)
  #   print(string_id)
  #   string_address = interf._read32(string_table_address+i*8+4)
  #   print(hex(string_address))
  #   print(read_text(string_address))

  # print(interf._read32(0x6b4110+0x44))
  print(interf._read32(0x1365be0+0x44))
  print()
  print(interf._read32(0x1357f80+0x44))
  print(interf._read32(0x1350560+0x44))
  print(interf._read32(0x135aba0+0x44))
  print(interf._read32(0x36DB98))