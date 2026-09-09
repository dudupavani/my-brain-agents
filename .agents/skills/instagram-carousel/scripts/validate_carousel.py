#!/usr/bin/env python3
"""Valida um carrossel já renderizado contra seus templates declarativos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from render_carousel import ASSETS_ROOT, CarouselError, DESIGN_SYSTEM_PATH, load_carousel, load_json, template_registry
from render_slide import validate_rendered_slide


def validate_carousel(content_path: Path, output_dir: Path) -> list[dict]:
    carousel = load_carousel(content_path)
    registry = template_registry()
    design_system = load_json(DESIGN_SYSTEM_PATH)
    results = []
    for number, slide in enumerate(carousel["slides"], start=1):
        template_id = slide.get("templateId")
        if template_id not in registry:
            raise CarouselError(f"Template incompatível ou ausente: {template_id}")
        results.append(
            validate_rendered_slide(
                output_dir / f"slide-{number:02d}.png",
                registry[template_id],
                slide.get("content", {}),
                design_system,
                ASSETS_ROOT,
            )
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        results = validate_carousel(args.content, args.output_dir)
    except CarouselError as error:
        parser.error(str(error))
    print(json.dumps({"status": "passed", "slides": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
