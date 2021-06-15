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

This guide makes use of a hardware image, stylesheet, data file, and a Python script. Sample files are included with the package and can be duplicated for your use. Open a command line (with enabled virtual environment if you are using one) in the location you plan to work and enter the following::

    py -m pinout.file_manager --duplicate quick_start

    # expected output:
    # >>> data.py duplicated.
    # >>> hardware.png duplicated.
    # >>> pinout_diagram.py duplicated.
    # >>> styles.css duplicated.

*Spoiler Alert*: 'pinout_diagram.py' is a completed script that duplicates the code in this guide. Running it will create a sample SVG pinout diagram - identical to the one pictured here - that can be viewed in your browser.

Once you have installed the *pinout* package explore its features in the :ref:`tutorial`.