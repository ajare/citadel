"""Human entity definition."""

#
# Imports
#
import libtcodpy as libtcod
from entity import Entity
from inventory import Inventory

#
# Human
#
class Human(Entity):
    """Human entity."""
  
    #
    # __init__()
    #
    def __init__(self, name, gender, x, y, view_radius, inventory_size):
        """Create new human entity instance.
        
        Arguments:
        name - name of entity
        gender - either "Male" or "Female"
        x - x-position in world
        y - y-position in world
        view_radius - number of tiles they can see into the distance
        inventory_size - size of their inventory, in game weight units
        
        """
        super(Human, self).__init__(name, "Human", x, y, '@', libtcod.white)

        self.gender = gender
        self.view_radius = view_radius
        self.inventory = Inventory(inventory_size)

    #
    # __str__()
    #
    def __str__(self):
        """Overridden from base class to include gender and name."""
        return "{0} human named {1}".format(self.gender.lower(), self.name)
        
    #
    # action_get()
    #
    def action_get(self, map, x, y):
        """Pick pick an entity up.
        
        Arguments:
        map - map the action is being performed on.
        x - x-position in world to pick up from
        y - y-position in world to pick up from

        TODO: check inventory space
        """
        tile = map.tiles[x][y]
        item = tile.inventory
        item.x = -1
        item.y = -1
        self.inventory.add_item(item)
        tile.inventory = None
        
        self.add_message("You pick up %s." % item.def_name,
                         "%s picks up %s." % (self.def_name, item.def_name))

        return True

    #
    # action_drop()
    #
    def action_drop(self, entity, map):
        """Drop an entity."""
        return entity.drop_me(self, map)
    
    #
    # action_consume()
    #
    def action_consume(self, entity, map):
        """Consume an entity."""
        return entity.consume_me(self)