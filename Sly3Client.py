from typing import Optional, Dict
import asyncio
import multiprocessing
import traceback

from .data import Items, Locations
from .data.Constants import EPISODES, CHALLENGES
from CommonClient import logger, server_loop, gui_enabled, get_base_parser
import Utils

from .Sly3Interface import Sly3Interface, Sly3Episode, PowerUps
from .Sly3Callbacks import init, update

# Load Universal Tracker
tracker_loaded: bool = False
try:
  from worlds.tracker.TrackerClient import (
    TrackerCommandProcessor as ClientCommandProcessor,
    TrackerGameContext as CommonContext,
    UT_VERSION
  )

  tracker_loaded = True
except ImportError:
  from CommonClient import ClientCommandProcessor, CommonContext

class Sly3CommandProcessor(ClientCommandProcessor): # type: ignore[misc]
  def _cmd_deathlink(self):
    """Toggle deathlink from client. Overrides default setting."""
    if isinstance(self.ctx, Sly3Context):
      self.ctx.death_link_enabled = not self.ctx.death_link_enabled
      Utils.async_start(
        self.ctx.update_death_link(
          self.ctx.death_link_enabled
        ),
        name="Update Deathlink"
      )
      message = f"Deathlink {'enabled' if self.ctx.death_link_enabled else 'disabled'}"
      logger.info(message)
      self.ctx.notification(message)

  def _cmd_menu(self):
    """Reload to the episode menu"""
    if isinstance(self.ctx, Sly3Context):
      self.ctx.game_interface.to_episode_menu()

  def _cmd_coins(self, amount: str):
    """Add coins to game."""
    if isinstance(self.ctx, Sly3Context):
      self.ctx.game_interface.add_coins(int(amount))

class Sly3Context(CommonContext): # type: ignore[misc]
  command_processor = Sly3CommandProcessor
  game_interface: Sly3Interface
  game = "Sly 3: Honor Among Thieves"
  items_handling = 0b111
  pcsx2_sync_task: Optional[asyncio.Task] = None
  is_connected_to_game: bool = False
  is_connected_to_server: bool = False
  slot_data: Optional[Dict[str, Utils.Any]] = None
  last_error_message: Optional[str] = None
  notification_queue: list[str] = []
  notification_timestamp: float = 0
  showing_notification: bool = False
  deathlink_timestamp: float = 0
  death_link_enabled = False
  queued_deaths: int = 0

  # Game state
  is_loading: bool = False
  in_safehouse: bool = False
  in_hub: bool = False
  current_map: Optional[int] = None
  current_job: Optional[int] = None

  # Items and checks
  inventory: Dict[int,int] = {l.code: 0 for l in Items.item_dict.values()}
  available_episodes: Dict[Sly3Episode,bool] = {e: False for e in Sly3Episode}
  thiefnet_items: Optional[list[str]] = None
  powerups: PowerUps = PowerUps()
  thiefnet_purchases: PowerUps = PowerUps()
  jobs_completed: list[list[list[bool]]] = [
      [[False for _ in chapter] for chapter in episode]
      for episode in EPISODES.values()
  ]
  challenges_completed: list[list[list[bool]]] = [
      [[False for _ in chapter] for chapter in episode]
      for episode in CHALLENGES.values()
  ]

  def __init__(self, server_address, password):
    super().__init__(server_address, password)
    self.version = [0,0,0]
    self.game_interface = Sly3Interface(logger)

  def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
    # TODO
    pass

  def make_gui(self):
    ui = super().make_gui()
    ui.base_title = f"Sly 3 Client v{'.'.join([str(i) for i in self.version])}"
    if tracker_loaded:
        ui.base_title += f" | Universal Tracker {UT_VERSION}"

    # AP version is added behind this automatically
    ui.base_title += " | Archipelago"
    return ui

  # async def server_auth(self, password_requested: bool = False) -> None:
  #   if password_requested and not self.password:
  #     await super(Sly3Context, self).server_auth(password_requested)
  #   await self.get_username()
  #   await self.send_connect()

  def on_package(self, cmd: str, args: dict):
    super().on_package(cmd, args)
    if cmd == "Connected":
      self.slot_data = args["slot_data"]

      if self.version[:2] != args["slot_data"]["world_version"][:2]:
        raise Exception(f"World generation version and client version don't match up. The world was generated with version {args["slot_data"]["world_version"]}, but the client is version {self.version}")

      self.thiefnet_purchases = PowerUps(*[
        Locations.location_dict[f"ThiefNet {i+1:02}"].code in self.checked_locations
        for i in range(24)
      ])

      # Set death link tag if it was requested in options
      if "death_link" in args["slot_data"]:
        self.death_link_enabled = bool(args["slot_data"]["death_link"])
        Utils.async_start(self.update_death_link(
          bool(args["slot_data"]["death_link"])
        ))

      Utils.async_start(self.send_msgs([{
        "cmd": "LocationScouts",
        "locations": [
          Locations.location_dict[location].code
          for location in Locations.location_groups["Purchase"]
        ]
      }]))

  def notification(self):
    # TODO
    pass

def update_connection_status(ctx: Sly3Context, status: bool):
  if ctx.is_connected_to_game == status:
    return

  if status:
    logger.info("Connected to Sly 3")
  else:
    logger.info("Unable to connect to the PCSX2 instance, attempting to reconnect...")

  ctx.is_connected_to_game = status

async def _handle_game_not_ready(ctx: Sly3Context):
  """If the game is not connected, this will attempt to retry connecting to the game."""
  if not ctx.exit_event.is_set():
    ctx.game_interface.connect_to_game()
  await asyncio.sleep(3)

async def _handle_game_ready(ctx: Sly3Context) -> None:
  current_map = ctx.game_interface.get_current_map()
  ctx.in_hub = ctx.game_interface.in_hub()
  ctx.current_job = ctx.game_interface.get_current_job()

  ctx.game_interface.skip_cutscene()

  if ctx.game_interface.is_loading():
    ctx.is_loading = True
    await asyncio.sleep(0.1)
    return
  elif ctx.is_loading:
    ctx.is_loading = False
    await asyncio.sleep(1)

  connected_to_server = (ctx.server is not None) and (ctx.slot is not None)

  new_connection = ctx.is_connected_to_server != connected_to_server
  if ctx.current_map != current_map or new_connection:
    ctx.current_map = current_map
    ctx.is_connected_to_server = connected_to_server
    await init(ctx)

  await update(ctx)

  if ctx.server:
    ctx.last_error_message = None
    if not ctx.slot:
      await asyncio.sleep(1)
      return

    await asyncio.sleep(0.1)
  else:
    message = "Waiting for player to connect to server"
    if ctx.last_error_message is not message:
      logger.info("Waiting for player to connect to server")
      ctx.last_error_message = message
    await asyncio.sleep(1)

async def pcsx2_sync_task(ctx: Sly3Context):
  logger.info("Starting Sly 3 Connector, attempting to connect to emulator...")
  ctx.game_interface.connect_to_game()
  while not ctx.exit_event.is_set():
    try:
      is_connected = ctx.game_interface.get_connection_state()
      update_connection_status(ctx, is_connected)
      game_started = ctx.game_interface.is_game_started()
      if is_connected and game_started:
        await _handle_game_ready(ctx)
      else:
        await _handle_game_not_ready(ctx)
    except ConnectionError:
      ctx.game_interface.disconnect_from_game()
    except Exception as e:
      if isinstance(e, RuntimeError):
        logger.error(str(e))
      else:
        logger.error(traceback.format_exc())
      await asyncio.sleep(3)
      continue

def launch_client():
  Utils.init_logging("Sly 3 Client")

  async def main(args):
    multiprocessing.freeze_support()
    logger.info("main")
    ctx = Sly3Context(args.connect, args.password)

    logger.info("Connecting to server...")
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

    # Runs Universal Tracker's internal generator
    if tracker_loaded:
        ctx.run_generator()
        ctx.tags.remove("Tracker")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    logger.info("Running game...")
    ctx.pcsx2_sync_task = asyncio.create_task(pcsx2_sync_task(ctx), name="PCSX2 Sync")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await ctx.shutdown()

    if ctx.pcsx2_sync_task:
      await asyncio.sleep(3)
      await ctx.pcsx2_sync_task

  import colorama

  colorama.init()


  parser = get_base_parser()
  args, _ = parser.parse_known_args()

  asyncio.run(main(args))
  colorama.deinit()

if __name__ == "__main__":
  launch_client()
