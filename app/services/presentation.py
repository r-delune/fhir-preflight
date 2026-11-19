"""Display helpers. They navigate JSON and never perform FHIR validation."""

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

FIXTURES = {
    "valid-infant-weight": ("Complete weight example", "A complete fictional measurement."),
    "broken-structure": ("Structural errors", "A missing status and a number supplied as text."),
    "broken-profile-and-reference": (
        "Profile & reference errors",
        "Wrong measurement code, wrong unit and a missing patient link."
    ),
}
FIXTURE_ROOT = Path(__file__).resolve().parents[2] / "fhir/fixtures"


def load_fixture(name: str) -> dict:
    if name not in FIXTURES:
        raise KeyError(name)
    return json.loads((FIXTURE_ROOT / f"{name}.json").read_text())


def normalize(text: str) -> str:
    return re.sub(r"/tmp/fhir-preflight-[^/\s]+/input\.json", "<input>", text)


def issue_id(issue: dict) -> str:
    semantic = {
        "severity": issue.get("severity"), "code": issue.get("code"),
        "message": normalize(issue.get("details", {}).get("text", "")),
        "diagnostics": normalize(issue.get("diagnostics", "")),
        "locations": sorted(normalize(p) for p in issue.get(
            "expression", issue.get("location", [])
        )),
        "message_type": sorted(
            e.get("valueCode", "") for e in issue.get("extension", [])
            if e.get("url", "").endswith("operationoutcome-message-id")
        ),
    }
    digest = hashlib.sha256(json.dumps(semantic, sort_keys=True).encode()).hexdigest()
    return "VAL-" + digest[:16].upper()


def nested_message(text: str) -> str | None:
    """Extract a verbatim nested message, never synthesize an explanation."""
    match = re.search(r"\bmessage=", text)
    if not match:
        return None
    start, depth, quote, escaped = match.end(), 0, None, False
    end = len(text)
    for index in range(start, len(text)):
        char = text[index]
        if escaped:
            escaped = False
        elif char == "\\" and quote:
            escaped = True
        elif quote:
            if char == quote:
                quote = None
        elif char in {"'", '"'} and (index == start or not text[index - 1].isalnum()):
            quote = char
        elif char == "[":
            depth += 1
        elif char == "]":
            if depth == 0:
                end = index
                break
            depth -= 1
    summary = text[start:end].strip()
    # This removes only trailing source detail, leaving an exact substring of the original.
    summary = summary.split(" in the profile ", 1)[0]
    if len(summary) > 240:
        summary = summary[:240].rsplit(" ", 1)[0]
    return summary or None


def json_lines(payload: dict) -> tuple[list[dict], dict]:
    lines, ranges = [], {}

    def render(value, path, depth=0, prefix="", suffix=""):
        start = len(lines) + 1

        def emit(text):
            lines.append({"number": len(lines) + 1, "text": "  " * depth + text})

        if isinstance(value, (dict, list)) and value:
            opening, closing = ("{", "}") if isinstance(value, dict) else ("[", "]")
            emit(prefix + opening)
            items = list(value.items()) if isinstance(value, dict) else list(enumerate(value))
            for index, (key, child) in enumerate(items):
                child_prefix = json.dumps(key) + ": " if isinstance(value, dict) else ""
                render(child, path + (key,), depth + 1, child_prefix,
                       "," if index < len(items) - 1 else "")
            emit(closing + suffix)
        else:
            emit(prefix + json.dumps(value, ensure_ascii=False) + suffix)
        ranges[path] = (start, len(lines))

    render(payload, ())
    return lines, ranges


def locate(payload: dict, expression: str, ranges: dict) -> dict:
    """Resolve only known emitted path forms; fall back honestly, never evaluate code."""
    path = re.sub(r"/\*.*?\*/", "", expression).strip()
    path = re.sub(r"\.ofType\((?:FHIR\.)?([A-Za-z0-9]+)\)",
                  lambda m: m.group(1)[0].upper() + m.group(1)[1:], path)
    parts = path.split(".")
    if not parts or parts[0] != payload.get("resourceType"):
        return {"start": 0, "end": 0, "note": "Location could not be mapped to this JSON."}
    current, pointer = payload, ()
    exact = True
    for part in parts[1:]:
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)(?:\[(\d+)\])?", part.replace("[x]", ""))
        if not match or not isinstance(current, dict):
            exact = False
            break
        key, index = match.groups()
        if key not in current:
            choices = [k for k in current if k.startswith(key) and len(k) > len(key)
                       and k[len(key)].isupper()]
            if len(choices) != 1:
                exact = False
                break
            key = choices[0]
        pointer += (key,)
        current = current[key]
        if index is not None:
            index = int(index)
            if not isinstance(current, list) or index >= len(current):
                exact = False
                break
            pointer += (index,)
            current = current[index]
    start, end = ranges.get(pointer, (0, 0))
    return {
        "start": start, "end": end,
        "note": "Matching JSON location highlighted." if exact else
        "Closest matching parent highlighted; the exact field may be missing or path unsupported.",
    }


def present(payload: dict, result: dict | None = None) -> dict:
    lines, ranges = json_lines(payload)
    issues = []
    if result:
        for issue in result["outcome"]["issue"]:
            locations = issue.get("expression") or issue.get("location") or []
            mapped = [locate(payload, path, ranges) for path in locations]
            location = next((m for m in mapped if m["start"]), {
                "start": 0, "end": 0, "note": "No mapped location supplied by the validator."
            })
            message = issue.get("details", {}).get("text") or issue.get("diagnostics", "")
            issues.append({
                "id": issue_id(issue), "severity": issue["severity"],
                "message": message, "summary": nested_message(message),
                "paths": locations, **location,
            })
        order = {"fatal": 0, "error": 1, "warning": 2, "information": 3}
        issues.sort(key=lambda i: (order.get(i["severity"], 4), i["id"]))
    return {"lines": lines, "issues": issues,
            "counts": Counter(i["severity"] for i in issues)}
