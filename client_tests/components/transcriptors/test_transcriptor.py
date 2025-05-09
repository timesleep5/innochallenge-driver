import unittest

from client.components.transcriptors.transcriptor import Transcriptor


class TestTranscriptor(unittest.TestCase):
    def setUp(self):
        self.transcription_service_url = "http://127.0.0.1:8000/v1/speech/transcribe"
        self.transcriptor = Transcriptor(self.transcription_service_url)

    def prepare_for_assert(self, string: str) -> str:
        return string.lower().replace(",", "").replace(".", "").replace("'", "")

    def test_transcribe_bad_english_file_returns_consistent_transcription(self):
        file_path = "./../data/bad_test_english/iamdriverp5.wav"
        expected_transcription = "Hey, I'm driver P5 and I'm not feeling well today. I'm sorry but I can't take my shift."
        expected_transcription = self.prepare_for_assert(expected_transcription)

        for _ in range(10):
            transcription = self.transcriptor.transcribe(file_path)
            transcription = self.prepare_for_assert(transcription)

            self.assertEqual(transcription, expected_transcription)

    def test_transcribe_different_files_returns_consistent_transcriptions(self):
        path_to_transcription = {
            "./../data/bad_test_english/iamdriverp5.wav": "Hey, I'm driver P5 and I'm not feeling well today. I'm sorry but I can't take my shift.",
            "./../data/bad_test_english/idontfeelwell.wav": "Hey I don't feel well.",
            "./../data/bad_test_german/fahrerp5.wav": "Hallo, ich bin Fahrer P5 und mir gehts heute nicht gut. Ich kann heute leider nicht zur Arbeit kommen",
            "./../data/bad_test_german/hallomirgehtsnichtgut.wav": "Hallo, mir gehts heute leider nicht gut",
        }

        for path, expected_transcription in path_to_transcription.items():
            transcription = self.transcriptor.transcribe(path)

            transcription = self.prepare_for_assert(transcription)
            expected_transcription = self.prepare_for_assert(expected_transcription)

            self.assertEqual(transcription, expected_transcription)
