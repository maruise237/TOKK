import torch
import librosa
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

class FrenchTranscriber:
    def __init__(self, model_id="LeBenchmark/wav2vec2-FR-7k-large"):
        print(f"Loading model {model_id} on CPU...")
        self.processor = Wav2Vec2Processor.from_pretrained(model_id)
        self.model = Wav2Vec2ForCTC.from_pretrained(model_id)
        self.model.to("cpu")
        self.sample_rate = 16000

    def transcribe(self, audio_path, chunk_length_s=30, progress_callback=None):
        """
        Transcribes an audio file with chunking to manage RAM.
        """
        # Load audio and resample to 16kHz
        speech, sr = librosa.load(audio_path, sr=self.sample_rate)

        # Calculate chunk size in samples
        chunk_size = chunk_length_s * self.sample_rate
        total_samples = len(speech)
        chunks = [speech[i:i + chunk_size] for i in range(0, total_samples, chunk_size)]

        full_transcription = []
        num_chunks = len(chunks)

        for i, chunk in enumerate(chunks):
            # Process the chunk
            input_values = self.processor(chunk, return_tensors="pt", sampling_rate=self.sample_rate).input_values

            with torch.no_grad():
                logits = self.model(input_values).logits

            # Take argmax and decode
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = self.processor.batch_decode(predicted_ids)[0]
            full_transcription.append(transcription)

            if progress_callback:
                progress_callback((i + 1) / num_chunks)

        return " ".join(full_transcription).strip()

if __name__ == "__main__":
    # Quick test if run directly
    import sys
    if len(sys.argv) > 1:
        transcriber = FrenchTranscriber()
        result = transcriber.transcribe(sys.argv[1])
        print("Transcription result:")
        print(result)
