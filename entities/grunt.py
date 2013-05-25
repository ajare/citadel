"""Basic enemy."""

#
# Imports
#
import random
import libtcodpy as libtcod
from human import Human

#
# Grunt
#
class Grunt(Human):
    """Basic, dumb enemy for target practise."""
    
    #
    # __init__()
    #
    def __init__(self):
        """Initialise entity, randomly assigning male or female.
        """
        super(Grunt, self).__init__("grunt", "male" if random.randint(0, 1) else "female", 10, 10)
        self.colour = libtcod.red
        
    #
    # turn()
    #
    def turn(self):
        pass
        