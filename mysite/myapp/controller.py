import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
LIGHT_PIN = 23
GPIO.setup(LIGHT_PIN, GPIO.IN)

while True:
    print(GPIO.input(LIGHT_PIN))
    time.sleep(10)
