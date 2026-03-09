import unittest
from unittest.mock import MagicMock, patch, sys
import numpy as np

# Mocking sounddevice and pynput before importing our modules
mock_sd = MagicMock()
sys.modules['sounddevice'] = mock_sd
sys.modules['pynput'] = MagicMock()
sys.modules['pyperclip'] = MagicMock()
sys.modules['pyautogui'] = MagicMock()
sys.modules['pystray'] = MagicMock()

from transcriber import FrenchTranscriber
from recorder import AudioRecorder
from tokk_handler import TokkHandler

class TestTokkComponents(unittest.TestCase):

    @patch('transformers.Wav2Vec2Processor.from_pretrained')
    @patch('transformers.Wav2Vec2ForCTC.from_pretrained')
    def test_transcriber_numpy(self, mock_model_from, mock_proc_from):
        import torch
        # Mock processor and model
        mock_proc = MagicMock()
        mock_model = MagicMock()
        mock_proc_from.return_value = mock_proc
        mock_model_from.return_value = mock_model
        mock_model.to.return_value = mock_model

        transcriber = FrenchTranscriber()

        # Create dummy audio data
        audio_data = np.zeros(16000) # 1 second at 16kHz

        # Mock processor output
        mock_input = MagicMock()
        mock_input.input_values = torch.zeros(1, 100)
        mock_proc.return_value = mock_input

        # Mock model output
        mock_output = MagicMock()
        mock_output.logits = torch.zeros(1, 10, 32)
        mock_model.return_value = mock_output

        # Mock decoding
        mock_proc.batch_decode.return_value = ["test transcription"]

        result = transcriber.transcribe(audio_data)
        self.assertEqual(result, "test transcription")

    def test_recorder_basic(self):
        recorder = AudioRecorder()

        # Simulation: stop returns some dummy data
        recorder.audio_data = [np.zeros((1024, 1), dtype='float32')]
        recorder.recording = True
        recorder._thread = MagicMock()

        data = recorder.stop()

        self.assertEqual(len(data), 1024)

    @patch('tokk_handler.FrenchTranscriber')
    def test_handler_process_audio(self, mock_transcriber):
        import pyperclip
        import pyautogui

        mock_transcriber_instance = MagicMock()
        mock_transcriber.return_value = mock_transcriber_instance
        mock_transcriber_instance.transcribe.return_value = "hello world"

        handler = TokkHandler()
        audio_data = np.zeros(16000)

        handler.process_audio(audio_data)

        pyperclip.copy.assert_called_with("hello world")
        pyautogui.hotkey.assert_called_with('ctrl', 'v')

if __name__ == "__main__":
    unittest.main()
