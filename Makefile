UV_CACHE_DIR ?= /private/tmp/fhir-preflight-uv-cache
export UV_CACHE_DIR

.PHONY: setup dev dev-python stop build-metadata validator-download validate regression test lint trace
setup:
	uv sync --locked
validator-download:
	python3.12 scripts/download_validator.py
build-metadata:
	python3.12 scripts/prepare_build_metadata.py
dev: validator-download build-metadata
	docker compose up --build -d --wait
dev-python:
	uv run --locked uvicorn app.main:app --reload --host 127.0.0.1
stop:
	docker compose down
validate:
	python3.12 scripts/validate.py $(or $(FILE),fhir/fixtures/valid-infant-weight.json)
regression:
	python3.12 scripts/regression_validator.py
test:
	MODEL_ADAPTER=mock uv run --locked pytest
	node --test tests/frontend.test.cjs
lint:
	uv run --locked ruff check .
trace:
	@echo "Traceability generator is scheduled for Step 6; see docs/TRACEABILITY.md."
