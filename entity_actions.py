"""Entity actions.  Attached to entities (and removed if necessary)."""

#
# Imports
#

#
# action_drop()
#
def action_drop(self, entity, map):
    """Drop an entity."""
    return entity.drop_me(self, map)

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
    entity = map.remove_entity_from_inventory(x, y)
    self.add_entity_to_inventory(entity)
    
    self.add_message("You pick up %s." % entity.def_name,
                     "%s picks up %s." % (self.def_name, entity.def_name))

    return True

#
# action_consume()
#
def action_consume(self, entity, map):
    """Consume an entity."""
    return entity.consume_me(self)
