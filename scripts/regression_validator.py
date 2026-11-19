"""Real-validator fixture checks; save evidence without making any AI calls."""

import collections
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "valid-infant-weight": {"status": "pass", "terms": []},
    "broken-structure": {"status": "fail", "terms": ["status", "decimal"]},
    "broken-profile-and-reference": {
        "status": "fail", "terms": ["29463-7", "demo-subject-1", "g"]
    },
}


def main() -> int:
    destination = ROOT / "docs/examples/step-1"
    destination.mkdir(parents=True, exist_ok=True)
    rows = []
    failed = False
    for name, expected in CASES.items():
        run = subprocess.run([
            sys.executable, str(ROOT / "scripts/validate.py"),
            str(ROOT / f"fhir/fixtures/{name}.json"), "--envelope",
        ], capture_output=True, text=True, timeout=250, check=False)
        if run.returncode not in {0, 1}:
            print(f"{name}: incomplete — {run.stderr}", file=sys.stderr)
            failed = True
            continue
        result = json.loads(run.stdout)
        (destination / f"{name}.json").write_text(json.dumps(result, indent=2) + "\n")
        issues = result["outcome"]["issue"]
        errors = [issue for issue in issues if issue["severity"] in {"error", "fatal"}]
        text = json.dumps(errors)
        missing = [term for term in expected["terms"] if term not in text]
        success = result["status"] == expected["status"] and not missing
        failed |= not success
        counts = dict(collections.Counter(issue["severity"] for issue in issues))
        rows.append({
            "fixture": name, "expected": expected["status"], "actual": result["status"],
            "counts": counts, "expected_error_terms_missing": missing, "matched": success,
        })
        print(f"{name}: {result['status']} — {counts}; expectation matched: {success}")
    (destination / "summary.json").write_text(json.dumps(rows, indent=2) + "\n")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
