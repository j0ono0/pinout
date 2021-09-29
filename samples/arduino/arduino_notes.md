# Arduino pinout

The Arduino samples endeavour to maximise common components and styles across different diagrams. 
This has been done by converting files into a Python package with repeated resources grouped into a 'common' folder.
Consequently some aspects of the code deviate from the official docs:

+ Paths are relative to the package
+ Use of a preprocessing function to better seperate data and configuration

There are likely to be alternative ways to organise pinout to cater for mulitple related diagrams - use this example as a launching point for ideas rather than a best-practice example.

Build Uno diagram, open command-line at the location of this file and enter:
```py -m pinout.manager --export arduino/uno/arduino_uno.py pinout_arduino_uno_rev3.svg -o```


Build RP2024 diagram, open command-line at the location of this file and enter:
```py -m pinout.manager --export arduino/rp2040/arduino_nano_rp2040_connect.py pinout_arduino_nano_rp2040_connect.svg -o```

