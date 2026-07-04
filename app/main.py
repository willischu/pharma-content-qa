"""FastAPI application entrypoint for the pharma content QA demo."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes.generate import router as generate_router

load_dotenv()

app = FastAPI(title="Pharma Content QA", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return a simple readiness payload for local development."""
    return {"status": "ok"}
