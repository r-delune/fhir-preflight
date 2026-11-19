"""Safe Markdown presentation of the literal governance catalog."""

import html
import posixpath
import re
from urllib.parse import parse_qs, unquote, urlencode, urlsplit

from markdown_it import MarkdownIt
from markupsafe import Markup

from app.governance_catalog import DOCUMENTS
from app.services.document_source import ROOT, metadata_and_body, provenance, source_bytes


def fragment_id(text: str) -> str:
    if re.fullmatch(r"(?:req-\d+|step-\d+(?:-\d+)?|section-[a-z0-9-]+)", text):
        return text
    return "section-" + (re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "heading")


def safe_href(href: str, source_path: str) -> str | None:
    try:
        target = urlsplit(href)
    except ValueError:
        return None
    if target.scheme:
        return href if target.scheme.lower() == "https" and target.netloc else None
    if target.netloc or "\\" in href or any(ord(c) < 32 for c in href):
        return None
    fragment = "#" + fragment_id(unquote(target.fragment)) if target.fragment else ""
    if not target.path:
        return fragment or None
    if target.path == "/governance":
        key = parse_qs(target.query).get("doc", [""])[0]
        return "/governance?" + urlencode({"doc": key}) + fragment if key in DOCUMENTS else None
    if target.query:
        return None
    path = unquote(target.path)
    relative = posixpath.normpath(posixpath.join(posixpath.dirname(source_path), path))
    lookup = {value[1]: key for key, value in DOCUMENTS.items()}
    key = lookup.get(relative)
    return "/governance?" + urlencode({"doc": key}) + fragment if key else None


def render_markdown(body: str, source_path: str) -> Markup:
    renderer = MarkdownIt("js-default", {"html": False, "linkify": False})

    def link_open(tokens, index, options, env):
        token = tokens[index]
        destination = safe_href(token.attrGet("href") or "", source_path)
        if destination:
            token.attrSet("href", destination)
            if destination.startswith("https:"):
                token.attrSet("rel", "noopener noreferrer")
        else:
            token.attrs.pop("href", None)
            token.attrSet("class", "unavailable-link")
            token.attrSet("title", "This target is not exposed by the governance browser.")
        return renderer.renderer.renderToken(tokens, index, options, env)

    def image(tokens, index, options, env):
        return ('<span class="omitted-image">[Image: '
                + html.escape(tokens[index].content) + "]</span>")

    renderer.renderer.rules["link_open"] = link_open
    renderer.renderer.rules["image"] = image
    # Legacy journal anchor markers are inert; headings provide their safe equivalents.
    body = re.sub(r'^<a id="[a-z0-9-]+"></a>\s*$', "", body, flags=re.MULTILINE)
    tokens = renderer.parse(body)
    used = set()
    for index, token in enumerate(tokens):
        if token.type == "heading_open" and index + 1 < len(tokens):
            title = tokens[index + 1].content
            entry = re.match(r"#\d+[a-z]?\s+—\s+Step (\d+)", title)
            identifier = "step-" + entry[1] if entry else fragment_id(title)
            base, suffix = identifier, 1
            while identifier in used:
                suffix += 1
                identifier = f"{base}-{suffix}"
            used.add(identifier)
            token.attrSet("id", identifier)
        if token.type == "tr_open":
            for following in tokens[index + 1:]:
                if following.type == "tr_close":
                    break
                if following.type == "inline":
                    requirement = following.content.strip("` ")
                    if re.fullmatch(r"REQ-\d+", requirement):
                        token.attrSet("id", requirement.lower())
                    break
    # Only the configured renderer's escaped/generated HTML crosses this boundary.
    return Markup(renderer.renderer.render(tokens, renderer.options, {}))


def get_document(document_id: str, root=ROOT) -> dict:
    raw = source_bytes(document_id, root)
    title, path, group = DOCUMENTS[document_id]
    metadata, body = metadata_and_body(raw.decode("utf-8"))
    return {"id": document_id, "title": title, "path": path, "group": group,
            **metadata, "provenance": provenance(document_id, raw, root),
            "html": render_markdown(body, path)}


def document_index(root=ROOT) -> list[dict]:
    documents = []
    for key, (title, path, group) in DOCUMENTS.items():
        raw = source_bytes(key, root)
        metadata, _ = metadata_and_body(raw.decode("utf-8"))
        documents.append({"id": key, "title": title, "path": path, "group": group, **metadata})
    return documents
