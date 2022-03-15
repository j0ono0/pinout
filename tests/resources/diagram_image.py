# Build with:
# py -m pinout.manager -e diagram_image.py diagram_image.svg -o

from pinout.core import Image, Use
from pinout.components.layout import Diagram

diagram = Diagram(800, 800, tag="diagram")


# PNG image
# ---------

# PNG linked
img = diagram.add(Image("200x200.png", x=0, y=0))

# PNG linked, resized
diagram.add(Image("200x200.png", x=400, y=400, width=400, height=400))

# PNG embedded
diagram.add(Image("200x200.png", x=200, y=0, embed=True))


# PNG def, linked
png_def_linked = diagram.add_def(Image("200x200.png"))

# Referenced linked
useImg = diagram.add(Use(png_def_linked, x=400, y=0))

# PNG def, embedded
im = Image("200x200.png", embed=True, y=0, rotate=0)
png_def_embedded = diagram.add_def(im)

# Referenced embedded
diagram.add(Use(png_def_embedded, x=600, y=0, rotate=0))


# SVG image
# ---------

# SVG linked
diagram.add(Image("200x200.svg", x=0, y=200))

# SVG embedded
diagram.add(Image("200x200.svg", x=200, y=200, width=200, height=200, embed=True))

# SVG linked rezised
diagram.add(Image("200x200.svg", x=0, y=400, width=400, height=400))

# Referenced linked
svg_def_linked = diagram.add_def(Image("200x200.svg", embed=False))
diagram.add(Use(svg_def_linked, x=400, y=200))

# Referenced embedded
svg_def_embedded = diagram.add_def(Image("200x200.svg", embed=True))
diagram.add(Use(svg_def_embedded, x=600, y=200))
