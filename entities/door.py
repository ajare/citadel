"""Door entity definition."""

#
# Imports
#
import libtcodpy as libtcod
import ui
from entity import *

#
# Door
#
class Door(Entity):
    """Door entity.  Can be opened/closed and destroyed.  May be locked, or opened by some other means."""
    
    #
    # __init__()
    #
    def __init__(self):
        """Create door."""
        super(Door, self).__init__("Door", EntityType.OTHER, '+', libtcod.white)

        # Start off closed and unlocked.
        self.closed = True
        self.locked = False
        self.blocks_sight = True
        self.blocks_move = True
 
    #
    # action_open()
    #
    def action_open(self):
        """Try and open the door."""
        if not self.closed:
            ui.Screens.msg.add_message("This door is already open.")
            return

        self.closed = False
        self.blocks_sight = False
        self.blocks_move = False
        self.char = '.'
        ui.Screens.msg.add_message("You open the door.")
      
    #
    # action_close()
    #
    def action_close(self):
        """Try and close the door."""
        if self.closed:
            ui.Screens.msg.add_message("This door is already closed.")
            return

        self.closed = True
        self.blocks_sight = True
        self.blocks_move = True
        self.char = '+'
        ui.Screens.msg.add_message("You close the door.")
      
    #
    # action_lock()
    #
    def action_lock(self):
        """Try and lock the door."""
        if not self.closed:
            ui.Screens.msg.add_message("You cannot lock an open door.")
            return
      
        self.locked = True
        ui.Screens.msg.add_message("You lock the door.")
      
    #
    # action_unlock()
    #
    def action_unlock(self):
        """Try and unlock the door."""
        if not self.closed:
            ui.Screens.msg.add_message("You cannot unlock an open door.")
            return
      
        self.locked = False
        ui.Screens.msg.add_message("You unlock the door.")
