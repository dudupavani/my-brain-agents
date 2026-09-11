#!/usr/bin/env python3
"""Build the deterministic Pomake design/post index.

The index is derived from archived source JSONs, operational design.json
files, and per-PNG manifests. It is safe to rebuild; it does not alter any
design or image artifact.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} precisa conter um objeto JSON")
    return data


def relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def build_index(root: Path) -> dict[str, object]:
    designs: list[dict[str, object]] = []
    designs_dir = root / "designs"
    generated_dir = root / "generated"

    if not designs_dir.is_dir():
        return {"$schema": "./schemas/index.schema.json", "indexVersion": 1, "designs": []}

    for design_dir in sorted(path for path in designs_dir.iterdir() if path.is_dir()):
        design_id = design_dir.name
        source_path = design_dir / "design.source.json"
        operational_path = design_dir / "design.json"
        source_versions: list[dict[str, str]] = []

        source = read_json(source_path)
        source_version = source.get("designVersionId")
        if not isinstance(source_version, str):
            raise ValueError(f"{source_path}: designVersionId ausente ou inválido")
        source_versions.append(
            {"designVersionId": source_version, "path": relative(root, source_path)}
        )

        versions_dir = design_dir / "versions"
        if versions_dir.is_dir():
            for version_path in sorted(versions_dir.glob("version-*.source.json")):
                version = read_json(version_path)
                version_id = version.get("designVersionId")
                if not isinstance(version_id, str):
                    raise ValueError(f"{version_path}: designVersionId ausente ou inválido")
                source_versions.append(
                    {"designVersionId": version_id, "path": relative(root, version_path)}
                )

        posts: list[dict[str, str]] = []
        design_generated_dir = generated_dir / design_id
        if design_generated_dir.is_dir():
            for manifest_path in sorted(design_generated_dir.glob("*.manifest.json")):
                manifest = read_json(manifest_path)
                required = ("generationId", "designVersionId", "assetPath")
                missing = [field for field in required if not isinstance(manifest.get(field), str)]
                if missing:
                    raise ValueError(f"{manifest_path}: campos inválidos: {', '.join(missing)}")
                posts.append(
                    {
                        "generationId": manifest["generationId"],
                        "designVersionId": manifest["designVersionId"],
                        "pngPath": manifest["assetPath"],
                        "manifestPath": relative(root, manifest_path),
                    }
                )

        designs.append(
            {
                "designId": design_id,
                "designSourcePath": relative(root, source_path),
                "designOperationalPath": relative(root, operational_path),
                "sourceVersions": source_versions,
                "posts": posts,
            }
        )

    return {"$schema": "./schemas/index.schema.json", "indexVersion": 1, "designs": designs}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="raiz do domínio do Pomake (padrão: diretório pai de scripts)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="grava o índice em index.json; sem esta opção apenas imprime o resultado",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    index = build_index(root)
    serialized = json.dumps(index, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        (root / "index.json").write_text(serialized, encoding="utf-8")
    else:
        print(serialized, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
