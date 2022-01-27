
KiCad integration
=================

Overview kicad2pinout.

processes are largely identical for kicad version 5 and 6 (Hence the combined instructions). Where they differ both options will be presented. Please ensure you follow the correct instructions!


Before you start
----------------
Create a KiCad project! This project must include a PCB design which will be enhanced with additional pinout information.

Ensure *pinout* is installed and a Python virtual environment launched if you are using one. For more information regarding this step please refer to :ref:`Install and quickstart<install>` 

Optionally, duplicate the pinout config file. Some KiCad library settings can be customised from this file - Most usefully, the layer used by the library can be changed here::

    py -m pinout.manager -d config

Create a KiCad footprint Library
--------------------------------

*pinout* can generate its KiCad footprint library from the command line `py -m pinout.manager <destination folder> <config file> --version <kicad version 5 | 6>`. The version defaults to 6 if omitted. _config_ _file_ and _version_ are optional.  ::

    #Example: KiCad 6, saving into the current directory
    py -m pinout.manager --kicad_lib . 

    #Example: KiCad 6, saving into the current directory and referencing a config file
    py -m pinout.manager --kicad_lib . config.py

    #Example: KiCad 5, saving into the relative directory named 'lib'
    py -m pinout.manager --kicad_lib ./lib -v 5 

    # Expected output:
    # >>> pinout footprint library for KiCad created successfully.

A folder named *pinout.pretty* will now be present at the location referenced in the command. This folder can now be added as a footprint library in the KiCad project.

.. note::
    **KiCad 6**: Footprints are on *User.1* layer by default.

    **KiCad 5**: Footprints are on *Eco1.User* layer by default.

.. warning::
    KiCad 6 allows users assign an alias to layer names. Only use KiCad's default layer names when generating a pinout library. 

The pinout footprints are now accessible in KiCad and can be placed like any other component.


Add an origin
-------------

The hardware image used in a diagram must be aligned to KiCad's coordinate system for pinout to successfully align components. This can be done by placing an Origin footprint at a corrosponding location in KiCad.


Add pin-labels
--------------
1. Select the PinLabel footprint from the *Choose Footprint* dialogue.
2. Place the footprint at the pin location
3. Move the *Value* text to the desired label location
4. Edit the text value to reflect label content and styling.

Multiple labels can be documented for a single pin by adding additional `text {{tag}}` pairs to the *Value* field. For example this become a row of three labels::

    GPIO1 {{gpio}} ADC {{analog}} TOUCH {{touch}}

By editing the footprint two more fields, that are hidden by default, can be viewed and edited. The *Reference designator* documents the footprints purpose and can be altered without affecting pinout's functions. The additional field is used to document pin-label attributes. 

Currently only the pin-label leaderline attribute is supported. It can be changed to suit the desired layout and reflects start/end leaderline directions. Valid values are:

- **hh**: horizontal - horizontal
- **vh**: vertical - horizontal

Add an annotation
-----------------
Annotations can be added by the same method as pin-labels.
1. Select the Annotation footprint from the *Choose Footprint* dialogue.
2. Place the footprint at the location to be annotated
3. Move the *Value* text to the desired label location
4. Edit the text value to reflect label content and styling.

Tagging the annotation is done with the same 'moustache' style tag `{{tag}}`. The tag text is applied to the final annotation as a css class. Further styling can then be applied via the CSS stylesheet.

By editing the annotation footprint other fields can be accessed and altered - with the same features and limitations - as the PinLabel footprint.

Add a textblock
---------------

A diagram is likely to require text content that is independent from the pinout diagram itself - for instance titles and explainatory notes. To assist with this *pinout* provides the facility to import 'Text items' from KiCad. This allows a better separation of layout and content and KiCad can be used as a single content source for a diagram.

KiCad's *Text item* tool is the ideal interface to authoring blocks of text. This tool cannot be used within a footprint but *pinout* collates all Text items that include a moustache-style tag in them. A dictionary is then returned for use within a pinout script. For example::

    # import kicad pcb data into pinout
    kdata = k2p.PinoutParser("kicad6_test.kicad_pcb", dpi=72)

    # Retrieve 'Text item' content from KiCad as a dictionary
    text = kdata.gr_text()

    # Use Text item content to populate a TextBlock 
    diagram.add(TextBlock(text["txt_tag_01"], tag="txt_tag_01", x=20, y=30))
