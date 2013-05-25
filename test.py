
# define behaviours to be implemented by entities
# we need a standard set of behaviours/interactions, otherwise entities will have to hardcode interactions with other entities.
# these behaviours are essentially interfaces between entities

# eg, a behaviour would be: is_flammable
# if a gas has this behaviour (ie one gas entity, on one tile), it will implement a function thus:
# on_flammable(source, args)
# where source is the entity igniting it

# to take an example, let's say a tile has a flammable gas with density X, and the player lights a torch.
# the gas has is_flammable and the torch has is_onfire
# the torch entity is updated, and checks all entities on the tile to see if they have any interactions with it
# it finds the gas entity and calls gas.on_flammable(self, self.temperature)
# gas.on_flammable compares the temperature and its density, and decides whether to explode, and with what force.

# what about if an entity gets a new behaviour?
# if something plastic, which is not flammable, gets covered in oil, it may then melt when on fire whereas before
# it would not catch alight.  Or something hard may be frozen in liquid nitrogen and becomes easy to break.
# We don't need a super-detailed model for this sort of thing, but we could use materials
# for this instance.  May be best to just define a large range of interactions first to see, and then classify each
# entity with these.  Entity-entity interactions may also involve them getting new behaviours.

# is_flammable
# is_freezable
# is_openable
# is_pickupable
# is_organic
# is_robotic