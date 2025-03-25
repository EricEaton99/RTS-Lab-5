from threaded_driving import RobotController
from threaded_keyboard import KeyboardController
from threaded_ultrasonic import Ultrasonic
import time

robot = RobotController()
keyboard = KeyboardController()
ultrasonic = Ultrasonic()

# Flag to indicate if the program should exit
exit_flag = False

def uninit():
    global exit_flag
    exit_flag = True  # Set the flag to True to indicate that the program should exit

def us_callback():
    print("us callback!")

def init():
    # Register keys and their corresponding callbacks
    keyboard.register_key("w", lambda: robot.send_instruction(["f", 2000]))  # Move forward
    keyboard.register_key("a", lambda: robot.send_instruction(["t", 1300]))  # Turn left
    keyboard.register_key("s", lambda: robot.send_instruction(["f", 1700]))  # Move backward
    keyboard.register_key("d", lambda: robot.send_instruction(["t", 1700]))  # Turn right
    keyboard.register_key("q", lambda: robot.send_instruction(["s", 0]))     # Stop
    keyboard.register_key("x", uninit)  # Pass the function itself, not its result
    ultrasonic.register_callback(10, us_callback)

init()

# Keep the main thread alive while the keyboard listener runs
try:
    while not exit_flag:
        time.sleep(1)
except KeyboardInterrupt:
    uninit()
finally:
    # Cleanup resources
    keyboard.stop()
    robot.stop()