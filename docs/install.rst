.. _install:

Install and Quickstart
======================


Install
-------

Using a virtual environment is recommended; Start by installing the *pinout* package. Either clone this repo and pip install it or install directly from github::
 
    pip install git+https://github.com/j0ono0/pinout@main

NOTE for package upgrading: pip upgrade doesn't work from git repos! Please install again if you want to try out the latest version (*warning*: new versions may not be backwards compatible).

.. _quickstart:

Quickstart
----------

.. image:: _static/finished_sample_diagram.*

You will need an image and stylesheet to complete this guide. Some sample files are included with the package and can be duplicated for your use. Launch Python REPL from a command-line in the folder you intend to work and enter the following::

    from pinout import resources
    resources.duplicate()

    # expected output:
    # >>> sample_diagram.py duplicated.
    # >>> sample_hardware_board.png duplicated.
    # >>> sample_styles.css duplicated.

*Spoiler Alert*: 'sample_diagram.py' is a completed script that duplicates the code in this guide. Running it will create a sample SVG pinout diagram - identical to the one pictured here - that can be viewed in your browser.

Once you have installed the *pinout* package explore its features in the :ref:`tutorial`.