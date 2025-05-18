import pyautogui
import time
import os
import threading
import customtkinter as ctk

CONFIDENCE = 0.7  # Image match confidence

class AutoAcceptApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LoL Auto Accept")
        self.geometry("300x300")
        self.resizable(False, False)
        self.configure(bg="#121212")

        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.button_images = [
            {"path": os.path.join(self.script_dir, "accept_en.png"), "conf": CONFIDENCE},
            {"path": os.path.join(self.script_dir, "accept_kr.png"), "conf": CONFIDENCE},
        ]

        self.running = False
        self.thread = None

        # Font for the toggle button using customtkinter.CTkFont
        button_font = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")

        # UI elements
        self.status_label = ctk.CTkLabel(self, text="Idle", text_color="#FFFFFF", font=("Segoe UI", 25))
        self.status_label.pack(pady=(100, 20))

        self.toggle_button = ctk.CTkButton(
            self,
            text="Start",
            command=self.toggle_watcher,
            width=222,
            height=62,
            font=button_font
        )
        self.toggle_button.pack(side="bottom", pady=50)

    def watcher(self):
        self.set_status("Waiting for match...", color="#FFFFFF")
        while self.running:
            location = None
            for button in self.button_images:
                try:
                    location = pyautogui.locateOnScreen(button["path"], confidence=button["conf"])
                except Exception:
                    continue

                if location:
                    self.set_status("Match found!", color="green")
                    pyautogui.click(pyautogui.center(location))
                    time.sleep(5)
                    break

            time.sleep(1)

        self.set_status("Idle", color="#FFFFFF")

    def set_status(self, text, color="#FFFFFF"):
        self.status_label.configure(text=text, text_color=color)

    def toggle_watcher(self):
        if not self.running:
            self.running = True
            self.toggle_button.configure(text="Stop")
            self.thread = threading.Thread(target=self.watcher, daemon=True)
            self.thread.start()
        else:
            self.running = False
            self.toggle_button.configure(text="Start")

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = AutoAcceptApp()
    app.mainloop()

if __name__ == "__main__":
    main()
