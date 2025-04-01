import threading
import time
import pigpio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class RobotController:
    servos = [23, 24]

    right_turn_speed = 1700
    left_turn_speed = 1300
    forward_speed = 2000
    stop_speed = 1500

    forward_time = 2

    def __init__(self):
        self.servos = [23, 24]
        self.raspi = pigpio.pi()
        self.current_instruction = None
        self.instruction_lock = threading.Lock()
        self.running = True
        self.thread = threading.Thread(target=self._execute_instructions)
        self.thread.start()

    def reverse_motor_pwm(self, pwm):
        return 3000 - pwm

    def robot_forward(self, speed):
        self.raspi.set_servo_pulsewidth(self.servos[0], speed)
        self.raspi.set_servo_pulsewidth(self.servos[1], self.reverse_motor_pwm(speed))

    def robot_stop(self):
        self.raspi.set_servo_pulsewidth(self.servos[0], 0)
        self.raspi.set_servo_pulsewidth(self.servos[1], 0)

    def robot_right(self, speed):
        self.raspi.set_servo_pulsewidth(self.servos[0], speed)
        self.raspi.set_servo_pulsewidth(self.servos[1], speed)
        print(f"turning at {speed}, {self.reverse_motor_pwm(speed)}")

    def robot_left(self, speed):
        self.raspi.set_servo_pulsewidth(self.servos[0], self.reverse_motor_pwm(speed))
        self.raspi.set_servo_pulsewidth(self.servos[1], self.reverse_motor_pwm(speed))

    def send_instruction(self, instruction):
        with self.instruction_lock:
            self.current_instruction = instruction

    def stop(self):
        self.running = False
        self.robot_stop()
        self.raspi.stop()
        self.thread.join()

    def _execute_instructions(self):
        while self.running:
            with self.instruction_lock:
                if self.current_instruction is not None:
                    move = self.current_instruction
                    self.current_instruction = None  # Clear the instruction after execution
                else:
                    move = None

            if move is not None:
                self._execute_move(move)
            time.sleep(0.1)  # Small delay to prevent busy-waiting

    def _execute_move(self, move):
        match move[0]:
            case "f":
                self.robot_forward(move[1])
            case "t":
                self.robot_right(move[1])
            case "s":
                self.robot_stop()


# Example usage
if __name__ == "__main__":
    robot = RobotController()

    # Send instructions dynamically
    robot.send_instruction(["f", 2000])  # Move forward for 2 seconds
    time.sleep(3)
    robot.send_instruction(["t", 1700])  # Turn right for 0.24 seconds
    time.sleep(1)
    robot.send_instruction(["s", 0])  # Stop

    # Stop the robot and clean up
    robot.stop()