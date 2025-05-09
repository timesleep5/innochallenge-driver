import unittest
from unittest.mock import patch, MagicMock

from client.components.data_senders.data_sender import DataSender
from client.config.config import backend_url


class TestDataSender(unittest.TestCase):
    def setUp(self):
        self.data_sender = DataSender()

    @patch('client.components.data_senders.data_sender.requests.post')
    def test_send_data_post_called_with_truck_drivers(self, mock_post):
        test_data = {
            'id': 'D01',
            'type': 'truck-drivers',
            'active': False
        }

        self.run_post_test(mock_post, test_data)

    @patch('client.components.data_senders.data_sender.requests.post')
    def test_send_data_post_called_with_trucks(self, mock_post):
        test_data = {
            'id': 'TK1',
            'type': 'trucks',
            'active': True
        }

        self.run_post_test(mock_post, test_data)

    @patch('client.components.data_senders.data_sender.requests.post')
    def test_send_data_post_called_with_trailers(self, mock_post):
        test_data = {
            'id': 'TR1',
            'type': 'trailers',
            'active': True
        }

        self.run_post_test(mock_post, test_data)

    def run_post_test(self, mock_post, test_data: dict):
        self.set_up_mock_post(mock_post)

        self.data_sender.send_data(test_data)

        self.assert_post(mock_post, test_data)

    def set_up_mock_post(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

    def assert_post(self, mock_post, test_data: dict):
        id = test_data['id']
        route = test_data['type']
        active = test_data['active']

        expected_url = f'{backend_url}/{route}/{id}'
        expected_payload = {'active': active}
        expected_headers = {'Content-Type': 'application/json'}

        mock_post.assert_called_once_with(
            url=expected_url,
            json=expected_payload,
            headers=expected_headers
        )
