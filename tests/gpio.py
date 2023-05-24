import RPi.GPIO as GPIO
import time

# GPIO-Pin für die LED
LED_PIN = 5

def led_an():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.HIGH)

def led_aus():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)

# Initialisiere die GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Beispielaufrufe
led_an()  # LED einschalten
time.sleep(5)  # Die LED für 5 Sekunden eingeschaltet lassen
led_aus()  # LED ausschalten

# Aufräumarbeiten
GPIO.cleanup()