import os
from typing import List, Set

import requests

from http_requests.client_interface import IClient
from http_requests.http_client_provider import HttpClientProvider
from middleware.schemas.trip import TripRequest, Trip, Pin


class TripService:
    def __init__(self):
        self.client: IClient = HttpClientProvider.get_client()

        self.core_optimizer_url = os.getenv("CORE_OPTIMIZER_URL")
        self.open_route_service_url = os.getenv("OPEN_ROUTE_SERVICE_URL")
        self.open_route_service_token = os.getenv("OPEN_ROUTE_SERVICE_TOKEN")

        self._cache_pins()

    def _cache_pins(self) -> None:
        data = self._get_location_coordinates_json()
        pins = {}
        for json_data in data:
            self._set_pin(json_data, pins)

        self.cached_pins = pins

    def _get_location_coordinates_json(self) -> dict:
        url = f'{self.core_optimizer_url}/location-coordinates'
        response = self.client.get(url)
        data = response.json()
        print(f'fetched {len(data)} location coordinates from database')
        return data

    def _set_pin(self, json_data: dict, pins: dict) -> None:
        location_id = json_data['locationId']
        pins[location_id] = Pin(
            startLocationId=json_data['locationId'],
            latitude=json_data['latitude'],
            longitude=json_data['longitude']
        )

    def get_pins_and_route(self, request: TripRequest) -> dict:
        pins = self._get_pins(request.trips)
        route = self._get_route(pins)
        return {'pins': pins, 'route': route}

    def _get_pins(self, trips: List[Trip]) -> List[Pin]:
        pins = set()
        for trip in trips:
            self._add_if_exists(trip.startLocationId, pins)
            self._add_if_exists(trip.endLocationId, pins)
        pins = list(pins)
        return pins

    def _add_if_exists(self, location_id: int, pins: Set[Pin]) -> None:
        location_id_string = str(location_id)
        if location_id_string in self.cached_pins:
            pin = self.cached_pins[location_id_string]
            pins.add(pin)
        else:
            print(f'Location ID {location_id_string} not found in location coordinates.')

    def _get_route(self, pins: List[Pin]) -> dict:
        url = self.open_route_service_url
        payload = {
            'coordinates': [
                [pin.longitude, pin.latitude] for pin in pins
            ]
        }
        headers = {
            'Authorization': self.open_route_service_token,
            'Content-Type': 'application/json'
        }

        response = requests.post(url=url, headers=headers, json=payload)
        data = response.json()
        return data
