from fastapi import UploadFile, File, APIRouter
from middleware.services.speech_service import SpeechService

router = APIRouter()
speech_service = SpeechService()

@router.post("/start")
def start_recording():
    """Startet die Sprachaufnahme."""
    return speech_service.start_recording()

@router.post("/stop/save")
def save_recording():
    """Beendet die Sprachaufnahme und speichert die Ergebnisse."""
    return speech_service.save_recording()

@router.post("/transcribe")
def transcribe_recording(file: UploadFile = File(...)):
    """Beendet die Sprachaufnahme und lädt die Ergebnisse für weitere Verarbeitung."""
    return speech_service.transcribe_recording(file)
