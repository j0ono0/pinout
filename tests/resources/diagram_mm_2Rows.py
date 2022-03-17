# Testing millimetre units with panel layout

#################################################

# From the command line:
# ----------------------

# Export diagram as SVG:
# >>> py -m pinout.manager -e diagram_mm_2Rows.py diagram_mm_2Rows.svg -o

from pinout.components import layout
from pinout import config_manager

config_manager.add_file("mm_config.py")

# A5 landscape dimensions
diagram = layout.Diagram_2Rows(210, 148, 74)

diagram.add_stylesheet("mm_styles.css", embed=False)
diagram.add_stylesheet("mm_dimensions.css", embed=False)
