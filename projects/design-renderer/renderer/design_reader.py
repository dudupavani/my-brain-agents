"""Small compatibility layer for extracted design JSON files.

The extractor stores observations as {"value", "origin", "confidence"}.  This
module removes that envelope only while reading, and also accepts direct fields
so the renderer is not tied to a single JSON spelling.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Iterable


FACT_KEYS = {"value", "origin", "confidence", "note"}
MISSING_MEDIA_VALUES = {"", "unknown", "none", "null", "n/a", "not-applicable"}


class DesignError(ValueError):
    """Raised when a design file cannot describe a renderable canvas."""


def unwrap(value: Any) -> Any:
    """Recursively remove the extractor's fact envelope without losing objects."""
    if isinstance(value, dict):
        if "value" in value and set(value).issubset(FACT_KEYS):
            return unwrap(value["value"])
        return {key: unwrap(item) for key, item in value.items()}
    if isinstance(value, list):
        return [unwrap(item) for item in value]
    return value


def _lookup(mapping: Any, *names: str, default: Any = None) -> Any:
    if not isinstance(mapping, dict):
        return default
    for name in names:
        if name in mapping:
            return unwrap(mapping[name])
    return default


def _number(value: Any, default: float | None = None) -> float | None:
    value = unwrap(value)
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        found = re.search(r"-?\d+(?:\.\d+)?", value)
        if found:
            return float(found.group())
    return default


def _integer(value: Any, default: int | None = None) -> int | None:
    parsed = _number(value)
    return int(round(parsed)) if parsed is not None else default


def _text_value(element: dict[str, Any]) -> Any:
    """Return text content exactly as represented by common JSON spellings."""
    if "text" in element:
        raw = element["text"]
        if isinstance(raw, dict) and "value" in raw:
            return unwrap(raw["value"])
        if isinstance(raw, str) or raw is None:
            return raw
        if isinstance(raw, dict):
            return _lookup(raw, "content", "text", "value")
    if "value" in element:
        return unwrap(element["value"])
    if "content" in element:
        return unwrap(element["content"])
    return None


def _has_explicit_missing_media(element: dict[str, Any]) -> bool:
    raw = element.get("image", element.get("media"))
    if raw is None and ("image" in element or "media" in element):
        return True
    if isinstance(raw, dict):
        if "value" in raw and raw["value"] is None:
            return True
        unwrapped = unwrap(raw)
        if isinstance(unwrapped, dict):
            if any(unwrapped.get(key, object()) is None for key in ("src", "path", "asset", "file", "url")):
                return True
    # An image element without a resolvable source is an unresolved media slot,
    # even when the extractor only recorded descriptive fields such as `fit` or
    # `content`. This prevents the renderer from silently dropping a photo.
    return _media_source(element) is None


def _media_source(element: dict[str, Any]) -> str | None:
    for container in (element, unwrap(element.get("image")), unwrap(element.get("media"))):
        if isinstance(container, str):
            candidate = container
        elif isinstance(container, dict):
            candidate = _lookup(container, "src", "path", "asset", "file", "url", "value")
        else:
            continue
        if isinstance(candidate, str) and candidate.strip().lower() not in MISSING_MEDIA_VALUES:
            return candidate
    return None


def _bbox(element: dict[str, Any], canvas: tuple[int, int]) -> tuple[int, int, int, int]:
    """Read pixel geometry first, then normalized geometry as a fallback."""
    width, height = canvas
    raw = _lookup(element, "bbox_px", "bboxPx", "boundsPx", "bounds", "bbox", "geometry", default={})
    if isinstance(raw, (list, tuple)) and len(raw) == 4:
        return tuple(int(round(_number(item, 0) or 0)) for item in raw)  # type: ignore[return-value]
    raw = unwrap(raw) if isinstance(raw, dict) else {}

    x = _number(_lookup(raw, "xPx", "x_px", "leftPx", "left"))
    y = _number(_lookup(raw, "yPx", "y_px", "topPx", "top"))
    w = _number(_lookup(raw, "widthPx", "width_px", "wPx", "w"))
    h = _number(_lookup(raw, "heightPx", "height_px", "hPx", "h"))
    if None not in (x, y, w, h):
        return int(round(x)), int(round(y)), int(round(w)), int(round(h))

    norm = _lookup(element, "bbox_norm", "bboxNorm", "boundsNorm", default=raw)
    if isinstance(norm, (list, tuple)) and len(norm) == 4:
        nx, ny, nw, nh = (_number(item, 0) or 0 for item in norm)
    else:
        norm = unwrap(norm) if isinstance(norm, dict) else {}
        nx = _number(_lookup(norm, "x", "left"), 0) or 0
        ny = _number(_lookup(norm, "y", "top"), 0) or 0
        nw = _number(_lookup(norm, "width", "w"), 0) or 0
        nh = _number(_lookup(norm, "height", "h"), 0) or 0
    return round(nx * width), round(ny * height), round(nw * width), round(nh * height)


@dataclass(frozen=True)
class Element:
    id: str
    type: str
    role: str
    bbox: tuple[int, int, int, int]
    z_index: int
    raw: dict[str, Any]
    source_index: int

    @property
    def typography(self) -> dict[str, Any]:
        style = _lookup(self.raw, "typography", "textStyle", "style", default={})
        return style if isinstance(style, dict) else {}


@dataclass(frozen=True)
class Slot:
    id: str
    kind: str
    role: str
    bbox: tuple[int, int, int, int]
    element: Element


@dataclass(frozen=True)
class Design:
    path: Path
    canvas: tuple[int, int]
    raw: dict[str, Any]
    elements: tuple[Element, ...]

    def text_slots(self) -> list[Slot]:
        return [
            Slot(item.id, "text", item.role, item.bbox, item)
            for item in self.elements
            if item.type == "text" and _text_value(item.raw) is None
        ]

    def image_slots(self) -> list[Slot]:
        return [
            Slot(item.id, "image", item.role, item.bbox, item)
            for item in self.elements
            if item.type in {"image", "media"} and _has_explicit_missing_media(item.raw)
        ]

    def slots(self) -> list[Slot]:
        by_id = {slot.id: slot for slot in [*self.text_slots(), *self.image_slots()]}
        return [by_id[item.id] for item in self.elements if item.id in by_id]


def _raw_elements(raw: dict[str, Any]) -> Iterable[Any]:
    """Prefer the visual order in elements while supporting separated slot arrays."""
    seen: set[str] = set()
    for field in ("elements", "textSlots", "slots", "images", "shapes"):
        entries = unwrap(raw.get(field, []))
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            element_id = str(_lookup(entry, "id", "slotId", "name", default=""))
            if element_id and element_id in seen:
                continue
            if element_id:
                seen.add(element_id)
            yield entry


def _canvas(raw: dict[str, Any]) -> tuple[int, int]:
    source = _lookup(raw, "canvas", default={})
    source = source if isinstance(source, dict) else {}
    width = _integer(_lookup(source, "widthPx", "width", "w", default=_lookup(raw, "widthPx", "width")))
    height = _integer(_lookup(source, "heightPx", "height", "h", default=_lookup(raw, "heightPx", "height")))
    # The product fallback is intentional only when the design supplies neither value.
    width = width or 1080
    height = height or 1350
    if width <= 0 or height <= 0:
        raise DesignError("canvas dimensions must be positive")
    return width, height


def load_design(path: str | Path) -> Design:
    file_path = Path(path).expanduser().resolve()
    try:
        raw = json.loads(file_path.read_text(encoding="utf-8"))
    except OSError as error:
        raise DesignError(f"cannot read design.json: {error}") from error
    except json.JSONDecodeError as error:
        raise DesignError(f"invalid JSON: {error}") from error
    if not isinstance(raw, dict):
        raise DesignError("design.json root must be an object")

    canvas = _canvas(raw)
    elements: list[Element] = []
    for index, entry in enumerate(_raw_elements(raw)):
        element_id = str(_lookup(entry, "id", "slotId", "name", default=f"element-{index + 1}"))
        raw_type = str(_lookup(entry, "type", "kind", default="")).lower()
        if not raw_type:
            raw_type = "text" if "text" in entry else "image" if "image" in entry or "media" in entry else "shape"
        role = str(_lookup(entry, "role", "semanticRole", default=raw_type))
        z_index = _integer(_lookup(entry, "zIndex", "z_index", "layer", "order"), index) or index
        elements.append(Element(element_id, raw_type, role, _bbox(entry, canvas), z_index, entry, index))

    return Design(file_path, canvas, raw, tuple(elements))


def text_value(element: Element) -> Any:
    return _text_value(element.raw)


def media_source(element: Element) -> str | None:
    return _media_source(element.raw)


def value(element: Element, *names: str, default: Any = None) -> Any:
    return _lookup(element.raw, *names, default=default)
