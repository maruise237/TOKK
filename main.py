import customtkinter as ctk
import threading
from tokk_handler import TokkHandler
import pystray
from PIL import Image, ImageDraw
import sys
import os

class TokkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tokk - Transcription FR")
        self.geometry("400x200")
        self.resizable(False, False)

        self.setup_ui()
        self.handler = TokkHandler(update_status_callback=self.update_status)

        # Run the keyboard listener in a background thread
        self.listener_thread = threading.Thread(target=self.handler.run, daemon=True)
        self.listener_thread.start()

        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.status_label = ctk.CTkLabel(self, text="Tokk prêt. Appuyez sur Ctrl+Alt+F", font=ctk.CTkFont(size=14))
        self.status_label.grid(row=0, column=0, padx=20, pady=20)

        self.info_label = ctk.CTkLabel(self, text="Raccourci : Ctrl+Alt+F pour démarrer/arrêter l'enregistrement", font=ctk.CTkFont(size=10))
        self.info_label.grid(row=1, column=0, padx=20, pady=10)

        self.btn_quit = ctk.CTkButton(self, text="Quitter", command=self.quit_app)
        self.btn_quit.grid(row=2, column=0, padx=20, pady=10)

    def update_status(self, message):
        self.after(0, lambda: self.status_label.configure(text=message))

    def minimize_to_tray(self):
        self.withdraw()
        self.create_tray_icon()

    def create_tray_icon(self):
        # Create a simple icon
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), (0, 0, 0))
        dc = ImageDraw.Draw(image)
        dc.rectangle((width // 4, height // 4, width * 3 // 4, height * 3 // 4), fill=(0, 255, 0))

        menu = (pystray.MenuItem('Afficher', self.show_window),
                pystray.MenuItem('Quitter', self.quit_app))
        self.tray_icon = pystray.Icon("Tokk", image, "Tokk", menu)
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def show_window(self, icon=None, item=None):
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.after(0, self.deiconify)

    def quit_app(self, icon=None, item=None):
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = TokkApp()
    app.mainloop()
