"""Define a map.  This is the first level of Ground Control."""

import random
import tile
import mapgen

import entities.general_entities as general_entities
import entities.grunt as enemies

# Ground Control.    This is the first part of the game.    The outline of the building is hard-coded, and each floor
# will have certain areas which are always in the same location/configuration, but other offices, rooms and ducts
# will have a degree of randomness to them.

#
# level_1_raw()
#
def level_1_raw(map):
    """Create level 1, loading the main structure from a RAW (image) file.
    
    Arguments:
    map - map instance to build.
    
    """
    map.set_size(80, 80)
    map.entry_point = 40, 76

    with open("maps/ground_control_1.raw", "rb") as f:
        bytes = f.read(80 * 80 * 3)

    index = 0
    for y in range(80):
        for x in range(80):
            r = ord(bytes[index + 0])
            g = ord(bytes[index + 1])
            b = ord(bytes[index + 2])
            index += 3
            
            if r == 0 and g == 255 and b == 0:
                map.tiles[x][y] = mapgen.create_light_grass(x, y) if random.randint(0, 10) < 5 else mapgen.create_dark_grass(x, y)
            elif r == 0 and g == 0 and b == 0:
                map.tiles[x][y] = mapgen.create_wall(x, y)
            elif r == 160 and g == 160 and b == 160:
                map.tiles[x][y] = mapgen.create_desk(x, y)
            elif r == 255 and g == 0 and b == 0:
                map.tiles[x][y] = mapgen.create_window(x, y)
            elif r == 255 and g == 255 and b == 0:
                map.tiles[x][y] = mapgen.create_door(x, y)
            elif r == 128 and g == 128 and b == 128:
                map.tiles[x][y] = mapgen.create_laminate_floor(x, y)

    # add entities
    map.add_entity_as_inventory(40, 73, general_entities.MedKit())
    map.add_entity_as_inventory(43, 72, general_entities.PowerArmour())
    map.add_entity_as_inventory(44, 73, general_entities.Pistol())
    map.add_entity_as_inventory(43, 70, general_entities.SodaCan())
    map.add_entity_as_inventory(42, 73, general_entities.QuantumAnalyser())
    map.add_entity_as_inventory(41, 71, general_entities.QuantumAnalyser())
    map.add_entity(41, 65, enemies.Grunt())
    map.add_entity(37, 62, enemies.Grunt())