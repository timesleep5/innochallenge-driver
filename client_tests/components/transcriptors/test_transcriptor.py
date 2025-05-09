import unittest

from client.components.transcriptors.transcriptor import Transcriptor


class TestTranscriptor(unittest.TestCase):
    def setUp(self):
        self.transcription_service_url = "http://127.0.0.1:8000/v1/speech/transcribe"
        self.transcriptor = Transcriptor(self.transcription_service_url)

    def test_transcribe_valid_file_path_returns_consistent_transcription(self):
        file_path = "./../data/bad_test_english/iamdriverp5.wav"
        expected_transcription = "Hey, I'm Driver P5 and I'm not feeling well today. I'm sorry but I can't take my shift."

        for _ in range(100):
            transcription = self.transcriptor.transcribe(file_path)

            self.assertEqual(transcription, expected_transcription)
