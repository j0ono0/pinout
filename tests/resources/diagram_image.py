from pinout.core import Image
from pinout.components.layout import Diagram


diagram = Diagram(800, 200, tag="pinout")

# Image def, linked
img_def_linked = diagram.add_def(Image("200x200.png"))

# Image def, embedded
img_def_embedded = diagram.add_def(Image("200x200.png", embed=True))

# Linked
diagram.add(Image("200x200.png", x=0, y=0))

# Embedded
diagram.add(Image("200x200.png", x=200, y=0, embed=True))

# Referenced linked
diagram.add(Image(img_def_linked, x=400, y=0))

# Referenced embedded
diagram.add(Image(img_def_embedded, x=600, y=0))
