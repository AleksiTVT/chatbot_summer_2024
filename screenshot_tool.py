from PIL import ImageGrab
import tkinter as tk
import time
import asyncio
import os

class ScreenshotTool:
    def __init__(self, root):
        self.window = tk.Toplevel(master=root)
        self.window.config(
            background='skyblue'
        )
        self.window.geometry('600x300')
        self.window.title = "screenshot tool"

        self.screenshot = None
        self.path_to_temp_screenshot= None

        label = tk.Label(
            master=self.window,
            text="q = quit, s = take screenshot",
            font=("Arial", 20),
            background="skyblue"
        )

        self.window.bind(sequence="<KeyPress>", func=self.handle_key_press)

        label.pack(side=tk.LEFT)

    def quit(self):
        self.window.destroy()

    def save_temp_screenshot(self):
        directory = os.getcwd() + "\\temp\\screenshot"

        if not os.path.exists(directory):
            os.makedirs(directory)

        self.path_to_temp_screenshot = os.path.join(directory, "screenshot.png")

        self.screenshot.save(self.path_to_temp_screenshot)

    def take_screenshot(self):
        self.window.withdraw()
        time.sleep(0.3)

        self.screenshot = ImageGrab.grab()

        self.save_temp_screenshot()

        self.window.deiconify()

    def handle_key_press(self, event):
        if event.char.lower() == "s":
            self.take_screenshot()
        elif event.char.lower() == "q":
            self.quit()

    def get_path_to_screenshot(self):
        return self.path_to_temp_screenshot
    
    async def wait_until_screenshot_taken(self):
        while self.screenshot == None:
            await asyncio.sleep(0.1)

    def delete_temp_screenshot(self):
        if os.path.exists(self.path_to_temp_screenshot):
            os.remove(self.path_to_temp_screenshot)
