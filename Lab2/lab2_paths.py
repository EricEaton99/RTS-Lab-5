#Import Libraries
import threading
import time
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
import pigpio
import RPi.GPIO as GPIO
from WheelEncoderGPIO import WheelEncoder
from PlotDataRobot import multiplePlots
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
        
servos = [23,24]
raspi= pigpio.pi()

samples = 5

#creation of two encoders using WheelEncoder class
leftEncoderCount = WheelEncoder(11, 32, 5.65/2)
rightEncoderCount = WheelEncoder(13, 32, 5.65/2)

xmax = 5
plotData = multiplePlots(leftEncoderCount, rightEncoderCount,
    samples, xmax)


def reverse_motor_pwm(pwm): 
    return 3000 - pwm

#Returning values to plot the data
def loopData(self):
    plotData.updateData()
    return plotData.p011, plotData.p012, plotData.p021, plotData.p022
	
def Left_forward(n):
    raspi.set_servo_pulsewidth(servos[0], n)
	
def Left_stop():
    raspi.set_servo_pulsewidth(servos[0], 0)

#Value for servo speed forward now an argument that must be passed    
def Right_forward(n):
    raspi.set_servo_pulsewidth(servos[1], reverse_motor_pwm(n))
    
def Right_stop():
    raspi.set_servo_pulsewidth(servos[1], 0)

#robot forward function takes two arguments for each motors servo speed
def Robot_forward(n):
    Left_forward(n)
    Right_forward(n)
    
def Robot_reverse(n):
    Left_forward(reverse_motor_pwm(n))
    Right_forward(reverse_motor_pwm(n))
    
def Robot_stop():
    Left_stop()
    Right_stop()
        
def Robot_right(n):
    Left_forward(n)
    Right_forward(reverse_motor_pwm(n))

def Robot_left():
    Left_forward(reverse_motor_pwm(n))
    Right_forward(n)

#Function to stop all motors    
def motorStop():
    for s in servos:
        raspi.set_servo_pulsewidth(s,0)
     
#Function for encoder output takes wheelEncoder object and a name for the encoder as #arguments
def Encoders(wheelEncoder, name):
    while(True):
        dist = wheelEncoder.getCurrentDistance()
        totDist = wheelEncoder.getTotalDistance()
        # print("\n{} Distance: {}cm".format(name, dist))
        # print("\n{} Ticks: {}".format(name, wheelEncoder.getTicks()))
        # print("\n{} Total Distance: {}cm".format(name, totDist))
        # print("\n{} Total Ticks: {}".format(name, wheelEncoder.getTotalTicks()))
        time.sleep(0.01)


#create a function to move the robot, with 2 arguments
#remember to add the functions that you need from the previous codes,
#as Robot_forward() and Robot_stop()
turn45 = 1.2/5
right_turn_speed = 1700
left_turn_speed = 1300
forward_speed = 2000
stop_speed = 1500

forward = ["f", forward_speed, 5]

profile1 = [
    ["f", forward_speed, 2], 
    ["t", left_turn_speed, 2*turn45], 
    ["f", forward_speed, 2], 
    ["t", right_turn_speed, 2*turn45],
    ["f", forward_speed, 2], 
    ["t", right_turn_speed, 2*turn45], 
    ["f", forward_speed, 2], 
    ["t", left_turn_speed, 2*turn45], 
    ["f", forward_speed, 2], 
    ["2", stop_speed, 0]]

profile2 = [
    ["f", forward_speed, 2], 
    ["t", right_turn_speed, 2*turn45], 
    ["f", forward_speed, 1], 
    ["t", left_turn_speed, 3*turn45],
    ["f", forward_speed, 1.414*2], 
    ["t", right_turn_speed, 3*turn45], 
    ["f", forward_speed, 1], 
    ["t", left_turn_speed, 2*turn45], 
    ["f", forward_speed, 2], 
    ["2", stop_speed, 0]]

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

#create a thread to call this function
movementThread = threading.Thread(target = moves, args = ('anything','anything2'))

#start the thread
movementThread.start()

