import threading
import time
import pigpio
import RPi.GPIO as GPIO
from WheelEncoderGPIO import WheelEncoder

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Driving:
    servos = [23, 24]
    raspi = pigpio.pi()
    samples = 5
    leftEncoderCount = WheelEncoder(11, 32, 5.65 / 2)
    rightEncoderCount = WheelEncoder(13, 32, 5.65 / 2)

    right_turn_speed = 1700
    left_turn_speed = 1300
    forward_speed = 2000
    stop_speed = 1500

    forward_time = 2
    turn45_time = 1.2 / 5

    def reverse_motor_pwm(self, pwm):
        return 3000 - pwm

    def Left_forward(self, n):
        self.raspi.set_servo_pulsewidth(self.servos[0], n)

    def Left_stop(self):
        self.raspi.set_servo_pulsewidth(self.servos[0], 0)

    def Right_forward(self, n):
        self.raspi.set_servo_pulsewidth(self.servos[1], self.reverse_motor_pwm(n))

    def Right_stop(self):
        self.raspi.set_servo_pulsewidth(self.servos[1], 0)

    def Robot_forward(self, n):
        self.Left_forward(n)
        self.Right_forward(n)

    def Robot_reverse(self, n):
        self.Left_forward(self.reverse_motor_pwm(n))
        self.Right_forward(self.reverse_motor_pwm(n))

    def Robot_stop(self):
        self.Left_stop()
        self.Right_stop()

    def Robot_right(self, n):
        self.Left_forward(n)
        self.Right_forward(self.reverse_motor_pwm(n))

    def Robot_left(self, n):
        self.Left_forward(self.reverse_motor_pwm(n))
        self.Right_forward(n)

    def motorStop(self):
        for s in self.servos:
            self.raspi.set_servo_pulsewidth(s, 0)

    def Encoders(self, wheelEncoder, name):
        while True:
            dist = wheelEncoder.getCurrentDistance()
            totDist = wheelEncoder.getTotalDistance()
            time.sleep(0.01)

    def do_move(self, move):
        match move[0]:
            case "f":
                self.Robot_forward(move[1])
            case "t":
                self.Robot_right(move[1])
            case "s":
                self.Robot_stop()
        time.sleep(move[2])

    def moves(self, profile):
        for move in profile:
            self.do_move(move)

        self.Robot_stop()
        self.raspi.stop()