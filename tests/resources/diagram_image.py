# Build with:
# py -m pinout.manager -e diagram_image.py diagram_image.svg -o

from pinout.core import Image
from pinout.components.layout import Diagram


diagram = Diagram(800, 800, tag="pinout")

# PNG image
# ---------

# PNG def, linked
png_def_linked = diagram.add_def(Image("200x200.png"))

# PNG def, embedded
png_def_embedded = diagram.add_def(Image("200x200.png", embed=True))

# PNG linked
diagram.add(Image("200x200.png", x=0, y=0))

# PNG embedded
diagram.add(Image("200x200.png", x=200, y=0, embed=True))

# Referenced linked
diagram.add(Image(png_def_linked, x=400, y=0))

# Referenced embedded
diagram.add(Image(png_def_embedded, x=600, y=0))

# PNG linked, resized
diagram.add(Image("200x200.png", x=400, y=400, width=400, height=400))

# SVG image
# ---------


# SVG linked
diagram.add(Image("200x200.svg", x=0, y=200))

# SVG embedded
diagram.add(Image("200x200.svg", x=200, y=200, width=200, height=200, embed=True))

# Referenced linked
svg_def_linked = diagram.add_def(Image("200x200.svg"))
diagram.add(Image(svg_def_linked, x=400, y=200))

# Referenced embedded
svg_def_embedded = diagram.add_def(Image("200x200.svg", embed=True))
diagram.add(Image(svg_def_embedded, x=600, y=200))

# SVG linked rezised
diagram.add(Image("200x200.svg", x=0, y=400, width=400, height=400))
