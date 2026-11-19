"""Explicit manual smoke probe. Never called by the app, CI or unit tests."""

import argparse
import json
import os
import time
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from model.config import REVISION, SERVED_NAME


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward a bearer token to another host.


def check_url(value):
    parsed = urlsplit(value)
    if (parsed.scheme != "https" or not parsed.hostname
            or not parsed.hostname.endswith(".modal.run")
            or parsed.username or parsed.password or parsed.query or parsed.fragment
            or parsed.path not in ("", "/") or parsed.port not in (None, 443)):
        raise ValueError("Use the HTTPS root URL of the approved modal.run endpoint")
    return value.rstrip("/")


def completion(client, url, key, clock=time.perf_counter):
    body = {
        "model": SERVED_NAME,
        "messages": [{"role": "user", "content": "Reply with exactly: synthetic smoke test"}],
        "max_tokens": 32, "temperature": 0,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    request = Request(
        url + "/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    started = clock()
    with client.open(request, timeout=600) as response:
        result = json.load(response)
    elapsed = clock() - started
    if result.get("model") != SERVED_NAME:
        raise ValueError("Unexpected model identity; no fallback allowed")
    content = result["choices"][0]["message"]["content"]
    if content.strip() != "synthetic smoke test":
        raise ValueError("Unexpected smoke response; inspect privately, do not claim success")
    tokens = result["usage"]["completion_tokens"]
    return {"seconds": elapsed, "completion_tokens": tokens,
            "end_to_end_tokens_per_second": tokens / elapsed if elapsed > 0 else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--confirmed-cold", action="store_true",
                        help="Only after dashboard confirms zero containers before this probe")
    args = parser.parse_args()
    url = check_url(args.url)
    key = os.environ.get("PREFLIGHT_API_KEY", "")
    if len(key) < 32:
        raise ValueError("Set PREFLIGHT_API_KEY securely; do not pass it as a CLI argument")
    client = build_opener(NoRedirects())
    # Inference comes first: the auth probe itself could otherwise wake a container.
    first = completion(client, url, key)
    warm = completion(client, url, key)
    try:
        client.open(Request(url + "/v1/models"), timeout=60)
    except HTTPError as error:
        if error.code != 401:
            raise RuntimeError("Unexpected unauthenticated API status") from None
    else:
        raise RuntimeError("API authentication check failed")
    print(json.dumps({"model": SERVED_NAME, "revision": REVISION,
                      "first_call": first, "cold_precondition_confirmed": args.confirmed_cold,
                      "warm_call": warm, "unauthenticated_status": 401}, indent=2))


if __name__ == "__main__":
    main()
