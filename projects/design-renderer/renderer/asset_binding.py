"""Generation identifiers and append-only design.json asset binding."""

from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import tempfile
import uuid

from .design_reader import Design


SAFE_DESIGN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class AssetBindingError(ValueError):
    pass


@dataclass(frozen=True)
class GeneratedAsset:
    generation_id: str
    design_version_id: str
    relative_path: str
    absolute_path: Path


def _design_id(design: Design) -> str:
    raw_id = design.raw.get("designId")
    if isinstance(raw_id, dict) and "value" in raw_id:
        raw_id = raw_id["value"]
    if not isinstance(raw_id, str) or not raw_id:
        raise AssetBindingError("design.json must contain a non-empty designId")
    if not SAFE_DESIGN_ID.fullmatch(raw_id):
        raise AssetBindingError("designId must be a safe path component (letters, numbers, '.', '_' or '-')")
    if "assetBinding" not in design.raw:
        raise AssetBindingError("design.json must contain assetBinding")
    return raw_id


def _design_version_id(design: Design) -> str:
    raw_id = design.raw.get("designVersionId")
    if isinstance(raw_id, dict) and "value" in raw_id:
        raw_id = raw_id["value"]
    if not isinstance(raw_id, str) or not raw_id:
        raise AssetBindingError("design.json must contain a non-empty designVersionId")
    if not SAFE_DESIGN_ID.fullmatch(raw_id):
        raise AssetBindingError("designVersionId must be a safe path component")
    return raw_id


def reserve_generation(design: Design, project_root: str | Path, product_name: str) -> GeneratedAsset:
    """Reserve a collision-free UUID-v4 PNG path without changing the design JSON."""
    design_id = _design_id(design)
    design_version_id = _design_version_id(design)
    root = Path(project_root).expanduser().resolve()
    for _ in range(10):
        generation_id = str(uuid.uuid4())
        relative = (
            Path("generated-content")
            / product_name
            / "styles"
            / design_id
            / "versions"
            / design_version_id
            / "posts"
            / f"{design_id}--{generation_id}.png"
        )
        absolute = root / relative
        if not absolute.exists():
            return GeneratedAsset(generation_id, design_version_id, relative.as_posix(), absolute)
    raise AssetBindingError("could not reserve a unique generation path")


def append_generated_asset(design_path: str | Path, asset: GeneratedAsset) -> None:
    """Append one exact generatedAssets record while retaining all previous records."""
    path = Path(design_path).expanduser().resolve()
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise AssetBindingError(f"cannot update design.json: {error}") from error
    except json.JSONDecodeError as error:
        raise AssetBindingError(f"cannot update invalid design.json: {error}") from error
    if not isinstance(document, dict):
        raise AssetBindingError("design.json root must be an object")
    if not isinstance(document.get("generatedAssets", []), list):
        raise AssetBindingError("generatedAssets must be an array when present")

    records = document.setdefault("generatedAssets", [])
    records.append({"generationId": asset.generation_id, "designVersionId": asset.design_version_id, "path": asset.relative_path})

    # Replace only after the complete updated JSON has been written successfully.
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(document, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except OSError as error:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        raise AssetBindingError(f"cannot persist generatedAssets: {error}") from error
