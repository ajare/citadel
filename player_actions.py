"""Actions that the player can perform."""

#
# Imports
#
from common import *

import ui
from tile import Tile, TileType

#
# Actions.    There are four types of action, and these are handled differently by the input handler.
#     Immediate
#         action is performed directly after key-press.    Eg: move
#     Directional
#         action requires a direction before it is performed.    Eg: open
#     Targeted
#         action requires a target tile before it is performed.    Eg: shoot
#     Menu
#         action requires an option to be chosen from a menu before it is performed.    Eg: drop
#

#
# ActionException
#
class ActionException(Exception):
    """Raised by actions."""
    pass
    
#
# action_exit()
#
def action_exit(entity, map, args):
    """Exits the game.  This is signalled by returning None for the first argument.
    
    Arguments:
    entity - entity performing the action.  Not used.
    map - map the action is being performed on.  Not used.
    args - additional arguments.
    
    Returns:
    tuple specifying: did the action do anything, new input mode, function for delayed execution.
    
    """
    return None, None, None

#
# action_none()
#
def action_none(entity, map, args):
    """Default 'null action'.
    
    Arguments:
    entity - entity performing the action.  Not used.
    map - map the action is being performed on.  Not used.
    args - additional arguments.  First argument is input_type, second is delayed_action.
    
    Returns:
    tuple specifying: did the action do anything, new input mode, function for delayed execution.
    
    """
    return False, args[0], args[1]

#
# Cancel the action you were about to do (in directional, targeted or menu mode)
#
def action_cancel(entity, map, args):
    """Cancel the action you were about to do (in directional or targeted mode).
    
    Arguments:
    entity - entity performing the action.  Not used.
    map - map the action is being performed on.  Not used.
    args - additional arguments.
    
    Returns:
    tuple specifying: did the action do anything, new input mode, function for delayed execution.
    
    """    
    entity.add_message("You decide not to continue with this plan.")
    return False, InputType.IMMEDIATE, None

#
# action_show_inventory()
#
def action_show_inventory(entity, map, args):
    """Displays an entity's inventory.
    
    Arguments:
    entity - entity performing the action.
    map - map the action is being performed on.  Not used.
    args - additional arguments.  First argument is filter to start with.
    
    Returns:
    tuple specifying: did the action do anything, new input mode, function for delayed execution.
    
    """
    ui.Screens.inv.show_and_activate(args[0])
    return False, InputType.INVENTORY_SCREEN, None

#
# action_hide_inventory()
#
def action_hide_inventory(entity, map, args):
    """Hides the inventory screen,
    
    Arguments:
    entity - entity performing the action.
    map - map the action is being performed on.  Not used.
    args - additional arguments.
    
    Returns:
    tuple specifying: did the action do anything, new input mode, function for delayed execution.
    
    """
    ui.Screens.inv.hide_and_deactivate()
    return False, InputType.IMMEDIATE, None

#
# action_move()
#
def action_move(entity, map, args):
    """Move an entity around a map.
    
    Arguments:
    entity - entity performing the action.
    map - map the action is being performed on.
    args - additional arguments.  Here it will be x-delta, y-delta
    
    Returns:
    tuple specifying: did the action do anything, new input mode, function for delayed execution.
    
    """
    tx = entity.x + args[0]
    ty = entity.y + args[1]
    
    tile = map.tiles[tx][ty]
    
    if tx >= 0 and tx < map.x_max and ty >= 0 and ty < map.y_max:
        # If we've moving diagonally, make sure we aren't cutting a corner,
        # or trying to squeeze through a gap
        if args[0] != 0 and args[1] != 0:
            t0 = map.tiles[entity.x][ty]
            t1 = map.tiles[tx][entity.y]
            if t0.blocks_movement or t1.blocks_movement:
                return False, InputType.IMMEDIATE, None
                
        # Check to see if we're moving into a closed door.
        # Windows must be explicitly opened.
        if tile.type == TileType.DOOR:
            if tile.door.closed:
                tile.door.action_open()
            elif not tile.blocks_movement:
                map.move_entity(entity, tx, ty, True)
            return True, InputType.IMMEDIATE, None
        elif not tile.blocks_movement:
            map.move_entity(entity, tx, ty, True)
            return True, InputType.IMMEDIATE, None

    return False, InputType.IMMEDIATE, None

#
# action_moveghost()
#
def action_moveghost(entity, map, args):
    """Move an entity around the map as a ghost, ie moving through walls.
    These entities do not live on the map, so we update them directly.
    
    Arguments:
    entity - entity performing the action.
    map - map the action is being performed on.  Not used.
    args - additional arguments.  Here it will be x-delta, y-delta
    
    Returns:
    tuple specifying: did the action do anything, new input mode, function for delayed execution.
    
    """
    tx = entity.x + args[0]
    ty = entity.y + args[1]
    
    if tx >= 0 and tx < map.x_max and ty >= 0 and ty < map.y_max:
        entity.x = tx
        entity.y = ty
        return True, InputType.IMMEDIATE, None
    else:
        return False, InputType.IMMEDIATE, None

#
# action_moveprobe()
#
def action_moveprobe(entity, map, args):
    """Move an entity around the map as a probe, ie allowing movement within a specified field of view
    
    Arguments:
    entity - entity performing the action.
    map - map the action is being performed on.  Not used.
    args - additional arguments.  Here, it will be x-delta, y-delta, fov_map
    
    Returns:
    tuple specifying: did the action do anything, new input mode, function for delayed execution.
    
    TODO: implement this!
    """
    tx = entity.x + args[0]
    ty = entity.y + args[1]
    fov_map = args[2]
    
    if tx >= 0 and tx < map.x_max and ty >= 0 and ty < map.y_max:
        entity.x = tx
        entity.y = ty
        return True, InputType.IMMEDIATE, None
    else:
        return False, InputType.IMMEDIATE, None
        
#
# action_get()
#
def action_get(entity, map, args):
    """Get an item from the world.  First of all, we check to see if there is
    anything on the entity's current tile.  If so, we try and pick this up.  If
    there is nothing, then we check neighbouring tiles.  If there is exactly one
    item, then pick that up.  If there are 2 or more, then ask which one to pick up.
    
    Arguments:
    entity - entity performing the action.
    map - map the action is being performed on.
    args - additional arguments.
 
    """
    tile = map.tiles[entity.x][entity.y]
    
    if tile.inventory:
        item_name = tile.inventory.def_name
        entity.action_get(entity, map, entity.x, entity.y)
        return True, InputType.IMMEDIATE, None
    else:
        gettables = []
        for y in range(entity.y - 1, entity.y + 2):
            for x in range(entity.x - 1, entity.x + 2):
                if x < 0 or x >= map.x_max or y < 0 or y >= map.y_max or (x == entity.x and y == entity.y):
                    continue
                
                tile = map.tiles[x][y]
                if tile.inventory:
                    gettables.append(tile.inventory)

        if len(gettables) == 0:
            ui.Screens.msg.add_message("There is nothing here for you to pick up.")
            return False, InputType.IMMEDIATE, None
        elif len(gettables) == 1:
            return entity.action_get(entity, map, gettables[0].x, gettables[0].y), InputType.IMMEDIATE, None
        else:
            ui.Screens.msg.add_message("Which direction to pick up in?")
        
            # Return a closure to execute after we've chosen the direction.
            # 'actor' and 'map' are required arguments, actor being the performer
            # of the action, not the object.
            # 'delta' is an array of arguments particular to the method.
            def action_get_item(actor, map, delta):
                
                tx = actor.x + delta[0]
                ty = actor.y + delta[1]
                tile = map.tiles[tx][ty]
                if tile.inventory:
                    actor.action_get(actor, map, tx, ty)
                else:
                    ui.Screens.msg.add_message("There is nothing there to pick up.")
                    
                return True, InputType.IMMEDIATE, None
            
            return False, InputType.DIRECTIONAL, action_get_item
    
#
# action_examine()
#
def action_examine(entity, map, args):
    """Examine a particular tile.  This shows what is on it."""
    def action_examine_tile(actor, map, delta):
        
        tile = map.tiles[entity.x + delta[0]][entity.y + delta[1]]
        if tile.type == TileType.DOOR:
            tile.door.action_open()
        elif tile.type == TileType.WINDOW:
            tile.window.action_open()
        elif tile.entity:
            tile.entity.action_open()
        else:
            ui.Screens.msg.add_message("There is nothing there to open.  %s" % DEBUG_MSG)
            
        return False, InputType.IMMEDIATE, None

    return False, InputType.TARGETED, action_examine_tile
    
#
# action_open()
#
def action_open(entity, map, args):
    """Try and open a nearby object.  First of all, we check neighbouring tiles.  If
    there is exactly one openable object, then try and open it.  If there are 2 or more, 
    then ask which one choose.  We do not try and open anything on the same tile that
    the entity is on.
    
    Arguments:
    entity - entity performing the action.
    map - map the action is being performed on.  Not used.
    args - additional arguments.
 
    """
    openables = []
    for y in range(entity.y - 1, entity.y + 2):
        for x in range(entity.x - 1, entity.x + 2):
            if x < 0 or x >= map.x_max or y < 0 or y >= map.y_max or (x == entity.x and y == entity.y):
                continue
            
            tile = map.tiles[x][y]
            
            # Check to see if there is a door or a window, or just an entity
            if tile.type == TileType.DOOR and tile.door.closed:
                    openables.append(tile.door)
            elif tile.type == TileType.WINDOW and tile.window.closed:
                openables.append(tile.window)
            elif tile.entity and hasattr(tile.entity, "action_open") and tile.entity.closed:
                openables.append(tile.entity)

    if len(openables) == 0:
        ui.Screens.msg.add_message("There is nothing here for you to open.")
        return False, InputType.IMMEDIATE, None
    elif len(openables) == 1:
        openables[0].action_open()
        return True, InputType.IMMEDIATE, None
    else:
        ui.Screens.msg.add_message("Which direction to open in?")
    
        # Return a closure to execute after we've chosen the direction.
        # 'actor' and 'map' are required arguments, actor being the performer
        # of the action, not the object.
        # 'delta' is an array of arguments particular to the method.
        def action_open_entity(actor, map, delta):
            
            tile = map.tiles[entity.x + delta[0]][entity.y + delta[1]]
            if tile.type == TileType.DOOR:
                tile.door.action_open()
            elif tile.type == TileType.WINDOW:
                tile.window.action_open()
            elif tile.entity:
                tile.entity.action_open()
            else:
                ui.Screens.msg.add_message("There is nothing there to open.  %s" % DEBUG_MSG)
                
            return True, InputType.IMMEDIATE, None
        
        return False, InputType.DIRECTIONAL, action_open_entity

#
# action_close()
#
def action_close(entity, map, args):
    """Try and close a nearby object.  First of all, we check neighbouring tiles.  If
    there is exactly one closeable object, then try and clos it.  If there are 2 or more, 
    then ask which one choose.  We do not try and close anything on the same tile that
    the entity is on.
    
    Arguments:
    entity - entity performing the action.
    map - map the action is being performed on.  Not used.
    args - additional arguments.
 
    """
    closeables = []
    for y in range(entity.y - 1, entity.y + 2):
        for x in range(entity.x - 1, entity.x + 2):
            if x < 0 or x >= map.x_max or y < 0 or y >= map.y_max or (x == entity.x and y == entity.y):
                continue
            
            tile = map.tiles[x][y]
            
            # Check to see if there is a door or a window, or just an entity
            if tile.type == TileType.DOOR and not tile.door.closed:
                    closeables.append(tile.door)
            elif tile.type == TileType.WINDOW and not tile.window.closed:
                closeables.append(tile.window)
            elif tile.entity and hasattr(tile.entity, "action_close") and not tile.entity.closed:
                closeables.append(tile.entity)

    if len(closeables) == 0:
        ui.Screens.msg.add_message("There is nothing here for you to close.")
        return False, InputType.IMMEDIATE, None
    elif len(closeables) == 1:
        closeables[0].action_close()
        return True, InputType.IMMEDIATE, None
    else:
        ui.Screens.msg.add_message("Which direction to close in?")
    
        # Return a closure to execute after we've chosen the direction.
        # 'actor' and 'map' are required arguments, actor being the performer
        # of the action, not the object.
        # 'delta' is an array of arguments particular to the method.
        def action_close_entity(actor, map, delta):
            
            tile = map.tiles[entity.x + delta[0]][entity.y + delta[1]]
            if tile.type == TileType.DOOR:
                tile.door.action_close()
            elif tile.type == TileType.WINDOW:
                tile.window.action_close()
            elif tile.entity:
                tile.entity.action_close()
            else:
                ui.Screens.msg.add_message("There is nothing there to close.  %s" % DEBUG_MSG)
                
            return True, InputType.IMMEDIATE, None
        
        return False, InputType.DIRECTIONAL, action_close_entity
