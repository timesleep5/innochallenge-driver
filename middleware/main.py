import uvicorn
from fastapi import FastAPI, Depends

from middleware.routers.llm_router import router as llm_router
from middleware.routers.speech_router import router as speech_router
from middleware.routers.trip_router import router as trip_router
from middleware.services.speech_service import SpeechService

app = FastAPI()

# Globale Instanz von SpeechService
speech_service = SpeechService()

app.include_router(speech_router, prefix="/v1/speech", tags=["Speech"], dependencies=[Depends(lambda: speech_service)])
app.include_router(llm_router, prefix="/v1/llm", tags=["LLM"], dependencies=[Depends(lambda: speech_service)])
app.include_router(trip_router, prefix="/v1/trip", tags=["Trip"])


@app.get("/")
def root():
    return {"message": "API up and running!"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
