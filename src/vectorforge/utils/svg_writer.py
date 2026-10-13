"""SVG writer with a strict sanitizer — no <script>, no <foreignObject>, no on*."""
from __future__ import annotations

import re
from pathlib import Path

from lxml import etree

FORBIDDEN_TAGS = {"script", "foreignObject", "iframe", "use"}
FORBIDDEN_ATTR_PREFIX = "on"
ON_ATTR = re.compile(r"^on[a-z]+$", re.IGNORECASE)
SVG_NS = "http://www.w3.org/2000/svg"


def sanitize(svg_text: str) -> str:
    parser = etree.XMLParser(resolve_entities=False, no_network=True, huge_tree=False)
    root = etree.fromstring(svg_text.encode("utf-8"), parser=parser)
    for el in list(root.iter()):
        tag = etree.QName(el).localname if isinstance(el.tag, str) else ""
        if tag in FORBIDDEN_TAGS:
            el.getparent().remove(el)
            continue
        for attr in list(el.attrib):
            if ON_ATTR.match(attr):
                del el.attrib[attr]
    return etree.tostring(root, encoding="unicode")


def write(svg_text: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(sanitize(svg_text), encoding="utf-8")
    return out_path