"""Map - update and render the map."""

#
# Imports
#
import random
import libtcodpy as libtcod
from common import *
import ui
from tile import Tile, TileType

#
# Map
#
class Map:
    """Class to hold a single level of the game, and render and update it as appropriate."""

    #
    # __init__()
    #
    def __init__(self, level_func, seed = None):
        """Create a map with the given function.
        
        Arguments:
        level_func - function to generate the map
        seed - optional seed for the RNG
        
        """
        self.x_max = 0           # max x-dimension of map
        self.y_max = 0           # max y-dimension of map
        self.tiles = None        # jagged array of tiles
        self.entry_point = 0, 0  # starting point for this level
        self.entities = []       # entities in this level, used for updating

        if seed is not None:
            random.seed(seed)
            
        level_func(self)

    #
    # set_size()
    #
    def set_size(self, x_max, y_max):
        """Set the map's size and allocate empty tiles.
        
        Arguments:
        x_max - max x-dimension of map
        y_max - max y-dimension of map
        
        """
        self.x_max = x_max
        self.y_max = y_max
	
        self.tiles = [[ Tile()            
            for y in range(y_max) ]
                for x in range(x_max) ]
         
    #
    # add_entity()
    #
    def add_entity(self, x, y, entity):
        """Add an entity.  This takes up the 'entity' attribute of a tile.  It is assumed the entity has
        a valid position, and this is used to determine which tile to place it on.  It does not do any bounds checking on map.
        
        Arguments:
        x - x-position in world to add to
        y - y-position in world to add to
        entity - the entity to add.
        
        """
        tile = self.tiles[x][y]
        if tile.entity is None:
            tile.entity = entity
            entity.owner = map
            entity.x = x
            entity.y = y
            self.entities.append(entity)
        else:
            raise LogicException("Entity placed on a tile where another entity already resides.")            

    #
    # add_entity_as_inventory()
    #
    def add_entity_as_inventory(self, x, y, entity):
        """Add an entity as 'inventory' to a tile.  Inventory entities are those which are small/can be picked up etc.
        This takes up the 'inventory' attribute of a tile.  It is assumed the item has a valid position, and this is
        used to determine which tile to place it on.  It does not do any bounds checking on map.
        
        Arguments:
        x - x-position in world to add to
        y - y-position in world to add to
        entity - the entity to add.
        
        TODO: allow multiple entities to be placed as inventory, and put a limit on the amount (ie give the tile and inventory).
        """
        tile = self.tiles[x][y]
        if tile.inventory is None:
            tile.inventory = entity
            entity.owner = map
            entity.x = x
            entity.y = y
            self.entities.append(entity)
        else:
            raise LogicException("Entity placed as inventory on a tile with full inventory.")            
        
    #
    # remove_entity_from_inventory()
    #
    def remove_entity_from_inventory(self, x, y):
        """Remove an entity as 'inventory' from a tile.

        Arguments:
        x - x-position in world to remove from.
        y - y-position in world to remove from.
        
        Returns:
        entity removed
        """
        tile = self.tiles[x][y]
        entity = tile.inventory
        
        if entity is None:
            raise LogicException("Tried to remove inventory from (%d,%d) but there was nothing there." % (x, y))

        entity.x = -1
        entity.y = -1
        entity.owner = None

        tile.inventory = None
        self.entities.remove(entity)
        return entity

    #
    # remove_entity_from_inventory()
    #
    def remove_entity(self, x, y):
        """Remove an entity from tile

        Arguments:
        x - x-position in world to remove from.
        y - y-position in world to remove from.

        Returns:
        entity removed
        """
        tile = map.tiles[x][y]
        entity = tile.entity
        
        if entity is None:
            raise LogicException("Tried to remove entity from (%d,%d) but there was nothing there." % (x, y))

        entity.x = -1
        entity.y = -1
        entity.owner = None

        tile.entity = None
        self.entities.remove(entity)
        return entity

    #
    # move_entity()
    #
    def move_entity(self, entity, x, y, is_player = False):
        """Move an entity to a new location on the map.  This overwrites any existing entity in the target tile.  It does
        not do any bounds checking on map.
        
        Arguments:
        entity - entity to move
        x - new x location
        y - new y location
        
        """
        old_tile = self.tiles[entity.x][entity.y]
        new_tile = self.tiles[x][y]
        
        old_tile.entity = None
        new_tile.entity = entity
        
        entity.x = x
        entity.y = y
        
        if is_player and new_tile.inventory:
          ui.Screens.msg.add_message("You see %s on the ground." % new_tile.inventory.indef_name)

    #
    # generate_fov_map()
    #
    def generate_fov_map(self, viewer):
        """Generates a map for libtcod to use, to determine what is visible and what is not.
      
        Arguments:
        viewer - the entity to use
      
        """
        fov_map = libtcod.map_new(self.x_max, self.y_max)
        
        for y in range(viewer.y - viewer.view_radius, viewer.y + viewer.view_radius + 1):
            for x in range(viewer.x - viewer.view_radius, viewer.x + viewer.view_radius + 1):
                if x >= 0 and x < self.x_max and y >= 0 and y < self.y_max:
                    libtcod.map_set_properties(fov_map, x, y, not self.tiles[x][y].blocks_sight, not self.tiles[x][y].blocks_movement)    
    
        # map, x, y, radius, light walls, algorithm
        libtcod.map_compute_fov(fov_map, viewer.x, viewer.y, viewer.view_radius, True, libtcod.FOV_BASIC)

        return fov_map
