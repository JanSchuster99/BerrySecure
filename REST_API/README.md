# REST_API
## Scripts
- RNGRaspPi
  - Generates a desired amount of bitstreams with a given length, also handles the conversion between binary to hex
  - Packages used: pyaudio, struct, subprocess
- RNGRaspPiTests
  - Implements all the tests used to make sure the numbers generated are random
  - Packages used: numpy, threading, math, itertools
- app
  - Flask restful interface
  - Packages used: flask, flask_restful
- init
  - Implements the init method for the restful interface which turns on the Radio
  - Packages used: RPi.GPIO, threading
- shutdown
  - Implements the shutdown method for the restful interface which turns off the Radio
  - Packages used: RPi.GPIO
