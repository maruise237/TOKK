import threading
import time
import pyperclip
import pyautogui
from pynput import keyboard
from recorder import AudioRecorder
from transcriber import FrenchTranscriber

class TokkHandler:
    def __init__(self, update_status_callback=None):
        self.recorder = AudioRecorder()
        self.transcriber = FrenchTranscriber()
        self.update_status = update_status_callback or (lambda x: print(f"Status: {x}"))
        self.recording = False
        self.listener = None
        self.shortcut = {keyboard.Key.ctrl, keyboard.Key.alt, keyboard.KeyCode.from_char('f')}
        self.current_keys = set()
        self.processing = False

    def on_press(self, key):
        if key in self.shortcut:
            self.current_keys.add(key)
            if all(k in self.current_keys for k in self.shortcut):
                self.toggle_recording()

    def on_release(self, key):
        if key in self.current_keys:
            self.current_keys.remove(key)

    def toggle_recording(self):
        if self.processing:
            return

        if not self.recording:
            self.start_tokk()
        else:
            self.stop_tokk()

    def start_tokk(self):
        self.recording = True
        self.update_status("Enregistrement...")
        self.recorder.start()

    def stop_tokk(self):
        self.recording = False
        self.update_status("Arrêt de l'enregistrement...")
        audio_data = self.recorder.stop()

        # Start transcription in background
        thread = threading.Thread(target=self.process_audio, args=(audio_data,))
        thread.start()

    def process_audio(self, audio_data):
        self.processing = True
        try:
            if len(audio_data) == 0:
                self.update_status("Aucun audio capturé.")
                return

            self.update_status("Transcription...")
            text = self.transcriber.transcribe(audio_data)

            if text:
                self.update_status(f"Texte transcrit: {text}")
                self.paste_text(text)
                self.update_status("Prêt (Ctrl+Alt+F)")
            else:
                self.update_status("Rien à transcrire.")
        except Exception as e:
            self.update_status(f"Erreur: {str(e)}")
        finally:
            self.processing = False

    def paste_text(self, text):
        # Using clipboard + Ctrl+V is usually more reliable and faster
        old_clipboard = pyperclip.paste()
        pyperclip.copy(text)
        time.sleep(0.1)  # Give some time for the clipboard to update
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        # Optionally restore clipboard (disabled for now to ensure text is available)
        # pyperclip.copy(old_clipboard)

    def run(self):
        self.update_status("Tokk actif. Raccourci : Ctrl+Alt+F")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            self.listener = listener
            listener.join()

if __name__ == "__main__":
    handler = TokkHandler()
    handler.run()
