import customtkinter as ctk
from tkinter import filedialog
from transcriber import FrenchTranscriber
import threading
import os

class TranscriberApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Transcription Audio FR (Ultra-léger)")
        self.geometry("600x450")

        self.transcriber = None
        self.loading_thread = threading.Thread(target=self.initialize_transcriber, daemon=True)
        self.loading_thread.start()

        self.setup_ui()

    def initialize_transcriber(self):
        try:
            self.transcriber = FrenchTranscriber()
            self.status_label.configure(text="Modèle chargé. Prêt à transcrire.")
        except Exception as e:
            self.status_label.configure(text=f"Erreur chargement : {str(e)}")

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Transcripteur Audio Français", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=20)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Chargement du modèle...")
        self.status_label.grid(row=1, column=0, padx=20, pady=5)

        # File selection button
        self.select_button = ctk.CTkButton(self, text="Sélectionner un fichier audio", command=self.select_file)
        self.select_button.grid(row=2, column=0, padx=20, pady=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.progress_bar.set(0)

        # Text area for results
        self.result_text = ctk.CTkTextbox(self, height=200)
        self.result_text.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        # Copy button
        self.copy_button = ctk.CTkButton(self, text="Copier le texte", command=self.copy_to_clipboard)
        self.copy_button.grid(row=5, column=0, padx=20, pady=10)

        self.grid_rowconfigure(4, weight=1)

    def select_file(self):
        if not self.transcriber:
            self.status_label.configure(text="Attendez le chargement du modèle...")
            return

        file_path = filedialog.askopenfilename(
            filetypes=[("Fichiers audio", "*.mp3 *.wav *.m4a"), ("Tous les fichiers", "*.*")]
        )

        if file_path:
            self.status_label.configure(text=f"Transcription de {os.path.basename(file_path)}...")
            self.progress_bar.set(0)
            self.result_text.delete("1.0", "end")

            # Run transcription in a separate thread to keep UI responsive
            thread = threading.Thread(target=self.start_transcription, args=(file_path,), daemon=True)
            thread.start()

    def start_transcription(self, file_path):
        try:
            def update_progress(val):
                self.after(0, lambda: self.progress_bar.set(val))

            text = self.transcriber.transcribe(file_path, progress_callback=update_progress)

            self.after(0, lambda: self.on_transcription_complete(text))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Erreur : {str(e)}"))

    def on_transcription_complete(self, text):
        self.result_text.insert("1.0", text)
        self.status_label.configure(text="Transcription terminée !")

    def copy_to_clipboard(self):
        text = self.result_text.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(text)
        self.status_label.configure(text="Texte copié dans le presse-papier !")

if __name__ == "__main__":
    app = TranscriberApp()
    app.mainloop()
