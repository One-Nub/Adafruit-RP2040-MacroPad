## My Adafruit RP2040 Macropad Config

As the title conveys, this is my setup for my macropad.

Pretty strightforward, I'm utilizing the CircuitPython uf2 provided by 
Adafruit for the macropad, and pretty much everything else is put together by me.

- [macroapp.py](macroapp.py) consists of the underlying logic for my interface between writing
simple layers and having the code handle the stuff like layer switching.

- [code.py](code.py) contains the actual layers themselves, and is what runs the MacroApp.

- [light-toggling.py](light-toggling.py) is a fun file that I made before making the macro
system which just lets you toggle the neopixels on the board on and 
off with random colors, as well as toggling pixel brightness control
via the encoder.
