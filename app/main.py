import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.adapters.mock import MockModelAdapter
from app.services.document_source import ROOT
from app.services.governance import document_index, get_document
from app.services.presentation import FIXTURES, load_fixture, present
from app.services.validation import ValidationServiceError, request_validation


def create_app() -> FastAPI:
    # Fail visibly rather than quietly using a different provider.
    if os.getenv("MODEL_ADAPTER", "mock") != "mock":
        raise RuntimeError("This build supports MODEL_ADAPTER=mock only.")
    enable_api_docs = os.getenv("ENABLE_API_DOCS") == "1"
    application = FastAPI(
        title="FHIR Preflight", version="0.0.0",
        docs_url="/docs" if enable_api_docs else None,
        redoc_url="/redoc" if enable_api_docs else None,
        openapi_url="/openapi.json" if enable_api_docs else None,
    )
    adapter = MockModelAdapter()
    templates = Jinja2Templates(directory=Path(__file__).parent / "templates")
    application.mount(
        "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
    )

    def render_workbench(request, fixture, *, run=False):
        try:
            payload = load_fixture(fixture)
        except KeyError:
            raise HTTPException(status_code=404, detail="Unknown built-in fixture") from None
        result, error = None, None
        if run:
            try:
                result = request_validation(payload)
                if (not isinstance(result, dict)
                        or result.get("status") not in {"pass", "fail"}
                        or not isinstance(result.get("outcome"), dict)
                        or result.get("outcome", {}).get("resourceType") != "OperationOutcome"
                        or not isinstance(result["outcome"].get("issue"), list)
                        or not result["outcome"]["issue"]
                        or any(not isinstance(i, dict) or i.get("severity") not in {
                            "fatal", "error", "warning", "information"
                        } for i in result["outcome"]["issue"])
                        or (result["status"] == "pass" and any(
                            i["severity"] in {"error", "fatal"}
                            for i in result["outcome"]["issue"]))):
                    raise ValidationServiceError("Validator returned an incomplete result.")
            except ValidationServiceError as exc:
                error, result = str(exc), None
        return templates.TemplateResponse(
            request=request, name="index.html",
            context={"model_status": adapter.describe(), "fixtures": FIXTURES,
                     "fixture": fixture, "result": result, "error": error,
                     "stage": "findings" if result else "validator" if error else "example",
                     "validator_version": (result or {}).get("provenance", {}).get(
                         "validator_version", json.loads(
                             (ROOT / "validator/config.json").read_text())["validator_version"]),
                     **present(payload, result)},
            status_code=503 if error else 200,
        )

    @application.get("/", response_class=HTMLResponse)
    def home(request: Request, fixture: str = "broken-profile-and-reference"):
        return render_workbench(request, fixture)

    @application.post("/workbench/validate", response_class=HTMLResponse)
    def workbench_validate(request: Request, fixture: str):
        return render_workbench(request, fixture, run=True)

    @application.get("/governance", response_class=HTMLResponse)
    def governance(request: Request, doc: str = "roadmap"):
        try:
            selected = get_document(doc)
            documents = document_index()
        except FileNotFoundError:
            raise HTTPException(
                status_code=404, detail="Governance document not available"
            ) from None
        response = templates.TemplateResponse(
            request=request, name="governance.html",
            context={"document": selected, "documents": documents,
                     "groups": list(dict.fromkeys(item["group"] for item in documents))},
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; style-src 'self'; img-src 'none'; script-src 'none'; "
            "base-uri 'none'; frame-ancestors 'none'; form-action 'none'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    @application.post("/api/validate")
    def validate_payload(payload: dict):
        try:
            return request_validation(payload)
        except ValidationServiceError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    return application


app = create_app()
