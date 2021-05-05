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

.. image:: /_static/quick_start_diagram.*

This guide makes use of a hardware image, stylesheet, and configuration file. The latter two are optional but included to demonstrate features and ensure a consistent result. Sample files are included with the package and can be duplicated for your use. Open a command line in the location you plan to work and enter the following::

    py -m pinout.file_manager --duplicate quick_start

    # expected output:
    # >>> quick_start_config.yaml duplicated.
    # >>> quick_start_hardware.png duplicated.
    # >>> quick_start_pinout.py duplicated.

*Spoiler Alert*: 'quick_start_pinout.py' is a completed script that duplicates the code in this guide. Running it will create a sample SVG pinout diagram - identical to the one pictured here - that can be viewed in your browser.

Once you have installed the *pinout* package explore its features in the :ref:`tutorial`.