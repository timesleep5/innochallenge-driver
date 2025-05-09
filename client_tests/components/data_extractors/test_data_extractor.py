import unittest
from unittest.mock import patch, MagicMock
from client.components.data_extractors.data_extractor import DataExtractor


class TestDataExtractor(unittest.TestCase):
    def setUp(self):
        self.llm_service_url = "http://127.0.0.1:8000/v1/llm/process"
        self.data_extractor = DataExtractor(self.llm_service_url)

    @patch("requests.post")
    def test_extract_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "driver_id": "P5",
            "status": "not feeling well",
            "action": "cannot take shift"
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        transcription = "Hey, I'm Driver P5 and I'm not feeling well today."

        for _ in range(100):
            result = self.data_extractor.extract_data(transcription)

            self.assertEqual(result, {
                "driver_id": "P5",
                "status": "not feeling well",
                "action": "cannot take shift"
            })

            mock_post.assert_called_with(self.llm_service_url, json={"transcription": transcription})
