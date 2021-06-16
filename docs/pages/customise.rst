Customisation
=============

Documentation conveys not just information about its subject but also the personality of the owner. In the context of product/electronics documentation this 'personality' may be of the hardware itself, the creator of the hardware, or company that creates/distributes/sells the hardware.

Many *pinout* components have facility for customisation and easy integration into a diagram.


Stylesheet
----------

The first stop for altering a diagram's appearance is to edit its stylesheet. Presentation styles are all controlled here. If you are coming with some knowlege of CSS for web, be aware SVG has some different names for rules!


Component config
----------------

Altering the geometry of default components can be done by changing, or providing new, config values. See the :ref:`Config` section for more details 

Building components
-------------------

It is possible to build new components and integrate them into *pinout*.

Existing components are split into parts to allow easier overriding. Where a universal change is desired this maybe the best approach - until a guide is written for this, reviewing the package code (hosted on `github <https://github.com/j0ono0/pinout>`_) is recommended.

Insertion of customised elements into some component instances is also possible and suitable where only small changes, or multiple variants, of a component are required in a single diagram.

**PinLabel** has 'leaderline' and 'body' attributes. These accept either a dictionary of values (see :ref:`Config`) or an instance that will be used in preference to the equivalent default component.

**Annotation** has 'leaderline', 'body', and 'target' atttributes that accept new component instances.

**An example**: The following code can be added to the quick_start script ('pinout_diagram.py') for quick and easy testing::

    # Import required modules and class at top of the script
    from pinout.components import pinlabel
    from pinout.core import Path

    # Create a new pin-label body class 
    # and override the render function
    class SkewLabelBody(pinlabel.Body):
        def render(self):
            skew = 3
            path_def = " ".join(
                [
                    f"M {self.x + skew} {self.y -self.height/2}",
                    f"l {self.width} 0",
                    f"l {-skew*2} {self.height}",
                    f"l {-self.width} 0" "Z",
                ]
            )
            body = Path(path_definition=path_def, tag="label__body")
            return body.render()


    # Insert the following before the export statement
    # Add an instance of the custom pin-label body to the diagram 
    diagram.add(
        pinlabel.PinLabel(
            content="SKEWED",
            x=50,
            y=50,
            body=SkewLabelBody(70, 0, 100, 30),
        )
    )
