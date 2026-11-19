"""Transport to the isolated validator; never derive results from model output."""

import json
import os
import urllib.error
import urllib.request


class ValidationServiceError(RuntimeError):
    pass


def request_validation(payload: dict) -> dict:
    url = os.environ.get("VALIDATOR_URL", "http://validator:8081/validate")
    request = urllib.request.Request(
        url, data=json.dumps(payload).encode(), method="POST",
        headers={"Content-Type": "application/fhir+json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=200) as response:
            return json.load(response)
    except (OSError, ValueError, urllib.error.URLError) as exc:
        raise ValidationServiceError("Local validator unavailable or response unreadable.") from exc
