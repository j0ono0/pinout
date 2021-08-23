.. _install:

Install and Quickstart
======================


Install
-------

Using a virtual environment is recommended; Start by installing the *pinout* package from PyPi::
 
    pip install pinout

    # Or upgrade to the latest version
    pip install --upgrade pinout


.. _quickstart:

Quickstart
----------

.. image:: /_static/quick_start_pinout_diagram.*

This guide makes use of a hardware image, stylesheet, data file, and a Python script. Sample files are included with the package and can be duplicated for your use. Open a command line (with enabled virtual environment if you are using one) in the location you plan to work and enter the following

.. note::
    Depending on your operating system the command to invoke Python may differ. This guide uses Windows default method. Exchanging 'py' for 'python' or similar may be required for examples to work on other systems.

::

    py -m pinout.manager --duplicate quick_start

    # expected output:
    # >>> data.py duplicated.
    # >>> hardware.png duplicated.
    # >>> pinout_diagram.py duplicated.
    # >>> styles.css duplicated.


Generating the final SVG graphic is done from the command line::

    py -m pinout.manager --export pinout_diagram diagram.svg

If everything is correctly configured the newly created file 'diagram.svg' can be viewed in a browser and should look identical to the diagram pictured here.

.. warning::
    **Not all SVG viewers are build equal!**
    *pinout* uses SVG format 'under-the-hood' and can also output diagrams in this format. SVG is well supported by modern browsers and applications that *specialize* in rendering SVG such as InkScape. If a *pinout* diagram displays unexpected results (eg. mis-aligned text) cross-check by viewing the diagram in an up-to-date browser (eg. Firefox or Chrome) as an initial trouble-shooting step.

Once you have installed the *pinout* package explore its main features in the :ref:`tutorial`.