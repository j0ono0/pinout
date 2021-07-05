.. _Config:

Config
======

Components with a graphical representation have a variety of configuration attributes that affect their appearance. These attributes can be modified at several location whilst scripting.


Default values
--------------

These attributes are stored as Python dictionaries in the **config** module.  

A complete set of all default configurations can be duplicated for reference from the command line::

    py -m pinout.manager --duplicate config
    
    # expected response:
    # >>> config.py duplicated.

Amending the default configurations can be done by replacing or updating any of the dictionaries with plain Python::

    from pinout import config
    config.pinlabel["body"].update({"width": 120})

    # All pin-label bodies will now default to 120 wide


Instance attributes
-------------------

PinLabels and Annotations accept a dictionary of configurations for some attributes. These values are used to update the default settings for that single instance. This is ideal when small alterations are required for a low number items::

    from pinout.core import Diagram
    from pinout.components.pinlabel import PinLabel

    diagram = Diagram(1200, 675, "pinout")
    diagram.add(
        PinLabel(
            x=30,
            y=30,
            tag="sm-label",
            body={"width": 40},
        )
    )

