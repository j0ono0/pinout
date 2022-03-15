from pinout.components.layout import Diagram
from pinout.components.text import TextBlock

diagram = Diagram(800, 400, tag="diagram")
diagram.add_stylesheet("styles.css")
diagram.add(TextBlock("Pinout export test.", x=100, y=100))

# Build with:
# py -m pinout.manager -e diagram_export.py diagram_export.svg -o
