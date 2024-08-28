import time
from pynput import mouse, keyboard
import requests
from threading import Timer

API_URL = "http://127.0.0.1:8000/api/input_activity/"

class InputActivityTracker:
    def __init__(self, api_url):
        self.api_url = api_url
        self.keyboard_count = 0
        self.mouse_count = 0
        self.start_time = time.time()

        # Start listening to keyboard and mouse
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)

        self.keyboard_listener.start()
        self.mouse_listener.start()

        # Setup a timer to send data every 10 seconds
        self.timer = Timer(10.0, self.send_data)
        self.timer.start()

    def on_key_press(self, key):
        self.keyboard_count += 1

    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            self.mouse_count += 1

    def send_data(self):
        elapsed_time = time.time() - self.start_time
        if self.keyboard_count > 0 or self.mouse_count > 0:
            data = {
                "keyboard_activity": self.keyboard_count,
                "mouse_activity": self.mouse_count,
            }
            response = requests.post(self.api_url, json=data)
            if response.status_code == 201:
                print(f"Data sent successfully: {data}")
            else:
                print(f"Failed to send data: {response.status_code}")

        # Reset counters
        self.keyboard_count = 0
        self.mouse_count = 0

        # Restart the timer
        self.timer = Timer(10.0, self.send_data)
        self.timer.start()

    def stop(self):
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
        self.timer.cancel()

if __name__ == "__main__":
    tracker = InputActivityTracker(API_URL)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tracker.stop()
        print("Activity tracking stopped.")
