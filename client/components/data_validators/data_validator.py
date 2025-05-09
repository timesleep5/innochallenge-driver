from dataclasses import dataclass

import requests
from requests import HTTPError

from client.components.data_validators.interface import IDataValidator
from client.config.config import backend_truck_drivers_url, backend_trailers_url, backend_trucks_url


@dataclass
class TypeConfig:
    id_prefix: str
    backend_url: str
    backend_id_key: str


class DataValidator(IDataValidator):
    def __init__(self):
        self.required_keys = {'id', 'type', 'active'}
        self.types = {
            'truck-drivers': TypeConfig(
                id_prefix='D',
                backend_url=backend_truck_drivers_url,
                backend_id_key='driverId'
            ),
            'trailers': TypeConfig(
                id_prefix='TR',
                backend_url=backend_trailers_url,
                backend_id_key='trailerId'
            ),
            'trucks': TypeConfig(
                id_prefix='TK',
                backend_url=backend_trucks_url,
                backend_id_key='truckId'
            )
        }

    def validate_data(self, data: dict) -> bool:
        if not self._required_keys_exist(data):
            print("Validation failed: Missing required keys.")
            return False

        if not self._fields_are_valid(data):
            print("Validation failed: One or more fields are invalid.")
            return False

        if not self._id_value_exists_in_database(data):
            print(f"Validation failed: ID '{data.get('id')}' does not exist in the database.")
            return False

        return True

    def _required_keys_exist(self, data: dict) -> bool:
        return self.required_keys.issubset(data.keys())

    def _fields_are_valid(self, data: dict) -> bool:
        if not self._type_field_is_valid(data):
            return False

        if not self._active_field_is_valid(data):
            return False

        if not self._id_field_is_valid(data):
            return False

        return True

    def _type_field_is_valid(self, data: dict) -> bool:
        vehicle_type = data.get('type')
        return vehicle_type in self.types.keys()

    def _active_field_is_valid(self, data: dict) -> bool:
        active_field = data.get('active')
        return isinstance(active_field, bool)

    def _id_field_is_valid(self, data: dict) -> bool:
        id_value = data.get('id')
        vehicle_type = data.get('type')
        type_config = self.types.get(vehicle_type)

        is_string = isinstance(id_value, str)
        is_properly_formatted = is_string and id_value.startswith(type_config.id_prefix)
        return is_properly_formatted

    def _id_value_exists_in_database(self, data: dict) -> bool:
        id_value = data.get('id')
        vehicle_type = data.get('type')
        type_config = self.types.get(vehicle_type)
        return self._exists_in_database(id_value, type_config)

    def _exists_in_database(self, id_value: str, type_config: TypeConfig) -> bool:
        backend_url = type_config.backend_url
        backend_id_key = type_config.backend_id_key
        try:
            response = requests.get(backend_url)
            response.raise_for_status()
            data = response.json()
            existing_ids = {object[backend_id_key] for object in data}
            return id_value in existing_ids

        except HTTPError:
            return False
