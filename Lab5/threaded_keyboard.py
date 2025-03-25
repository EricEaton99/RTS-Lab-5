import time
import sys
import tty
import termios
import threading
from threaded_driving import RobotController

class KeyboardController:
    def __init__(self):
        self.key_callbacks = {}  # Dictionary to store key-callback pairs
        self.running = True
        self.thread = threading.Thread(target=self._listen_for_keys)
        self.thread.start()

    def register_key(self, key, callback):
        """
        Register a key and its corresponding callback.
        """
        self.key_callbacks[key] = callback

    def stop(self):
        """
        Stop the keyboard listener and clean up resources.
        """
        self.running = False
        self.thread.join()

    def _listen_for_keys(self):
        """
        Listen for keyboard input in a separate thread.
        """
        while self.running:
            char = self._getch()
            if char in self.key_callbacks:
                self.key_callbacks[char]()  # Call the registered callback
            time.sleep(0.1)  # Small delay to prevent busy-waiting

    def _getch(self):
        """
        Capture a single character from the keyboard.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# Example usage
if __name__ == "__main__":
    controller = KeyboardController()

    # Register keys and their corresponding callbacks
    controller.register_key("w", lambda: controller.robot.send_instruction(["f", 2000]))  # Move forward
    controller.register_key("a", lambda: controller.robot.send_instruction(["t", 1300]))  # Turn left
    controller.register_key("s", lambda: controller.robot.send_instruction(["f", 1700]))  # Move backward
    controller.register_key("d", lambda: controller.robot.send_instruction(["t", 1700]))  # Turn right
    controller.register_key("q", lambda: controller.robot.send_instruction(["s", 0]))     # Stop
    controller.register_key("x", lambda: controller.stop())                               # Exit

    print("Press keys to control the robot. Press 'x' to exit.")

    # Keep the main thread alive while the keyboard listener runs
    try:
        while controller.running:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.stop()