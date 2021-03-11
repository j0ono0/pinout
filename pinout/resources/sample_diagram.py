from pinout import diagram

# Create a new diagram
pinout_diagram = diagram.Diagram()
pinout_diagram.stylesheet = 'sample_styles.css'

# Add an image
pinout_diagram.add_image(0, 0, 220, 300, 'sample_hardware_board.png')


# add a pin and labels (the slow way)
leftpin = diagram.Pin(16, 80, 'left')

leftpin.add_label('#1', 'gpio', 60, 20, 60)
leftpin.add_label('A1', 'analog')
leftpin.add_label('PWM', 'pwm')

pinout_diagram.components.append(leftpin)


# Add a Pin and add Labels (the fast way)
label_data = [('#2', 'gpio',60, 20, 60),('GPI', 'gpi')]  
pinout_diagram.add_pin(16, 120, 'left', label_data)

# Add multiple pins and labels with some python-foo!
custom_specs = (60, 20, 60) 
pin_label_data = [
        [('Vss', 'pwr-mgt', 40, 20, 190)], 
        [('GND', 'pwr-mgt', 40, 20, 190)], 
        [('#6', 'gpi',*custom_specs),('A3', 'analog'),('CLK', 'gpi')], 
        [('#5', 'gpio',*custom_specs),('A2', 'analog')], 
    ]

y_offset = 80
x_offset = 204
pitch = 40

for i, label_data in enumerate(pin_label_data):
    y = y_offset + pitch * i
    pinout_diagram.add_pin(x_offset, y, 'right', label_data)


# Export the finished diagram
pinout_diagram.export('sample_diagram.svg', overwrite=True)