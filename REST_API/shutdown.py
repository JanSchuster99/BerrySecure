import RPi.GPIO as GPIO

# Shutdown the radio
def die():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(4, GPIO.OUT)

    GPIO.output(4, False)

