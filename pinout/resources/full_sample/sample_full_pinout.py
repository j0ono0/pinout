###########################################
#
# Example script to build a pinout diagram
#
###########################################

from pinout import diagram

# Create a new diagram
pinout_diagram = diagram.Diagram()

# Add a stylesheet
pinout_diagram.add_stylesheet('tutorial_pinout_styles.css', embed=True)

# Add a hardware image
pinout_diagram.add_image(0, 0, 220, 300, 'tutorial_pinout_hardware.png', embed=True)

# Set some default values for labels
diagram.Label.default_width = 70
diagram.Label.default_height = 26
diagram.Label.default_gap = 6
diagram.Label.default_cnr = 3

# Document pin and label data
pin_headers = [
    {
        # Bottom left
        'pin_coords': (65, 284),
        'label_coords': (-30 ,320),
        'pitch': 30,
        'labels': [
            [('3', 'gpio'),('A3', 'analog')], 
            [('4', 'gpio'), ('PWM','pwm', 70, 26, 76)],
        ]
    },{
        # Bottom right
        'pin_coords': (125, 284),
        'label_coords': (250, 320),
        'pitch': 30,
        'labels': [
            [('5', 'gpio'), ('A1', 'analog')], 
            [('3V3', 'pwr-mgt')],
        ]
    },{
        # Left
        'pin_coords': (15, 105),
        'label_coords': (-30, 105),
        'pitch': 30,
        'labels':[
            [('Vcc', 'pwr-mgt')], 
            [('RST', 'pwr-mgt')],  
            [('1', 'gpio'), ('CLK','comms'), ('PWM','pwm')], 
            [('2', 'gpio'),('A8', 'analog'), ('PWM','pwm')]
        ]
    },{
        # Right
        'pin_coords': (205, 105),
        'label_coords': (250, 105),
        'pitch': 30,
        'labels':[
            [('GND', 'pwr-mgt')], 
            [('8', 'gpio qqqq'),('DAC2', 'analog-out'), ('PWM','pwm')], 
            [('7', 'gpio'),('A1', 'analog'), ('MISO','comms')], 
            [('6', 'gpio'),('A2', 'analog'), ('MOSI','comms')],
        ]
    },{
        # Aux1
        'pin_coords': (46, 78),
        'label_coords': (-30, -20),
        'labels': [
            [('9', 'gpio'),('LED', 'led')],
        ]
    },{
        # Aux2
        'pin_coords': (62, 95),
        'label_coords': (-30, -50),
        'labels': [
            [('AREF', 'pwr-mgt')],
        ]
    },{
        # LED
        'pin_coords': (87, 85),
        'label_coords': (110, -50),
        'labels': [
            [('*LED', 'led')],
        ]
    }
]

# Alternative: Single Pins can be added via diagram.add_pin 
# pinout_diagram.add_pin(87, 85, 110, -50, [('LED', 'led')])

# Add data into pinout_diagram
for header in pin_headers:
    pinout_diagram.add_pin_header(header)

# Export the finished diagram
pinout_diagram.export('tutorial_pinout_diagram.svg', overwrite=True)