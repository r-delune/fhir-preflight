FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
WORKDIR /work
COPY requirements.lock .
RUN pip install --no-cache-dir --no-deps -r requirements.lock
RUN useradd --create-home --uid 10001 preflight
COPY app app
COPY fhir/fixtures fhir/fixtures
COPY validator/config.json validator/config.json
COPY docs docs
COPY *.md ./
COPY .cache/workbench-source.json .cache/workbench-source.json
RUN find /work/docs -type d -exec chmod 0555 {} + \
    && find /work/docs -type f -exec chmod 0444 {} + \
    && chmod 0444 /work/*.md /work/.cache/workbench-source.json
USER preflight
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
