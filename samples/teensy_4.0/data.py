lg_lline = {"body": {"x": 92}}
lg_body = {"body": {"width": 166}}

# Pinlabels

header_rhs = [
    [("Vin (3.6 to 5.5 volts)", "pwr", lg_body)],
    [("GND", "gnd", lg_body)],
    [("3.3V (250 mA max)", "pwr", lg_body)],
    [
        ("23", "digital"),
        ("A9", "analog"),
        ("CRX1", "canbus"),
        ("MCLK1", "audio"),
        ("PWM", "pwm"),
    ],
    [
        ("22", "digital"),
        ("A8", "analog"),
        ("CTX1", "canbus"),
        ("MCLK1", "audio"),
        ("PWM", "pwm"),
    ],
    [("21", "digital"), ("A7", "analog"), ("RX5", "serial"), ("BCLK1", "audio")],
    [
        ("20", "digital"),
        ("A6", "analog"),
        ("TX5", "serial"),
        ("LRCLK1", "audio"),
    ],
    [("19", "digital"), ("A5", "analog"), ("SCL0", "i2c", lg_lline), ("PWM", "pwm")],
    [("18", "digital"), ("A4", "analog"), ("SDA0", "i2c", lg_lline), ("PWM", "pwm")],
    [("17", "digital"), ("A3", "analog"), ("TX4", "serial"), ("SDA1", "i2c")],
    [("16", "digital"), ("A2", "analog"), ("RX4", "serial"), ("SCL1", "i2c")],
    [
        ("15", "digital"),
        ("A1", "analog"),
        ("RX3", "serial"),
        ("S/PDIF IN", "audio"),
        ("PWM", "pwm"),
    ],
    [
        ("14", "digital"),
        ("A0", "analog"),
        ("TX3", "serial"),
        ("S/PDIF OUT", "audio"),
        ("PWM", "pwm"),
    ],
    [("13", "digital"), ("SCK", "spi"), ("CRX1", "canbus"), ("PWM", "pwm", lg_lline)],
]

header_lhs = [
    [("GND", "gnd", lg_body)],
    [("0", "digital"), ("RX1", "serial"), ("CRX2", "canbus"), ("PWM", "pwm")],
    [("1", "digital"), ("TX1", "serial"), ("CTX2", "canbus"), ("PWM", "pwm")],
    [("2", "digital"), ("OUT2", "audio", lg_lline), ("PWM", "pwm")],
    [("3", "digital"), ("LRCLK2", "audio", lg_lline), ("PWM", "pwm")],
    [("4", "digital"), ("BCLK2", "audio", lg_lline), ("PWM", "pwm")],
    [("5", "digital"), ("IN2", "audio", lg_lline), ("PWM", "pwm")],
    [("6", "digital"), ("OUT1D", "audio", lg_lline), ("PWM", "pwm")],
    [("7", "digital"), ("RX2", "serial"), ("OUT1A", "audio"), ("PWM", "pwm")],
    [("8", "digital"), ("TX2", "serial"), ("IN1", "audio"), ("PWM", "pwm")],
    [("9", "digital"), ("OUT1C", "audio", lg_lline), ("PWM", "pwm")],
    [("10", "digital"), ("CS", "spi"), ("MQSR", "audio"), ("PWM", "pwm")],
    [("11", "digital"), ("MOSI", "spi"), ("CTX1", "canbus"), ("PWM", "pwm")],
    [("12", "digital"), ("MISO", "spi"), ("MQSL", "audio"), ("PWM", "pwm")],
]


header_end_lhs = [
    [("VBat", "pwr")],
    [("3.3v", "pwr")],
    [("GND", "gnd")],
]
header_end_rhs = [
    [("Program", "pwr")],
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
Wire librarly"""

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

instructions = """To begin using Teensy please visit 
'Getting Started' at <tspan class='url'>www.pjrc.com/teensy</tspan>"""

notes = """&#8226; All digital pins have interrupt capability.
&#8226; Loading status (Red LED): dim: Ready  |  bright: Writing  |  blink: No USB
&#8226; LED on pin-13"""