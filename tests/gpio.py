import RPi.GPIO as GPIO
import time

# GPIO-Pin für die LED
LED_PIN_GREEN = 4
LED_PIN_RED = 17

def led_an():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN_GREEN, GPIO.OUT)
    GPIO.output(LED_PIN_GREEN, GPIO.HIGH)
    GPIO.setup(LED_PIN_RED, GPIO.OUT)
    GPIO.output(LED_PIN_RED, GPIO.HIGH)

def led_aus():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN_GREEN, GPIO.OUT)
    GPIO.output(LED_PIN_GREEN, GPIO.LOW)
    GPIO.setup(LED_PIN_RED, GPIO.OUT)
    GPIO.output(LED_PIN_RED, GPIO.LOW)

# Initialisiere die GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Beispielaufrufe
led_an()  # LED einschalten
time.sleep(5)  # Die LED für 5 Sekunden eingeschaltet lassen
led_aus()  # LED ausschalten

# Aufräumarbeiten
GPIO.cleanup()