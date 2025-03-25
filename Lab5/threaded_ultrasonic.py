from HCSR04 import HCSR04
import threading
import time


class Ultrasonic:

    def __init__(self):
        self.readPeriod = 0.1
        self.numMeasures = 3

        self.threshold_callbacks = []

        self.sensor = HCSR04(7, 12)
        self.running = True
        self.thread = threading.Thread(target=self._execute_instructions)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()


    def register_callback(self, distance, callback):
        """
        Register a key and its corresponding callback.
        """
        self.threshold_callbacks.append((distance, callback))

    def _execute_instructions(self):
        while self.running:
            self._measure_helper()
            time.sleep(self.readPeriod)  # Small delay to prevent busy-waiting
            
    
    def get_distance(self):
        self._measure_helper()

    def _measure_helper(self):
        distance = self.sensor.measure(self.numMeasures, "cm")
        for threshold, callback in self.threshold_callbacks:
            if distance < threshold:
                # print(f"{distance} cm")
                callback()  # Call the registered callback if distance is less than threshold




# Example usage
if __name__ == "__main__":
    us = Ultrasonic()
    time.sleep(3)
    us.stop()
    time.sleep(1)
    us.get_distance()