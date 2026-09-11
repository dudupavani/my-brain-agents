#!/usr/bin/env python3
"""Rebuild the deterministic Pomake index from versioned design.json files."""

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
    if not designs_dir.is_dir():
        return {"indexVersion": 1, "designs": []}

    for design_dir in sorted(path for path in designs_dir.iterdir() if path.is_dir() and path.name != "conflicts"):
        versions: list[dict[str, object]] = []
        versions_dir = design_dir / "versions"
        if not versions_dir.is_dir():
            continue
        for version_dir in sorted(path for path in versions_dir.iterdir() if path.is_dir() and path.name != "conflicts"):
            source_path = version_dir / "design.source.json"
            operational_path = version_dir / "design.json"
            source = read_json(source_path)
            operational = read_json(operational_path)
            version_id = source.get("designVersionId")
            if not isinstance(version_id, str):
                raise ValueError(f"{source_path}: designVersionId ausente ou inválido")
            assets = operational.get("generatedAssets")
            if not isinstance(assets, list):
                raise ValueError(f"{operational_path}: generatedAssets precisa ser uma lista")
            posts: list[dict[str, str]] = []
            for record in assets:
                if not isinstance(record, dict):
                    raise ValueError(f"{operational_path}: registro inválido")
                generation_id = record.get("generationId")
                record_version = record.get("designVersionId")
                path_value = record.get("path")
                if not all(isinstance(item, str) for item in (generation_id, record_version, path_value)):
                    raise ValueError(f"{operational_path}: registro incompleto")
                posts.append({"generationId": generation_id, "designVersionId": record_version, "pngPath": path_value})
            versions.append(
                {
                    "designVersionId": version_id,
                    "designSourcePath": relative(root, source_path),
                    "designJsonPath": relative(root, operational_path),
                    "posts": posts,
                }
            )
        designs.append({"designId": design_dir.name, "versions": versions})

    return {"indexVersion": 1, "designs": designs}


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
