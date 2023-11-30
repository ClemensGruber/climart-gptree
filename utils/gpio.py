# simple LED on/off functionality
import platform

if platform.system() == 'Linux':
    import RPi.GPIO as GPIO
  

def led(LED, state="on"):
  if platform.system() == 'Linux':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)
    if state == "on":
      GPIO.output(LED, GPIO.HIGH)
    else:
      GPIO.output(LED, GPIO.LOW)
