from fastapi import FastAPI, Depends
from innovation.routers.speech_router import router as speech_router
from innovation.routers.llm_router import router as llm_router
from innovation.services.speech_service import SpeechService

app = FastAPI()

# Globale Instanz von SpeechService
speech_service = SpeechService()

# Router registrieren und Instanz weitergeben
app.include_router(speech_router, prefix="/speech", tags=["Speech"], dependencies=[Depends(lambda: speech_service)])
app.include_router(llm_router, prefix="/llm", tags=["LLM"], dependencies=[Depends(lambda: speech_service)])

@app.get("/")
def root():
    return {"message": "API up and running!"}