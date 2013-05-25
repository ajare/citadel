SCREEN_WIDTH = 70
SCREEN_HEIGHT = 51

#
# UI settings
#
MAP_WINDOW = SCREEN_WIDTH - SCREEN_HEIGHT, 1, SCREEN_HEIGHT - 2, SCREEN_HEIGHT - 7
INVENTORY_WINDOW = MAP_WINDOW
MINIMAP_WINDOW = 1, 1, MAP_WINDOW[0] - 2, MAP_WINDOW[0] - 2
MSG_WINDOW = SCREEN_WIDTH - SCREEN_HEIGHT, SCREEN_HEIGHT - 5, SCREEN_HEIGHT, 5

#
# Program name
#
PROGRAM_NAME = "Citadel"

#
# Debug message
#
DEBUG_MSG = "[YOU SHOULD NOT BE SEEING THIS]"

# enum helper
def enum(**enums):
    return type('Enum', (), enums)

#
# Different types of input action.
#
InputType = enum(
    IMMEDIATE        = 0,
    DIRECTIONAL      = 1,
    TARGETED         = 2,
    # Specific screens
    INVENTORY_SCREEN = 3
)

#
# Exceptions
#
class LogicException(Exception):
    """Generic exception raised when something unexpectedly in the game logic."""
    pass