from unittest import TestCase

from client.config import config
from client.config.config import find_file
from client.factory.interface import IFactory
from client.factory.pitch_factory import PitchFactory
from utils import Utils


class TestIntegration(TestCase):
    def setUp(self):
        config.file_location = find_file("../../data/right_test_german/ichbinfahrerd05.wav")
        process_factory: IFactory = PitchFactory()
        self.sound_file_provider = process_factory.create_sound_file_provider()
        self.transcriptor = process_factory.create_transcriptor()
        self.data_extractor = process_factory.create_data_extractor()
        self.data_validator = process_factory.create_data_validator()
        self.data_sender = process_factory.create_data_sender()

    def test_end_to_end(self):
        sound_file_path = self.sound_file_provider.get_sound_file()
        transcribed_text = self.transcriptor.transcribe(sound_file_path)
        extracted_data = self.data_extractor.extract_data(transcribed_text)
        is_valid = self.data_validator.validate_data(extracted_data)
        response_code = self.data_sender.send_data(extracted_data)

        expected_sound_file_path_end = 'data/right_test_german/ichbinfahrerd05.wav'
        self.assertTrue(sound_file_path.endswith(expected_sound_file_path_end))

        expected_transcribed_text = 'Hallo, ich bin Fahrer D05 und mir gehts heute nicht gut, ich kann heute leider nicht arbeiten.'
        expected_transcribed_text = Utils.prepare_for_assert(expected_transcribed_text)
        transcribed_text = Utils.prepare_for_assert(transcribed_text)
        self.assertEqual(transcribed_text, expected_transcribed_text)

        expected_extracted_data = {
            'id': 'D05',
            'type': 'truck-drivers',
            'active': False
        }
        self.assertEqual(extracted_data, expected_extracted_data)

        self.assertTrue(is_valid)

        self.assertEqual(response_code, 200)
