import RPi.GPIO as GPIO
import time

# Define GPIO Pins
trig_pin = 20         # GPIO pin for triggering the ultrasonic sensor
echo_pin = 16         # GPIO pin for receiving the ultrasonic echo
buzzer_pin = 12       # GPIO pin connected to a buzzer for sound feedback

# GPIO Setup
GPIO.setmode(GPIO.BCM)  # Set the GPIO pin numbering mode to Broadcom SOC channel numbering
GPIO.setup(trig_pin, GPIO.OUT)    # Configure the trigger pin as an output
GPIO.setup(echo_pin, GPIO.IN)     # Configure the echo pin as an input
GPIO.setup(buzzer_pin, GPIO.OUT)  # Configure the buzzer pin as an output

def distance():
    time.sleep(0.1)
    # Generate ultrasonic burst by setting the trigger pin high.
    GPIO.output(trig_pin, True)
    
    # Wait for a short time and then set the trigger pin low.
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)
 
    # Record the time when the burst is sent.
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()

    # Record the time when the echo is received.
    while GPIO.input(echo_pin) == 1:
        end_time = time.time()

    # Calculate the time taken for the response.
    response_time = end_time - start_time

    # Calculate the distance by multiplying with the speed of sound
    # and dividing by 2 as we account for the time to and from the target.
    # The result is in centimeters.
    distance = (response_time * 34300) / 2
    return distance

def set_buzzer_intensity(sound_intensity):
    # Ensure the sound intensity is within a valid range.
    if sound_intensity < 0:
        sound_intensity = 0
    elif sound_intensity > 100:
        sound_intensity = 100
    # Set the buzzer intensity using PWM (Pulse Width Modulation).
    buzzer_pwm.ChangeDutyCycle(sound_intensity)

# Initialize PWM for the buzzer with a 100 Hz frequency.
buzzer_pwm = GPIO.PWM(buzzer_pin, 100)
buzzer_pwm.start(0)  # Start with 0% duty cycle

# Adjust the buzzer intensity based on the object's distance.
# Louder when closer, softer when farther.
def adjust_sound(object_distance):
    if object_distance < 100:
        set_buzzer_intensity(100 - object_distance)
    else:
        set_buzzer_intensity(0)

# Continuously read distance and adjust the buzzer until a keyboard interrupt occurs.
try:
    while True:
        object_distance = distance()
        adjust_sound(object_distance)
        
except KeyboardInterrupt:
    # Stop the buzzer and clean up GPIO configurations on keyboard interrupt.
    buzzer_pwm.stop()
    GPIO.cleanup()
