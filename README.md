# PinOut

A Python package that generates hardware pinout diagrams as SVG images. The package is designed to be quite flexible and works well for general 'pinning' labels to an image.

## How to use
Some demonstration code and notes are a quick way to get started. Browsing the source code is recommended in the absence of more detailed explaination. The guide here walks through creating a diagram, add an image and some labels. Then finally exporting the resulting SVG graphic. 

### Setup

Using a virtual environment is recommended; Start by installing the *PinOut* diagram package. Either clone this repo and pip install it or it can be installed directly from github...
```
pip install git+https://github.com/j0ono0/pinout@main
```

You will need an image and a stylesheet to complete this guide. Some sample files are included with the package and can be duplicated for your use. Launch Python at the location you intent to work and enter the following:
```python
from pinout import resources
resources.duplicate()

# expected output:
# >>> sample_diagram.py duplicated.
# >>> sample_hardware_board.png duplicated.
# >>> sample_styles.css duplicated.
```
*Spoiler Alert*: 'sample_diagram.py' is a completed script that duplicated the code in this guide.

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

### Add an image to the diagram
Note: the image is linked in the final diagram (not embedded or copied to the output folder). The path here is relative to where the diagram is saved.
```python
pinout_diagram.add_image(0, 0, 212, 475, 'board_huzzah32.png')
```

### Create a pin 

This is slow way, included to provide an idea of the steps going on behind the scene.
```python
leftpin = diagram.Pin(0, 110, 'left')
```
Add some labels to the pin
Note: label width, height, and gap to next label, can be 
controlled per label.
```python
leftpin.add_label('LEFT', 'type-o', 60, 20, 60)
leftpin.add_label('OUT', 'type-o')
leftpin.add_label('WAY', 'type-i')
```

Add this pin to the diagram
```python
pinout_diagram.components.append(leftpin)
```

### Create a Pin and Labels in a single action

The fast - and recommended - way.
```python
label_data = [('LBL1', 'type-o',60, 20, 60),('LBL2', 'power-mgt'),('LBL3', 'type-io')]  
pinout_diagram.add_pin(212, 30, 'right', label_data)
```

With a little 'python-foo' this process can be streamlined dramatically
```python
custom_specs = (60, 20, 60) 
pin_label_data = [
        [('OUT', 'type-o',*custom_specs),('IN', 'power-mgt'),('TEST', 'type-io')], 
        [('Vss', 'power-mgt',*custom_specs)], 
        [('SNSK', 'type-io',*custom_specs)], 
        [('SNS', 'type-o',*custom_specs)], 
        [('Vdd', 'power-mgt',*custom_specs)], 
        [], 
        [('SYNC', 'type-i',*custom_specs),('Vdd', 'power-mgt'),('SYNC', 'type-i')],
    ]
```

Hardware headers have evenly spaced pins - which can be taken advantage of in a loop. These variables were determined by 
measuring pin locations on the image.
```python
y_offset = 158
x_offset = 212
pitch = 23.6

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
