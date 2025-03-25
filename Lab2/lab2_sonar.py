from HCSR04 import HCSR04
import time
import threading
from driving import Driving
import pigpio

raspi= pigpio.pi()
min_distance = 10
samples = 5
# Creation of sonar sensor
sensor = HCSR04(7, 12)
wheels = Driving()
sensorThread = 0
movementThread = 0

wheels.Robot_forward(2000)

while True:
    distance = sensor.measure(samples, "cm")
    print(f"{distance} cm\n")
    if distance < min_distance:
        wheels.Robot_stop()
        raspi.stop()

    time.sleep(0.01)

# #square motion
# profile1 = [
#     ["f", wheels.forward_speed, 8], 
#     ["s", wheels.stop_speed, 0]]


# profile2 = [
#     ["t", wheels.left_turn_speed, 2*wheels.turn45_time], 
#     ["f", wheels.forward_speed, 2], 
#     ["t", wheels.left_turn_speed, 2*wheels.turn45_time], 
#     ["s", wheels.stop_speed, 0]]


# def sonar_interupt(data):
#     movementThread = data
#     movementThread.stop()
#     wheels.Robot_stop()
#     movementThread = threading.Thread(target = Move, args = (wheels, profile2))

# # Function for sonar sensor takes HCSR04 object and sample number for accuracy of distance
# def Sonar(sensor, data):
#     while True:
#         distance = sensor.measure(data[0], "cm")
#         if distance < min_distance:
#             sonar_interupt(data[1])

#         time.sleep(0.01)

# def Move(wheels, driving_profile):
#     wheels.moves(driving_profile)



# movementThread = threading.Thread(target = Move, args = (wheels, profile1))
# movementThread.start()


# sensorThread = threading.Thread(target=Sonar, args=(sensor, [samples, movementThread]))
# sensorThread.start()