import pigpio
import time

class ServoController:
    def __init__(self, servo_pin=25):
        self.pi = pigpio.pi()  # Initialize pigpio
        self.SERVO_PIN = servo_pin  # BCM GPIO 25 by default

    def look_forward(self):
        """Set servo to neutral position (1500 µs)."""
        self.pi.set_servo_pulsewidth(self.SERVO_PIN, 1500)
        time.sleep(1)

    def look_right(self):
        """Move servo to 2000 µs (e.g., full right for a servo)."""
        self.pi.set_servo_pulsewidth(self.SERVO_PIN, 2500)
        time.sleep(1)

    def look_left(self):
        """Move servo to 1000 µs (e.g., full left for a servo)."""
        self.pi.set_servo_pulsewidth(self.SERVO_PIN, 500)
        time.sleep(1)

    def look_around(self):
        self.look_left()    # Move left (1000 µs)
        time.sleep(0.5)
        self.look_right()   # Move right (2000 µs)
        time.sleep(0.5)
        servo.look_forward() # Center (1500 µs)


    def stop(self):
        """Stop servo (0 turns off PWM)."""
        self.pi.set_servo_pulsewidth(self.SERVO_PIN, 0)

    def cleanup(self):
        """Cleanup resources."""
        self.pi.stop()


# Example usage
if __name__ == "__main__":
    servo = ServoController()
    try:
        servo.look_left()    # Move left (1000 µs)
        time.sleep(0.5)
        servo.look_right()   # Move right (2000 µs)
        time.sleep(0.5)
        servo.look_forward() # Center (1500 µs)
    finally:
        servo.stop()       # Turn off PWM
        servo.cleanup()    # Cleanup pigpio