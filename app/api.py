from fastapi import FastAPI, Query
from pydantic import BaseModel

from app.encryption import EncryptionLevel
from app.services.ollama_service import OllamaService


app = FastAPI(title="Encryption Simulation API")
service = OllamaService()


@app.get("/getting_plaintext")
def get_plain_message():
    return {"plaintext": service.generate_plaintext()}


@app.get("/getting_ciphertext")
def get_cipher_message(level: EncryptionLevel | None = Query(default=None)):
    return {"ciphertext": service.get_ciphertext(level)}


class PlayerAnswer(BaseModel):
    message: str


@app.post("/evaluating_message")
def eval_message(request: PlayerAnswer):
    similarity_score = service.evaluate_analysis(request.message)
    return {"similarity_score": similarity_score}
