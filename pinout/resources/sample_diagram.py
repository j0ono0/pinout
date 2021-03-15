from pinout import diagram

# Create a new diagram
pinout_diagram = diagram.Diagram()
pinout_diagram.stylesheet = 'sample_styles.css'

# Define some label categories/tags and add a legend
label_categories = [
    # (name, tag(s), color),
    ('GPIO', 'gpio'),
    ('GPI', 'gpi'),
    ('Analog', 'analog'),
    ('PWM', 'pwm'),
    ('Power Management', 'pwr-mgt'),
]
pinout_diagram.add_legend(204, -190, 249, 'legend legend-labels', label_categories)

# Add an image
pinout_diagram.add_image(0, 0, 220, 300, 'sample_hardware_board.png')

# Set default values for labels
diagram.Label.default_width = 70
diagram.Label.default_height = 25
diagram.Label.default_gap = 5

# Add a pin and labels (the slow way)
leftpin = diagram.Pin(16, 105, 'left')

leftpin.add_label('#1', 'gpio', 60, 25, 60)
leftpin.add_label('A1', 'analog')
leftpin.add_label('PWM', 'pwm')

pinout_diagram.components.append(leftpin)

# Add a Pin and add Labels (the fast way)
label_data = [('#2', 'gpio',60, 25, 60),('GPI', 'gpi')]  
pinout_diagram.add_pin(16, 135, 'left', label_data)

# Add multiple pins and labels with some python-foo!
custom_specs = (60, 25, 60) 
pin_label_data = [
        [('Vss', 'pwr-mgt', 40, 20, 190)], 
        [('GND', 'pwr-mgt', 40, 20, 190)], 
        [('#6', 'gpi',*custom_specs),('A3', 'analog'),('CLK', 'gpi')], 
        [('#5', 'gpio',*custom_specs),('A2', 'analog')], 
    ]

y_offset = 105
x_offset = 204
pitch = 30

for i, label_data in enumerate(pin_label_data):
    y = y_offset + pitch * i
    pinout_diagram.add_pin(x_offset, y, 'right', label_data)

# Export the finished diagram
pinout_diagram.export('sample_diagram.svg', overwrite=True)