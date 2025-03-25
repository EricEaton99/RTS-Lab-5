import time
import sys
import tty
import termios
from driving import Driving
import pigpio

## Object detection in stingray using TensorFlow lite
## Save the file as object_detection.py
## Lab 3
import os
import argparse
import cv2
import numpy as np
from threading import Thread
import importlib.util
import threading
import queue

class Video_PiCamera:
    def __init__(self, resolution=(640, 480), framerate=60):
        # Initializing the Picamera of the Stingray
        self.stream = cv2.VideoCapture(0)
        if not self.stream.isOpened():
            print("Error: Could not open video stream.")
            self.stopped = True
            return
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.stream.set(3, resolution[0])
        self.stream.set(4, resolution[1])
        cv2.waitKey(100)
        (self.grabbed, self.frame) = self.stream.read()  # Reading the initial frame from the video stream
        if not self.grabbed:
            print("Error: Failed to grab initial frame.")
            self.stopped = True
            return
        self.stopped = False
        self.frame_queue = queue.Queue()  # Queue to hold frames for the main thread

    def start(self):
        threading.Thread(target=self.update, args=()).start()  # Start the video capturing in a background thread
        return self

    def update(self):
        while True:
            if self.stopped:
                self.stream.release()  # Stop the thread when camera is stopped
                cv2.destroyAllWindows()
                return
            (self.grabbed, self.frame) = self.stream.read()  # Read the next frame if the camera is running
            if self.grabbed:
                self.frame_queue.put(self.frame)  # Push the frame to the queue for main thread processing

    def read(self):
        if not self.frame_queue.empty():
            return self.frame_queue.get()  # Return the most recent frame
        return None  # If queue is empty, return None

    def stop(self):
        self.stopped = True  # Stop the video capturing

# Parsing the arguments for the tf input
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', required=True)
parser.add_argument('--graph', default='detect.tflite')
parser.add_argument('--labels', default='labelmap.txt')
parser.add_argument('--threshold', default=0.5)
parser.add_argument('--resolution', default='600x300')
args = parser.parse_args()

model = args.modeldir
graph_n = args.graph
label_ = args.labels
minimum_confidence = float(args.threshold)
resW, resH = args.resolution.split('x')
imW, imH = int(resW), int(resH)

# Import the tflite libraries
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
else:
    from tensorflow.lite.python.interpreter import Interpreter

current_dir = os.getcwd()  # Get path to the current directory
tflite_directory = os.path.join(current_dir, model, graph_n)  # Path to the .tflite file
label_destination = os.path.join(current_dir, model, label_)  # Path to the label map file

with open(label_destination, 'r') as f:  # Load the label map
    labels = [line.strip() for line in f.readlines()]
if labels[0] == '???':  # Remove the first label if needed
    del labels[0]

model_interpreter = Interpreter(model_path=tflite_directory)
model_interpreter.allocate_tensors()
input = model_interpreter.get_input_details()
output = model_interpreter.get_output_details()
height = input[0]['shape'][1]
width = input[0]['shape'][2]
floating_model = (input[0]['dtype'] == np.float32)
input_mean = 127.5
input_std = 127.5

# Initializing the video streaming
piCamera = Video_PiCamera(resolution=(imW, imH), framerate=60).start()

if piCamera is None:
    print("Error: Video_PiCamera is None")
print("Video_PiCamera grabbed successfully")

time.sleep(1)

def detection(any, any2):
    while True:
        ret, original_frame = piCamera.stream.read()  # Get the most recent frame from the camera
        if original_frame is None:
            print("Failed to capture frame. Exiting...")
            break


        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n Exiting the frame")
            break

        # ret, original_frame = piCamera.stream.read()  # Grab frame from video stream
        # if not ret:
        #     print("Failed to capture frame. Exiting...")
        #     break
        
        # #debug original_frame
        # if original_frame is None:
        #     print("Error: original_frame is None")
        #     return  # Skip the rest of the loop iteration if frame is None
        # print("original_frame grabbed successfully")
        

        # cv2.imshow("Stingray Live Video Feed", original_frame)

        # Duplicating the frame and adjusting the size of it
        frame = original_frame.copy()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalize the pixels for a non-quantized model
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        model_interpreter.set_tensor(input[0]['index'], input_data)
        model_interpreter.invoke()

        box = model_interpreter.get_tensor(output[0]['index'])[0]  # Bounding box coordinates
        classes = model_interpreter.get_tensor(output[1]['index'])[0]  # Class index of objects
        conf_value = model_interpreter.get_tensor(output[2]['index'])[0]  # Confidence values

        for i in range(len(conf_value)):  # Compare with the minimum threshold
            if (conf_value[i] > minimum_confidence) and (conf_value[i] <= 1.0):
                # Get bounding box coordinates
                ymin = int(max(1, (box[i][0] * imH)))
                xmin = int(max(1, (box[i][1] * imW)))
                ymax = int(min(imH, (box[i][2] * imH)))
                xmax = int(min(imW, (box[i][3] * imW)))
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)

                # Draw label around the box
                object_name = labels[int(classes[i])]
                label = '%s: %d%%' % (object_name, int(conf_value[i] * 100))
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                label_ymin = max(ymin, labelSize[1] + 10)
                cv2.rectangle(frame, (xmin, label_ymin - labelSize[1] - 10),
                              (xmin + labelSize[0], label_ymin + baseLine - 10), (255, 255, 255), cv2.FILLED)
                cv2.putText(frame, label, (xmin, label_ymin - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        cv2.imshow('Object Detection in Stingray', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            print("\n Exiting the frame")
            break

    cv2.destroyAllWindows()
    piCamera.stop()

# Creating a thread for object detection
objectDetectionThread = threading.Thread(target=detection, args=('any1', 'any2'))
objectDetectionThread.start()














#-------------------------------------------------------













raspi= pigpio.pi()
wheels = Driving()

# Function to capture keyboard input
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Main loop
while True:
    # Capture keyboard input
    char = getch()

    if char == "w":
        # forward
        print("w")
        wheels.Robot_forward(2000)
    elif char == "a":
        # left
        print("a")
        wheels.Robot_left(1700)
    elif char == "s":
        # bask
        print("s")
        wheels.Robot_reverse(1700)
    elif char == "d":
        # right
        print("d")
        wheels.Robot_right(1700)
    # stop
    elif char == "q":
        wheels.Robot_stop()
    # Exit program
    elif char == "x":
        wheels.Robot_stop()
        
        raspi.stop()
        exit()
    
