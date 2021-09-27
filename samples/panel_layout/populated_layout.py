#
# Example: Inserting content into 'panel_layout'
#
# export this sample via the command line:
# >>> py -m pinout.manager --export populated_layout output/populated_layout.svg
#

from pinout.components.text import TextBlock
from pinout.core import Rect
import panel_layout as layout

# pinout expects to see 'diagram' here when exporting
from panel_layout import diagram

# All of the content panels are now available for content to be added
layout.panel_banner.add(TextBlock(content="Banner", x=20, y=40))
layout.panel_main.add(TextBlock(content="Main", x=20, y=40))
layout.panel_detail_01.add(TextBlock(content="Detail 01", x=20, y=40))
layout.panel_detail_02.add(TextBlock(content="Detail 02", x=20, y=40))
layout.panel_detail_03.add(TextBlock(content="Detail 03", x=20, y=40))
layout.panel_footer.add(TextBlock(content="Footer", x=20, y=40))
