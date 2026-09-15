#!/usr/bin/env python3
"""Validate design.json against the project's JSON Schema and safety rules."""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = ROOT / "schema" / "design.schema.json"


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def resolve_ref(schema: Dict[str, Any], reference: str) -> Dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError("only local schema references are supported")
    target: Any = schema
    for part in reference[2:].split("/"):
        target = target[part]
    return target


def schema_errors(value: Any, rule: Dict[str, Any], root: Dict[str, Any], path: str = "$") -> List[str]:
    if "$ref" in rule:
        return schema_errors(value, resolve_ref(root, rule["$ref"]), root, path)
    errors: List[str] = []
    if "const" in rule and value != rule["const"]:
        errors.append("{} must equal {!r}".format(path, rule["const"]))
    if "enum" in rule and value not in rule["enum"]:
        errors.append("{} must be one of {}".format(path, rule["enum"]))
    expected = rule.get("type")
    kinds = {
        "object": isinstance(value, dict), "array": isinstance(value, list), "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool), "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool), "null": value is None,
    }
    if expected and not kinds.get(expected, True):
        return errors + ["{} must be {}".format(path, expected)]
    if isinstance(value, dict):
        properties = rule.get("properties", {})
        for name in rule.get("required", []):
            if name not in value:
                errors.append("{}.{} is required".format(path, name))
        for name, item in value.items():
            if name in properties:
                errors.extend(schema_errors(item, properties[name], root, path + "." + name))
            elif rule.get("additionalProperties") is False:
                errors.append("{}.{} is not allowed".format(path, name))
    if isinstance(value, list):
        if len(value) < rule.get("minItems", 0):
            errors.append("{} needs at least {} items".format(path, rule["minItems"]))
        if isinstance(rule.get("items"), dict):
            for index, item in enumerate(value):
                errors.extend(schema_errors(item, rule["items"], root, "{}[{}]".format(path, index)))
    return errors


def evidence_errors(value: Any, path: str = "$") -> List[str]:
    errors: List[str] = []
    if isinstance(value, dict):
        if {"value", "origin", "confidence"}.issubset(value):
            if value["origin"] == "inferred" and not str(value.get("note", "")).strip():
                errors.append("{} inferred value needs a note".format(path))
        for key, item in value.items():
            errors.extend(evidence_errors(item, path + "." + key))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(evidence_errors(item, "{}[{}]".format(path, index)))
    return errors


def semantic_errors(design: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    width = design["canvas"]["widthPx"]["value"]
    height = design["canvas"]["heightPx"]["value"]
    identifiers = set()
    for element in design["elements"]:
        identifier = element["id"]["value"]
        if identifier in identifiers:
            errors.append("duplicate element id {}".format(identifier))
        identifiers.add(identifier)
        bounds = element["bounds"]
        x, y = bounds["xPx"]["value"], bounds["yPx"]["value"]
        w, h = bounds["widthPx"]["value"], bounds["heightPx"]["value"]
        if min(x, y) < 0 or w <= 0 or h <= 0 or x + w > width or y + h > height:
            errors.append("{} bounds fall outside the canvas".format(identifier))
        for key in ("x", "y", "width", "height"):
            normalized = bounds[key]["value"]
            if not isinstance(normalized, (int, float)) or not 0 <= normalized <= 1:
                errors.append("{} normalized {} must be between 0 and 1".format(identifier, key))
        if element["type"]["value"] == "text" and element.get("text", {}).get("value") is not None and not isinstance(element["text"]["value"], str):
            errors.append("{} text must be a string or null".format(identifier))
    family = design["typography"]["fontFamily"]
    if family["value"] != "unknown" and family["origin"] != "user-provided":
        errors.append("fontFamily must be unknown unless the user provided it")
    return errors


def validate_document(design: Dict[str, Any]) -> List[str]:
    schema = load_json(SCHEMA_PATH)
    return schema_errors(design, schema, schema) + evidence_errors(design) + semantic_errors(design) if isinstance(design, dict) and "canvas" in design and "elements" in design and "typography" in design else schema_errors(design, schema, schema)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("design", type=Path)
    args = parser.parse_args()
    try:
        document = load_json(args.design)
        errors = validate_document(document)
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        parser.exit(2, "invalid: {}\n".format(exc))
    if errors:
        parser.exit(1, "invalid:\n- {}\n".format("\n- ".join(errors)))
    print("valid")


if __name__ == "__main__":
    main()
