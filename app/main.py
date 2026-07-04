"""FastAPI application entrypoint for the pharma content QA demo."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

reports_dir = Path(__file__).resolve().parent.parent / "reports"
app.mount("/reports", StaticFiles(directory=str(reports_dir), html=True), name="reports")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Return a simple readiness payload for local development."""
    return {"status": "ok"}
