Text
====

.. currentmodule:: pinout.components.text

TextBlock
---------

.. autoclass:: TextBlock
    :show-inheritance:

    The TextBlock accepts either a string or list for content. Each list entry is presented as a line of text. Where a string is provided, it is converted to a list by splitting on new-line characters ('\\n') and stripping whitespace from start and end of each line created.

    .. note::
    
        *pinout* cannot detect text character size! Consequently care should be taken to ensure text does not render outside expected boundaries

    :param content: Text to be displayed
    :type content: String or List
    :param line_height: Distance between lines, defaults to None
    :type line_height: int, optional