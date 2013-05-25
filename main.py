"""Entry-point for game."""

#
# Imports
#
import sys
import optparse
import libtcodpy as libtcod
from common import *
import input
import ui
import sim
import actions

from map import Map
from entity import Entity

# maps
import maps.ground_control

# entities
from entities.human import Human
from entities.general_entities import *

#
# process_command_line()
#
def process_command_line(argv):
    """
    Return a 2-tuple: (settings object, args list).
    
    Arguments:
    argv - list of arguments, or 'None' for "sys.argv[1:]".
    
    """
    if argv is None:
        argv = sys.argv[1:]

    # Initialize the parser object:
    parser = optparse.OptionParser(
        formatter = optparse.TitledHelpFormatter(width=78),
        add_help_option = None)

    # define options here:
    parser.add_option(      # customized description; put --help last
        '-h', '--help', action='help',
        help='Show this help message and exit.')

    settings, args = parser.parse_args(argv)

    # Check number of arguments, verify values, etc.
    if args:
        parser.error('program takes no command-line arguments: ' '"%s" ignored.' % (args,))

    # Further process settings & args if necessary
    return settings, args

#
# main()
#
def main(argv = None):
    """ Entry-point into program."""
    settings, args = process_command_line(argv)
    
    # Initialise libtcod
    libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, PROGRAM_NAME, False)
    libtcod.sys_set_fps(10)

    # Create a map and add starting entities.
    map = Map(maps.ground_control.level_1_raw)

    player = Human("Bob Smith", "male", map.entry_point[0], map.entry_point[1], 15, 30)
    player.report = ReportType.PLAYER
    map.add_entity(player)

    # Ghost is used to move around map for viewing
    ghost = Human("Ghost", "male", map.entry_point[0], map.entry_point[1], 15, 0)

    # Set up UI
    ui.Screens.map = ui.MapScreen(MAP_WINDOW[0], MAP_WINDOW[1], MAP_WINDOW[2], MAP_WINDOW[3])
    ui.Screens.msg = ui.MessageScreen(MSG_WINDOW[0], MSG_WINDOW[1], MSG_WINDOW[2], MSG_WINDOW[3])
    ui.Screens.inv = ui.InventoryScreen(INVENTORY_WINDOW[0], INVENTORY_WINDOW[1], INVENTORY_WINDOW[2], INVENTORY_WINDOW[3])
    
    ui.Screens.map.show_and_activate()
    ui.Screens.msg.show_and_activate()
    ui.Screens.inv.hide_and_deactivate()
        
    # Set up main game loop.
    # turn_taken - did the action actually take a turn - ie do we want to update the simulation now?  Initially true, to force a initial render.
    # input_type - what input state did the action leave us in?  Are we expecting the next input to be part of the current action?
    # delayed_action - if we are in the middle of a multi-stage action, this is the action (closure) to be performed at the end of it.
    turn_taken = True
    input_type = InputType.IMMEDIATE
    delayed_action = None
    
    current_turn = 1

    # main loop
    while not libtcod.console_is_window_closed():

        libtcod.console_clear(0)
        libtcod.console_set_default_foreground(0, libtcod.white)
    
        # set up render bounds
        centre_bounds = int(MAP_WINDOW[2] / 2), int(MAP_WINDOW[3] / 2), map.x_max - int(MAP_WINDOW[2] / 2) - 1, map.y_max - int(MAP_WINDOW[3] / 2) - 1
        
        # are we viewing the player or the ghost entity which acts as the automap viewer?
        view_centre = max(centre_bounds[0], min(player.x, centre_bounds[2])), max(centre_bounds[1], min(player.y, centre_bounds[3]))

        # Render screens
        if ui.Screens.map.show:
            ui.Screens.map.render(map, view_centre, player)
        if ui.Screens.msg.show:
            ui.Screens.msg.render()
        if ui.Screens.inv.show:
            ui.Screens.inv.render(player)
        
        ui.render_entity_info(player, map)
        
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print(0, 0, 0, "Turn: %d" % current_turn)

        # Blit to console
        libtcod.console_flush()
        
        # Process input
        player_action = input.handle_input(player, input_type, delayed_action)
        turn_taken, input_type, delayed_action = player_action[0](player, map, player_action[1:])

        if turn_taken:
            current_turn += 1
        
        # Quit the loop?
        if turn_taken is None:
            break
        
        # If we've done something, update world and render
        if turn_taken:
            sim.update_world()

    # Return peacefully
    return 0
    
#
# Execute in non-import mode.
#            
if __name__ == '__main__':
    status = main()
    sys.exit(status)