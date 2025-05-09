from typing import List

from pydantic import BaseModel, ConfigDict


class Trip(BaseModel):
    startLocationId: int
    endLocationId: int


class TripRequest(BaseModel):
    trips: List[Trip]


class Pin(BaseModel):
    model_config = ConfigDict(frozen=True)

    startLocationId: int
    latitude: float
    longitude: float
