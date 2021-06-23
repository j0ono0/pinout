# Arduino pinout

The Arduino samples endeavour to maximise common components and styles across different diagrams. 
This has been done by converting multiple pinout scripts into a Python package with repeated resources grouped into a 'common' folder.
Consequently some aspects of the code deviate from the official docs:

+ Paths are relative to the package
+ The scripts must be run from the parent folder. 'build_samples.py' exports both samples.
+ Use of a preprocessing function to better seperate data and configuration

There are likely to be alternative ways to organise pinout to cater for mulitple related diagrams - use this example as a launching point for ideas rather than a best-practice example.