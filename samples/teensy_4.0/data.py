lline_84 = {"body": {"x": 80}, "tag": "lline--visible"}
lline_53 = {"body": {"x": 60}, "tag": "lline--visible"}
lline_40 = {"body": {"x": 40}, "tag": "lline--visible"}
lg_body = {"body": {"width": 170}}


# Pinlabels

header_rhs = [
    [("Vin", "pwr"), ("(3.6 to 5.5 volts)", "note", lg_body)],
    [("GND", "gnd")],
    [("3.3V", "pwr"), ("(250 mA max)", "note", lg_body)],
    [
        ("23", "digital"),
        ("A9", "analog"),
        ("PWM", "pwm"),
        ("CRX1", "canbus"),
        ("MCLK1", "audio"),
    ],
    [
        ("22", "digital"),
        ("A8", "analog"),
        ("PWM", "pwm"),
        ("CTX1", "canbus"),
        ("MCLK1", "audio"),
    ],
    [
        ("21", "digital"),
        ("A7", "analog"),
        ("RX5", "serial", lline_53),
        ("BCLK1", "audio"),
    ],
    [
        ("20", "digital"),
        ("A6", "analog"),
        ("TX5", "serial", lline_53),
        ("LRCLK1", "audio"),
    ],
    [("19", "digital"), ("A5", "analog"), ("PWM", "pwm"), ("SCL0", "i2c", lline_84)],
    [("18", "digital"), ("A4", "analog"), ("PWM", "pwm"), ("SDA0", "i2c", lline_84)],
    [("17", "digital"), ("A3", "analog"), ("TX4", "serial", lline_53), ("SDA1", "i2c")],
    [("16", "digital"), ("A2", "analog"), ("RX4", "serial", lline_53), ("SCL1", "i2c")],
    [
        ("15", "digital"),
        ("A1", "analog"),
        ("PWM", "pwm"),
        ("RX3", "serial"),
        ("DIF IN", "audio tight"),
    ],
    [
        ("14", "digital"),
        ("A0", "analog"),
        ("PWM", "pwm"),
        ("TX3", "serial"),
        ("DIF OUT", "audio tight"),
    ],
    [
        ("13", "digital"),
        ("PWM", "pwm", lline_40),
        ("CRX1", "canbus"),
        ("SCK", "spi"),
    ],
]

header_lhs = [
    [("GND", "gnd")],
    [("0", "digital"), ("PWM", "pwm"), ("RX1", "serial"), ("CRX2", "canbus")],
    [("1", "digital"), ("PWM", "pwm"), ("TX1", "serial"), ("CTX2", "canbus")],
    [("2", "digital"), ("PWM", "pwm"), ("OUT2", "audio", lline_84)],
    [("3", "digital"), ("PWM", "pwm"), ("LRCLK2", "audio", lline_84)],
    [("4", "digital"), ("PWM", "pwm"), ("BCLK2", "audio", lline_84)],
    [("5", "digital"), ("PWM", "pwm"), ("IN2", "audio", lline_84)],
    [("6", "digital"), ("PWM", "pwm"), ("OUT1D", "audio", lline_84)],
    [("7", "digital"), ("PWM", "pwm"), ("RX2", "serial"), ("OUT1A", "audio")],
    [("8", "digital"), ("PWM", "pwm"), ("TX2", "serial"), ("IN1", "audio")],
    [("9", "digital"), ("PWM", "pwm"), ("OUT1C", "audio", lline_84)],
    [("10", "digital"), ("PWM", "pwm"), ("CS", "spi"), ("MQSR", "audio")],
    [("11", "digital"), ("PWM", "pwm"), ("MOSI", "spi"), ("CTX1", "canbus")],
    [("12", "digital"), ("PWM", "pwm"), ("MISO", "spi"), ("MQSL", "audio")],
]


header_end_lhs = [
    [("VBat", "pwr")],
    [("3.3v", "pwr")],
    [("GND", "gnd")],
]
header_end_rhs = [
    [("Prog", "pwr")],
    [("On/Off", "gnd")],
]


# Legend
legend_digital = """<tspan class='legend__title'>Digital Pins</tspan>
digitalRead
digitalWrite
pinMode"""

legend_analog = """<tspan class='legend__title'>Analog Pins</tspan>
analogRead"""

legend_pwm = """<tspan class='legend__title'>PWM Pins</tspan>
analogWrite"""

legend_audio = """<tspan class='legend__title'>Digital Audio</tspan>
Audio library"""

legend_serial = """<tspan class='legend__title'>Serial Ports</tspan>
Serial1 - Serial7"""

legend_i2c = """<tspan class='legend__title'>I2C Port</tspan>
Wire library"""

legend_spi = """<tspan class='legend__title'>SPI Port</tspan>
SPI library"""

legend_canbus = """<tspan class='legend__title'>CAN Bus</tspan>
FlexCAN_t4 
library"""

legend_content = [
    (legend_digital, "digital"),
    (legend_analog, "analog"),
    (legend_pwm, "pwm"),
    (legend_audio, "audio"),
    (legend_serial, "serial"),
    (legend_i2c, "i2c"),
    (legend_spi, "spi"),
    (legend_canbus, "canbus"),
]

# Text

title = ["Teensy 4 pinout"]

title_2 = """32 Bit Arduino Compatible 
Microcontroller"""

instructions = """To begin please visit 'Getting Started' 
at <tspan class='url'>www.pjrc.com/teensy</tspan>"""

notes = """&#8226; All digital pins have interrupt capability.
&#8226; Loading status (Red LED): dim: Ready  |  bright: Writing  |  blink: No USB
&#8226; LED on pin-13"""