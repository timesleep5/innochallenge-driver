from fastapi import APIRouter, HTTPException
from middleware.services.speech_service import SpeechService
from middleware.services.llm_service import LLMService

router = APIRouter()
speech_service = SpeechService()
llm_service = LLMService()

@router.post("/process")
def process_transcription():
    """Sendet die transkribierte Sprache an das LLM und gibt die strukturierte Antwort zurück."""
    recognized_texts = speech_service.get_results().get("recognized_text", [])
    if not recognized_texts:
        raise HTTPException(status_code=400, detail="Keine transkribierten Texte verfügbar.")

    # Kombinieren aller transkribierten Texte
    combined_text = " ".join(recognized_texts)
    print(f"Sende an LLM: {combined_text}")

    # Senden an das LLM
    llm_response = llm_service.send_to_llm(combined_text)
    return {"structured_response": llm_response}