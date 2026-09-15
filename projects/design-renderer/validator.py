"""Validation for a resolved design render, without inspecting any reference image."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Mapping

from PIL import Image

from renderer.collector import Resolution, load_resolutions
from renderer.design_reader import Design, DesignError, load_design
from renderer.raster_renderer import RenderResult


class ValidationError(ValueError):
    pass


def validate_resolutions(design: Design, resolutions: Mapping[str, Resolution]) -> None:
    pending = [slot.id for slot in design.slots() if slot.id not in resolutions]
    if pending:
        raise ValidationError(f"unresolved slots: {', '.join(pending)}")
    invalid = [slot_id for slot_id, item in resolutions.items() if item.status not in {"filled", "skipped"}]
    if invalid:
        raise ValidationError(f"invalid slot statuses: {', '.join(invalid)}")
    missing_values = [slot.id for slot in design.slots() if resolutions[slot.id].status == "filled" and resolutions[slot.id].value is None]
    if missing_values:
        raise ValidationError(f"filled slots need a value: {', '.join(missing_values)}")


def validate_output(design: Design, output: str | Path, result: RenderResult | None = None) -> None:
    path = Path(output)
    if not path.is_file():
        raise ValidationError(f"output was not created: {path}")
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            if image.size != design.canvas:
                raise ValidationError(f"output dimensions {image.size} differ from canvas {design.canvas}")
    except (OSError, ValueError) as error:
        raise ValidationError(f"invalid output image: {error}") from error
    if result is not None:
        unresolved_rendered = [
            item.id for item in design.elements
            if item.type == "text" and item.id in result.rendered_text_ids and item.id in {slot.id for slot in design.text_slots()}
            and item.id in result.skipped_slot_ids
        ]
        if unresolved_rendered:
            raise ValidationError(f"skipped text was rendered: {', '.join(unresolved_rendered)}")


def validate(design_path: str | Path, answers_path: str | Path, output: str | Path) -> Design:
    design = load_design(design_path)
    validate_resolutions(design, load_resolutions(answers_path))
    validate_output(design, output)
    return design


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate resolved slots and a final raster image.")
    parser.add_argument("design", help="path to design.json")
    parser.add_argument("--answers", required=True, help="JSON object with filled/skipped slot resolutions")
    parser.add_argument("--output", required=True, help="PNG or JPG to validate")
    args = parser.parse_args()
    try:
        design = validate(args.design, args.answers, args.output)
    except (DesignError, ValidationError, OSError, ValueError) as error:
        parser.error(str(error))
    print(f"valid: {args.output} ({design.canvas[0]}x{design.canvas[1]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
