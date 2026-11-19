"""Send a synthetic FHIR file to the local validator; print raw OperationOutcome."""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--url", default="http://127.0.0.1:8002/api/validate")
    parser.add_argument(
        "--envelope", action="store_true", help="Include status, checks and provenance"
    )
    args = parser.parse_args()
    try:
        data = args.file.read_bytes()
        json.loads(data)
        request = urllib.request.Request(
            args.url, data=data, headers={"Content-Type": "application/fhir+json"}, method="POST"
        )
        with urllib.request.urlopen(request, timeout=240) as response:
            result = json.load(response)
        if result.get("status") not in {"pass", "fail"}:
            raise ValueError("Incomplete validator response")
        print(json.dumps(result if args.envelope else result["outcome"], indent=2))
        print(f"Validation: {result['status']} (remote terminology disabled)", file=sys.stderr)
        return 0 if result["status"] == "pass" else 1
    except (OSError, ValueError, KeyError, urllib.error.URLError) as exc:
        print(f"Validation incomplete: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
