Leaderlines
===========

.. currentmodule:: pinout.components.leaderline


Leaderline
----------
.. autoclass:: Leaderline
    :show-inheritance:

    :param direction: 2 letter code, defaults to "hh"
    :type direction: str, optional

    The leaderline connects an origin and destination point. Route taken is controlled with a *direction* argument where the first character dictates the start direction and the second character the end direction:

    - **vh**: vertical , horizontal
    - **hv**: horizontal , vertical
    - **hh**: horizontal , horizontal
    - **vv**: vertical , vertical


    .. automethod:: Leaderline.end_points

        The end_point method takes two components as arguments and returns coordinates that are  aligned with the centre coordinates of the relevant side.
        
        :param origin: origin component 
        :type origin: component with width and height attributes and bounding_coords method
        :param destination: destination component
        :type destination: component with width and height attributes and bounding_coords method
        :return: coordinates of start and end points
        :rtype: Tuple ((ox, oy), (dx, dy))

Curved
------
.. autoclass:: Curved
    :show-inheritance:


Angled
------
.. autoclass:: Angled
    :show-inheritance:


Straight
--------
.. autoclass:: Straight
    :show-inheritance:
