"""Base class for a screen."""

#
# Imports
#

#
# Screen
#
class Screen(object):
    """Base screen class.  Contains basic functionality for a screen."""
    
    #
    #  __init__()
    #
    def __init__(self, x_offset, y_offset, width, height):
        """Create screen.
        
        Arguments:
        x_offset - absolute left location on screen
        y_offset - absolute top location on screen
        width - width of screen
        height - height of screen
        
        """
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.active = False
        self.show = False
        self.order = 1
       
    #
    # show()
    #
    def show_and_activate(self, order = 1):
        """Sets the screen to be rendered and be the focus for input.
        
        Arguments:
        order - render order
        
        """
        self.show = True
        self.active = True
        self.order = order
        
    def hide_and_deactivate(self):
        """Sets the screen to be hidden and lose the input focus."""
        self.show = False
        self.active = False
    
