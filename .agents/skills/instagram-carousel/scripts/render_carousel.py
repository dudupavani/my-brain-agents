#!/usr/bin/env python3
"""Renderiza um carrossel usando somente conteúdo e templates declarativos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from render_slide import CarouselError, load_json, render_slide, validate_rendered_slide, validate_template


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS_ROOT = SKILL_ROOT / "assets"
TEMPLATES_ROOT = ASSETS_ROOT / "templates"
DESIGN_SYSTEM_PATH = ASSETS_ROOT / "design-system.json"


def template_registry() -> dict[str, dict[str, Any]]:
    templates: dict[str, dict[str, Any]] = {}
    for path in sorted(TEMPLATES_ROOT.glob("*.json")):
        template = load_json(path)
        validate_template(template)
        template_id = template["templateId"]
        if template_id in templates:
            raise CarouselError(f"templateId duplicado em assets/templates: {template_id}")
        templates[template_id] = template
    if not templates:
        raise CarouselError(f"Nenhum template JSON foi encontrado em {TEMPLATES_ROOT}")
    return templates


def load_carousel(path: Path) -> dict[str, Any]:
    data = load_json(path)
    carousel = data.get("carousel")
    if not isinstance(carousel, dict):
        raise CarouselError("O arquivo de conteúdo deve conter o objeto 'carousel'")
    if carousel.get("width") != 1080 or carousel.get("height") != 1350:
        raise CarouselError("O contrato de conteúdo deve declarar width=1080 e height=1350")
    slides = carousel.get("slides")
    if not isinstance(slides, list) or not slides:
        raise CarouselError("O carrossel precisa conter ao menos um slide")
    return carousel


def render_carousel(content_path: Path, output_dir: Path) -> list[dict[str, Any]]:
    carousel = load_carousel(content_path)
    registry = template_registry()
    design_system = load_json(DESIGN_SYSTEM_PATH)
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    for number, slide in enumerate(carousel["slides"], start=1):
        template_id = slide.get("templateId")
        if template_id not in registry:
            available = ", ".join(registry)
            raise CarouselError(f"Template incompatível ou ausente: {template_id}. Disponíveis: {available}")
        content = slide.get("content")
        if not isinstance(content, dict):
            raise CarouselError(f"O slide {number} precisa conter um objeto 'content'")
        template = registry[template_id]
        if (template["canvas"]["widthPx"], template["canvas"]["heightPx"]) != (carousel["width"], carousel["height"]):
            raise CarouselError(f"O template {template_id} não é compatível com o canvas do carrossel")
        image, _ = render_slide(template, content, design_system, ASSETS_ROOT)
        output_path = output_dir / f"slide-{number:02d}.png"
        image.save(output_path, "PNG", optimize=True)
        results.append(validate_rendered_slide(output_path, template, content, design_system, ASSETS_ROOT))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--content", required=True, type=Path, help="JSON separado com conteúdo e templateId por slide")
    parser.add_argument("--output-dir", required=True, type=Path, help="Pasta dos PNGs finais")
    args = parser.parse_args()
    try:
        results = render_carousel(args.content, args.output_dir)
    except CarouselError as error:
        parser.error(str(error))
    print(json.dumps({"status": "passed", "slides": results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
