from pinout import diagram

# Create a new diagram
pinout_diagram = diagram.Diagram()

# Add a stylesheet
pinout_diagram.add_stylesheet('get_started_styles.css', embed=True)

# Add an image
pinout_diagram.add_image(0, 0, 220, 260, 'get_started_board.png', embed=True)

# Define some label categories/tags and add a legend
label_categories = [
    # (name, tag(s), color),
    ('GPIO', 'gpio'),
    ('Analog', 'analog'),
    ('PWM', 'pwm'),
    ('Power Management', 'pwr'),
]
pinout_diagram.add_legend(-160, 310, 225, 'legend legend-labels', label_categories)

# Set default values for labels
diagram.Label.default_width = 70
diagram.Label.default_height = 25
diagram.Label.default_gap = 6
diagram.Label.default_cnr = 3

# Add a pin and labels (the slow way)
pin01 = diagram.Pin(16, 100, -50, 100)

pin01.add_label('1', 'gpio')
pin01.add_label('A1', 'analog')
pin01.add_label('PWM', 'pwm')

pinout_diagram.components.append(pin01)

# A Pin and its labels can be added in a single line
# Note: this pin's coordinates target the left-most pin on the lower header. 
label_data = [('AREF', 'pwr')]
pinout_diagram.add_pin(65, 244, -50, 280, label_data)

# Add multiple pins and labels grouped as a list of 'header' dicts.
pin_headers = [
    {
        # LHS header - lower half
        'pin_coords': (16, 130),
        'label_coords': (-50 ,130),
        'pitch': 30,
        'labels': [
            [('Vcc', 'pwr')], 
            [('2', 'gpio'),('A2', 'analog')],
        ]
    },{
        # RHS header
        'pin_coords': (204, 100),
        'label_coords': (270 ,100),
        'pitch': 30,
        'labels': [
            [('8', 'gpio'),('A3', 'analog')], 
            [('7', 'gpio'),('A3', 'analog'), ('PWM','pwm')],
            [('GND', 'pwr')],
        ]
    },{
        # Lower header - remaining 3 pins
        'pin_coords': (95, 244),
        'label_coords': (270 ,280),
        'pitch': 30,
        'labels': [
            [('4', 'gpio'),('ADC', 'analog')], 
            [('5', 'gpio'),('ADC', 'analog'), ('PWM','pwm')],
            [('6', 'gpio'),('PWM', 'pwm', 70, 25, 82)],
        ]
    }
]

for header in pin_headers:
    pinout_diagram.add_pin_header(header)

#######################################
"""
# Add a Pin and add Labels (the fast way)
pinout_diagram.add_pin(16, 135, 'left', label_data)

# Add multiple pins and labels with some python-foo!
custom_specs = (70, 25, 50)
pin_label_data = [
        [('Vss', 'pwr', 40, 20, 200)], 
        [('GND', 'pwr', 40, 20, 200)], 
        [('#6', 'gpi',*custom_specs),('A3', 'analog'),('CLK', 'gpi')], 
        [('#5', 'gpio',*custom_specs),('A2', 'analog')], 
    ]

y_offset = 105
x_offset = 204
pitch = 30

for i, label_data in enumerate(pin_label_data):
    y = y_offset + pitch * i
    pinout_diagram.add_pin(x_offset, y, 'right', label_data)
"""
# Export the finished diagram
pinout_diagram.export('get_started_diagram.svg', overwrite=True)