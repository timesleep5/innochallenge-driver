import unittest

from client.components.data_extractors.data_extractor import DataExtractor


class TestDataExtractor(unittest.TestCase):
    def setUp(self):
        self.llm_service_url = "http://127.0.0.1:8000/v1/llm/process"
        self.data_extractor = DataExtractor(self.llm_service_url)

    def test_extract_success(self):
        transcription = "Hey, I'm Driver D05 and I'm not feeling well today."

        for _ in range(10):
            extracted_data = self.data_extractor.extract_data(transcription)

            expected_extracted_data = {
                "id": "D05",
                "type": "truck-drivers",
                "active": False
            }

            self.assertEqual(expected_extracted_data, extracted_data)
