# pinout

Python package that generates hardware pinout diagrams as SVG images.

## How to use
Some demonstration code and notes are a quick way to get started. Browsing the source code is recommended in the absence of more detailed explaination. The text below walks through the code to create a diagram, add and image and some labels to it, then save the resulting SVG graphic to file. 

Note: Before you start find a hardware image to use as your base image (to replace 'board_huzzah32.png').

TODO: write better instructions and include a sample image.

Using a virtual environment is recommended; Start by installing the *pinout* diagram package. Either clone this repo and pip install it or it can be installed directly from github...
```
pip install git+https://github.com/j0ono0/pinout
```

Start by importing the pinout diagram module
```python
from pinout import diagram
```

Create a new diagram
'css_path' argument is relative to the templates folder
```python
pinout_diagram = diagram.Diagram('styles/pin_label_styles.css')
```

Add an image to the diagram
Note: the image is linked in the final diagram (not embedded or copied to the output folder). The path here is relative to where the diagram is saved.
```python
pinout_diagram.add_image(0, 0, 212, 475, '../board_huzzah32.png')
```

Create a pin (the slow way)
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

Create a Pin and add Labels in a single action (the fast way)
```python
label_data = [('LBL1', 'type-o',60, 20, 60),('LBL2', 'power-mgt'),('LBL3', 'type-io')]  
pinout_diagram.add_pin(212, 30, 'right', label_data)
```

Add multiple pins and labels with some python-foo!
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
Render the diagram as an SVG graphic and write to file
```python
with open('output/diagram2.svg','w') as f:
    f.write(
        pinout_diagram.as_svg()
    )
```