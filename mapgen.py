import libtcodpy as libtcod
from tile import Tile, TileType
from inventory import Inventory

from entities.door import Door
from entities.window import Window

#
# functions to create tile types
#
def create_wall(x, y):
    tile = Tile()
    tile.type             = TileType.WALL
    tile.block_sight = True
    tile.block_move    = True
    tile.char             = ' '
    tile.fcolour        = libtcod.Color(96, 96, 96)
    tile.bcolour        = libtcod.Color(96, 96, 96)
    return tile

def create_desk(x, y):
    tile = Tile()
    tile.type             = TileType.DESK
    tile.block_sight = False
    tile.block_move    = True
    tile.char             = ' '
    tile.fcolour        = libtcod.Color(120, 120, 120)
    tile.bcolour        = libtcod.Color(120, 120, 120)
    return tile
    
def create_window(x, y):
    tile = Tile()
    tile.type             = TileType.WINDOW
    tile.block_sight = False
    tile.block_move    = True
    tile.char             = ' '
    tile.fcolour        = libtcod.Color(196, 196, 196)
    tile.bcolour        = libtcod.Color(96, 96, 96)
    tile.window         = Window(x, y)
    return tile

def create_door(x, y):
    tile = Tile()
    tile.type             = TileType.DOOR
    tile.block_sight = False
    tile.block_move    = False
    tile.char             = ' '
    tile.fcolour        = libtcod.Color(140, 140, 190)
    tile.bcolour        = libtcod.Color(140, 140, 190)
    tile.door             = Door(x, y)
    return tile
    
def create_light_grass(x, y):
    tile = Tile()
    tile.type             = TileType.GRASS
    tile.block_sight = False
    tile.block_move    = False
    tile.char             = ' '
    tile.fcolour        = libtcod.Color(0, 132, 0)
    tile.bcolour        = libtcod.Color(0, 132, 0)
    return tile

def create_dark_grass(x, y):
    tile = Tile()
    tile.type             = TileType.GRASS
    tile.block_sight = False
    tile.block_move    = False
    tile.char             = ' '
    tile.fcolour        = libtcod.Color(0, 108, 0)
    tile.bcolour        = libtcod.Color(0, 108, 0)
    return tile
    
def create_laminate_floor(x, y):
    tile = Tile()
    tile.type             = TileType.LAMINATE_FLOOR
    tile.block_sight = False
    tile.block_move    = False
    tile.char             = ' '
    tile.fcolour        = libtcod.Color(140, 140, 190)
    tile.bcolour        = libtcod.Color(140, 140, 190)
    return tile
