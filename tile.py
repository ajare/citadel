"""Tile code"""

#
# Imports
#
import libtcodpy as libtcod
from common import *

#
# TileType
#
TileType = enum(
    UNKNOWN        = 0,
    WALL           = 1,
    DESK           = 2,
    WINDOW         = 3,
    DOOR           = 4,
    GRASS          = 5,
    LAMINATE_FLOOR = 6
)

#
# Tile
#
class Tile:
    """Tiles - part of the map."""
    
    #
    # __init__()
    #
    def __init__(self):
        """Constructor."""
        self.type        = TileType.UNKNOWN
        self.block_sight = False
        self.block_move  = False
        self.seen        = False
        self.char        = ' '
        self.fcolour     = libtcod.Color(255, 0, 255)
        self.bcolour     = libtcod.Color(255, 0, 255)
        self.inventory   = None
        self.entity      = None
        
    @property
    def blocks_movement(self):
        """Gets whether or not this tile blocks movement."""
        return self.door.blocks_move if self.type == TileType.DOOR else self.window.blocks_move if self.type == TileType.WINDOW else self.entity.blocks_move if self.entity else self.block_move

    @property
    def blocks_sight(self):
        """Gets whether or not this tile blocks sight."""
        return self.door.blocks_sight if self.type == TileType.DOOR else self.window.blocks_sight if self.type == TileType.WINDOW else self.entity.blocks_sight if self.entity else self.block_sight
        