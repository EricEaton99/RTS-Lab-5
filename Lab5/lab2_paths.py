import threading
import time
import pigpio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

servos = [23, 24]
raspi = pigpio.pi()


def reverse_motor_pwm(pwm):
    return 3000 - pwm

def Robot_forward(n):
    raspi.set_servo_pulsewidth(servos[0], n)
    raspi.set_servo_pulsewidth(servos[1], reverse_motor_pwm(n))

def Robot_stop():
    raspi.set_servo_pulsewidth(servos[0], 0)
    raspi.set_servo_pulsewidth(servos[1], 0)

def Robot_right(n):
    raspi.set_servo_pulsewidth(servos[0], n)
    raspi.set_servo_pulsewidth(servos[1], reverse_motor_pwm(n))



# Movement constants
turn45 = 1.2 / 5
right_turn_speed = 1700
left_turn_speed = 1300
forward_speed = 2000
stop_speed = 1500

# Movement profiles
profile2 = [
    ["f", forward_speed, 2],
    ["t", right_turn_speed, 2 * turn45],
    ["f", forward_speed, 1],
    ["t", left_turn_speed, 3 * turn45],
    ["f", forward_speed, 1.414 * 2],
    ["t", right_turn_speed, 3 * turn45],
    ["f", forward_speed, 1],
    ["t", left_turn_speed, 2 * turn45],
    ["f", forward_speed, 2],
    ["2", stop_speed, 0]
]

def do_move(move):
    match move[0]:
        case "f":
            Robot_forward(move[1])
        case "t":
            Robot_right(move[1])
        case "s":
            Robot_stop()
    time.sleep(move[2])

def moves(any, any2):
    for move in profile2:
        do_move(move)
    Robot_stop()
    raspi.stop()

# Create and start a thread for movement
movementThread = threading.Thread(target=moves, args=('anything', 'anything2'))
movementThread.start()
