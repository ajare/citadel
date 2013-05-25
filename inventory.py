"""Inventory class.  Entities can have an inventory of items."""

#
# Imports
#
from common import *

#
# Inventory
#
class Inventory:
    """Inventory.  Holds a list of items (entities), up to a certain capacity."""
    
    #
    # __init__()
    #
    def __init__(self, max_capacity):
        """Initialise the inventory with a given capacity.
        
        Arguments:
        max_capacity - the maximum amount this inventory can hold, in game 'weight units'
        
        """
        if max_capacity < 0:
            raise LogicException("Inventory capacity cannot be negative!")

        self.cur_capacity = 0
        self.max_capacity = max_capacity
        self.items = []

    #
    # __iter__()
    #
    def __iter__(self):
        """Return an iterator for the inventory.  This will be invalidated if items are added or removed while it is in use."""
        return InventoryIterator(self)

    #
    # spare_capacity
    #
    @property
    def spare_capacity(self):
        """Gets the remaining amount of capacity (in game weight units) that this inventory can hold."""
        return self.max_capacity - cur_capacity

    #
    # increase_capacity()
    #
    def increase_capacity(self, inc):
        """Increase capacity by a given amount.
        
        Arguments:
        inc - amount to increase by (in game weight units)
        
        """
        if inc <= 0:
            raise LogicException("Inventory capacity was increased by a negative amount!")
            
        self.max_capacity += inc
    
    #
    # add_item()
    #
    def add_item(self, item):
        """Add an item to the inventory.
        
        Arguments:
        item - item (entity) to add.
        
        TODO: check we have enough capacity!
        """
        self.items.append(item)
        
    #
    # remove_item()
    #
    def remove_item(self, item):
        """Remove an item from the inventory.
        
        Arguments:
        item - item (entity) to remove.
        
        """
        self.items.remove(item)
#
# InventoryIterator
#        
class InventoryIterator:
    """Simple iterator class to iterate over an inventory, returning items in order."""

    current = 0  # current index
    
    #
    # __init__()
    #
    def __init__(self, inv):
        """Initialise iterator with inventory.
        
        Arguments:
        inv - Inventory to iterate over.
        
        """
        self.inventory = inv

    #
    # next()
    #
    def next(self):
        """Required for an iterator.  Return next element in sequence."""
        if self.current >= len(self.inventory.items):
            raise StopIteration
        else:
            item = self.inventory.items[self.current]
            self.current += 1
            return item
