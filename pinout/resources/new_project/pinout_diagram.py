####################################################

# Pinout project template
# =======================

# Docs: pinout.readthedocs.io
# Code and samples: https://github.com/j0ono0/pinout

####################################################

# *IMPORTANT*
# -----------
# 'py' is the Windows operation system command to invoke Python.
# Examples may need to be changed for you operating system.
# Eg. Use 'python' in place of 'py'.

# Export a diagram from a terminal:
# >>> py -m pinout.manager --export pinout_diagram.py pinout_diagram.svg -o


from pinout import config_manager
from pinout.components.layout import Diagram, Panel

# This file is a duplicate of default_config. Values that are deleted
# will fall back to the default_config.
config_manager.add_file("config.py")


diagram = Diagram(1024, 576)


# As components are added to the diagram they will require additional styling rules.
# New default rules can be automatically generated from the command line:
# >>> py -m pinout.manager --css pinout_diagram.py default_styles.css -o
diagram.add_stylesheet("default_styles.css")


# Tags on components become CSS classes. Add CSS styles that target them here.
# Colours change with each regeneration of default_styles. To retain rules
# copy them into this file to avoid the risk of being overwritten.
# diagram.add_stylesheet("styles.css")


panel = diagram.add(Panel(1024, 567, tag="diagram__bg"))
