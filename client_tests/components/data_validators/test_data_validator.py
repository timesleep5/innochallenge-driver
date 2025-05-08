from unittest import TestCase

from client.components.data_validators.data_validator import DataValidator


class TestDataValidator(TestCase):
    def setUp(self):
        self.validator = DataValidator()

    def test_validate_data_valid_json_returns_true(self):
        truck_driver_json = {
            'id': 'D01',
            'type': 'truck-drivers',
            'active': True
        }

        truck_json = {
            'id': 'TK1',
            'type': 'trucks',
            'active': True
        }

        trailer_json = {
            'id': 'TR1',
            'type': 'trailers',
            'active': True
        }

        truck_driver_json_is_valid = self.validator.validate_data(truck_driver_json)
        truck_json_is_valid = self.validator.validate_data(truck_json)
        trailer_json_is_valid = self.validator.validate_data(trailer_json)

        self.assertTrue(truck_driver_json_is_valid)
        self.assertTrue(truck_json_is_valid)
        self.assertTrue(trailer_json_is_valid)

    def test_validate_data_empty_json_returns_false(self):
        empty_json = {}

        is_empty_json_valid = self.validator.validate_data(empty_json)

        self.assertFalse(is_empty_json_valid)

    def test_validate_data_missing_keys_json_returns_false(self):
        missing_keys_json_1 = {
            'id': 'D01',
            'type': 'truck-drivers'
        }

        missing_keys_json_2 = {
            'id': 'D01',
            'active': True
        }

        missing_keys_json_3 = {
            'type': 'truck-drivers',
            'active': True
        }

        is_missing_keys_json_valid_1 = self.validator.validate_data(missing_keys_json_1)
        is_missing_keys_json_valid_2 = self.validator.validate_data(missing_keys_json_2)
        is_missing_keys_json_valid_3 = self.validator.validate_data(missing_keys_json_3)

        self.assertFalse(is_missing_keys_json_valid_1)
        self.assertFalse(is_missing_keys_json_valid_2)
        self.assertFalse(is_missing_keys_json_valid_3)

    def test_validate_data_wrong_datatype_json_returns_false(self):
        wrong_datatype_json_type = {
            'id': 'D01',
            'type': 1,
            'active': True
        }

        wrong_datatype_json_id = {
            'id': 1,
            'type': 'truck-drivers',
            'active': True
        }

        wrong_datatype_json_active = {
            'id': 'D01',
            'type': 'truck-drivers',
            'active': '1'
        }

        is_wrong_datatype_json_valid_type = self.validator.validate_data(wrong_datatype_json_type)
        is_wrong_datatype_json_valid_id = self.validator.validate_data(wrong_datatype_json_id)
        is_wrong_datatype_json_valid_active = self.validator.validate_data(wrong_datatype_json_active)

        self.assertFalse(is_wrong_datatype_json_valid_type)
        self.assertFalse(is_wrong_datatype_json_valid_id)
        self.assertFalse(is_wrong_datatype_json_valid_active)

    def test_validate_data_wrong_enum_returns_false(self):
        wrong_enum_json = {
            'id': 'D01',
            'type': 'nonexistent-enum-value',
            'active': True
        }

        is_wrong_enum_json_valid = self.validator.validate_data(wrong_enum_json)

        self.assertFalse(is_wrong_enum_json_valid)

    def test_validate_data_valid_data_but_nonexistent_value_returns_false(self):
        nonexistent_value_json = {
            'id': 'D00',
            'type': 'truck-drivers',
            'active': True
        }

        is_nonexistent_value_json_valid = self.validator.validate_data(nonexistent_value_json)

        self.assertFalse(is_nonexistent_value_json_valid)
