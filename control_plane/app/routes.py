from fastapi import APIRouter
from app.services import generate_response, compare_models
from app.schemas import GenerateRequest, CompareRequest, GenerateResponse
from app.config import config

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "healthy"}


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    model = request.model or config["default_model"]
    return generate_response(model, request.prompt)



@router.post("/compare")
def compare(request: CompareRequest):
    return compare_models(request.prompt)
