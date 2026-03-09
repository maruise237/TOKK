import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import torch
from transcriber import FrenchTranscriber

class TestFrenchTranscriber(unittest.TestCase):
    @patch('transformers.Wav2Vec2Processor.from_pretrained')
    @patch('transformers.Wav2Vec2ForCTC.from_pretrained')
    def setUp(self, mock_model_from_pretrained, mock_processor_from_pretrained):
        self.mock_processor = MagicMock()
        self.mock_model = MagicMock()

        mock_processor_from_pretrained.return_value = self.mock_processor
        mock_model_from_pretrained.return_value = self.mock_model

        # Ensure model.to("cpu") returns the mock itself
        self.mock_model.to.return_value = self.mock_model

        self.transcriber = FrenchTranscriber()

    @patch('librosa.load')
    def test_transcribe_chunking(self, mock_librosa_load):
        # Mock 40 seconds of audio at 16kHz
        sr = 16000
        duration = 40
        mock_audio = np.zeros(sr * duration)
        mock_librosa_load.return_value = (mock_audio, sr)

        # Mock processor output
        mock_input = MagicMock()
        mock_input.input_values = torch.zeros(1, 100)
        self.mock_processor.return_value = mock_input

        # Mock model output
        mock_output = MagicMock()
        mock_output.logits = torch.zeros(1, 10, 32) # Batch, Seq, Vocab
        self.mock_model.return_value = mock_output

        # Mock decoding
        self.mock_processor.batch_decode.return_value = ["test"]

        # Transcribe with 30s chunks
        result = self.transcriber.transcribe("fake_path.wav", chunk_length_s=30)

        # Should have 2 chunks (30s and 10s)
        self.assertEqual(self.mock_processor.call_count, 2)
        self.assertEqual(result, "test test")

if __name__ == "__main__":
    unittest.main()
