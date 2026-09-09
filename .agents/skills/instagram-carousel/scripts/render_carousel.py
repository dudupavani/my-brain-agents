#!/usr/bin/env python3
"""Renderiza um carrossel usando somente conteúdo e templates declarativos."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from render_slide import CarouselError, hydrate_template, load_json, render_slide, validate_design_system, validate_rendered_slide, validate_template


SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS_ROOT = SKILL_ROOT / "assets"
TEMPLATES_ROOT = ASSETS_ROOT / "templates"
DESIGN_SYSTEM_PATH = ASSETS_ROOT / "design-system.json"
TEMPLATE_REGISTRY_PATH = TEMPLATES_ROOT / "template-registry.json"


def design_system() -> dict[str, Any]:
    system = load_json(DESIGN_SYSTEM_PATH)
    validate_design_system(system)
    return system


def template_registry(system: dict[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    system = system or design_system()
    registry = load_json(TEMPLATE_REGISTRY_PATH)
    if registry.get("designSystemRef") != DESIGN_SYSTEM_PATH.name:
        raise CarouselError("template-registry.json deve apontar para o design-system.json da skill")
    entries = registry.get("templates")
    if not isinstance(entries, list) or not entries:
        raise CarouselError("template-registry.json precisa declarar ao menos um template")

    templates: dict[str, dict[str, Any]] = {}
    for entry in entries:
        template_id = entry.get("templateId")
        filename = entry.get("file")
        if not isinstance(template_id, str) or not isinstance(filename, str):
            raise CarouselError("Cada entrada do template-registry precisa de templateId e file")
        source = load_json(TEMPLATES_ROOT / filename)
        if source.get("templateId") != template_id:
            raise CarouselError(f"Registro e arquivo divergem para {template_id}")
        if source.get("designSystemRef") != DESIGN_SYSTEM_PATH.name:
            raise CarouselError(f"Template {template_id} não aponta para o design-system.json da skill")
        if template_id in templates:
            raise CarouselError(f"templateId duplicado em template-registry.json: {template_id}")
        template = hydrate_template(source, system)
        validate_template(template)
        templates[template_id] = template
    return templates


def load_carousel(path: Path, system: dict[str, Any] | None = None) -> dict[str, Any]:
    system = system or design_system()
    data = load_json(path)
    if "carousel" in data:
        carousel = data["carousel"]
    elif "slides" in data:
        carousel = {"width": system["canvas"]["widthPx"], "height": system["canvas"]["heightPx"], "slides": data["slides"]}
    else:
        raise CarouselError("O arquivo de conteúdo deve conter 'carousel' ou 'slides'")
    if not isinstance(carousel, dict):
        raise CarouselError("O contrato de conteúdo do carrossel é inválido")
    expected_size = (system["canvas"]["widthPx"], system["canvas"]["heightPx"])
    if (carousel.get("width"), carousel.get("height")) != expected_size:
        raise CarouselError(f"O contrato de conteúdo deve declarar width={expected_size[0]} e height={expected_size[1]}")
    slides = carousel.get("slides")
    if not isinstance(slides, list) or not slides:
        raise CarouselError("O carrossel precisa conter ao menos um slide")
    return carousel


def render_carousel(content_path: Path, output_dir: Path) -> list[dict[str, Any]]:
    system = design_system()
    carousel = load_carousel(content_path, system)
    registry = template_registry(system)
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
        image, _ = render_slide(template, content, system, ASSETS_ROOT)
        output_path = output_dir / f"slide-{number:02d}.png"
        image.save(output_path, "PNG", optimize=True)
        results.append(validate_rendered_slide(output_path, template, content, system, ASSETS_ROOT))
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
