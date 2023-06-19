# simple LED on/off functionality
import os

if os.name == "posix":
  import RPi.GPIO as GPIO


def led(LED, state="on"):
  if os.name == "posix":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)
    if state == "on":
      GPIO.output(LED, GPIO.HIGH)
    else:
      GPIO.output(LED, GPIO.LOW)
