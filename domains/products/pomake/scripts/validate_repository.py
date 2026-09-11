#!/usr/bin/env python3
"""Validate the append-only Pomake design/post repository.

This validator intentionally checks only the contract known to the repository:
identifiers, paths, JSON references, manifests, and file checksums. The full
canonicalization algorithm used to calculate designVersionId remains owned by
the Extractor and is not reimplemented here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from build_index import build_index


VERSION_RE = re.compile(r"^version-[0-9a-f]{16}$")
UUID_V4_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def load_json(path: Path, errors: list[str]) -> object | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"arquivo ausente: {path}")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"JSON inválido em {path}: {exc}")
    return None


def sha256(path: Path) -> str | None:
    try:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def relative_to_root(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def validate_identifier(value: object, pattern: re.Pattern[str], label: str, path: Path, errors: list[str]) -> bool:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        errors.append(f"{path}: {label} inválido: {value!r}")
        return False
    return True


def validate_source(root: Path, design_id: str, path: Path, errors: list[str]) -> str | None:
    data = load_json(path, errors)
    if not isinstance(data, dict):
        errors.append(f"{path}: a raiz precisa ser um objeto JSON")
        return None

    if data.get("designId") != design_id:
        errors.append(f"{path}: designId não corresponde ao diretório {design_id!r}")

    source = data.get("source")
    source_value = source.get("value") if isinstance(source, dict) else None
    source_sha = source_value.get("sha256") if isinstance(source_value, dict) else None
    validate_identifier(source_sha, SHA256_RE, "source.value.sha256", path, errors)

    version_id = data.get("designVersionId")
    if validate_identifier(version_id, VERSION_RE, "designVersionId", path, errors):
        return version_id
    return None


def validate_manifest(
    root: Path,
    design_id: str,
    png_path: Path,
    record: dict[str, object],
    source_paths: dict[str, Path],
    errors: list[str],
) -> None:
    manifest_path = png_path.with_suffix(".manifest.json")
    manifest = load_json(manifest_path, errors)
    if not isinstance(manifest, dict):
        return

    generation_id = record.get("generationId")
    asset_path = relative_to_root(root, png_path)

    if manifest.get("manifestVersion") != 1:
        errors.append(f"{manifest_path}: manifestVersion precisa ser 1")
    if manifest.get("designId") != design_id:
        errors.append(f"{manifest_path}: designId não corresponde ao diretório")
    if manifest.get("generationId") != generation_id:
        errors.append(f"{manifest_path}: generationId não corresponde a design.json")
    if manifest.get("assetPath") != asset_path:
        errors.append(f"{manifest_path}: assetPath deveria ser {asset_path!r}")

    version_id = manifest.get("designVersionId")
    validate_identifier(version_id, VERSION_RE, "designVersionId", manifest_path, errors)
    if isinstance(version_id, str) and version_id not in source_paths:
        errors.append(f"{manifest_path}: designVersionId não possui JSON-fonte arquivado")

    source_path_value = manifest.get("designSourcePath")
    if not isinstance(source_path_value, str):
        errors.append(f"{manifest_path}: designSourcePath ausente ou inválido")
    else:
        source_path = root / source_path_value
        if not source_path.is_file():
            errors.append(f"{manifest_path}: designSourcePath não existe: {source_path_value}")
        elif not any(source_path == candidate for candidate in source_paths.values()):
            errors.append(f"{manifest_path}: designSourcePath não é uma versão ativa arquivada")
        else:
            source_data = load_json(source_path, errors)
            if isinstance(source_data, dict):
                if source_data.get("designId") != design_id:
                    errors.append(f"{manifest_path}: JSON-fonte tem designId diferente")
                if source_data.get("designVersionId") != version_id:
                    errors.append(f"{manifest_path}: JSON-fonte não corresponde ao designVersionId")

    operational_path_value = manifest.get("designOperationalPath")
    expected_operational = f"designs/{design_id}/design.json"
    if operational_path_value != expected_operational:
        errors.append(f"{manifest_path}: designOperationalPath deveria ser {expected_operational!r}")
    elif not (root / expected_operational).is_file():
        errors.append(f"{manifest_path}: design.json operacional ausente")

    checksums = manifest.get("checksums")
    if not isinstance(checksums, dict):
        errors.append(f"{manifest_path}: checksums ausente ou inválido")
        return

    expected_asset_hash = checksums.get("assetSha256")
    if not validate_identifier(expected_asset_hash, SHA256_RE, "checksums.assetSha256", manifest_path, errors):
        return
    actual_asset_hash = sha256(png_path)
    if actual_asset_hash is not None and actual_asset_hash != expected_asset_hash:
        errors.append(f"{manifest_path}: checksum do PNG não confere")

    if isinstance(source_path_value, str) and (root / source_path_value).is_file():
        expected_source_hash = checksums.get("sourceJsonSha256")
        if validate_identifier(expected_source_hash, SHA256_RE, "checksums.sourceJsonSha256", manifest_path, errors):
            actual_source_hash = sha256(root / source_path_value)
            if actual_source_hash is not None and actual_source_hash != expected_source_hash:
                errors.append(f"{manifest_path}: checksum do JSON-fonte não confere")


def validate_design(root: Path, design_dir: Path, errors: list[str], generation_ids: dict[str, Path]) -> None:
    design_id = design_dir.name
    source_path = design_dir / "design.source.json"
    operational_path = design_dir / "design.json"
    versions_dir = design_dir / "versions"

    original_version = validate_source(root, design_id, source_path, errors)
    source_paths: dict[str, Path] = {}
    if original_version:
        source_paths[original_version] = source_path

    for version_path in sorted(versions_dir.glob("version-*.source.json")):
        version_id = validate_source(root, design_id, version_path, errors)
        if version_id:
            if version_id in source_paths:
                errors.append(f"{version_path}: designVersionId duplicado: {version_id}")
            else:
                source_paths[version_id] = version_path
            if version_path.stem.removesuffix(".source") != version_id:
                errors.append(f"{version_path}: nome do arquivo não corresponde ao designVersionId")

    operational = load_json(operational_path, errors)
    if not isinstance(operational, dict):
        return
    if operational.get("designId") != design_id:
        errors.append(f"{operational_path}: designId não corresponde ao diretório")
    operational_version = operational.get("designVersionId")
    if validate_identifier(operational_version, VERSION_RE, "designVersionId", operational_path, errors):
        if operational_version not in source_paths:
            errors.append(f"{operational_path}: designVersionId sem JSON-fonte correspondente")

    assets = operational.get("generatedAssets")
    if not isinstance(assets, list):
        errors.append(f"{operational_path}: generatedAssets precisa ser uma lista")
        return

    listed_paths: set[str] = set()
    listed_generation_ids: set[str] = set()
    generated_dir = root / "generated" / design_id

    for index, record in enumerate(assets):
        record_path = f"{operational_path} generatedAssets[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{record_path}: registro precisa ser um objeto")
            continue
        generation_id = record.get("generationId")
        valid_generation = validate_identifier(generation_id, UUID_V4_RE, "generationId", operational_path, errors)
        if isinstance(generation_id, str) and valid_generation:
            if generation_id in listed_generation_ids:
                errors.append(f"{record_path}: generationId duplicado: {generation_id}")
            listed_generation_ids.add(generation_id)
            previous = generation_ids.setdefault(generation_id, operational_path)
            if previous != operational_path:
                errors.append(f"{record_path}: generationId também aparece em {previous}")

        path_value = record.get("path")
        if not isinstance(path_value, str):
            errors.append(f"{record_path}: path ausente ou inválido")
            continue
        if path_value in listed_paths:
            errors.append(f"{record_path}: path duplicado: {path_value}")
        listed_paths.add(path_value)
        expected_prefix = f"generated/{design_id}/"
        if not path_value.startswith(expected_prefix) or not path_value.endswith(".png") or ".." in Path(path_value).parts:
            errors.append(f"{record_path}: path fora da convenção: {path_value}")
            continue
        expected_name = f"{design_id}--{generation_id}.png"
        if Path(path_value).name != expected_name:
            errors.append(f"{record_path}: nome do PNG deveria ser {expected_name!r}")
            continue
        png_path = root / path_value
        if not png_path.is_file():
            errors.append(f"{record_path}: PNG ausente: {path_value}")
            continue
        validate_manifest(root, design_id, png_path, record, source_paths, errors)

    if generated_dir.is_dir():
        for png_path in sorted(generated_dir.glob("*.png")):
            png_rel = relative_to_root(root, png_path)
            if png_rel not in listed_paths:
                errors.append(f"PNG sem registro em design.json: {png_rel}")
            if not png_path.with_suffix(".manifest.json").is_file():
                errors.append(f"PNG sem manifesto: {png_rel}")

        for manifest_path in sorted(generated_dir.glob("*.manifest.json")):
            png_path = manifest_path.with_suffix("").with_suffix(".png")
            if not png_path.is_file():
                errors.append(f"manifesto sem PNG correspondente: {relative_to_root(root, manifest_path)}")


def validate_index(root: Path, errors: list[str]) -> None:
    index_path = root / "index.json"
    if not index_path.is_file():
        return
    data = load_json(index_path, errors)
    if not isinstance(data, dict):
        return

    try:
        expected = build_index(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"{index_path}: não foi possível reconstruir o índice: {exc}")
        expected = None
    if expected is not None and data != expected:
        errors.append(f"{index_path}: não corresponde ao índice reconstruído a partir dos artefatos")

    if data.get("indexVersion") != 1:
        errors.append(f"{index_path}: indexVersion precisa ser 1")
    designs = data.get("designs")
    if not isinstance(designs, list):
        errors.append(f"{index_path}: designs precisa ser uma lista")
        return
    seen: set[str] = set()
    for entry in designs:
        if not isinstance(entry, dict):
            errors.append(f"{index_path}: entrada de design precisa ser um objeto")
            continue
        design_id = entry.get("designId")
        if not isinstance(design_id, str):
            errors.append(f"{index_path}: entrada sem designId")
            continue
        if design_id in seen:
            errors.append(f"{index_path}: designId duplicado: {design_id}")
        seen.add(design_id)
        for field in ("designSourcePath", "designOperationalPath"):
            value = entry.get(field)
            if not isinstance(value, str) or not (root / value).is_file():
                errors.append(f"{index_path}: {field} inválido para {design_id}: {value!r}")


def validate_current_repository(root: Path) -> list[str]:
    """Validate the version-folder contract without PNG sidecar manifests."""
    errors: list[str] = []
    generation_ids: set[str] = set()
    listed_pngs: set[str] = set()
    designs_dir = root / "designs"
    generated_dir = root / "generated"

    def json_object(path: Path) -> dict[str, object] | None:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"JSON inválido em {path}: {exc}")
            return None
        if not isinstance(data, dict):
            errors.append(f"{path}: a raiz precisa ser um objeto JSON")
            return None
        return data

    def source_sha(data: dict[str, object]) -> object:
        source = data.get("source")
        source_value = source.get("value") if isinstance(source, dict) and "value" in source else source
        if isinstance(source_value, dict) and set(source_value).issubset({"value", "origin", "confidence", "note"}):
            source_value = source_value.get("value")
        return source_value.get("sha256") if isinstance(source_value, dict) else None

    def canvas_size(data: dict[str, object]) -> tuple[int, int] | None:
        canvas = data.get("canvas")
        if not isinstance(canvas, dict):
            return None
        width = canvas.get("width")
        height = canvas.get("height")
        if isinstance(width, dict):
            width = width.get("value")
        if isinstance(height, dict):
            height = height.get("value")
        return (width, height) if isinstance(width, int) and isinstance(height, int) else None

    def valid_png(path: Path, expected_size: tuple[int, int] | None) -> bool:
        try:
            content = path.read_bytes()
            if not content.startswith(b"\x89PNG\r\n\x1a\n") or content[12:16] != b"IHDR":
                return False
            width = int.from_bytes(content[16:20], "big")
            height = int.from_bytes(content[20:24], "big")
            return expected_size is None or (width, height) == expected_size
        except OSError:
            return False

    if designs_dir.is_dir():
        for design_dir in sorted(path for path in designs_dir.iterdir() if path.is_dir() and path.name != "conflicts"):
            if not re.fullmatch(r"[^/\\]+", design_dir.name):
                errors.append(f"designId inválido no diretório: {design_dir.name}")
            versions_dir = design_dir / "versions"
            if not versions_dir.is_dir():
                errors.append(f"versions ausente: {versions_dir}")
                continue
            for version_dir in sorted(path for path in versions_dir.iterdir() if path.is_dir() and path.name != "conflicts"):
                if not re.fullmatch(r"[^/\\]+", version_dir.name):
                    errors.append(f"designVersionId inválido no diretório: {version_dir.name}")
                source_path = version_dir / "design.source.json"
                operational_path = version_dir / "design.json"
                source = json_object(source_path)
                operational = json_object(operational_path)
                if source is None or operational is None:
                    continue
                version_id = source.get("designVersionId")
                if source.get("designId") != design_dir.name or operational.get("designId") != design_dir.name:
                    errors.append(f"designId não corresponde a {version_dir}")
                if version_id != version_dir.name or operational.get("designVersionId") != version_id:
                    errors.append(f"designVersionId não corresponde a {version_dir}")
                digest = source_sha(source)
                if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
                    errors.append(f"source.value.sha256 inválido em {source_path}")
                assets = operational.get("generatedAssets")
                if not isinstance(assets, list):
                    errors.append(f"generatedAssets precisa ser uma lista em {operational_path}")
                    continue
                expected_size = canvas_size(operational)
                for index, record in enumerate(assets):
                    label = f"{operational_path} generatedAssets[{index}]"
                    if not isinstance(record, dict):
                        errors.append(f"{label}: registro precisa ser um objeto")
                        continue
                    generation_id = record.get("generationId")
                    path_value = record.get("path")
                    if not isinstance(generation_id, str) or not UUID_V4_RE.fullmatch(generation_id) or generation_id in generation_ids:
                        errors.append(f"{label}: generationId inválido ou duplicado: {generation_id!r}")
                    if isinstance(generation_id, str):
                        generation_ids.add(generation_id)
                    if record.get("designVersionId") != version_id:
                        errors.append(f"{label}: designVersionId inválido")
                    expected_path = f"generated/{design_dir.name}/{design_dir.name}--{generation_id}.png"
                    if path_value != expected_path:
                        errors.append(f"{label}: path deveria ser {expected_path!r}")
                        continue
                    png_path = root / path_value
                    listed_pngs.add(path_value)
                    if not png_path.is_file() or not valid_png(png_path, expected_size):
                        errors.append(f"{label}: PNG ausente ou inválido: {path_value}")

    if generated_dir.is_dir():
        for png_path in sorted(generated_dir.glob("*/*.png")):
            relative_path = relative_to_root(root, png_path)
            if relative_path not in listed_pngs:
                errors.append(f"PNG sem registro em design.json: {relative_path}")

    index_path = root / "index.json"
    index = json_object(index_path)
    if index is None:
        return errors
    try:
        if index != build_index(root):
            errors.append(f"{index_path}: não corresponde aos design.json operacionais")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"{index_path}: não foi possível reconstruir o índice: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="raiz do domínio do Pomake (padrão: diretório pai de scripts)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    errors = validate_current_repository(root)

    if errors:
        print("Validação falhou:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validação OK: {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
