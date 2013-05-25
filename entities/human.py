"""Human entity definition."""

#
# Imports
#
import libtcodpy as libtcod
from entity import Entity, ReportType
from inventory import Inventory
import entity_actions as ea
        
#
# Human
#
class Human(Entity):
    """Human entity."""
  
    #
    # __init__()
    #
    def __init__(self, name, gender, view_radius, inventory_size):
        """Create new human entity instance.
        
        Arguments:
        name - name of entity
        gender - either "Male" or "Female"
        view_radius - number of tiles they can see into the distance
        inventory_size - size of their inventory, in game weight units
        
        """
        super(Human, self).__init__(name, "Human", '@', libtcod.white)

        self.gender = gender
        self.view_radius = view_radius
        self.inventory = Inventory(inventory_size)
        
        self.report = ReportType.VISIBLE_NPC
        
        # Add actions
        self.action_drop = ea.action_drop
        self.action_get = ea.action_get
        self.action_consume = ea.action_consume

    #
    # __str__()
    #
    def __str__(self):
        """Overridden from base class to include gender and name."""
        return "{0} human named {1}".format(self.gender.lower(), self.name)
        
    #
    # add_entity_to_inventory()
    #
    def add_entity_to_inventory(self, entity):
        """Helper method to add an entity to inventory.
        
        Arguments:
        entity - entity to add.
        """
        entity.x = -1
        entity.y = -1
        entity.owner = self
        self.inventory.add_item(entity)

    #
    # remove_entity_from_inventory()
    #
    def remove_entity_from_inventory(self, entity):
        """Helper method to remove an entity from inventory.
        
        Arguments:
        entity - entity to remove.
        """
        entity.owner = None
        self.inventory.remove_item(entity)
