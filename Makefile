UV_CACHE_DIR ?= /private/tmp/fhir-preflight-uv-cache
export UV_CACHE_DIR

.PHONY: setup dev test lint trace
setup:
	uv sync --locked
dev:
	uv run --locked uvicorn app.main:app --reload --host 127.0.0.1
test:
	MODEL_ADAPTER=mock uv run --locked pytest
lint:
	uv run --locked ruff check .
trace:
	@echo "Traceability generation is scheduled for Step 6; no product requirements approved yet."
