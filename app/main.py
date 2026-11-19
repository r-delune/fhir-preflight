import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.adapters.mock import MockModelAdapter
from app.services.validation import ValidationServiceError, request_validation


def create_app() -> FastAPI:
    # Fail visibly rather than quietly using a different provider.
    if os.getenv("MODEL_ADAPTER", "mock") != "mock":
        raise RuntimeError("Step 0 supports MODEL_ADAPTER=mock only.")
    application = FastAPI(title="FHIR Preflight", version="0.0.0")
    adapter = MockModelAdapter()
    templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

    @application.get("/", response_class=HTMLResponse)
    def home(request: Request):
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"model_status": adapter.describe()},
        )

    @application.post("/api/validate")
    def validate_payload(payload: dict):
        try:
            return request_validation(payload)
        except ValidationServiceError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    return application


app = create_app()
