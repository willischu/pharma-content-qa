"""Routes for rendering the UI and generating marketing content."""

from typing import Any, Literal

from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app.services.ai_client import generate_content

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


class GenerateRequest(BaseModel):
    """Input payload for content generation requests."""

    prompt: str = Field(..., min_length=1)
    drug_name: str = Field(..., min_length=1)
    channel: Literal["social_media", "email", "web"]
    source_docs: dict[str, Any] = Field(default_factory=dict)


@router.get("/")
async def index(request: Request) -> Any:
    """Render the single-page UI used by the Playwright test harness."""
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})


@router.post("/api/generate")
async def generate(payload: GenerateRequest) -> dict[str, str]:
    """Generate compliant marketing content from the provided prompt and source docs."""
    try:
        content = generate_content(
            prompt=payload.prompt,
            drug_name=payload.drug_name,
            channel=payload.channel,
            source_docs=payload.source_docs,
        )
    except Exception as exc:  # pragma: no cover - defensive guard
        raise HTTPException(status_code=500, detail="Failed to generate content.") from exc

    return {"content": content}
