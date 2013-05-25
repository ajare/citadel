"""UI rendering methods."""

# UI needs a reworking, both in display and input, to make it simpler.
# We only have a certain number of UI screens, with defined positions, etc,
# so create a base screen class with 'visible' and 'order' attributes and
# then draw these each frame regardless of whether a turn is taken.
# For input, have an InputType for each, and deal with logic in a function,
# returning action_none



#
# Imports
#
import libtcodpy as libtcod
from common import *
from screen import Screen
from entity import EntityType
from tile import Tile, TileType

inventory_action = None

#
# Map screen
#
class MapScreen(Screen):
    """Screen to render map onto."""
    
    #
    # __init__()
    #
    def __init__(self, x_offset, y_offset, width, height):
        """Create map screen.
        
        Arguments:
        x_offset - absolute left location on screen
        y_offset - absolute top location on screen
        width - width of screen
        height - height of screen
        
        """
        super(MapScreen, self).__init__(x_offset, y_offset, width, height)

    #
    # render()
    #
    def render(self, map, view_centre, fov_entity):
        """Render map.
        
        Arguments:
        map - map to render
        view_centre - world location to centre map on when rendering
        fov_entity - entity to use for fov calculation
        
        """
        # Generate field of view map
        fov_map = map.generate_fov_map(fov_entity)
        
        # Calculate bounds for rendering
        half_xsize = int(self.width / 2)
        half_ysize = int(self.height / 2)
        
        x0 = view_centre[0] - half_xsize
        y0 = view_centre[1] - half_ysize
        x1 = view_centre[0] + half_xsize + 1
        y1 = view_centre[1] + half_ysize + 1
	
        for y in range(y0, y1):
            for x in range(x0, x1):
                
                tile = map.tiles[x][y]
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                
                # Calculate offset onto screen and render
                xt = self.x_offset + x - x0
                yt = self.y_offset + y - y0

                if not visible:
                    if tile.seen:
                        # 70% desaturation
                        greyscale = int(tile.bcolour.r * 0.3 + tile.bcolour.g * 0.59 + tile.bcolour.b * 0.11)
                        nonviscolour = libtcod.color_lerp(tile.bcolour, libtcod.Color(greyscale, greyscale, greyscale), 0.7)
                        libtcod.console_set_char_background(0, xt, yt, nonviscolour, libtcod.BKGND_SET)
                        libtcod.console_put_char(0, xt, yt, ' ', libtcod.BKGND_NONE)
                    else:
                        libtcod.console_set_char_background(0, xt, yt, libtcod.black, libtcod.BKGND_SET)
                        libtcod.console_put_char(0, xt, yt, ' ', libtcod.BKGND_NONE)
                else:
                    tile.seen = True
                    libtcod.console_set_char_background(0, xt, yt, tile.bcolour, libtcod.BKGND_SET)
                    
                    # Render entities in the world first
                    if tile.entity:
                        libtcod.console_set_default_foreground(0, tile.entity.colour)
                        libtcod.console_put_char(0, xt, yt, tile.entity.char, libtcod.BKGND_NONE)
                    elif tile.inventory:
                        libtcod.console_set_default_foreground(0, tile.inventory.colour)
                        libtcod.console_put_char(0, xt, yt, tile.inventory.char, libtcod.BKGND_NONE)
                    elif tile.type == TileType.DOOR:
                        libtcod.console_set_default_foreground(0, tile.door.colour)
                        libtcod.console_put_char(0, xt, yt, tile.door.char, libtcod.BKGND_NONE)
                    elif tile.type == TileType.WINDOW:
                        libtcod.console_set_default_foreground(0, tile.window.colour)
                        libtcod.console_put_char(0, xt, yt, tile.window.char, libtcod.BKGND_NONE)
                    elif not tile.blocks_movement:
                        libtcod.console_set_default_foreground(0, libtcod.black)
                        libtcod.console_put_char(0, xt, yt, '.', libtcod.BKGND_NONE)

#
# MessageScreebn
#
class MessageScreen(Screen):
    """Screen for showing game messages."""
    
    #
    # __init__()
    #
    def __init__(self, x_offset, y_offset, width, height):
        """Create message screen.
        
        Arguments:
        x_offset - absolute left location on screen
        y_offset - absolute top location on screen
        width - width of screen
        height - height of screen
        
        """
        super(MessageScreen, self).__init__(x_offset, y_offset, width, height)
        self.messages = []
                        
    #
    # add_message()
    #
    def add_message(self, msg):
        """Add a message to be shown.
        
        Arguments:
        msg - message
        
        """
        self.messages.append(msg)
        
    #
    # render()
    #
    def render(self):
        """Render message window.

        TODO: split messages which are too long to fit on one line!
        """
        msg_count = self.height - 1
        draw_msgs = self.messages[-msg_count:]
        
        lindex = cindex = cindex0 = len(draw_msgs) - 1
        for msg in reversed(draw_msgs):
            colour = 255 - (cindex0 - cindex) * 40
            libtcod.console_set_default_foreground(0, libtcod.Color(colour, colour, colour))
            
            # Pad message to fill the window so we overwrite any previous characters.
            libtcod.console_print(0, self.x_offset, self.y_offset + lindex, msg.ljust(self.width))
            cindex -= 1
            lindex -= 1

#
# InventoryScreen
#
class InventoryScreen(Screen):
    """Inventory screen for an entity."""
    
    #
    # __init__()
    #
    def __init__(self, x_offset, y_offset, width, height):
        """Create inventory screen.
        
        Arguments:
        x_offset - absolute left location on screen
        y_offset - absolute top location on screen
        width - width of screen
        height - height of screen
        
        """
        super(InventoryScreen, self).__init__(x_offset, y_offset, width, height)
        self.action_filter = None
        self.char_entity_map = {}
    
    #
    # show_and_activate()
    #
    def show_and_activate(self, filter):
        """We need to override this to reset the action filter.
        
        Arguments:
        filter - filter to start with.
        
        """
        super(InventoryScreen, self).show_and_activate()
        self.action_filter = filter
    
    #
    # render_inventory_types()
    #
    def render_types(self, inventory, x_offset, y_offset, type, name, char_list):
        """Helper method to render a set of items of a particular type from an inventory.
        
        Arguments:
        inventory - the inventory to render
        x_offset - screen x-location (absolute) to start at
        y_offset - screen y-location (absolute) to start at
        type - the EntityType of the inventory items to select
        name - the text header to display for this type
        char_list - the list of characters (subset of [A-Za-z]) to use for these entities.
        
        Returns:
        number of items rendered.
        
        """
        types = [elem for elem in inventory if elem.type == type]

        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print(0, x_offset, y_offset, name)
        
        # If there are none to display, then print '(none)' in grey
        if len(types) == 0:
            libtcod.console_set_default_foreground(0, libtcod.gray)
            libtcod.console_print(0, x_offset, y_offset + 2, "(none)")
            return 0
        else:
            index = 0
            for item in types:
                if self.action_filter:
                  func = self.action_filter.lower() + "_me"
                  if hasattr(item, func):
                      libtcod.console_set_default_foreground(0, libtcod.white)
                  else:
                      libtcod.console_set_default_foreground(0, libtcod.gray)
                      
                entity_char = char_list[index]
                item_string = "{0} {1}".format(entity_char, item.name)
                
                # Add char->entity mapping for lookup and print
                self.char_entity_map[ord(entity_char)] = item
                libtcod.console_print(0, x_offset, y_offset + 2 + index, item_string)
                index += 1
        
            return len(types)
                
    #
    # render()
    #
    def render(self, entity):
        """Renders an entity's inventory in the given window.
        
        Arguments:
        entity - the entity whose inventory you want to render
        
        """
        # Background
        libtcod.console_set_default_background(0, libtcod.black)
        libtcod.console_set_default_foreground(0, libtcod.black)
        libtcod.console_rect(0, self.x_offset, self.y_offset, self.width, self.height, True, libtcod.BKGND_SET)
        
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print(0, self.x_offset + 1, self.y_offset + 1, entity.name)
        
        if entity.inventory is None:
            libtcod.console_print(0, self.x_offset + 1, self.y_offset + 3, "This entity has no inventory.  %s" % DEBUG_MSG)
        else:
            char_list = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            
            # Draw actions text - highlight the selected one
            libtcod.console_set_color_control(libtcod.COLCTRL_1, libtcod.blue, libtcod.black)
            libtcod.console_set_color_control(libtcod.COLCTRL_2, libtcod.blue, libtcod.white)
            libtcod.console_set_color_control(libtcod.COLCTRL_3, libtcod.black, libtcod.white)

            action_text = "%cU%cse%c   %cD%crop%c   %cT%chrow%c   %cC%consume%c   %cE%cquip%c   %cW%cear%c"
            action_text_format = [libtcod.COLCTRL_1, libtcod.COLCTRL_STOP, libtcod.COLCTRL_STOP] * 6
            if self.action_filter is not None:
                index = ["use", "drop", "throw", "consume", "equip", "wear"].index(self.action_filter)
                action_text_format[index * 3 + 0] = libtcod.COLCTRL_2
                action_text_format[index * 3 + 1] = libtcod.COLCTRL_3
                          
            action_text = action_text % tuple(action_text_format)
            libtcod.console_print(0, self.x_offset + 1, self.y_offset + 3, action_text)
            
            # Set up screen offsets for rendering
            lcol = self.x_offset + 1
            rcol = self.x_offset + 25
            lrow = rrow = self.y_offset + 5
        
            # In the case of no items, render_types will return 0, but still render a line (none) - so we need to
            # take this line into account when adjusting offsets.
            char_index      = 0
            num_weapons     = self.render_types(entity.inventory, lcol, lrow, EntityType.WEAPON, "WEAPONS", char_list[char_index:])
            lrow           += max(1, num_weapons) + 3
            char_index     += num_weapons
            num_clothing    = self.render_types(entity.inventory, rcol, rrow, EntityType.CLOTHING, "CLOTHING", char_list[char_index:])
            rrow           += max(1, num_clothing) + 3
            char_index     += num_clothing
            num_comestibles = self.render_types(entity.inventory, lcol, lrow, EntityType.COMESTIBLE, "COMESTIBLES", char_list[char_index:])
            lrow           += max(1, num_comestibles) + 3
            char_index     += num_comestibles
            num_medecine    = self.render_types(entity.inventory, rcol, rrow, EntityType.MEDECINE, "MEDECINE", char_list[char_index:])
            rrow           += max(1, num_medecine) + 3
            char_index     += num_medecine
            num_other       = self.render_types(entity.inventory, lcol, lrow, EntityType.OTHER, "OTHER", char_list[char_index:])
                        
#
# Screens
#
class Screens:
    """This class holds screen instances for global access via class attributes."""
    
    map = None
    msg = None
    inv = None

#
# render_entity_info()
#
def render_entity_info(entity, map):
    """Render information for an entity to the UI.
    
    Arguments:
    entity - entity to render
    map - map the entity is in
    
    TODO: add entity stats, etc
    """
    pass

    
