from fastapi import APIRouter, HTTPException

from middleware.services.llm_service import LLMService
from middleware.services.speech_service import SpeechService

router = APIRouter()
speech_service = SpeechService()
llm_service = LLMService()


@router.post("/process")
def process_transcription():
    recognized_texts = speech_service.get_results().get("recognized_text", [])
    if not recognized_texts:
        raise HTTPException(status_code=400, detail="Keine transkribierten Texte verfügbar.")

    combined_text = " ".join(recognized_texts)
    print(f"Sende an LLM: {combined_text}")

    llm_response = llm_service.send_to_llm(combined_text)
    return {"structured_response": llm_response}
