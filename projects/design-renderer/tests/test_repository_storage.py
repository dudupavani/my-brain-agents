from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
import uuid

from PIL import Image

from renderer.asset_binding import GeneratedAsset, append_generated_asset
from renderer.repository_storage import (
    InputConflict,
    RepositoryStorageError,
    prepare_version,
    read_incoming_design,
    validate_product_name,
    validate_repository,
)


class RepositoryStorageTests(unittest.TestCase):
    def _input(self, directory: Path, version: str = "version-a", source_sha: str = "a" * 64, marker: str = "") -> Path:
        document = {
            "designId": "design-01",
            "designVersionId": version,
            "assetBinding": {"source": "structure-design"},
            "generatedAssets": [],
            "source": {"value": {"sha256": source_sha}},
            "canvas": {"width": 4, "height": 4},
            "elements": [],
            "marker": marker,
        }
        path = directory / f"input-{version}-{marker or 'base'}.json"
        path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def _post(self, workspace, generation_id: str | None = None) -> GeneratedAsset:
        generation_id = generation_id or str(uuid.uuid4())
        relative = (
            f"generated-content/{workspace.product_name}/styles/{workspace.design_id}/versions/"
            f"{workspace.design_version_id}/posts/{workspace.design_id}--{generation_id}.png"
        )
        absolute = workspace.repository_root / relative
        absolute.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGBA", (4, 4), "#FA6").save(absolute)
        asset = GeneratedAsset(generation_id, workspace.design_version_id, relative, absolute)
        append_generated_asset(workspace.operational_path, asset)
        return asset

    def test_product_style_version_and_multiple_posts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            first = prepare_version(read_incoming_design(self._input(directory)), directory, "Produto A")
            first_post = self._post(first)
            second_post = self._post(first)
            second = prepare_version(read_incoming_design(self._input(directory, "version-b")), directory, "Produto A")
            self._post(second)
            other_product = prepare_version(read_incoming_design(self._input(directory, "version-a", marker="other")), directory, "Produto B")
            self._post(other_product)

            validate_repository(directory)
            self.assertTrue(first.source_path.is_file())
            self.assertEqual(len(json.loads(first.operational_path.read_text()) ["generatedAssets"]), 2)
            self.assertEqual(first_post.design_version_id, "version-a")
            self.assertNotEqual(first_post.relative_path, second_post.relative_path)
            self.assertIn("generated-content/Produto A/styles/design-01/versions/version-a/posts/", first_post.relative_path)
            self.assertTrue(other_product.operational_path.is_file())

    def test_same_json_is_idempotent_and_source_bytes_are_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            incoming_path = self._input(directory)
            incoming = read_incoming_design(incoming_path)
            workspace = prepare_version(incoming, directory, "Produto A")
            source_before = workspace.source_path.read_bytes()
            again = prepare_version(read_incoming_design(incoming_path), directory, "Produto A")
            self.assertEqual(again.source_path.read_bytes(), source_before)
            self.assertEqual(again.operational_path, workspace.operational_path)

    def test_same_version_different_bytes_is_preserved_as_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            prepare_version(read_incoming_design(self._input(directory)), directory, "Produto A")
            conflicting = read_incoming_design(self._input(directory, marker="changed"))
            with self.assertRaises(InputConflict):
                prepare_version(conflicting, directory, "Produto A")
            conflict = directory / "generated-content/Produto A/styles/design-01/conflicts" / f"version-a--{conflicting.json_sha256}.json"
            self.assertEqual(conflict.read_bytes(), conflicting.raw_bytes)

    def test_incompatible_source_is_preserved_as_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            prepare_version(read_incoming_design(self._input(directory)), directory, "Produto A")
            conflicting = read_incoming_design(self._input(directory, "version-b", "b" * 64))
            with self.assertRaises(InputConflict):
                prepare_version(conflicting, directory, "Produto A")
            self.assertTrue((directory / "generated-content/Produto A/styles/design-01/conflicts" / f"version-b--{conflicting.json_sha256}.json").is_file())

    def test_repository_rejects_missing_png_and_unregistered_png(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            workspace = prepare_version(read_incoming_design(self._input(directory)), directory, "Produto A")
            asset = self._post(workspace)
            asset.absolute_path.unlink()
            with self.assertRaises(RepositoryStorageError):
                validate_repository(directory)

            asset.absolute_path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGBA", (4, 4), "#FA6").save(asset.absolute_path)
            operational = json.loads(workspace.operational_path.read_text(encoding="utf-8"))
            operational["generatedAssets"] = []
            workspace.operational_path.write_text(json.dumps(operational), encoding="utf-8")
            with self.assertRaises(RepositoryStorageError):
                validate_repository(directory)

    def test_repository_checks_extractor_width_px_canvas_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            input_path = self._input(directory)
            document = json.loads(input_path.read_text(encoding="utf-8"))
            document["canvas"] = {
                "widthPx": {"value": 4, "origin": "measured", "confidence": "high"},
                "heightPx": {"value": 4, "origin": "measured", "confidence": "high"},
            }
            input_path.write_text(json.dumps(document), encoding="utf-8")
            workspace = prepare_version(read_incoming_design(input_path), directory, "Produto A")
            asset = self._post(workspace)
            Image.new("RGBA", (3, 3), "#FA6").save(asset.absolute_path)
            with self.assertRaises(RepositoryStorageError):
                validate_repository(directory)

    def test_repository_rejects_duplicate_generation_id(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            workspace = prepare_version(read_incoming_design(self._input(directory)), directory, "Produto A")
            generation_id = str(uuid.uuid4())
            self._post(workspace, generation_id)
            duplicate = GeneratedAsset(
                generation_id,
                workspace.design_version_id,
                f"generated-content/{workspace.product_name}/styles/{workspace.design_id}/versions/{workspace.design_version_id}/posts/{workspace.design_id}--{generation_id}.png",
                workspace.repository_root / f"generated-content/{workspace.product_name}/styles/{workspace.design_id}/versions/{workspace.design_version_id}/posts/{workspace.design_id}--{generation_id}.png",
            )
            append_generated_asset(workspace.operational_path, duplicate)
            with self.assertRaises(RepositoryStorageError):
                validate_repository(directory)

    def test_product_name_must_be_one_safe_directory_component(self) -> None:
        self.assertEqual(validate_product_name("Meu Produto"), "Meu Produto")
        with self.assertRaises(RepositoryStorageError):
            validate_product_name("produto/outra-pasta")


if __name__ == "__main__":
    unittest.main()
