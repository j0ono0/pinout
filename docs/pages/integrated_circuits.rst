Integrated circuits
===================

.. currentmodule:: pinout.components.integrated_circuits

*pinout* can generate simple integrated circuit (IC) graphics - Ideal for documenting stand-alone IC components. 

DIP and QFP components can be utilised in a diagram in the same way as an image. However helper functions also exists for easy application of labels to these component.


Labelled QFP graphic
--------------------

.. autofunction:: labelled_qfn
    
    :param labels: List of label data
    :type labels: list
    :param length: length of the IC sides (including legs), defaults to 160
    :type length: int, optional
    :param label_start: Offset of the first label from the first pin, defaults to (100, 20)
    :type label_start: tuple, optional
    :param label_pitch: Offest between each label row, defaults to (0, 30)
    :type label_pitch: tuple, optional
    :return: IC graphic with pinlabels applied
    :rtype: SVG markup


Labelled DIP graphic
--------------------

.. autofunction:: labelled_dip

    :param labels: List of label data
    :type labels: list
    :param width: Width of IC (includes legs), defaults to 100
    :type width: int, optional
    :param height: Height of IC (includes inset), defaults to 160
    :type height: int, optional
    :param label_start_x: Offset in x-axis of first label from first pin, defaults to 100
    :type label_start_x: int, optional
    :param label_pitch: Offest between each label row, defaults to (0, 30)
    :type label_pitch: tuple, optional
    :return: IC graphic with pinlabels applied
    :rtype: SVG markup


Dual in-line package (DIP)
--------------------------

.. autoclass:: DIP
    :show-inheritance:

    :param pin_count: Total number of pins on the integrated circuit
    :type pin_count: int
    :param width: width of the graphic, including body and legs
    :type width: int
    :param height: height of the graphic, including body and legs
    :type height: int

    Dimensions can be modified to depict a variety of IC types, eg SOIC and TSOP. 

    .. autoproperty:: pin_coords
    
    :param index: Pin number (starts at 1)
    :type index: int
    :param rotate: If true, includes component rotation in the calculation, defaults to True
    :type rotate: bool, optional
    :return: coordinates of the pin relative to the IC's origin
    :rtype: namedtuple (x,y)


Quad flat package (QFP)
-----------------------

.. autoclass:: QFP
    :show-inheritance:

    :param pin_count: Total number of pins on the integrated circuit
    :type pin_count: int
    :param length: length of the QFP sides
    :type length: int

    Dimensions can be modified to depict a variety of 'quad' IC types.

    .. autoproperty:: pin_coords
    
    :param index: Pin number (starts at 1)
    :type index: int
    :param rotate: If true, includes component rotation in the calculation, defaults to True
    :type rotate: bool, optional
    :return: coordinates of the pin relative to the IC's origin
    :rtype: namedtuple (x,y)