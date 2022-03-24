# py -m pinout.manager --export diagram_dimensions.py diagram_dimensions.svg -o

from pinout.components import layout
from pinout.core import Rect, Circle, Path

diagram = layout.Diagram(100, 100, units="mm")
diagram.add_stylesheet("diagram_dimensions_styles.css", embed=False)
diagram.add_stylesheet("diagram_dimensions_custom_styles.css", embed=False)

diagram.add(layout.Panel(20, 20, inset=(5, 5, 5, 5)))

diagram.add(Rect(x=20, y=20, width=20, height=20, tag="blue"))
diagram.add(Circle(cx=30, cy=10, r=10, tag="red"))
diagram.add(Path(x=40, path_definition="M 0 0 l 20 0 l 0 20"))
