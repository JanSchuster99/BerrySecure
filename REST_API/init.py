import RPi.GPIO as GPIO
import threading
import RNGRaspPiTests
from RNGRaspPiTests import startupTest
from RNGRaspPi import generateRandomNumber  


# Generate a random number and run the startup test
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, True)
    number = generateRandomNumber(20000, 1)
    
    # Check if number is empty: if true output error code for microphone not connected
    if number == "":
        GPIO.output(4, False)
        return 409
    
    # Create a thread to run the startup test and wait for up to 60 seconds
    startup_thread = threading.Thread(target=startupTest, args=(number,))
    startup_thread.start()
    startup_thread.join(timeout=60)

    if RNGRaspPiTests.startupResult == None:
        # If the startupResult has not been set, return code 555 for timeout 
        GPIO.output(4, False)
        return 555
    elif not RNGRaspPiTests.startupResult:
        # If the startup test returned False, return status code 543 startup failed 
        GPIO.output(4, False)
        return 543
    elif RNGRaspPiTests.startupResult:
        # If startupResult returns True, return code 200
        return 200

startupResult = None


