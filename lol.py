import pyautogui
import time
import os
import ctypes
import sys
import threading
import webbrowser
import customtkinter as ctk
from PIL import Image, ImageTk
from itertools import count
from customtkinter import CTkImage

CONFIDENCE = 0.7  # Image match confidence

class AutoAcceptApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Load custom font on Windows
        if sys.platform == "win32":
            FR_PRIVATE = 0x10
            try:
                heavy_font_path = self.resource_path("BeaufortforLOL-Heavy.ttf")
                medium_font_path = self.resource_path("BeaufortforLOL-Medium.ttf")
                ctypes.windll.gdi32.AddFontResourceExW(heavy_font_path, FR_PRIVATE, 0)
                ctypes.windll.gdi32.AddFontResourceExW(medium_font_path, FR_PRIVATE, 0)
            except Exception:
                pass

        self.title("LoL Auto Accept")
        self.geometry("300x380")
        self.resizable(False, False)
        self.configure(fg_color="#0f0f0f")

        # Load and set the title bar icon (use .ico file on Windows)
        try:
            icon_path = self.resource_path("app_icon.ico")
            self.iconbitmap(icon_path)
        except Exception:
            pass

        # Set the directory to access bundled resources
        self.script_dir = self.resource_path("")

        self.button_images = [
            {"path": os.path.join(self.script_dir, "accept_en.png"), "conf": CONFIDENCE},
            {"path": os.path.join(self.script_dir, "accept_kr.png"), "conf": CONFIDENCE},
        ]

        self.running = False
        self.thread = None

        # Load animated GIF
        gif_path = self.resource_path("zzz_sleep.gif")
        self.gif = Image.open(gif_path)
        self.gif_frames = []
        self.gif_durations = []

        try:
            for frame in count(0):
                self.gif.seek(frame)
                frame_image = self.gif.copy().convert("RGBA")
                frame_image = frame_image.resize((200, 200), Image.Resampling.LANCZOS)
                ctk_image = CTkImage(light_image=frame_image, dark_image=frame_image, size=(200, 200))
                self.gif_frames.append(ctk_image)
                self.gif_durations.append(self.gif.info.get("duration", 100))
        except EOFError:
            pass

        self.current_frame = 0
        self.gif_label = ctk.CTkLabel(self, text="", image=self.gif_frames[0])
        self.gif_label.pack(pady=(10, 0))
        self.animate_gif()

        # Use your custom font family here
        button_font = ctk.CTkFont(family="Beaufort for LOL", size=25, weight="bold")

        self.status_label = ctk.CTkLabel(
            self,
            text="Waiting for start...",
            text_color="#ffac26",
            font=ctk.CTkFont(family="Beaufort for LOL", size=30, weight="bold")
        )
        self.status_label.pack(pady=(0, 10))

        self.toggle_button = ctk.CTkButton(
            self,
            text="Start",
            command=self.toggle_watcher,
            width=222,
            height=62,
            font=button_font,
            fg_color="#ffac26",
            hover_color="#9c5a21",
            text_color="#0f0f0f"
        )
        self.toggle_button.pack(side="bottom", pady=(1, 50))

        spacer = ctk.CTkFrame(self, fg_color="transparent")
        spacer.pack(expand=True, fill="both")

        self.creator_label = ctk.CTkLabel(
            self,
            text="Made by zyl0nz",
            text_color="#00a8ff",
            font=ctk.CTkFont(family="Beaufort for LOL", size=12),
            cursor="hand2"
        )
        self.creator_label.place(relx=0.5, rely=1.0, anchor="s", y=-5)
        self.creator_label.bind("<Button-1>", lambda e: self.open_github())

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def animate_gif(self):
        frame = self.gif_frames[self.current_frame]
        delay = self.gif_durations[self.current_frame]
        self.gif_label.configure(image=frame)
        self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
        self.after(delay, self.animate_gif)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def watcher(self):
        self.set_status("Waiting for match...", color="#ffac26")
        while self.running:
            location = None
            for button in self.button_images:
                try:
                    location = pyautogui.locateOnScreen(button["path"], confidence=button["conf"])
                except Exception:
                    continue

                if location:
                    self.set_status("Match found!", color="#00ff6c")
                    pyautogui.click(pyautogui.center(location))
                    time.sleep(5)
                    break

            time.sleep(1)

        self.set_status("Waiting for start...", color="#ffac26")

    def set_status(self, text, color="#FFFFFF"):
        self.status_label.configure(text=text, text_color=color)

    def toggle_watcher(self):
        if not self.running:
            self.running = True
            self.toggle_button.configure(
                text="Stop",
                fg_color="#ff3838",
                hover_color="#c22d2d",
                text_color="#0f0f0f"
            )
            self.thread = threading.Thread(target=self.watcher, daemon=True)
            self.thread.start()
        else:
            self.running = False
            self.toggle_button.configure(
                text="Start",
                fg_color="#ffac26",
                hover_color="#9c5a21",
                text_color="#0f0f0f"
            )

    def open_github(self):
        webbrowser.open("https://github.com/Zyl0nz/League-of-Legends-Auto-Accept")

    def on_close(self):
        self.running = False
        self.destroy()

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = AutoAcceptApp()
    app.mainloop()

if __name__ == "__main__":
    main()
