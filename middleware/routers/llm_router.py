from fastapi import APIRouter, HTTPException, Body
from middleware.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

@router.post("/process")
def process_transcription(transcription: str = Body(..., embed=True)):
    if not transcription.strip():
        raise HTTPException(status_code=400, detail="Der übergebene Text ist leer.")

    print(f"Sende an LLM: {transcription}")

    llm_response = llm_service.send_to_llm(transcription)
    return llm_response
