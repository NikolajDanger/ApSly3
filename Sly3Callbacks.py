from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .Sly3Client import Sly3Context

async def init(ctx: "Sly3Context", ap_connected: bool):
  """Called when the player connects to the AP server or changes map"""
  pass

async def update(ctx: "Sly3Context", ap_connected: bool):
  """Called continuously"""
  pass