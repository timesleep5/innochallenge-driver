from fastapi import UploadFile, File, APIRouter
from middleware.services.speech_service import SpeechService

router = APIRouter()
speech_service = SpeechService()

@router.post("/start")
def start_recording():
    """Startet die Sprachaufnahme."""
    return speech_service.start_recording()

@router.post("/stop/use")
def stop_recording_use():
    """Beendet die Sprachaufnahme und verwendet die Ergebnisse direkt."""
    return speech_service.stop_recording_use()

@router.post("/stop/load")
def stop_recording_load(file: UploadFile = File(...)):
    """Beendet die Sprachaufnahme und lädt die Ergebnisse für weitere Verarbeitung."""
    return speech_service.stop_recording_load(file)

@router.post("/stop/save")
def stop_recording_save():
    """Beendet die Sprachaufnahme und speichert die Ergebnisse."""
    return speech_service.stop_recording_save()