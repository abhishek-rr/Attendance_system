"""
This module handles all the grid registration.

A Grid object is created multiple times - when the HTML containing the grid is rendered, and every time a the grid's
data needs to be retrieved. Since each of these times is an independent HTTP request, we need to somehow pass the
information of the grid's class. This is done with a *Grid ID*.

Each HTTP request *gets its own Grid instance*, we just pass the information of the Grid's *class* around. Since we can't
create a class just because we've received its name in an HTTP request (it's a *huge* security hole), we only create
classes that have been registered before. We also don't want to pass class names in HTTP requests, so we pass class IDs.
"""
__author__ = 'zmbq'

# This is the registration dictionary. Grids have to register, then they can be retrieved.
_grids = {}

def register_grid(gridcls):
    """
    Registers a Grid class in the registry.

    Calls ``gridcls.get_grid_id`` to get the class's ID.

    Args:
        gridcls: Class of Grid to registry
    """
    _grids[gridcls.get_grid_id()] = gridcls

def get_grid_class(id):
    """
    Returns a class for a given ID.

    Args:
        Grid ID
    Returns:
        The grid's class
    Raises:
        KeyError if the ID hasn't been registered
    """
    return _grids[id]