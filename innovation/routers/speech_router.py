from fastapi import APIRouter
from innovation.services.speech_service import SpeechService

router = APIRouter()
speech_service = SpeechService()

@router.post("/start")
def start_recording():
    """Startet die Sprachaufnahme."""
    return speech_service.start_recording()

@router.post("/stop")
def stop_recording():
    """Beendet die Sprachaufnahme."""
    return speech_service.stop_recording()

@router.get("/results")
def get_results():
    """Gibt die erkannten Texte zurück."""
    return speech_service.get_results()