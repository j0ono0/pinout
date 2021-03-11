# PinOut

A Python package that generates hardware pinout diagrams as SVG images. The package is designed to be quite flexible and works well for general 'pinning' labels to an image.

## How to use
Some demonstration code and notes are a quick way to get started. Browsing the source code is recommended in the absence of more detailed explaination. The text below walks through the code to create a diagram, add and image and some labels to it, then save the resulting SVG graphic to file. 

Note: Before you start find a hardware image to use as your base image (to replace 'board_huzzah32.png').

TODO: write better instructions and include a sample image.

Using a virtual environment is recommended; Start by installing the *pinout* diagram package. Either clone this repo and pip install it or it can be installed directly from github...
```
pip install git+https://github.com/j0ono0/pinout@main
```
### Starting a pinout diagram

Start by importing the pinout diagram module
```python
from pinout import diagram
```

Create a new diagram
TODO: link styles to a user supplied style sheet rather than embed them.
```python
pinout_diagram = diagram.Diagram('styles/pin_label_styles.css')
```
### TIP: Component coordinates
On export the final diagram dimensions are calculated and all components shifted into view (via the SVG viewBox). Consequently, component 'x' and 'y' positioning is relative to each other and not the parent diagram. It is recommended to position your image to make easier calculations for subsequent pin placements.

### Add an image to the diagram
Note: the image is linked in the final diagram (not embedded or copied to the output folder). The path here is relative to where the diagram is saved.
```python
pinout_diagram.add_image(0, 0, 212, 475, '../board_huzzah32.png')
```

### Create a pin (the slow way)
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

### Create a Pin and Labels in a single action (the fast way)
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
The final diagram can be exported as a graphic in SVG format. This vector format and excellent for high quality printing but still an effecient size for web-based usage.
```python
pinout_diagram.export('output/my_diagram.svg')
```
