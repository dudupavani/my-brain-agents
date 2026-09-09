#!/usr/bin/env python3
"""Renderizador de um slide orientado exclusivamente pelo JSON do template."""

from __future__ import annotations

import copy
import json
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFont


class CarouselError(ValueError):
    """Erro de contrato que deve impedir uma renderização inválida."""


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        raise CarouselError(f"Arquivo não encontrado: {path}") from error
    except json.JSONDecodeError as error:
        raise CarouselError(f"JSON inválido em {path}: {error}") from error
    if not isinstance(data, dict):
        raise CarouselError(f"O JSON precisa conter um objeto: {path}")
    return data


def required(mapping: dict[str, Any], key: str, context: str) -> Any:
    if key not in mapping:
        raise CarouselError(f"Campo obrigatório ausente em {context}: {key}")
    return mapping[key]


def content_key(element: dict[str, Any]) -> str:
    return str(element.get("contentKey", element["id"]))


def rgb(value: str) -> tuple[int, int, int]:
    try:
        return ImageColor.getrgb(value)
    except ValueError as error:
        raise CarouselError(f"Cor inválida: {value}") from error


def hydrate_template(template: dict[str, Any], design_system: dict[str, Any]) -> dict[str, Any]:
    """Aplica somente o canvas global quando o template o omite."""
    hydrated = copy.deepcopy(template)
    hydrated.setdefault("canvas", copy.deepcopy(required(design_system, "canvas", "design-system")))
    return hydrated


def validate_design_system(design_system: dict[str, Any]) -> None:
    canvas = required(design_system, "canvas", "design-system")
    width = required(canvas, "widthPx", "canvas do design-system")
    height = required(canvas, "heightPx", "canvas do design-system")
    if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
        raise CarouselError("Canvas inválido no design-system")
    fonts = required(design_system, "fonts", "design-system")
    for token in ("primaryRegular", "primaryBold"):
        required(required(fonts, token, "design-system"), "assetPath", f"fonte {token}")


def _background_order(template: dict[str, Any]) -> set[str]:
    return {"background"} if "background" in template["renderOrder"] else {"background.baseColor", "background.layers"}


def validate_template(template: dict[str, Any]) -> None:
    template_id = required(template, "templateId", "template")
    if not isinstance(template_id, str) or not template_id:
        raise CarouselError("templateId deve ser uma string não vazia")

    canvas = required(template, "canvas", template_id)
    width = required(canvas, "widthPx", f"canvas de {template_id}")
    height = required(canvas, "heightPx", f"canvas de {template_id}")
    if not isinstance(width, int) or not isinstance(height, int) or width <= 0 or height <= 0:
        raise CarouselError(f"Canvas inválido em {template_id}")

    background = required(template, "background", template_id)
    rgb(required(background, "baseColor", f"background de {template_id}"))
    if not isinstance(required(background, "layers", f"background de {template_id}"), list):
        raise CarouselError(f"background.layers deve ser uma lista em {template_id}")

    elements = required(template, "elements", template_id)
    if not isinstance(elements, list) or not elements:
        raise CarouselError(f"elements deve conter ao menos um elemento em {template_id}")
    ids: set[str] = set()
    elements_by_id: dict[str, dict[str, Any]] = {}
    for element in elements:
        element_id = required(element, "id", f"elemento de {template_id}")
        if element_id in ids:
            raise CarouselError(f"Elemento duplicado em {template_id}: {element_id}")
        ids.add(element_id)
        elements_by_id[element_id] = element
        element_type = required(element, "type", element_id)
        if element_type not in ELEMENT_RENDERERS:
            raise CarouselError(f"Tipo de elemento ainda não suportado: {element_type}")
        required(element, "zIndex", element_id)
        z_index = required(element, "zIndex", element_id)
        if not isinstance(z_index, int):
            raise CarouselError(f"zIndex deve ser inteiro em {element_id}")
        if element_type == "text":
            required(element, "contentKey", element_id)
            required(element, "positionPx", element_id)
            required(element, "textAreaPx", element_id)
            typography = required(element, "typography", element_id)
            required(typography, "fontToken", f"tipografia de {element_id}")
            required(typography, "fontSizePx", f"tipografia de {element_id}")
            required(typography, "minimumFontSizePx", f"tipografia de {element_id}")
            required(typography, "lineHeightPx", f"tipografia de {element_id}")
            rgb(required(typography, "color", f"tipografia de {element_id}"))
            required(element, "wrapping", element_id)
        elif element_type == "image":
            required(element, "contentKey", element_id)
            required(element, "framePx", element_id)
            required(element, "fit", element_id)
            required(element, "cropAnchor", element_id)
            if "visibleFramePx" in element:
                required(element, "clipToCanvas", element_id)
                required(element, "bottomBleedPx", element_id)
        elif element_type == "shape":
            if element.get("shape") != "rounded-rectangle":
                raise CarouselError(f"Forma ainda não suportada em {element_id}: {element.get('shape')}")
            required(element, "framePx", element_id)
            rgb(required(element, "fill", element_id))

    content_model = template.get("contentModel", {})
    required_fields = content_model.get("requiredFields", [])
    if not isinstance(required_fields, list):
        raise CarouselError(f"contentModel.requiredFields deve ser uma lista em {template_id}")
    content_keys = {content_key(element) for element in elements if element["type"] in {"text", "image"}}
    unknown_fields = set(required_fields) - content_keys
    if unknown_fields:
        raise CarouselError(f"contentModel referencia campos sem elemento em {template_id}: {', '.join(sorted(unknown_fields))}")

    render_order = required(template, "renderOrder", template_id)
    if not isinstance(render_order, list) or not render_order:
        raise CarouselError(f"renderOrder inválido em {template_id}")
    expected_order_items = _background_order(template) | ids
    if set(render_order) != expected_order_items or len(render_order) != len(expected_order_items):
        raise CarouselError(f"renderOrder deve conter cada camada e elemento uma única vez em {template_id}")
    z_indexes = [elements_by_id[item]["zIndex"] for item in render_order if item in elements_by_id]
    if z_indexes != sorted(z_indexes):
        raise CarouselError(f"renderOrder e zIndex estão em conflito em {template_id}")


def resolve_font(typography: dict[str, Any], design_system: dict[str, Any], assets_root: Path) -> ImageFont.FreeTypeFont:
    token = required(typography, "fontToken", "tipografia")
    fonts = required(design_system, "fonts", "design-system")
    definition = required(fonts, token, "design-system")
    asset_path = Path(required(definition, "assetPath", f"fonte {token}"))
    font_path = assets_root.parent / asset_path if asset_path.parts and asset_path.parts[0] == "assets" else assets_root / asset_path
    if not font_path.is_file():
        raise CarouselError(f"Arquivo de fonte ausente para o token '{token}': {font_path}")
    size = required(typography, "_resolvedFontSizePx", "tipografia")
    try:
        return ImageFont.truetype(str(font_path), size)
    except OSError as error:
        raise CarouselError(f"Não foi possível carregar a fonte '{token}' em {font_path}") from error


def normalise_text(text: str, preserve_breaks: bool) -> list[str]:
    if preserve_breaks:
        return [" ".join(part.split()) for part in text.splitlines()] or [""]
    return [" ".join(text.replace("\n", " ").split())]


def wrap_text(text: str, font: ImageFont.FreeTypeFont, width: int, preserve_breaks: bool) -> list[str]:
    lines: list[str] = []
    for paragraph in normalise_text(text, preserve_breaks):
        if not paragraph:
            lines.append("")
            continue
        line = ""
        for word in paragraph.split(" "):
            candidate = word if not line else f"{line} {word}"
            if font.getlength(candidate) <= width:
                line = candidate
            elif not line:
                raise CarouselError(f"A palavra '{word}' não cabe na largura definida pelo template")
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def fit_text(element: dict[str, Any], text: str, design_system: dict[str, Any], assets_root: Path) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    typography = element["typography"]
    wrapping = element["wrapping"]
    area = element["textAreaPx"]
    if wrapping.get("strategy") != "word-wrap":
        raise CarouselError(f"Estratégia de quebra não suportada: {wrapping.get('strategy')}")
    max_lines = required(wrapping, "maximumLines", f"quebra de {element['id']}")
    line_height = required(typography, "lineHeightPx", f"tipografia de {element['id']}")
    initial_size = required(typography, "fontSizePx", f"tipografia de {element['id']}")
    minimum_size = required(typography, "minimumFontSizePx", f"tipografia de {element['id']}")
    if minimum_size > initial_size:
        raise CarouselError(f"minimumFontSizePx é maior que fontSizePx em {element['id']}")

    for size in range(initial_size, minimum_size - 1, -1):
        resolved = dict(typography, _resolvedFontSizePx=size)
        font = resolve_font(resolved, design_system, assets_root)
        lines = wrap_text(text, font, area["width"], wrapping.get("preserveExplicitLineBreaks", False))
        if len(lines) <= max_lines and len(lines) * line_height <= area["height"]:
            return font, lines

    constraints = element.get("contentConstraints", {})
    action = wrapping.get("overflowAction", "rejeitar conteúdo")
    raise CarouselError(
        f"O conteúdo de '{element['id']}' não cabe no template {action}. "
        f"Máximo: {max_lines} linhas e mínimo: {minimum_size}px. "
        f"Reduza a copy ou selecione outro template. Limites recomendados: {constraints.get('recommendedCharacters', 'não informado')}."
    )


def draw_tracked_text(draw: ImageDraw.ImageDraw, position: tuple[int, int], text: str, font: ImageFont.FreeTypeFont, fill: str, tracking: float) -> None:
    if tracking == 0:
        draw.text(position, text, font=font, fill=fill)
        return
    x, y = position
    for character in text:
        draw.text((x, y), character, font=font, fill=fill)
        x += font.getlength(character) + tracking


def tracked_text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, tracking: float) -> float:
    if tracking == 0:
        return draw.textlength(text, font=font)
    return sum(font.getlength(character) for character in text) + max(0, len(text) - 1) * tracking


def render_text(image: Image.Image, element: dict[str, Any], value: Any, design_system: dict[str, Any], assets_root: Path) -> dict[str, Any]:
    if not isinstance(value, str) or not value.strip():
        raise CarouselError(f"O conteúdo de texto '{element['id']}' deve ser uma string não vazia")
    font, lines = fit_text(element, value, design_system, assets_root)
    typography = element["typography"]
    position = element["positionPx"]
    area = element["textAreaPx"]
    line_height = typography["lineHeightPx"]
    block_height = len(lines) * line_height
    vertical = typography.get("verticalAlignment", "top")
    y = position["y"]
    if vertical == "center":
        y += (area["height"] - block_height) // 2
    elif vertical == "bottom":
        y += area["height"] - block_height
    elif vertical != "top":
        raise CarouselError(f"Alinhamento vertical não suportado: {vertical}")

    draw = ImageDraw.Draw(image)
    alignment = typography.get("alignment", "left")
    tracking = typography.get("letterSpacingPx", 0)
    for line in lines:
        line_width = tracked_text_width(draw, line, font, tracking)
        x = position["x"]
        if alignment == "center":
            x += (area["width"] - line_width) / 2
        elif alignment == "right":
            x += area["width"] - line_width
        elif alignment != "left":
            raise CarouselError(f"Alinhamento horizontal não suportado: {alignment}")
        draw_tracked_text(draw, (round(x), y), line, font, typography["color"], tracking)
        y += line_height
    return {"id": element["id"], "lines": lines, "fontSizePx": font.size}


def cover_crop(source: Image.Image, frame: dict[str, int], anchor: str) -> Image.Image:
    width, height = frame["width"], frame["height"]
    scale = max(width / source.width, height / source.height)
    resized = source.resize((math.ceil(source.width * scale), math.ceil(source.height * scale)), Image.Resampling.LANCZOS)
    horizontal, vertical = anchor.split("-")[-1], anchor.split("-")[0]
    if anchor in {"center", "top", "bottom"}:
        horizontal = "center"
    if anchor in {"center", "left", "right"}:
        vertical = "center"
    left = 0 if horizontal == "left" else resized.width - width if horizontal == "right" else (resized.width - width) // 2
    top = 0 if vertical == "top" else resized.height - height if vertical == "bottom" else (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def render_image(image: Image.Image, element: dict[str, Any], value: Any, _design_system: dict[str, Any], _assets_root: Path) -> dict[str, Any]:
    if not isinstance(value, str) or not value:
        raise CarouselError(f"O conteúdo de imagem '{element['id']}' deve ser um caminho de arquivo")
    source_path = Path(value)
    if not source_path.is_file():
        raise CarouselError(f"Imagem não encontrada para '{element['id']}': {source_path}")
    if element["fit"] != "cover" or element.get("allowDistortion", False):
        raise CarouselError(f"O renderer só aceita imagem com fit 'cover' e sem distorção: {element['id']}")
    frame = element["framePx"]
    visible = element.get("visibleFramePx", frame)
    if element.get("clipToCanvas", False):
        bleed = element.get("bottomBleedPx", 0)
        if frame["x"] != visible["x"] or frame["y"] != visible["y"] or frame["width"] != visible["width"] or frame["height"] - visible["height"] != bleed:
            raise CarouselError(f"visibleFramePx e bottomBleedPx inconsistentes em {element['id']}")
    with Image.open(source_path) as source:
        media = cover_crop(source.convert("RGB"), frame, element["cropAnchor"])
    radius = element.get("cornerRadiusPx", 0)
    mask = Image.new("L", media.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, media.width, media.height), radius=radius, fill=255)
    image.paste(media, (frame["x"], frame["y"]), mask)
    return {"id": element["id"], "framePx": frame, "visibleFramePx": visible, "cornerRadiusPx": radius, "fit": "cover"}


def render_shape(image: Image.Image, element: dict[str, Any], _value: Any, _design_system: dict[str, Any], _assets_root: Path) -> dict[str, Any]:
    frame = element["framePx"]
    if element["shape"] != "rounded-rectangle":
        raise CarouselError(f"Forma ainda não suportada: {element['shape']}")
    ImageDraw.Draw(image).rounded_rectangle(
        (frame["x"], frame["y"], frame["x"] + frame["width"] - 1, frame["y"] + frame["height"] - 1),
        radius=element.get("cornerRadiusPx", 0),
        fill=element["fill"],
    )
    return {"id": element["id"], "framePx": frame, "shape": "rounded-rectangle"}


ELEMENT_RENDERERS = {"text": render_text, "image": render_image, "shape": render_shape}


def interpolate_stops(stops: list[dict[str, Any]], resolution: int = 65536) -> list[tuple[int, int, int, int]]:
    if not stops:
        raise CarouselError("Gradiente sem stops")
    parsed = [(float(stop["offset"]), rgb(stop["color"]), float(stop["opacity"])) for stop in stops]
    if parsed[0][0] != 0 or parsed[-1][0] != 1:
        raise CarouselError("Os stops do gradiente precisam começar em 0 e terminar em 1")
    samples: list[tuple[int, int, int, int]] = []
    segment = 0
    for index in range(resolution):
        offset = index / (resolution - 1)
        while segment < len(parsed) - 2 and offset > parsed[segment + 1][0]:
            segment += 1
        start, end = parsed[segment], parsed[segment + 1]
        progress = (offset - start[0]) / (end[0] - start[0]) if end[0] != start[0] else 0
        channels = tuple(round(start[1][channel] + (end[1][channel] - start[1][channel]) * progress) for channel in range(3))
        alpha = round(255 * (start[2] + (end[2] - start[2]) * progress))
        samples.append((*channels, alpha))
    return samples


def render_gradient(canvas: Image.Image, layer: dict[str, Any]) -> None:
    if layer.get("type") != "elliptical-radial-gradient":
        raise CarouselError(f"Tipo de gradiente ainda não suportado: {layer.get('type')}")
    center = required(layer, "centerPx", "gradiente")
    radius = required(layer, "radiusPx", "gradiente")
    radius_x, radius_y = radius["x"], radius["y"]
    if radius_x <= 0 or radius_y <= 0:
        raise CarouselError("Os raios do gradiente devem ser positivos")
    lookup = interpolate_stops(required(layer, "stops", "gradiente"))
    pixel_data = bytearray(canvas.width * canvas.height * 4)
    point = 0
    for y in range(canvas.height):
        normalized_y = (y - center["y"]) / radius_y
        for x in range(canvas.width):
            distance = math.sqrt(((x - center["x"]) / radius_x) ** 2 + normalized_y**2)
            if distance <= 1:
                sample = lookup[min(round(distance * (len(lookup) - 1)), len(lookup) - 1)]
                pixel_data[point : point + 4] = bytes(sample)
            point += 4
    overlay = Image.frombytes("RGBA", canvas.size, bytes(pixel_data))
    canvas.alpha_composite(overlay)


def render_background(image: Image.Image, background: dict[str, Any]) -> None:
    ImageDraw.Draw(image).rectangle((0, 0, image.width, image.height), fill=rgb(background["baseColor"]) + (255,))
    for layer in background["layers"]:
        render_gradient(image, layer)


def required_content_keys(template: dict[str, Any]) -> set[str]:
    keys = set(template.get("contentModel", {}).get("requiredFields", []))
    keys.update(content_key(element) for element in template["elements"] if element.get("required", False))
    return keys


def render_slide(template: dict[str, Any], content: dict[str, Any], design_system: dict[str, Any], assets_root: Path) -> tuple[Image.Image, list[dict[str, Any]]]:
    validate_design_system(design_system)
    validate_template(template)
    missing = required_content_keys(template) - set(content)
    if missing:
        raise CarouselError(f"Conteúdo obrigatório ausente em {template['templateId']}: {', '.join(sorted(missing))}")
    canvas = template["canvas"]
    image = Image.new("RGBA", (canvas["widthPx"], canvas["heightPx"]), (0, 0, 0, 0))
    elements = {element["id"]: element for element in template["elements"]}
    rendered: list[dict[str, Any]] = []
    for item in template["renderOrder"]:
        if item == "background":
            render_background(image, template["background"])
            continue
        if item == "background.baseColor":
            ImageDraw.Draw(image).rectangle((0, 0, image.width, image.height), fill=rgb(template["background"]["baseColor"]) + (255,))
            continue
        if item == "background.layers":
            for layer in template["background"]["layers"]:
                render_gradient(image, layer)
            continue
        element = elements[item]
        if element["type"] == "shape":
            rendered.append(render_shape(image, element, None, design_system, assets_root))
            continue
        key = content_key(element)
        if key not in content:
            continue
        renderer = ELEMENT_RENDERERS[element["type"]]
        rendered.append(renderer(image, element, content[key], design_system, assets_root))
    return image.convert("RGB"), rendered


def validate_rendered_slide(output_path: Path, template: dict[str, Any], content: dict[str, Any], design_system: dict[str, Any], assets_root: Path) -> dict[str, Any]:
    if not output_path.is_file():
        raise CarouselError(f"Slide renderizado não encontrado: {output_path}")
    expected_image, rendered = render_slide(template, content, design_system, assets_root)
    with Image.open(output_path) as output:
        expected = (template["canvas"]["widthPx"], template["canvas"]["heightPx"])
        if output.size != expected:
            raise CarouselError(f"Dimensão inválida em {output_path}: {output.size}; esperado {expected}")
        if output.format != "PNG":
            raise CarouselError(f"Formato inválido em {output_path}: {output.format}; esperado PNG")
        if ImageChops.difference(output.convert("RGB"), expected_image).getbbox() is not None:
            raise CarouselError(f"O PNG não corresponde à renderização declarada pelo template: {output_path}")
    for element in template["elements"]:
        if element["type"] == "text" and element.get("required"):
            label = element.get("referenceContent", {}).get("text", "")
            if label and content.get(content_key(element)) == label and "placeholder" in label.lower():
                raise CarouselError(f"Texto de placeholder não pode ser usado em produção: {element['id']}")
    return {
        "file": str(output_path),
        "templateId": template["templateId"],
        "canvas": {"width": expected[0], "height": expected[1]},
        "renderedElements": rendered,
        "rules": template.get("validationRules", []),
        "status": "passed",
    }
