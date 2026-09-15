#!/usr/bin/env python3
"""Extract one evidence-backed visual-design description from a JPG or PNG."""

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from PIL import Image, ImageFilter, ImageStat


ORIGINS = {"measured", "inferred", "user-provided"}
CONFIDENCES = {"high", "medium", "low"}


def fact(value: Any, origin: str, confidence: str, note: str = None) -> Dict[str, Any]:
    if origin not in ORIGINS or confidence not in CONFIDENCES:
        raise ValueError("invalid evidence metadata")
    if origin == "inferred" and not note:
        raise ValueError("inferred values require a note")
    output = {"value": value, "origin": origin, "confidence": confidence}
    if note:
        output["note"] = note
    return output


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hex_color(rgb: Tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def dominant_colors(image: Image.Image, count: int = 8) -> List[Dict[str, Any]]:
    thumb = image.convert("RGB").resize((180, max(1, round(image.height * 180 / image.width))), Image.Resampling.BOX)
    quantized = thumb.quantize(colors=count, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette() or []
    bins = quantized.getcolors(maxcolors=count + 1) or []
    total = thumb.width * thumb.height
    result = []
    for pixels, index in sorted(bins, reverse=True):
        offset = index * 3
        result.append({"hex": hex_color(tuple(palette[offset:offset + 3])), "coverage": round(pixels / total, 4)})
    return result


def frame(x: int, y: int, width: int, height: int, canvas_width: int, canvas_height: int, confidence: str = "medium", note: str = None) -> Dict[str, Any]:
    measured = lambda value: fact(value, "measured", confidence, note)
    return {
        "xPx": measured(x), "yPx": measured(y), "widthPx": measured(width), "heightPx": measured(height),
        "x": measured(round(x / canvas_width, 6)), "y": measured(round(y / canvas_height, 6)),
        "width": measured(round(width / canvas_width, 6)), "height": measured(round(height / canvas_height, 6)),
    }


def bright_text_regions(image: Image.Image) -> List[Dict[str, int]]:
    """Find horizontal bright-ink bands. It intentionally does not perform OCR."""
    width = 300
    thumb = image.convert("RGB").resize((width, max(1, round(image.height * width / image.width))), Image.Resampling.BILINEAR)
    pixels = thumb.load()
    minimum = max(4, int(thumb.width * 0.012))
    rows: List[Tuple[int, int, int]] = []
    for y in range(thumb.height):
        xs = [x for x in range(thumb.width) if min(pixels[x, y]) >= 205 and max(pixels[x, y]) - min(pixels[x, y]) <= 75]
        if len(xs) >= minimum:
            rows.append((y, min(xs), max(xs)))
    bands: List[Dict[str, int]] = []
    for y, left, right in rows:
        if bands and y - (bands[-1]["y"] + bands[-1]["height"]) <= 2:
            prior = bands[-1]
            prior_right = prior["x"] + prior["width"]
            prior["x"] = min(prior["x"], left)
            prior["width"] = max(prior_right, right + 1) - prior["x"]
            prior["height"] = y - prior["y"] + 1
        else:
            bands.append({"x": left, "y": y, "width": right - left + 1, "height": 1})
    line_limit = max(3, int(thumb.height * 0.06))
    lines = [band for band in bands if 2 <= band["height"] <= line_limit]
    blocks: List[Dict[str, int]] = []
    for line in lines:
        if blocks and line["y"] - (blocks[-1]["y"] + blocks[-1]["height"]) <= max(5, int(thumb.height * 0.025)):
            block = blocks[-1]
            right = max(block["x"] + block["width"], line["x"] + line["width"])
            block["x"] = min(block["x"], line["x"])
            block["width"] = right - block["x"]
            block["height"] = line["y"] + line["height"] - block["y"]
            block["lines"] += 1
        else:
            blocks.append({**line, "lines": 1})
    scale_x, scale_y = image.width / thumb.width, image.height / thumb.height
    output = []
    for block in blocks:
        x = max(0, int(round(block["x"] * scale_x)))
        y = max(0, int(round(block["y"] * scale_y)))
        right = min(image.width, int(round((block["x"] + block["width"]) * scale_x)))
        bottom = min(image.height, int(round((block["y"] + block["height"]) * scale_y)))
        if right - x >= image.width * 0.12:
            output.append({"x": x, "y": y, "width": right - x, "height": bottom - y, "lines": block["lines"]})
    return output[:6]


def image_regions(image: Image.Image, text_regions: List[Dict[str, int]]) -> List[Dict[str, int]]:
    """Locate large high-variance zones that are likely image content, not text."""
    rgb = image.convert("RGB")
    cols, rows = 18, 24
    active = set()
    for row in range(rows):
        for col in range(cols):
            left, top = int(col * rgb.width / cols), int(row * rgb.height / rows)
            right, bottom = int((col + 1) * rgb.width / cols), int((row + 1) * rgb.height / rows)
            variance = sum(ImageStat.Stat(rgb.crop((left, top, right, bottom))).var) / 3.0
            if variance >= 420:
                active.add((col, row))
    components = []
    while active:
        stack = [active.pop()]
        component = []
        while stack:
            col, row = stack.pop()
            component.append((col, row))
            for neighbor in ((col - 1, row), (col + 1, row), (col, row - 1), (col, row + 1)):
                if neighbor in active:
                    active.remove(neighbor)
                    stack.append(neighbor)
        components.append(component)
    output = []
    for component in components:
        if len(component) < 10:
            continue
        left, right = min(col for col, _ in component), max(col for col, _ in component) + 1
        top, bottom = min(row for _, row in component), max(row for _, row in component) + 1
        candidate = {"x": int(left * rgb.width / cols), "y": int(top * rgb.height / rows), "width": int(right * rgb.width / cols) - int(left * rgb.width / cols), "height": int(bottom * rgb.height / rows) - int(top * rgb.height / rows)}
        area = candidate["width"] * candidate["height"]
        if area < rgb.width * rgb.height * 0.08:
            continue
        overlap = 0
        for text in text_regions:
            overlap += max(0, min(candidate["x"] + candidate["width"], text["x"] + text["width"]) - max(candidate["x"], text["x"])) * max(0, min(candidate["y"] + candidate["height"], text["y"] + text["height"]) - max(candidate["y"], text["y"]))
        if overlap / area < 0.35:
            output.append(candidate)
    return sorted(output, key=lambda item: item["width"] * item["height"], reverse=True)[:3]


def panel_regions(image: Image.Image) -> List[Dict[str, Any]]:
    """Find large pale, low-variance rectangles that read as panels or fields."""
    rgb = image.convert("RGB")
    cols, rows = 18, 24
    active = set()
    means: Dict[Tuple[int, int], Tuple[int, int, int]] = {}
    for row in range(rows):
        for col in range(cols):
            left, top = int(col * rgb.width / cols), int(row * rgb.height / rows)
            right, bottom = int((col + 1) * rgb.width / cols), int((row + 1) * rgb.height / rows)
            stat = ImageStat.Stat(rgb.crop((left, top, right, bottom)))
            mean = tuple(int(channel) for channel in stat.mean[:3])
            if min(mean) >= 215 and sum(stat.var) / 3.0 < 360:
                active.add((col, row))
                means[(col, row)] = mean
    output = []
    while active:
        stack = [active.pop()]
        component = []
        while stack:
            col, row = stack.pop()
            component.append((col, row))
            for neighbor in ((col - 1, row), (col + 1, row), (col, row - 1), (col, row + 1)):
                if neighbor in active:
                    active.remove(neighbor)
                    stack.append(neighbor)
        if len(component) < 4:
            continue
        left, right = min(col for col, _ in component), max(col for col, _ in component) + 1
        top, bottom = min(row for _, row in component), max(row for _, row in component) + 1
        candidate = {"x": int(left * rgb.width / cols), "y": int(top * rgb.height / rows), "width": int(right * rgb.width / cols) - int(left * rgb.width / cols), "height": int(bottom * rgb.height / rows) - int(top * rgb.height / rows)}
        if candidate["width"] * candidate["height"] < rgb.width * rgb.height * 0.035:
            continue
        mean = tuple(round(sum(means[cell][channel] for cell in component) / len(component)) for channel in range(3))
        output.append({**candidate, "fill": hex_color(mean)})
    return sorted(output, key=lambda item: item["width"] * item["height"], reverse=True)[:3]


def refine_panel_bounds(image: Image.Image, panel: Dict[str, Any]) -> Dict[str, Any]:
    """Refine a coarse pale-panel detection with full-resolution pixels."""
    rgb = image.convert("RGB")
    pad_x, pad_y = max(8, rgb.width // 24), max(8, rgb.height // 24)
    left, top = max(0, panel["x"] - pad_x), max(0, panel["y"] - pad_y)
    right, bottom = min(rgb.width, panel["x"] + panel["width"] + pad_x), min(rgb.height, panel["y"] + panel["height"] + pad_y)
    pixels = rgb.load()
    coordinates = []
    for y in range(top, bottom):
        for x in range(left, right):
            red, green, blue = pixels[x, y]
            if min(red, green, blue) >= 235 and max(red, green, blue) - min(red, green, blue) <= 18:
                coordinates.append((x, y))
    if len(coordinates) < 400:
        return panel
    xs, ys = [point[0] for point in coordinates], [point[1] for point in coordinates]
    return {"x": min(xs), "y": min(ys), "width": max(xs) - min(xs) + 1, "height": max(ys) - min(ys) + 1, "fill": panel["fill"]}


def sampled_background(image: Image.Image) -> List[Dict[str, Any]]:
    rgb = image.convert("RGB")
    points = [(0, 0), (rgb.width - 1, 0), (0, rgb.height - 1), (rgb.width - 1, rgb.height - 1), (rgb.width // 2, rgb.height // 2)]
    return [{"xPx": x, "yPx": y, "color": hex_color(rgb.getpixel((x, y)))} for x, y in points]


def agent_element(item: Dict[str, Any], canvas_width: int, canvas_height: int) -> Dict[str, Any]:
    """Turn a visual agent's scene reading into evidence-backed schema fields.

    Pillow supplies the canvas coordinate system.  The agent supplies the
    semantic meaning that pixels alone cannot establish (for example, whether
    a dark rectangle is a chat bubble or a decorative shape).
    """
    required = {"id", "type", "role", "bounds", "zIndex", "confidence", "note"}
    missing = sorted(required - set(item))
    if missing:
        raise ValueError("visual analysis element is missing: " + ", ".join(missing))
    x, y, width, height = item["bounds"]
    note = item["note"]
    confidence = item["confidence"]
    output = {
        "id": fact(item["id"], "inferred", confidence, note),
        "type": fact(item["type"], "inferred", confidence, note),
        "role": fact(item["role"], "inferred", confidence, note),
        "bounds": frame(x, y, width, height, canvas_width, canvas_height, confidence, "Measured against the source pixel grid after visual inspection."),
        "zIndex": fact(item["zIndex"], "inferred", confidence, "Layer order is reconstructed from visible overlap."),
        "confidence": fact(confidence, "inferred", confidence, note),
    }
    for name in ("text", "typography", "image", "shape"):
        if name in item:
            if name == "text":
                output[name] = fact(None, "inferred", "high", "Text content is intentionally omitted; only the text area's visual properties are extracted.")
            else:
                output[name] = fact(item[name], "inferred", confidence, note)
    return output


def build_design(path: Path, visual_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
    path = path.expanduser().resolve()
    if path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        raise ValueError("input must be a JPG or PNG")
    with Image.open(path) as opened:
        image = opened.convert("RGB")
    width, height = image.size
    colors = dominant_colors(image)
    text_boxes = bright_text_regions(image)
    image_boxes = image_regions(image, text_boxes)
    panels = [refine_panel_bounds(image, panel) for panel in panel_regions(image)]
    filtered_images = []
    for candidate in image_boxes:
        area = candidate["width"] * candidate["height"]
        panel_overlap = 0
        for panel in panels:
            panel_overlap = max(panel_overlap, max(0, min(candidate["x"] + candidate["width"], panel["x"] + panel["width"]) - max(candidate["x"], panel["x"])) * max(0, min(candidate["y"] + candidate["height"], panel["y"] + panel["height"]) - max(candidate["y"], panel["y"])))
        if panel_overlap / max(1, area) < 0.30:
            filtered_images.append(candidate)
    image_boxes = filtered_images
    elements: List[Dict[str, Any]] = []
    images: List[Dict[str, Any]] = []
    shapes: List[Dict[str, Any]] = []
    if visual_analysis is not None:
        raw_elements = visual_analysis.get("elements")
        if not isinstance(raw_elements, list) or not raw_elements:
            raise ValueError("visual analysis needs a non-empty elements list")
        elements = [agent_element(item, width, height) for item in raw_elements]
        images = [item for item in elements if item["type"]["value"] == "image"]
        shapes = [item for item in elements if item["type"]["value"] == "shape"]
    for index, box in enumerate([] if visual_analysis is not None else image_boxes, start=1):
        identifier = "image-{:02d}".format(index)
        element = {
            "id": fact(identifier, "inferred", "medium", "Identifier assigned in visual reading order."),
            "type": fact("image", "inferred", "medium", "Large contiguous high-variance region."),
            "role": fact("image-area", "inferred", "medium", "Likely photographic or illustrated content; confirm if needed."),
            "bounds": frame(**box, canvas_width=width, canvas_height=height, confidence="medium", note="Detected from local color variance."),
            "zIndex": fact(10 + index, "inferred", "medium", "Placed below detected text by visual convention."),
            "confidence": fact("medium", "inferred", "medium", "Geometry is measured; semantic classification is inferred."),
            "image": fact({"content": "unknown", "fit": "unknown", "crop": "unknown"}, "inferred", "low", "The raster does not reveal the original image asset or crop rules."),
        }
        images.append(element)
        elements.append(element)
    for index, box in enumerate([] if visual_analysis is not None else panels, start=1):
        identifier = "shape-{:02d}".format(index)
        element = {
            "id": fact(identifier, "inferred", "medium", "Identifier assigned in visual reading order."),
            "type": fact("shape", "inferred", "medium", "Large pale low-variance region."),
            "role": fact("panel", "inferred", "medium", "Likely panel, input field or card; confirm semantic role if needed."),
            "bounds": frame(box["x"], box["y"], box["width"], box["height"], width, height, "medium", "Detected from low variance and pale color."),
            "zIndex": fact(50 + index, "inferred", "medium", "Panel is above media and below text or controls."),
            "confidence": fact("medium", "inferred", "medium", "Geometry is measured; shape role and corner radius are inferred."),
            "shape": fact({"kind": "rounded-rectangle", "fill": box["fill"], "cornerRadiusPx": "unknown"}, "inferred", "low", "Corner radius cannot be measured reliably with the grid detector."),
        }
        shapes.append(element)
        elements.append(element)
    for index, box in enumerate([] if visual_analysis is not None else text_boxes, start=1):
        identifier = "text-{:02d}".format(index)
        element = {
            "id": fact(identifier, "inferred", "medium", "Identifier assigned in top-to-bottom reading order."),
            "type": fact("text", "inferred", "low", "Horizontal bright-ink bands suggest text."),
            "role": fact("text-area", "inferred", "low", "The geometric detection cannot prove semantic copy type."),
            "bounds": frame(box["x"], box["y"], box["width"], box["height"], width, height, "medium", "Derived from bright horizontal pixel bands."),
            "zIndex": fact(100 + index, "inferred", "medium", "Text is visually above detected image content."),
            "confidence": fact("low", "inferred", "low", "Geometry is measured but OCR, typeface and role are not deterministic."),
            "text": fact(None, "inferred", "high", "Text content is intentionally omitted; only the text area's visual properties are extracted."),
            "typography": fact({"fontFamily": "unknown", "fontCandidates": [], "weight": "unknown", "sizePx": "unknown", "color": "unknown", "lineCount": box["lines"]}, "inferred", "low", "A raster image does not prove the original font, weight or exact metrics."),
        }
        elements.append(element)
    ordered = sorted(elements, key=lambda item: item["zIndex"]["value"])
    frames = [item["bounds"] for item in ordered]
    if frames:
        left = min(item["xPx"]["value"] for item in frames)
        top = min(item["yPx"]["value"] for item in frames)
        right = max(item["xPx"]["value"] + item["widthPx"]["value"] for item in frames)
        bottom = max(item["yPx"]["value"] + item["heightPx"]["value"] for item in frames)
        margins = {"left": left, "top": top, "right": width - right, "bottom": height - bottom}
        vertical = sorted(frames, key=lambda item: item["yPx"]["value"])
        gaps = [vertical[index + 1]["yPx"]["value"] - (vertical[index]["yPx"]["value"] + vertical[index]["heightPx"]["value"]) for index in range(len(vertical) - 1)]
    else:
        margins, gaps = {"left": 0, "top": 0, "right": 0, "bottom": 0}, []
    analysis_layout = (visual_analysis or {}).get("layout", {})
    analysis_gradients = (visual_analysis or {}).get("gradients", [])
    source_hash = sha256(path)
    design_id = "design-" + source_hash[:16]
    design = {
        "schemaVersion": "1.0.0",
        "designId": fact(design_id, "inferred", "high", "Deterministic binding identifier derived from the measured source SHA-256 fingerprint."),
        "source": fact({"filename": path.name, "sha256": source_hash, "designId": design_id, "format": path.suffix.lower().lstrip(".")}, "measured", "high", "designId is a deterministic binding identifier derived from the measured source SHA-256 fingerprint."),
        "assetBinding": {
            "directoryTemplate": fact("generated/{designId}/", "inferred", "high", "Generated assets are grouped in a directory named by the designId."),
            "filenameTemplate": fact("{designId}--{generationId}.png", "inferred", "high", "The PNG filename carries both the source design ID and the per-generation ID."),
            "pngMetadataKeys": fact(["designId", "designVersionId", "generationId", "sourceDesignPath"], "inferred", "medium", "The generator should embed these textual metadata keys when the PNG writer supports them."),
            "registrationRule": fact("Append one generatedAssets entry containing designVersionId, generationId and path after each successful PNG write.", "inferred", "high", "The JSON manifest is the reverse lookup from a design version to its generated files.")
        },
        "canvas": {"widthPx": fact(width, "measured", "high"), "heightPx": fact(height, "measured", "high"), "aspectRatio": fact(round(width / height, 6), "measured", "high")},
        "colors": [fact(color, "measured", "high", "Quantized dominant color from source pixels.") for color in colors],
        "background": {"baseColor": fact(colors[0]["hex"], "measured", "medium", "Dominant color; background may contain additional layers."), "samples": fact(sampled_background(image), "measured", "high"), "gradients": fact(analysis_gradients, "inferred", "low", "Approximate gradient reading supplied by visual analysis; original stops and blend modes are unknown.")},
        "layout": {"margins": fact(analysis_layout.get("margins", margins), "measured", "medium", "Measured from source element bounds."), "alignments": fact(analysis_layout.get("alignments", {"horizontal": "unknown", "vertical": "unknown"}), "inferred", "low", "Alignment is a semantic interpretation of the visible composition."), "spacingPx": fact(analysis_layout.get("spacingPx", gaps), "measured", "medium", "Distances measured between visible element bounds."), "layerOrder": fact(["background"] + [item["id"]["value"] for item in ordered], "inferred", "medium", "Reconstructed from visible overlap and reading order." )},
        "typography": {"fontFamily": fact("unknown", "inferred", "low", "No font file or reliable font metadata is contained in the raster."), "fontCandidates": fact([], "inferred", "low", "No candidate is asserted without user-provided evidence.")},
        "images": images,
        "shapes": shapes,
        "elements": ordered,
        "generatedAssets": [],
        "uncertainties": [
            {"field": "typography.fontFamily", "reason": "A raster image cannot prove the original font.", "confidence": "low"},
            {"field": "gradients", "reason": "Pixels do not reveal original stops, opacity or blend settings.", "confidence": "low"},
            {"field": "semanticRoles", "reason": "Detected regions are classified conservatively from visual features.", "confidence": "low"}
        ]
    }
    canonical = json.dumps({key: value for key, value in design.items() if key not in {"generatedAssets", "designVersionId"}}, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    version_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    design["designVersionId"] = fact("version-" + version_hash[:16], "inferred", "high", "Deterministic identifier derived from the canonical extracted JSON, excluding mutable generatedAssets.")
    return design


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--output", type=Path, default=Path("outputs/design.json"))
    parser.add_argument("--analysis", type=Path, help="Optional temporary semantic scene reading from the visual agent (JSON).")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if args.output.exists() and not args.overwrite:
        parser.error("output already exists; use --overwrite only after reviewing it")
    try:
        visual_analysis = json.loads(args.analysis.read_text(encoding="utf-8")) if args.analysis else None
    except (OSError, json.JSONDecodeError) as exc:
        parser.error("cannot read --analysis: {}".format(exc))
    design = build_design(args.image, visual_analysis)
    from validator import validate_document
    errors = validate_document(design)
    if errors:
        parser.error("extractor produced invalid design.json: " + "; ".join(errors))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(design, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
