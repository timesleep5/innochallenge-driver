from fastapi import APIRouter

from middleware.schemas.trip import TripRequest
from middleware.services.trip_service import TripService

router = APIRouter()
trip_service = TripService()


@router.put("/geo")
def start_recording(request: TripRequest):
    return trip_service.get_pins_and_route(request)
