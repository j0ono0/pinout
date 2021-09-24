from typing import Text
from pinout.components.layout import Diagram
from pinout.components.text import TextBlock

diagram = Diagram(800, 400, tag="pinout")
diagram.add_stylesheet("styles.css")
diagram.add(TextBlock("Pinout export test.", x=100, y=100))
