"""General entities which do not require their own file."""

#
# Imports
#
import libtcodpy as libtcod
from entity import *
from liquids import LiquidType

#
# MedKit
#
class MedKit(Entity):
    """MedKits restore a certain amount of health.
    
    TODO: maybe they could instead be containers holding various medecines, depending on how
    detailed we want to make health simulation.
    """
    
    #
    # __init__()
    #
    def __init__(self):
        """Create MedKit."""
        super(MedKit, self).__init__("medkit", EntityType.MEDECINE, '=', libtcod.white)
        self.blocks_move = False
        self.blocks_sight = False

#
# Pistol
#
class Pistol(Entity):
    """Test weapon."""
    
    #
    # __init__()
    #
    def __init__(self):
        """Create pistol."""
        super(Pistol, self).__init__("pistol", EntityType.WEAPON, '/', libtcod.white)
        self.blocks_move = False
        self.blocks_sight = False

#
# Power armour
#
class PowerArmour(Entity):
    """Test clothing."""
    
    #
    # __init__()
    #
    def __init__(self):
        """Create power armour."""
        super(PowerArmour, self).__init__("power armour", EntityType.CLOTHING, '#', libtcod.white)
        self.blocks_move = False
        self.blocks_sight = False

    #
    # wear_me()
    #
    def wear_me(self, wearer):
        """Put on the power armour, and start applying its effects."""
        ui.Screens.msg.add_message("You put on %s." % self.def_name)
        return True
        
#
# Soda can
#
class SodaCan(Entity):
    """Test comestible."""
    
    #
    # __init__()
    #
    def __init__(self):
        """Create soda can."""
        super(SodaCan, self).__init__("soda can", EntityType.COMESTIBLE, '^', libtcod.white)
        self.blocks_move = False
        self.blocks_sight = False
        self.liquid = LiquidType.SODA
        
    #
    # consume_me()
    #
    def consume_me(self, consumer):
        """Drink the soda.
        
        TODO: If we don't destroy it, we will have an empty can, which we can't drink.  Can we remove
        the consumeable property?  Or do we replace this entity with an empty can entity which can be filled
        up with something else?  We could make bottles into molotov cocktails, for instance.
        
        We also need a way to report messages.  If the entity is the player then should always report (in 2nd
        person).  If it is another entity in sight, then should report in 3rd person.
        """
        if self.liquid is None:
            self.add_message("You cannot drink this.  The can is empty!")
            return False
        
        # What are we drinking?
        if self.liquid == LiquidType.WATER:
            ui.Screens.msg.add_message("The water refreshes you.")
        elif self.liquid == LiquidType.SODA:
            ui.Screens.msg.add_message("The soda refreshes you.")
        elif self.liquid == LiquidType.PETROLEUM:
            pass
        elif self.liquid == LiquidType.ALCOHOL:
            ui.Screens.msg.add_message("You feel slightly more intoxicated.")
        elif self.liquid == LiquidType.SULPHURIC_ACID:
            pass
        else:
            ui.Screens.msg.add_message("You drink the unknown liquid.  %s" % DEBUG_MSG,
                                       "%s drinks the unknown liquid.  %s" + (consumer.def_name, DEBUG_MSG))
        
        self.name = "empty soda can"
        self.liquid = None
        
        # Destroy self - an empty soda can is useless...or is it?
        # consumer.inventory.remove_item(self)
        return True

#
# Quantum analyser
#
class QuantumAnalyser(Entity):
    """Test unknown."""
    
    #
    # __init__()
    #
    def __init__(self):
        """Create quantum analyser."""
        super(QuantumAnalyser, self).__init__("quantum analyser", EntityType.OTHER, '?', libtcod.white)
        self.blocks_move = False
        self.blocks_sight = False
