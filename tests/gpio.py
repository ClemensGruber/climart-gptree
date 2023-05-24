import RPi.GPIO as GPIO

# GPIO-Pin für die LED
LED_PIN = 8

def led_an():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.HIGH)

def led_aus():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)

# Beispielaufrufe
led_an()  # LED einschalten