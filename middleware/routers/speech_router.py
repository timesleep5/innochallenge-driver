from fastapi import APIRouter
from middleware.services.speech_service import SpeechService

router = APIRouter()
speech_service = SpeechService()

# @router.post("/start")
# def start_recording():
#     return speech_service.start_recording()
#
# @router.post("/stop/save")
# def save_recording():
#     return speech_service.save_recording()

@router.post("/transcribe")
def transcribe_recording(filepath: str):
    return speech_service.transcribe_recording(filepath)
