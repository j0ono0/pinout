.. _tutorial:

Tutorial
===============

This tutorial walks through the main features available in *pinout*. If you have not installed *pinout* already please read the :ref:`install` section. This tutorial duplicates code from *quick_start_pinout.py*. To access a copy of this file and other resources see :ref:`quickstart`.

.. figure:: /_static/quick_start_pinout_diagram.*

   The finished diagram from this tutorial.


Import modules
--------------
Start by importing pinout modules required to create the sample diagram. For this tutorial the diagram data has been stored in a separate file which is also imported here::

    from pinout.core import Diagram, Group, Rect, Image
    from pinout.components.pinlabel import PinLabelGroup, Label
    from pinout.components.type import TextBlock
    from pinout.components import leaderline as lline
    from pinout.components.legend import Legend
    
    import data


Diagram layout
-------------- 
Presenting a diagram with context and as a complete document assists with reader comprehension. Grouping components also helps with geometry calculations as components are added::

    # Create a new diagram and add a background
    diagram = Diagram(1024, 576, "diagram")
    diagram.add(Rect(0, 0, 1024, 576, "diagram__bg"))


    # Create a layout for diagram
    panel_main = diagram.add(Group(2, 2, "panel panel--main"))
    panel_main.add(Rect(0, 0, 1020, 438, "panel__bg"))

    info_panel = diagram.add(Group(x=2, y=442, tag="panel panel--info"))
    info_panel.add(Rect(0, 0, 1020, 132, tag="panel__bg"))

    # Create a group to hold the actual diagram components.
    graphic = panel_main.add(Group(400, 42))

Presentation styles
-------------------
Graphical styles that affect the appearance, but not geometric layout, are supplied via a cascading stylesheet. Note: the *path* attribute is relative to the stylesheet file if *embed* is set to False and relative to the Python script if *embed* is set to True::

    # Add a stylesheet
    diagram.add_stylesheet("styles.css", True)


Hardware image
--------------
A width and height must be supplied (*pinout* does no auto detect this dimensions). It is recommended to use images at a **1:1 ratio** to simplify calculating component locations. Optionally 'x' and 'y' attributes can be supplied to position the top-left of the images to more suitable coordinates. Note: the *path* attribute is relative to the image file if *embed* is set to False and relative to the Python script if *embed* is set to True::

    # Add and embed an image
    graphic.add(Image("hardware.png", width=220, height=260, embed=True))


Add a single pin-label
----------------------
In some instances adding pins individually might be appropriate. This pin is being added to the 'graphic' group so its (x,y) coordinates are relative to that group's origin. Also demonstrated on this pin are some customisations of the pin-label's body and leaderline::

    # Create a single pin label
    graphic.add(
        PinLabel(
            content="RESET",
            x=155,
            y=244,
            tag="pwr",
            body={"x": 117, "y": 30},
            leaderline={"direction": "vh"},
        )
    )

Add Multiple pin-labels 
-----------------------
Where pins are arranged in 'headers' (a line of evenly spaced pins) the PinLabelGroup class can be used to automate many of the geometry calculations required to place individual pin-labels. 

- **x, y**: Coordinates of the first pin in the header.
- **pin_pitch**: Distance between each pin of the header. (0, 30) steps 0px right and 30px down for each pin. *TIP*: (30, 0) creates a horizontal header.
- **label_start**: Offset of the first label from the first pin, note that negative x values here may produce unexpected results. pin-label groups should be flipped with scale instead (more explaination later).
- **label_pitch**: Distance between each row of labels.
- **labels**: Label data. See data.py for examples 

::
    
    # Create pinlabels on the right header
    graphic.add(
        PinLabelGroup(
            x=206,
            y=100,
            pin_pitch=(0, 30),
            label_start=(60, 0),
            label_pitch=(0, 0),
            labels=data.right_header,
        )
    )

Pin-label orientation
------------------------------
SVG format allows 'flipping' or 'mirroring' elements by scaling them with a negative value eg. `scale=(-1, 1)` flips a component around a vertical axis. _pinout_ makes use of this feature, a scale attribute can be supplied to components to flip their layout. This can take some getting use to but provides a concise method of control. The following pin-label groups are scaled to orient in the opposite direction.  
::

    # Create pinlabels on the left header
    graphic.add(
        PinLabelGroup(
            x=16,
            y=100,
            pin_pitch=(0, 30),
            label_start=(60, 0),
            label_pitch=(0, 0),
            scale=(-1, 1),
            labels=data.left_header,
        )
    )

    # Create pinlabels on the lower header
    graphic.add(
        PinLabelGroup(
            x=65,
            y=244,
            scale=(-1, 1),
            pin_pitch=(30, 0),
            label_start=(110, 30),
            label_pitch=(30, 30),
            labels=data.lower_header,
            leaderline=lline.Curved(direction="vh"),
        )
    )

Title block
-----------
Adding a title and supporting notes can help readers quickly place a diagram in context and summarise important points:: 

        # Create a title and a text-block
        title_block = info_panel.add(
            TextBlock(
                data.title,
                x=0,
                y=0,
                width=338,
                height=42,
                offset=(20, 33),
                line_height=18,
                tag="panel title_block",
            )
        )
        info_panel.add(
            TextBlock(
                data.description.split("\n"),
                x=0,
                y=title_block.y + title_block.height,
                width=title_block.width,
                height=info_panel.height - title_block.height,
                offset=(20, 18),
                line_height=18,
                tag="panel text_block",
            )
        )

Legend
------
Adding a legend is easy as a dedicated component exists in _pinout_. The component flows into multiple columns if a 'max_height' is supplied::

    # Create a legend
    legend = info_panel.add(
        Legend(
            data.legend,
            x=338,
            y=0,
            max_height=132,
        )
    )

Export the diagram
------------------
The final diagram can be exported as a graphic in SVG format and should match the finished diagram shown here. This format is excellent for high quality printing but still an effecient size for web-based usage::

    # Export final SVG diagram
    diagram.export("quick_start_pinout_diagram.svg", True)

    # expected output:
    # > 'quick_start_pinout_diagram.svg' exported successfully.

.. figure:: /_static/quick_start_pinout_diagram.*

    The finished diagram from this tutorial.

    
The most convenient method of viewing the newly exported SVG file is with your browser.
    
**Note on coodinates**: SVG format sets (0, 0) as top-left with increasing x and y values moving to the right and down respectively. Component placement in pinout is made from an arbitrary (0, 0) location. The final diagram size and boundaries are calculated on export ensuring all components are visible - ie negative coordinates do not risk being outside the final diagram boundaries.

In this tutorial all (x, y) coordinates are relative to the hardware images's top-left corner which is positioned at (0, 0).



Next steps
----------

This guide has glossed over many attribute and configuration definitions. Experimenting with changing values and re-exporting the diagram will quickly reveal their purpose. All function are documented in the :ref:`modules` section.

The default config.yaml file can be duplicated and makes a good resource of what attributes can be modified::

    py -m pinout.file_manager --duplicate config

Depending on you intended usage, linking (instead of embedding) the image might be desirable. Set `embed=False` when adding an image to achieve this outcome. *Note:* When linking, URLs are relative to the exported diagram file. When embedding these URLs are relative to the current working directory (the directory you run the script from).

**TIP:** Embedding the image allows the SVG display correctly in InkScape. This might be an appealing work-flow option for encorporating the diagram into other media.

A more feature-rich example are available in the samples folder of the `pinout github repository <https://github.com/j0ono0/pinout>`_.