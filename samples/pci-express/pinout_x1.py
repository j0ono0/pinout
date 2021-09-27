#####################################################
#
#
# This sample is a WORK IN PROGRESS!
#
# ...It should work but might be a bit
# rough around the edges.
#
#####################################################

from pinout.components.layout import Diagram, Panel
from pinout.core import Group, Image
from pinout.components.pinlabel import PinLabelGroup
from pinout import config

# Python has multiple options for reading popular spreadsheet formats.
# This example uses Pandas in conjunction with openpyxl.
# Installation of these packages can be done via the command line.
# (**If you are using a virtual environment, ensure it is activated):
# >>> pip install pandas
# >>> pip install openpyxl

# Export:
# >>> py -m pinout.manager -e pinout_x1 pinout_x1.svg

import data

# configuration customsations
config.pinlabel["body"]["corner_radius"] = 0
config.pinlabel["body"]["height"] = 28

diagram = Diagram(1200, 675, "diagram")
diagram.add_stylesheet("autostyles.css")
content = diagram.add(Panel(width=1200, height=675, tag="panel__content"))

graphic = content.add(Group(30, 10))
graphic.add(Image("pci-express_x1.svg", width=94, height=264, embed=True, scale=(2, 2)))
graphic.add(
    PinLabelGroup(
        x=80 * 2,
        y=64.5 * 2,
        pin_pitch=(0, 9 * 2),
        label_start=(100, -40),
        label_pitch=(0, 30),
        labels=data.get_from_xlsx("pci-express_data.xlsx")[0:11],
    )
)
graphic.add(
    PinLabelGroup(
        x=80 * 2,
        y=181 * 2,
        pin_pitch=(0, 9 * 2),
        label_start=(100, -181 * 2 + 64.5 * 2 + 30 * 10),
        label_pitch=(0, 30),
        labels=data.get_from_xlsx("pci-express_data.xlsx")[11:18],
    )
)
