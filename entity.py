"""Base entity definition class."""

#
# Imports
#
import libtcodpy as libtcod
from common import *
import ui
from inventory import Inventory

#
# EntityType
#
EntityType = enum(
    WEAPON     = 0,
    CLOTHING   = 1,
    COMESTIBLE = 2,
    MEDECINE   = 3,
    OTHER      = 4
)

#
# ReportType
#
ReportType = enum(
    NONE        = 0,
    VISIBLE_NPC = 1,
    PLAYER      = 2
)

#
# Entity
#
class Entity(object):
    """Base entity.  Used for all entities, and only contains the most basic attributes."""

    #
    # __init__()
    #
    def __init__(self, name, type, char, colour):
        """Create a new entity.
        
        Arguments:
        name - the friendly name of the entity
        type - the basic type, used for internal categorisation (see EntityType)
        char - the printable character to use to render this entity
        colour - the colour to print the character in
        
        """
        self.name = name
        self.type = type
        self.x = -1
        self.y = -1
        self.char = char
        self.colour = colour
        self.blocks_move = True
        self.blocks_sight = False
        self.owner = None
        self.report = ReportType.NONE # don't print messages on actions

    #
    # indef_name
    #
    @property
    def indef_name(self):
        """Get the indefinite name, ie 'a'/'an' object."""
        if self.name.lower()[0] in ['a', 'e', 'i', 'o', 'u']:
            return "an " + self.name
        else:
            return "a " + self.name

    #
    # def_name
    #
    @property
    def def_name(self):
        """Get the definite name, ie 'the' object."""
        return "the " + self.name
    
    #
    # add_message()
    #
    def add_message(self, msg_player, msg_npc = None):
        """Add a message to be displayed.
        
        Arguments:
        msg_player - message to be displayed for player
        msg_npc - message to be displayed for NPC
        
        """
        if self.report == ReportType.NONE:
            return
        
        if self.report == ReportType.PLAYER and msg_player:
            ui.Screens.msg.add_message(msg_player)
        elif self.report == ReportType.VISIBLE_NPC and msg_npc:
            ui.Screens.msg.add_message(msg_npc)
        else:
            ui.Screens.msg.add_message("A message from the void!  " + DEBUG_MSG)
            
    #
    # drop_me()
    #
    def drop_me(self, dropper, map):
        """Entity is dropped on the ground.  All entities which can be picked up can be dropped.  If a character is very
        strong, they may be able to pick up anything.
        
        Arguments:
        dropper - the entity holding this entity
        map - the map that they're on.
        
        Returns:
        Whether or not a turn was taken.
        
        """
        tile = map.tiles[dropper.x][dropper.y]
        if tile.inventory:
            self.add_message("There is not enough space to drop %." + self.def_name)
            return False
        else:
            dropper.remove_entity_from_inventory(self)
            map.add_entity_as_inventory(dropper.x, dropper.y, self)

            dropper.add_message("You drop %s." % self.def_name, 
                                "%s drops %s." % (dropper.def_name, self.def_name))
            return True

    #
    # throw_me()
    #
    def throw_me(self, holder, map, tx, ty):
        """Entity is thrown at a target tile.  All entities which can be picked up can be thrown, although distance will vary.
        
        Arguments:
        holder - the entity holding this entity
        map - the map that they're on.
        tx - target x-position
        ty - target y-position
        
        """
        pass
