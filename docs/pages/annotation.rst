Annotations
===========

.. currentmodule:: pinout.components.annotation

Annotation
----------

.. autoclass:: AnnotationLabel
    :show-inheritance:
    
    An alternative method to 'label' a diagram, suitable for highlighting hardware details.

    It is likely the body, leaderline, and target will all require customisation to best suit specific usages. Several methods of customisation are possible:
    
    **diagram-wide customisations**:
    
    - Over-ride dictionary settings in pinout.config.annotation
    - Over-ride default annotation body, leaderline, and target classes 
    
    **instance specific customisations**:

    - Supply a dictionary of arguments to body, content, leaderline, and target attributes. These override config.annotation settings
    - provide an alternative component instance to body, content, leaderline, and target attributes.

    :param content: [description]
    :type content: [type]
    :param body: [description], defaults to None
    :type body: [type], optional
    :param leaderline: [description], defaults to None
    :type leaderline: [type], optional
    :param target: [description], defaults to None
    :type target: [type], optional


Body
----
.. autoclass:: Body
    :show-inheritance:


Content
-------
.. autoclass:: Content
    :show-inheritance:
        
    Content can be provided as a string, list, dictionary, or component instance. Strings are presented as a single line. Entries of a list present as lines of text. If a dictionary is provided it updates the default config settings and expects the 'content' attribute to be a list.
    
    
Leaderline
----------

.. autoclass:: Leaderline
    :show-inheritance:

Target
------

.. autoclass:: Target
    :show-inheritance: