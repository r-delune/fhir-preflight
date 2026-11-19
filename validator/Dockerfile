FROM eclipse-temurin:17-jre-jammy@sha256:aa6381384f8db99762fa7d0d3c2b5de58874e5f12c96df4c13a1455376ae0ed1 AS java
FROM python:3.12-slim-bookworm@sha256:935c3c5b12357a7e10caa9c1e6ca5692344d97cf229832ef584be2cec9fc03df
COPY --from=java /opt/java/openjdk /opt/java/openjdk
ENV PATH="/opt/java/openjdk/bin:${PATH}"
WORKDIR /work
RUN useradd --create-home --uid 10001 preflight
COPY validator validator
COPY fhir fhir
COPY .cache/validator/validator_cli.jar .cache/validator/validator_cli.jar
RUN python -c "import hashlib; from validator.runner import CONFIG,JAR; assert hashlib.sha256(JAR.read_bytes()).hexdigest() == CONFIG['validator_sha256']"
USER preflight
# Populate FHIR packages while building. Runtime requests prohibit all HTTP access.
RUN python -m validator.runner --bootstrap
CMD ["python", "-m", "validator.server"]
