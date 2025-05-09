import unittest
from unittest.mock import patch, MagicMock

from client.components.data_senders.data_sender import DataSender
from client.config.config import backend_url


class TestDataSender(unittest.TestCase):
    def setUp(self):
        self.data_sender = DataSender()

    @patch('client.components.data_senders.data_sender.requests.patch')
    def test_send_data_post_called_with_truck_drivers(self, mock_patch):
        test_data = {
            'id': 'D01',
            'type': 'truck-drivers',
            'active': False
        }

        self.run_patch_test(mock_patch, test_data)

    @patch('client.components.data_senders.data_sender.requests.patch')
    def test_send_data_post_called_with_trucks(self, mock_patch):
        test_data = {
            'id': 'TK1',
            'type': 'trucks',
            'active': True
        }

        self.run_patch_test(mock_patch, test_data)

    @patch('client.components.data_senders.data_sender.requests.patch')
    def test_send_data_post_called_with_trailers(self, mock_patch):
        test_data = {
            'id': 'TR1',
            'type': 'trailers',
            'active': True
        }

        self.run_patch_test(mock_patch, test_data)

    def run_patch_test(self, mock_patch, test_data: dict):
        self.set_up_mock_patch(mock_patch)

        self.data_sender.send_data(test_data)

        self.assert_patch(mock_patch, test_data)

    def set_up_mock_patch(self, mock_patch):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_patch.return_value = mock_response

    def assert_patch(self, mock_patch, test_data: dict):
        id = test_data['id']
        route = test_data['type']
        active = test_data['active']

        expected_url = f'{backend_url}/{route}/{id}'
        expected_payload = {'active': active}
        expected_headers = {'Content-Type': 'application/json'}

        mock_patch.assert_called_once_with(
            url=expected_url,
            json=expected_payload,
            headers=expected_headers
        )
