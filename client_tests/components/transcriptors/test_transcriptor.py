import unittest
from unittest.mock import patch, MagicMock
from client.components.transcriptors.transcriptor import Transcriptor
from requests import HTTPError


class TestTranscriptor(unittest.TestCase):
    def setUp(self):
        self.transcription_service_url = "http://127.0.0.1:8000/v1/speech/transcribe"
        self.transcriptor = Transcriptor(self.transcription_service_url)

    @patch("requests.post")
    def test_transcribe_valid_file_path_returns_consistent_transcription(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"transcription": "Hey, I'm Driver P5 and I'm not feeling well today. I'm sorry but I can't take my shift."}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        file_path = "./../data/bad_test_english/iamdriverp5.wav"
        expected_transcription = "Hey, I'm Driver P5 and I'm not feeling well today. I'm sorry but I can't take my shift."

        for _ in range(100):
            transcription = self.transcriptor.transcribe(file_path)
            mock_post.assert_called_with(f"{self.transcription_service_url}?filepath={file_path}")
            self.assertEqual(transcription, expected_transcription)

        self.assertEqual(mock_post.call_count, 100)