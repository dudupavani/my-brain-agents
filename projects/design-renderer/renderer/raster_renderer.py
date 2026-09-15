"""Pillow compositor for a normalized design.json."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import hypot
from pathlib import Path
import os
import re
from typing import Any

from PIL import Image, ImageColor, ImageDraw, ImageFont

from .collector import Resolution
from .design_reader import Design, Element, media_source, text_value, unwrap, value


class RenderError(ValueError):
    """Raised when a resolved element cannot be safely rendered."""


@dataclass
class RenderResult:
    path: Path
    rendered_text_ids: list[str] = field(default_factory=list)
    skipped_slot_ids: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _number(raw: Any, default: float | None = None) -> float | None:
    raw = unwrap(raw)
    if isinstance(raw, bool):
        return default
    if isinstance(raw, (int, float)):
        return float(raw)
    if isinstance(raw, str):
        match = re.search(r"-?\d+(?:\.\d+)?", raw)
        if match:
            return float(match.group())
    return default


def _rgba(raw: Any, opacity: float = 1.0) -> tuple[int, int, int, int] | None:
    raw = unwrap(raw)
    if raw is None:
        return None
    if isinstance(raw, list):
        raw = raw[0] if raw else None
    if isinstance(raw, dict):
        raw = raw.get("hex", raw.get("color", raw.get("fill")))
    if not isinstance(raw, str) or raw.strip().lower() in {"", "none", "transparent", "unknown"}:
        return None
    try:
        red, green, blue, alpha = ImageColor.getcolor(raw, "RGBA")
    except ValueError:
        return None
    return red, green, blue, round(alpha * max(0.0, min(1.0, opacity)))


def _opacity(element: Element, style: dict[str, Any] | None = None) -> float:
    raw = (style or {}).get("opacity", value(element, "opacity", "alpha", default=1))
    parsed = _number(raw, 1) or 0
    return parsed / 100 if parsed > 1 else max(0, min(1, parsed))


def _style(element: Element) -> dict[str, Any]:
    result = dict(element.typography)
    direct = unwrap(element.raw.get("style", {}))
    if isinstance(direct, dict):
        result = {**direct, **result}
    return result


def _style_value(element: Element, style: dict[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in style:
            return unwrap(style[name])
    return value(element, *names, default=default)


def _background(design: Design) -> dict[str, Any]:
    raw = unwrap(design.raw.get("background", {}))
    return raw if isinstance(raw, dict) else {}


def _blend_color(start: tuple[int, int, int, int], end: tuple[int, int, int, int], amount: float) -> tuple[int, int, int, int]:
    amount = max(0.0, min(1.0, amount))
    return tuple(round(a + (b - a) * amount) for a, b in zip(start, end))  # type: ignore[return-value]


def _gradient_stops(gradient: dict[str, Any]) -> list[tuple[float, tuple[int, int, int, int]]]:
    """Normalize common `colors`/`stops` spellings into positioned RGBA stops."""
    raw = gradient.get("colors", gradient.get("stops", []))
    if isinstance(raw, dict):
        raw = list(raw.values())
    if not isinstance(raw, list):
        raw = [gradient.get("color")]
    parsed: list[tuple[float | None, tuple[int, int, int, int]]] = []
    for item in raw:
        offset: float | None = None
        color_raw = item
        if isinstance(item, dict):
            color_raw = item.get("color", item.get("hex", item.get("value", item.get("fill"))))
            offset = _number(item.get("offset", item.get("position", item.get("stop"))))
            if offset is not None and offset > 1:
                offset /= 100
        color = _rgba(color_raw)
        if color is not None:
            parsed.append((offset, color))
    if not parsed:
        return []
    if len(parsed) == 1:
        return [(0.0, parsed[0][1]), (1.0, parsed[0][1])]
    missing = [index for index, (offset, _) in enumerate(parsed) if offset is None]
    for index in missing:
        parsed[index] = (index / (len(parsed) - 1), parsed[index][1])
    return sorted((max(0.0, min(1.0, float(offset))), color) for offset, color in parsed if offset is not None)


def _gradient_color(stops: list[tuple[float, tuple[int, int, int, int]]], amount: float) -> tuple[int, int, int, int]:
    amount = max(0.0, min(1.0, amount))
    if amount <= stops[0][0]:
        return stops[0][1]
    if amount >= stops[-1][0]:
        return stops[-1][1]
    for (left, start), (right, end) in zip(stops, stops[1:]):
        if left <= amount <= right:
            span = right - left or 1
            return _blend_color(start, end, (amount - left) / span)
    return stops[-1][1]


def _gradient_layer(size: tuple[int, int], gradient: dict[str, Any], opacity: float) -> Image.Image | None:
    stops = _gradient_stops(gradient)
    if not stops:
        return None
    width, height = size
    origin = gradient.get("approximateOriginPx", gradient.get("originPx", gradient.get("center", [width / 2, height / 2])))
    if isinstance(origin, dict):
        origin = [origin.get("x", width / 2), origin.get("y", height / 2)]
    if not isinstance(origin, (list, tuple)) or len(origin) < 2:
        origin = [width / 2, height / 2]
    center = (_number(origin[0], width / 2) or width / 2, _number(origin[1], height / 2) or height / 2)
    kind = str(gradient.get("kind", "radial")).lower()
    if kind not in {"radial", "radial-gradient", "linear", "linear-gradient"}:
        raise RenderError(f"unsupported background gradient kind: {kind}")
    layer = Image.new("RGBA", size)
    pixels = layer.load()
    if kind in {"linear", "linear-gradient"}:
        angle = _number(gradient.get("angleDeg", gradient.get("angle", 0)), 0) or 0
        from math import cos, radians, sin
        direction = (cos(radians(angle)), sin(radians(angle)))
        extent = abs(direction[0]) * width / 2 + abs(direction[1]) * height / 2 or 1
        for y in range(height):
            for x in range(width):
                amount = 0.5 + ((x - center[0]) * direction[0] + (y - center[1]) * direction[1]) / (2 * extent)
                color = _gradient_color(stops, amount)
                pixels[x, y] = color[:3] + (round(color[3] * opacity),)
    else:
        radius = _number(gradient.get("radiusPx", gradient.get("radius")))
        if not radius:
            radius = max(hypot(center[0] - x, center[1] - y) for x, y in ((0, 0), (width, 0), (0, height), (width, height))) or 1
        for y in range(height):
            for x in range(width):
                amount = hypot(x - center[0], y - center[1]) / radius
                color = _gradient_color(stops, amount)
                pixels[x, y] = color[:3] + (round(color[3] * opacity),)
    return layer


def _radial_glow(size: tuple[int, int], color: tuple[int, int, int, int], center: tuple[float, float], opacity: float) -> Image.Image:
    width, height = size
    layer = Image.new("RGBA", size)
    pixels = layer.load()
    radius = max(hypot(center[0] - x, center[1] - y) for x, y in ((0, 0), (width, 0), (0, height), (width, height))) or 1
    for y in range(height):
        for x in range(width):
            intensity = max(0.0, 1.0 - hypot(x - center[0], y - center[1]) / radius)
            pixels[x, y] = color[:3] + (round(color[3] * opacity * intensity * intensity),)
    return layer


def _apply_background(canvas: Image.Image, design: Design) -> None:
    background = _background(design)
    base = _rgba(background.get("baseColor", background.get("color", background.get("fill", "#FFFFFF")))) or (255, 255, 255, 255)
    ImageDraw.Draw(canvas).rectangle((0, 0, *canvas.size), fill=base)
    gradients = background.get("gradients", background.get("gradient", []))
    if isinstance(gradients, dict):
        gradients = [gradients]
    if not isinstance(gradients, list):
        return
    for gradient in gradients:
        if not isinstance(gradient, dict):
            continue
        opacity = _number(gradient.get("opacity"), 1) or 0
        if opacity > 1:
            opacity /= 100
        layer = _gradient_layer(canvas.size, gradient, opacity)
        if layer is not None:
            canvas.alpha_composite(layer)


def _shape_spec(element: Element) -> dict[str, Any]:
    raw = unwrap(element.raw.get("shape", {}))
    return raw if isinstance(raw, dict) else {}


def _radius(raw: Any, fallback: int = 0) -> int:
    return max(0, int(round(_number(raw, fallback) or 0)))


def _rotation(raw: Any) -> float:
    return _number(raw, 0) or 0


def _composite_box(canvas: Image.Image, piece: Image.Image, bbox: tuple[int, int, int, int], angle: float = 0) -> None:
    """Composite a local element, applying its optional clockwise rotation."""
    x, y, width, height = bbox
    if abs(angle) < 0.01:
        canvas.alpha_composite(piece, (x, y))
        return
    # Pillow's positive angle is counter-clockwise in image coordinates; design
    # JSON uses the more familiar clockwise-positive convention.
    rotated = piece.rotate(-angle, resample=Image.Resampling.BICUBIC, expand=True)
    left = round(x + (width - rotated.width) / 2)
    top = round(y + (height - rotated.height) / 2)
    canvas.alpha_composite(rotated, (left, top))


def _draw_shape(canvas: Image.Image, element: Element, warnings: list[str]) -> None:
    shape = _shape_spec(element)
    kind = str(shape.get("kind", value(element, "kind", default="rectangle"))).lower()
    x, y, width, height = element.bbox
    if width <= 0 or height <= 0:
        return
    style = unwrap(element.raw.get("style", {}))
    style = style if isinstance(style, dict) else {}
    opacity = _opacity(element, style)
    fill = _rgba(shape.get("fill", style.get("fill", value(element, "fill", "color"))), opacity)
    stroke = _rgba(shape.get("stroke", style.get("stroke", value(element, "stroke", "borderColor"))), opacity)
    stroke_width = max(1, _radius(shape.get("strokeWidth", style.get("strokeWidth", style.get("borderWidth", 1))), 1))
    radius = _radius(shape.get("cornerRadiusPx", shape.get("cornerRadius", style.get("borderRadius", 0))))
    layer = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(layer)
    box = (0, 0, width, height)
    if kind in {"ellipse", "circle", "circle-with-brand-mark", "oval"}:
        draw.ellipse(box, fill=fill, outline=stroke, width=stroke_width if stroke else 1)
    elif kind in {"line", "divider"}:
        draw.line((0, 0, width, height), fill=stroke or fill, width=stroke_width)
    elif kind in {"check-mark", "checkmark"}:
        color = fill or stroke
        if color:
            draw.line((0, height // 2, width * 0.38, height, width, 0), fill=color, width=stroke_width, joint="curve")
    elif kind in {"rectangle", "rect", "rounded-rectangle", "rounded_rectangle", "pill", ""}:
        if kind in {"rounded-rectangle", "rounded_rectangle", "pill"} or radius:
            draw.rounded_rectangle(box, radius=radius or height // 2 if kind == "pill" else radius, fill=fill, outline=stroke, width=stroke_width if stroke else 1)
        else:
            draw.rectangle(box, fill=fill, outline=stroke, width=stroke_width if stroke else 1)
    else:
        raise RenderError(f"unsupported shape kind for '{element.id}': {kind}")
    rotation = shape.get("rotationDeg", shape.get("rotation", value(element, "rotationDeg", "rotation", default=style.get("rotationDeg", style.get("rotation")))))
    _composite_box(canvas, layer, (x, y, width, height), _rotation(rotation))


def _local_path(source: str, design: Design) -> Path:
    path = Path(source).expanduser()
    return path if path.is_absolute() else (design.path.parent / path).resolve()


def _position(raw: Any, extra: int, axis: str) -> int:
    if isinstance(raw, str):
        raw = raw.lower()
        if raw in {"left", "top"}:
            return 0
        if raw in {"right", "bottom"}:
            return extra
    fraction = _number(raw)
    if fraction is not None:
        if fraction > 1:
            fraction /= 100
        return round(max(0, min(1, fraction)) * extra)
    return extra // 2


def _draw_image(canvas: Image.Image, design: Design, element: Element, source: str, warnings: list[str]) -> None:
    path = _local_path(source, design)
    if not path.is_file():
        raise RenderError(f"image for '{element.id}' was not found: {path}")
    x, y, width, height = element.bbox
    if width <= 0 or height <= 0:
        return
    try:
        image = Image.open(path).convert("RGBA")
    except (OSError, ValueError) as error:
        raise RenderError(f"image for '{element.id}' cannot be opened: {error}") from error
    media = unwrap(element.raw.get("image", element.raw.get("media", {})))
    media = media if isinstance(media, dict) else {}
    fit = str(media.get("fit", value(element, "fit", "objectFit", default="cover"))).lower()
    source_w, source_h = image.size
    ratio = min(width / source_w, height / source_h) if fit == "contain" else max(width / source_w, height / source_h)
    resized = image.resize((max(1, round(source_w * ratio)), max(1, round(source_h * ratio))), Image.Resampling.LANCZOS)
    if fit == "contain":
        piece = Image.new("RGBA", (width, height))
        piece.alpha_composite(resized, ((width - resized.width) // 2, (height - resized.height) // 2))
    else:
        crop = media.get("crop", value(element, "crop", default={}))
        crop = crop if isinstance(crop, dict) else {"position": crop}
        focal_x = crop.get("focalX", crop.get("x", media.get("focalX", media.get("position", "center"))))
        focal_y = crop.get("focalY", crop.get("y", media.get("focalY", media.get("position", "center"))))
        position = crop.get("position", media.get("position", "center"))
        if isinstance(position, str):
            focal_x = position if "focalX" not in crop and "x" not in crop and "focalX" not in media else focal_x
            focal_y = position if "focalY" not in crop and "y" not in crop and "focalY" not in media else focal_y
        crop_x = _position(focal_x, resized.width - width, "x")
        crop_y = _position(focal_y, resized.height - height, "y")
        piece = resized.crop((crop_x, crop_y, crop_x + width, crop_y + height))
    style = unwrap(element.raw.get("style", {}))
    style = style if isinstance(style, dict) else {}
    radius = _radius(media.get("cornerRadiusPx", media.get("borderRadius", style.get("borderRadius", 0))))
    if radius:
        mask = Image.new("L", (width, height), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, width, height), radius=radius, fill=255)
        piece.putalpha(mask)
    opacity = _opacity(element, style)
    if opacity < 1:
        piece.putalpha(piece.getchannel("A").point(lambda alpha: round(alpha * opacity)))
    rotation = media.get("rotationDeg", media.get("rotation", value(element, "rotationDeg", "rotation", default=style.get("rotationDeg", style.get("rotation")))))
    _composite_box(canvas, piece, (x, y, width, height), _rotation(rotation))


def _is_bold(weight: Any) -> bool:
    if isinstance(weight, (int, float)):
        return weight >= 600
    return any(word in str(weight or "").lower() for word in ("bold", "black", "heavy", "semibold", "extra"))


def _font(size: int, family: Any, weight: Any) -> ImageFont.ImageFont:
    candidates: list[str] = []
    if isinstance(family, str) and family.strip().lower() not in {"", "unknown", "none"}:
        candidates.append(family)
    elif isinstance(family, list):
        candidates.extend(str(item) for item in family if isinstance(item, str))
    bold = _is_bold(weight)
    candidates.extend([
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ])
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def _tracking(style: dict[str, Any], size: int) -> float:
    raw = style.get("letterSpacingPx", style.get("letterSpacing", style.get("tracking", 0)))
    if isinstance(raw, str) and raw.strip().endswith("em"):
        return (_number(raw, 0) or 0) * size
    return _number(raw, 0) or 0


def _measure(draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont, text: str, tracking: float) -> float:
    if not text:
        return 0
    return draw.textlength(text, font=font) + max(0, len(text) - 1) * tracking


def _wrap_line(draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont, source: str, max_width: int, tracking: float) -> list[str]:
    if not source:
        return [""]
    lines: list[str] = []
    line = ""
    # Keeping whitespace tokens means the user-supplied character sequence is not normalized.
    for token in re.findall(r"\S+|\s+", source):
        if not line or _measure(draw, font, line + token, tracking) <= max_width:
            line += token
            continue
        lines.append(line)
        line = token
        while _measure(draw, font, line, tracking) > max_width and len(line) > 1:
            prefix = ""
            for character in line:
                if prefix and _measure(draw, font, prefix + character, tracking) > max_width:
                    break
                prefix += character
            lines.append(prefix)
            line = line[len(prefix):]
    lines.append(line)
    return lines


def _wrap(draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont, text: str, max_width: int, tracking: float) -> list[str]:
    lines: list[str] = []
    for paragraph in text.split("\n"):
        lines.extend(_wrap_line(draw, font, paragraph, max_width, tracking))
    return lines


def _line_height(font: ImageFont.ImageFont, style: dict[str, Any], size: int) -> int:
    explicit = style.get("lineHeightPx", style.get("lineHeight", style.get("leading")))
    parsed = _number(explicit)
    if parsed is not None:
        return max(1, round(parsed * size if parsed <= 4 else parsed))
    return max(1, round(size * 1.18))


def _ink_height(draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont, lines: list[str], line_height: int) -> int:
    """Estimate the actual painted height, including the distance between lines."""
    if not lines:
        return 0
    glyph_heights = [
        draw.textbbox((0, 0), line or "Ag", font=font)[3] - draw.textbbox((0, 0), line or "Ag", font=font)[1]
        for line in lines
    ]
    return (len(lines) - 1) * line_height + max(glyph_heights, default=0)


def _fit_text(element: Element, text: str) -> tuple[ImageFont.ImageFont, list[str], float, int, dict[str, Any]]:
    style = _style(element)
    _, _, width, height = element.bbox
    if width <= 0 or height <= 0:
        raise RenderError(f"text slot '{element.id}' has an empty bbox")
    prescribed = _number(_style_value(element, style, "fontSize", "sizePx", "font_size"))
    max_lines = int(_number(_style_value(element, style, "maxLines", "max_lines", "lineCount"), 0) or 0)
    initial = round(prescribed) if prescribed else max(1, height // max(1, round((max_lines or 1) * 1.18)))
    # A prescribed size is a visual starting point, not a hard ceiling. This lets
    # short posts use the otherwise empty area while retaining the declared bbox.
    upper = max(initial, round(initial * 1.5))
    family = _style_value(element, style, "fontFamily", "font", default="unknown")
    candidates = _style_value(element, style, "fontCandidates", default=[])
    if (not family or str(family).lower() == "unknown") and candidates:
        family = candidates
    weight = _style_value(element, style, "weight", "fontWeight", default="regular")
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    for size in range(max(1, upper), 0, -1):
        font = _font(size, family, weight)
        tracking = _tracking(style, size)
        lines = _wrap(probe, font, text, width, tracking)
        if max_lines and len(lines) > max_lines:
            continue
        line_height = _line_height(font, style, size)
        # Extracted line-height values can come from a larger reference canvas.
        # Keep the same visual intent, but never let the leading create a hole or
        # push a valid line outside the element's existing box.
        line_height = min(line_height, max(1, height // max(1, len(lines))))
        if _ink_height(probe, font, lines, line_height) <= height:
            return font, lines, tracking, line_height, style
    # At one pixel this only fails for an extreme input. Do not silently truncate it.
    raise RenderError(f"text for '{element.id}' cannot fit inside its declared bbox")


def _draw_tracked(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, font: ImageFont.ImageFont, color: Any, tracking: float) -> None:
    x, y = xy
    if tracking == 0:
        draw.text((x, y), text, font=font, fill=color)
        return
    for character in text:
        draw.text((x, y), character, font=font, fill=color)
        x += draw.textlength(character, font=font) + tracking


def _draw_text(canvas: Image.Image, element: Element, text: str) -> None:
    font, lines, tracking, line_height, style = _fit_text(element, text)
    x, y, width, _ = element.bbox
    alignment = str(_style_value(element, style, "align", "alignment", "textAlign", default="left")).lower()
    color_value = _style_value(element, style, "color", "fill", "textColor", default="#000000")
    colors = color_value if isinstance(color_value, list) else [color_value]
    layer = Image.new("RGBA", canvas.size)
    draw = ImageDraw.Draw(layer)
    for index, line in enumerate(lines):
        line_width = _measure(draw, font, line, tracking)
        line_x = x if alignment not in {"center", "right", "end"} else x + (width - line_width) / (2 if alignment == "center" else 1)
        bbox = draw.textbbox((0, 0), line or "Ag", font=font)
        line_y = y + index * line_height - bbox[1]
        color = _rgba(colors[min(index, len(colors) - 1)], _opacity(element, style)) or (0, 0, 0, 255)
        _draw_tracked(draw, (line_x, line_y), line, font, color, tracking)
    canvas.alpha_composite(layer)


def render(design: Design, output: str | Path, resolutions: dict[str, Resolution] | None = None) -> RenderResult:
    """Compose one PNG/JPG solely from the JSON, supplied text, and supplied media."""
    output_path = Path(output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGBA", design.canvas)
    _apply_background(canvas, design)
    answers = resolutions or {}
    result = RenderResult(output_path)

    for element in sorted(design.elements, key=lambda item: (item.z_index, item.source_index)):
        resolution = answers.get(element.id)
        if resolution and resolution.status == "skipped":
            result.skipped_slot_ids.append(element.id)
            continue
        if element.type == "text":
            content = resolution.value if resolution and resolution.status == "filled" else text_value(element)
            if content is None:
                continue
            _draw_text(canvas, element, str(content))
            result.rendered_text_ids.append(element.id)
        elif element.type in {"image", "media"}:
            source = resolution.value if resolution and resolution.status == "filled" else media_source(element)
            if source:
                _draw_image(canvas, design, element, source, result.warnings)
            elif resolution is None or resolution.status != "skipped":
                raise RenderError(f"image slot '{element.id}' has no generated or supplied image")
        elif element.type in {"shape", "vector"}:
            _draw_shape(canvas, element, result.warnings)
        else:
            raise RenderError(f"unsupported element type for '{element.id}': {element.type}")

    if output_path.suffix.lower() in {".jpg", ".jpeg"}:
        canvas.convert("RGB").save(output_path, quality=95)
    else:
        canvas.save(output_path, format="PNG")
    return result
