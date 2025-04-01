from threaded_driving import RobotController
from threaded_keyboard import KeyboardController
from threaded_ultrasonic import Ultrasonic
from threaded_servo import ServoController
# from threaded_objectdetection import startThread
#from maze_gui import MazeGUI
import time

robot = RobotController()
keyboard = KeyboardController()
ultrasonic = Ultrasonic()
servo = ServoController()
# objectDetection = startThread()

turn90_time_l = 0.35
turn90_time_r = 0.23



def turn_l():
    robot.send_instruction(["t", 1300]) 
    time.sleep(turn90_time_l) 
    robot.send_instruction(["s", 0])
    time.sleep(1) 

def turn_r():
    robot.send_instruction(["t", 1700]) 
    time.sleep(turn90_time_r) 
    robot.send_instruction(["s", 0])
    time.sleep(1) 

def short_forward(num_units):
    time_per_unit = 0.8

    robot.send_instruction(["f", 1700])
    time.sleep(num_units * time_per_unit) 
    robot.send_instruction(["s", 0])
    time.sleep(1) 

def dodge_l():
    turn_l()
    short_forward(1)
    turn_r()
    short_forward(2)
    turn_r()
    short_forward(1)
    turn_l()


def dodge_r():
    turn_r()
    short_forward(1)
    turn_l()
    short_forward(2)
    turn_l()
    short_forward(1)
    turn_r()


# Flag to indicate if the program should exit
exit_flag = False
us_distance = 30 # cm
total_turns = 5
current_turn = -1
stretch_start_time = -1
obstacle_flag = False



def uninit():
    global exit_flag
    exit_flag = True  # Set the flag to True to indicate that the program should exit



def look_around():
    servo.look_left()
    time.sleep(0.5)
    left_dist = ultrasonic.get_distance()
    time.sleep(0.1)

    servo.look_right()
    time.sleep(0.5)
    right_dist = ultrasonic.get_distance()
    time.sleep(0.1)

    servo.look_forward()
    if(left_dist < right_dist):
        return "l"
    else:
        return "r" 


def at_object():
    global obstacle_flag
    obstacle_flag = True

    open_direction = look_around()
    if(open_direction == "l"):
        dodge_l()
    else:
        dodge_r()



def at_corner():
    global obstacle_flag
    global stretch_start_time
    global current_turn

    # if(not obstacle_flag):
    current_turn+=1
    if current_turn > total_turns:
        print("stop!")
        uninit()
        return

    open_direction = look_around()

    if(open_direction == "l"):
        turn_l()
    else:
        turn_r()
    
    time.sleep(1)

    robot.send_instruction(["f", 1700])

    stretch_start_time = time.time()
    obstacle_flag = False


def us_callback():
    global current_turn
    global total_turns
    global stretch_start_time
    global obstacle_flag
    stretch_expected_dtimes = [4.4506, 2.3700, 2.6100, 1.7599]
    stretch_dtime_error = 0.4

    print("us callback!")

    ultrasonic.pause()

    robot.send_instruction(["s", 0])

    if current_turn < 0:    # first turn
        at_corner()
        ultrasonic.unpause()
        return
    
   
    stretch_dtime = time.time() - stretch_start_time
    stretch_expected_dtime = stretch_expected_dtimes[current_turn]
    print(f"expecting time {stretch_expected_dtime} got time {stretch_dtime}")

    if(stretch_dtime >= stretch_expected_dtime - stretch_dtime_error or obstacle_flag):
        # at corner current_turn
        at_corner()
    else:
        # at object stretch_dtime * velocity
        at_object()

    ultrasonic.unpause()

def us_log_callback():
    print("\r\nus log callback!")
    ultrasonic.pause()
    robot.send_instruction(["s", 0])

    dtime = time.time() - stretch_start_time
    print(f"\r\ndtime = {dtime}")
    at_corner()

    ultrasonic.unpause()



def init():
    global stretch_start_time
    stretch_start_time = time.time()
    # Register keys and their corresponding callbacks
    keyboard.register_key("w", lambda: robot.send_instruction(["f", 1700]))  # Move forward
    keyboard.register_key("a", turn_l)  # Turn left
    keyboard.register_key("s", lambda: robot.send_instruction(["f", 1000]))  # Move backward
    keyboard.register_key("d", turn_r)  # Turn right
    keyboard.register_key("q", lambda: robot.send_instruction(["s", 0]))     # Stop
    keyboard.register_key("x", uninit)  # Pass the function itself, not its result
    # ultrasonic.register_callback(us_distance, us_log_callback)
    ultrasonic.register_callback(us_distance, us_callback)
    robot.send_instruction(["f", 1700])
    
    # objectDetection = startThread()

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