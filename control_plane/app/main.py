from fastapi import FastAPI, Request
from app.routes import router
import time
import uuid
from app.logger import get_logger

logger = get_logger("neurostack")

app = FastAPI(title="NeuroStack AI Control Plane")

@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    logger.info(
        f"request_id={request_id} method={request.method} "
        f"path={request.url.path} latency_ms={round(process_time,2)}"
    )

    response.headers["X-Request-ID"] = request_id
    return response

app.include_router(router)
