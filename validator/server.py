"""Development-only HTTP boundary; all validation is delegated to HL7 Java."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import BoundedSemaphore

from validator.inventory import inventory
from validator.runner import CONFIG, ValidatorUnavailable, validate
from validator.runner import ROOT as PROJECT_ROOT

SLOT = BoundedSemaphore(1)
MAX_BYTES = 1_000_000


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status: int, value: dict):
        body = json.dumps(value).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/health":
            self.send_json(404, {"error": "Not found"})
            return
        self.send_json(200, {"service": "validator", "version": CONFIG["validator_version"]})

    def do_POST(self):
        if self.path != "/validate":
            self.send_json(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_BYTES:
                self.send_json(413, {"status": "incomplete", "error": "Payload size rejected"})
                return
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("Expected a JSON resource object")
        except (ValueError, UnicodeError):
            self.send_json(400, {"status": "incomplete", "error": "Invalid JSON object"})
            return
        if not SLOT.acquire(blocking=False):
            self.send_json(503, {"status": "incomplete", "error": "Validator busy; retry later"})
            return
        try:
            self.send_json(200, validate(payload))
        except ValidatorUnavailable as exc:
            self.send_json(503, {"status": "incomplete", "error": str(exc)})
        finally:
            SLOT.release()


if __name__ == "__main__":
    if inventory() != json.loads((PROJECT_ROOT / "validator/packages.lock.json").read_text()):
        raise RuntimeError("FHIR package inventory mismatch; refusing to serve.")
    ThreadingHTTPServer(("0.0.0.0", 8081), Handler).serve_forever()
