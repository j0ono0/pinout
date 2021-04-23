diagram
=======

add_stylesheet
--------------

Associate a stylesheet to the diagram. Multiple stylesheets can be added. If none are added one is automatically generated.

:param path: Path to the stylesheet file. *Note*: Where :code:`embed=False` the path is relative to the exported file. Where :code:`embed=True` the path is relative to the current working directory.
:type path: string
:param embed: Embed or link the stylesheet in the exported file, defaults to False
:type embed: bool, optional


add_image
---------
    
Associate a PNG, JPG or SVG formatted image to the diagram. *IMPORTANT*: Image width and height parameters must be supplied for the image to display! *pinout* does not auto-detect these attributes.

:param path: Path to the image file. *Note*: Where :code:`embed=False` the path is relative to the exported file. Where :code:`embed=True` the path is relative to the current working directory.
:type path: string
:param embed: Embed or link the image in the exported file, defaults to False
:type embed: bool, optional


add_legend
----------

Add a legend to the diagram. Content for the legend is provided via a config file
config = copy.deepcopy(self.cfg["legend"])
kwargs["config"] = self.patch_config(config, kwargs.get("legend", {}))
self.add_and_instantiate(Legend, categories, *args, **kwargs)


add_config
----------

Add configuration settings to the diagram. Parameters set in this fashion override the existing 'defaults' and referenced by components when parameters are not explicitly assigned.

A complete set of *pinout* defaults can be duplicated from the command line for reference::

    >>> py -m pinout.file_manager --duplicate config

:param path: Path to YAML formatted configuration file
:type path: str
    


add_annotation
--------------

    
generate_stylesheet
-------------------

Generate a stylesheet based on config settings and randomised (within set limits) values. Directly using this function is probably unnecessary. Diagrams with no associated stylesheet automatically call this function on export.

:param path: export path for stylesheet file
:type path: string
:param overwrite: Allow an existing file of the same name to be overwritten
:type overwrite: bool
    

export
------

Output the diagram in SVG format. If no stylesheet(s) are included one will be generated and exported automatically. See style_tools.default_css() for more details.

:param path: Name of svg file to be created, including export path.
:type path: str
:param overwrite: When set to False, this function aborts if the file already exists avoiding accidental overwriting. Defaults to False.
:type overwrite: bool, optional
