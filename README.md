# PinOut

A Python package that generates hardware pinout diagrams as SVG images. The package is designed to be quite flexible and works well for general 'pinning' labels to an image.

## How to use
Some demonstration code and notes are a quick way to get started. Browsing the source code is recommended in the absence of more detailed explaination. The guide here walks through creating a diagram, add an image and some labels. Then finally exporting the resulting SVG graphic. 

### Setup

Using a virtual environment is recommended; Start by installing the *PinOut* diagram package. Either clone this repo and pip install it or it can be installed directly from github...
```
pip install git+https://github.com/j0ono0/pinout@main
```

You will need an image and a stylesheet to complete this guide. Some sample files are included with the package and can be duplicated for your use. Launch Python at the location you intend to work and enter the following:
```python
from pinout import resources
resources.duplicate()

# expected output:
# >>> sample_diagram.py duplicated.
# >>> sample_hardware_board.png duplicated.
# >>> sample_styles.css duplicated.
```
<<<<<<< HEAD
*Spoiler Alert*: 'sample_diagram.py' is a completed script that duplicates the code in this guide.
=======
*Spoiler Alert*: 'sample_diagram.py' is a completed script that duplicates the code in this guide. Running it will create a sample SVG pinout diagram.
>>>>>>> 24ad4769d2034a6e55ca26a85c1c9d3aeb060fba

### Starting a pinout diagram

Start by importing the pinout diagram module
```python
from pinout import diagram
```

Create a new diagram and add a stylesheet.

```python
pinout_diagram = diagram.Diagram()
pinout_diagram.stylesheet = 'sample_styles.css'
```
### TIP: Component coordinates
On export the final diagram dimensions are calculated and all components shifted into view (via the SVG viewBox). Consequently, component 'x' and 'y' positioning is relative to each other and not the parent diagram. It is recommended to position your image to make easier calculations for subsequent pin placements.

### Define some label categories/tags and add a legend
Each tuple in the list becomes an entry on the legend. Use the same tags when defining labels. They become css classes that are used to style the labels.

Arguments - Diagram.add_legend(x, y, width, tags, items). Height is calculated depending on the number of items. 'x', 'y' and 'width' may require some trial-and-error for best alignment. The can be influenced by font choices in your stylesheet and consequently can't be automatically calculated during the render process.  
```python
items = [
    ('GPIO', 'gpio'),
    ('GPI', 'gpi'),
    ('Analog', 'analog'),
    ('PWM', 'pwm'),
    ('Power Management', 'pwr-mgt'),
]
pinout_diagram.add_legend(204, -190, 249, 'legend legend-labels', items)
```

### Add an image to the diagram
The image is linked in the final diagram (not embedded or copied to the export destination). If a relative path is used it must be relative to where the diagram is exported to.
```python
pinout_diagram.add_image(0, 0, 220, 300, 'sample_hardware_board.png')
```

### Create a pin 

This is slow way, included to provide an idea of the steps going on behind the scene.
```python
leftpin = diagram.Pin(16, 80, 'left')
```
Add some labels to the pin
Note: label width, height, and gap to next label, can be 
controlled per label and override default settings.
```python
leftpin.add_label('#1', 'gpio', 60, 20, 60)
leftpin.add_label('A1', 'analog')
leftpin.add_label('PWM', 'pwm')
```

Add this pin to the diagram
```python
pinout_diagram.components.append(leftpin)
```

### Create a Pin and Labels in a single action

The fast - and recommended - way.
```python
label_data = [('#2', 'gpio',60, 20, 60),('GPI', 'gpi')]  
pinout_diagram.add_pin(16, 120, 'left', label_data)
```

With a little 'python-foo' this process can be streamlined dramatically
```python
custom_specs = (60, 20, 60) 
pin_label_data = [
        [('Vss', 'pwr-mgt', 40, 20, 190)], 
        [('GND', 'pwr-mgt', 40, 20, 190)], 
        [('#6', 'gpi',*custom_specs),('A3', 'analog'),('CLK', 'gpi')], 
        [('#5', 'gpio',*custom_specs),('A2', 'analog')], 
    ]
```

Hardware headers have evenly spaced pins - which can be taken advantage of in a loop. These variables were determined by 
measuring pin locations on the image.
```python
y_offset = 80
x_offset = 204
pitch = 40

for i, label_data in enumerate(pin_label_data):
    y = y_offset + pitch * i
    pinout_diagram.add_pin(x_offset, y, 'right', label_data)
```

### Export the diagram
The final diagram can be exported as a graphic in SVG format. This vector format and excellent for high quality printing but still an effecient size for web-based usage. Note: the 'overwrite' argument is a safeguard to prevent unintentionally losing existing files. Set it to *True* for easier tinkering on a single SVG graphic.
```python
pinout_diagram.export('sample_diagram.svg', overwrite=False)

# expected output:
# > 'sample_diagram.svg' exported successfully.
```
