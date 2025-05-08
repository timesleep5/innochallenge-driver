from fastapi import FastAPI, Depends
from middleware.routers.speech_router import router as speech_router
from middleware.routers.llm_router import router as llm_router
from middleware.services.speech_service import SpeechService

app = FastAPI()

# Globale Instanz von SpeechService
speech_service = SpeechService()

# Router registrieren und Instanz weitergeben
app.include_router(speech_router, prefix="/v1/speech", tags=["Speech"], dependencies=[Depends(lambda: speech_service)])
app.include_router(llm_router, prefix="/v1/llm", tags=["LLM"], dependencies=[Depends(lambda: speech_service)])

@app.get("/")
def root():
    return {"message": "API up and running!"}