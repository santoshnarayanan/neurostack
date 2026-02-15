from pydantic import BaseModel
from typing import Dict

class GenerateRequest(BaseModel):
    model: str
    prompt: str

class GenerateResponse(BaseModel):
    model: str
    response: str
    latency_ms: float
    tokens_per_sec: float

class CompareRequest(BaseModel):
    prompt: str

class CompareResponse(BaseModel):
    results: Dict[str, str]
