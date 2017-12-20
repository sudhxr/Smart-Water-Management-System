import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.output(17, True)
time.sleep(3)
GPIO.output(17, False)
time.sleep(1)
GPIO.output(18, True)
time.sleep(3)
GPIO.output(18, False)
time.sleep(1)
GPIO.output(22, True)
time.sleep(3)
GPIO.output(22, False)
time.sleep(1)

GPIO.cleanup(17)
GPIO.cleanup(18)
GPIO.cleanup(22)