#
# Example: Inserting content into 'panel_layout'
#
# export this sample via the command line:
# >>> py -m pinout.manager --export populated_layout.py output/populated_layout.svg
#

from pinout.components.text import TextBlock

from pinout.components.layout import Diagram, Panel

# Create a blank diagram
diagram = Diagram(1200, 675, tag="panel_layout")

# 'auto_styles.css' was auto-generated and inserted here
# *AFTER* all components were added to this script.
# >>> py -m pinout.manager --css panel_layout styles.css
diagram.add_stylesheet("auto_styles.css")

# User defined styles can be added to the auto-generated
# file or included as an additional asset.
diagram.add_stylesheet("styles.css")

# Panel fills entire diagram.
# All other panels will be added to this one.
panel_00 = diagram.add(Panel(1200, 675, (2, 2, 2, 2)))

# Banner panel
panel_banner = panel_00.add(
    Panel(
        width=panel_00.inset_width,
        height=50,
        tag="panel--banner",
    )
)

# Main panel
panel_main = panel_00.add(
    Panel(
        width=panel_00.inset_width * 2 / 3,
        height=500,
        x=0,
        y=panel_banner.height,
        tag="panel--main",
    )
)

# Detail panel
# This component is a wrapper for easier alignment
panel_details = panel_00.add(
    Panel(
        x=panel_main.width,
        y=panel_banner.height,
        width=panel_00.inset_width - panel_main.width,
        height=panel_main.height,
        inset=(0, 0, 0, 0),
        tag="panel--detail",
    )
)

# x3 'sub' panels
panel_detail_01 = panel_details.add(
    Panel(
        x=0,
        y=0,
        width=panel_details.width,
        height=panel_details.height / 3,
        tag="panel--detail",
    )
)
panel_detail_02 = panel_details.add(
    Panel(
        x=0,
        y=panel_detail_01.bounding_coords().y2,
        width=panel_details.width,
        height=panel_details.height / 3,
        tag="panel--detail",
    )
)

panel_detail_03 = panel_details.add(
    Panel(
        x=0,
        y=panel_detail_02.bounding_coords().y2,
        width=panel_details.width,
        height=panel_details.height / 3,
        tag="panel--detail",
    )
)

# Footer panel
panel_footer = panel_00.add(
    Panel(
        x=0,
        y=panel_main.bounding_coords().y2,
        width=panel_00.inset_width,
        height=panel_00.inset_height - panel_main.bounding_coords().y2,
        tag="panel--footer",
    )
)


# All of the content panels are now available for content to be added
panel_banner.add(TextBlock(content="Banner", x=20, y=40))
panel_main.add(TextBlock(content="Main", x=20, y=40))
panel_detail_01.add(TextBlock(content="Detail 01", x=20, y=40))
panel_detail_02.add(TextBlock(content="Detail 02", x=20, y=40))
panel_detail_03.add(TextBlock(content="Detail 03", x=20, y=40))
panel_footer.add(TextBlock(content="Footer", x=20, y=40))
