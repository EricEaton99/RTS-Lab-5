import time
import sys
import tty
import termios
from driving import Driving
import pigpio

class KeybaordDriving:
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

    def keyboard_loop(self):
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
        
