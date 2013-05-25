"""Input handling.  Process keys"""

#
# Imports
#
import libtcodpy as libtcod
from common import *
import player_actions as pa
import ui

#
# handle_inventory_input()
#
def handle_inventory_input(entity, key):
    """Process keys when viewing inventory.
    
    Arguments:
    entity - entity of the player pressing key
    key - key pressed.
    
    """
    inv_filter = ui.Screens.inv.action_filter
    
    if key.vk == libtcod.KEY_ESCAPE:
        if inv_filter is None:
            return [pa.action_hide_inventory]
        else:
            ui.Screens.inv.action_filter = None
    elif inv_filter is None:
    
        # Closure to simplify code
        def make_filter_inventory(filter):
            def filter_inventory(entity, map, args):
              ui.Screens.inv.action_filter = filter
              return False, InputType.INVENTORY_SCREEN, None
            return filter_inventory
            
        if key.c == ord('u'):
            return [make_filter_inventory("use")]
        elif key.c == ord('d'):
            return [make_filter_inventory("drop")]
        elif key.c == ord('t'):
            return [make_filter_inventory("throw")]
        elif key.c == ord('c'):
            return [make_filter_inventory("consume")]
        elif key.c == ord('e'):
            return [make_filter_inventory("equip")]
        elif key.c == ord('w'):
            return [make_filter_inventory("wear")]
        else:
            return [pa.action_none, InputType.INVENTORY_SCREEN, None]
    else:
        ch = ord(chr(key.c).upper()) if key.shift else key.c
        if ch in ui.Screens.inv.char_entity_map:
            target_entity = ui.Screens.inv.char_entity_map[ch]
            source_func = "action_" + inv_filter
            target_func = inv_filter + "_me"

            # If the entity has this attribute, then execute it
            if hasattr(target_entity, target_func) and hasattr(entity, source_func):
                def perform_action(entity, map, args):
                    # Get the method to run, then hide the screen
                    ui.Screens.inv.hide_and_deactivate()
                    
                    # Now run the class method
                    turn_taken = getattr(entity, source_func)(entity, target_entity, map)
                    return turn_taken, InputType.IMMEDIATE, None
                return [perform_action]
    
    # Default return code if no action is caught
    return [pa.action_none, InputType.INVENTORY_SCREEN, None]

#
# handle_input()
#
def handle_input(entity, input_type, delayed_action):
    """Wait for an input - a keypress or a mouse action, and process it.
    
    Arguments:
    input_type - one of the InputType enum.  Ie, the context that the input is processed in.
    delayed_action - in the case of non-immediate input_type, the action that should be returned to be performed.
    
    Returns:
    A list containing the action to perform and a zero-or-greater number of arguments for that action.
    
    TODO: toggles for control keys, eg shift.  Need to catch shift, ctrl, alt, etc and modify key input based on this.
    """
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # We currently ignore mouse events.
    event_type = libtcod.sys_wait_for_event(libtcod.EVENT_KEY_PRESS, key, mouse, True)
 
    # Do we want to toggle fullscreen?
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        return [pa.action_none, input_type, delayed_action]
    
    if input_type == InputType.IMMEDIATE:
        if key.vk == libtcod.KEY_ESCAPE:
            return [pa.action_exit] # exit program
        #
        # Movement actions
        #
        elif key.vk in (libtcod.KEY_UP, libtcod.KEY_KP8):
            return [pa.action_move, 0, -1]
        elif key.vk in (libtcod.KEY_DOWN, libtcod.KEY_KP2):
            return [pa.action_move, 0, 1]
        elif key.vk  in (libtcod.KEY_LEFT, libtcod.KEY_KP4):
            return [pa.action_move, -1, 0]
        elif key.vk  in (libtcod.KEY_RIGHT, libtcod.KEY_KP6):
            return [pa.action_move, 1, 0]
        elif key.vk == libtcod.KEY_KP7:
            return [pa.action_move, -1, -1]
        elif key.vk == libtcod.KEY_KP9:
            return [pa.action_move, 1, -1]
        elif key.vk == libtcod.KEY_KP3:
            return [pa.action_move, 1, 1]
        elif key.vk == libtcod.KEY_KP1:
            return [pa.action_move, -1, 1]
        #
        # World interaction actions
        #
        elif key.c == ord('c') and key.lctrl:
                return [pa.action_close]
        elif key.c == ord('o') and key.lctrl:
                return [pa.action_open]
        elif key.c == ord('g'):
                return [pa.action_get]
        #
        # Inventory actions
        #
        elif key.c == ord('i'):
                return [pa.action_show_inventory, None]
        elif key.c == ord('d'):
                return [pa.action_show_inventory, "drop"]
        elif key.c == ord('t'):
                return [pa.action_show_inventory, "throw"]
        elif key.c == ord('u'):
                return [pa.action_show_inventory, "use"]
        elif key.c == ord('c'):
                return [pa.action_show_inventory, "consume"]
        elif key.c == ord('w'):
                return [pa.action_show_inventory, "wear"]
        elif key.c == ord('e'):
                return [pa.action_show_inventory, "equip"]
    elif input_type == InputType.DIRECTIONAL:
        if key.vk == libtcod.KEY_ESCAPE:
            return [pa.action_cancel] # cancel a multi-stage action we are in the processing of performing
        elif key.vk in (libtcod.KEY_UP, libtcod.KEY_KP8):
            return [delayed_action, 0, -1]
        elif key.vk in (libtcod.KEY_DOWN, libtcod.KEY_KP2):
            return [delayed_action, 0, 1]
        elif key.vk  in (libtcod.KEY_LEFT, libtcod.KEY_KP4):
            return [delayed_action, -1, 0]
        elif key.vk  in (libtcod.KEY_RIGHT, libtcod.KEY_KP6):
            return [delayed_action, 1, 0]
        elif key.vk == libtcod.KEY_KP7:
            return [delayed_action, -1, -1]
        elif key.vk == libtcod.KEY_KP9:
            return [delayed_action, 1, -1]
        elif key.vk == libtcod.KEY_KP3:
            return [delayed_action, 1, 1]
        elif key.vk == libtcod.KEY_KP1:
            return [delayed_action, -1, 1]
        else:
            return [pa.action_none, input_type, delayed_action]
    elif input_type == InputType.INVENTORY_SCREEN:
        return handle_inventory_input(entity, key)
    
    # If we get here somehow, return the 'null' action.
    return [pa.action_none, input_type, None]
