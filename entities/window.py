"""Door entity definition."""

#
# Imports
#
import libtcodpy as libtcod
import ui
from entity import *

#
# Window
#
class Window(Entity):
    """Window entity.  Can be opened/closed and smashed."""

    #
    # __init__()
    #
    def __init__(self, x, y):
        """Create window.
        
        Arguments:
        x - x-position in world
        y - y-position in world

        """
        super(Window, self).__init__("Window", EntityType.OTHER, x, y, libtcod.CHAR_CHECKBOX_UNSET, libtcod.white)

        # Start off closed.
        self.closed = True
        self.blocks_sight = False
        self.blocks_move = True
	
    #
    # action_open()
    #
    def action_open(self):
        """Try and open the window."""
        if not self.closed:
            ui.Screens.msg.add_message("This window is already open.")
            return

        self.closed = False
        self.blocks_move = False
        self.char = '*'
        ui.Screens.msg.add_message("You open the window.")
        
    #
    # action_close()
    #
    def action_close(self):
        """Try and close the window."""
        if self.closed:
            ui.Screens.msg.add_message("This window is already closed.")
            return

        self.closed = True
        self.blocks_move = True
        self.char = libtcod.CHAR_CHECKBOX_UNSET
        ui.Screens.msg.add_message("You close the window.")
