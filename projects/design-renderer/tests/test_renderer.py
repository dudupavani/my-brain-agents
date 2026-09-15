from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image

from renderer.asset_binding import append_generated_asset, reserve_generation
from renderer.collector import Resolution, collect
from renderer.design_reader import load_design
from renderer.raster_renderer import RenderError, _fit_text, render
from validator import validate_output, validate_resolutions


class RendererFlowTests(unittest.TestCase):
    def _fixture(self, directory: Path) -> Path:
        design = {
            "designId": "design-test-01",
            "designVersionId": "version-test-01",
            "assetBinding": {"source": "test"},
            "generatedAssets": [{
                "generationId": "previous",
                "designVersionId": "version-test-01",
                "path": "generated-content/Produto A/styles/design-test-01/versions/version-test-01/posts/design-test-01--previous.png",
            }],
            "canvas": {"width": 320, "height": 240},
            "background": {
                "baseColor": "#172033",
                "gradients": [{"kind": "radial", "approximateOriginPx": [320, 0], "colors": ["#D87B3B", "#172033"]}],
            },
            "elements": [
                {
                    "id": "backdrop",
                    "type": "shape",
                    "role": "panel",
                    "bbox_px": [12, 12, 296, 216],
                    "zIndex": 1,
                    "shape": {"kind": "rounded-rectangle", "fill": "#FFFFFF", "cornerRadiusPx": 20},
                },
                {
                    "id": "title",
                    "type": "text",
                    "role": "title",
                    "bbox_px": [28, 32, 170, 74],
                    "zIndex": 3,
                    "text": None,
                    "typography": {"sizePx": 34, "weight": "bold", "color": "#172033", "lineHeight": 1.05, "maxLines": 3},
                },
                {
                    "id": "portrait",
                    "type": "image",
                    "role": "hero-image",
                    "bbox_norm": [0.66, 0.16, 0.23, 0.55],
                    "zIndex": 2,
                    "image": {"path": None, "fit": "cover", "cornerRadiusPx": 14},
                },
                {
                    "id": "caption",
                    "type": "text",
                    "role": "support",
                    "bbox_px": [28, 130, 245, 48],
                    "zIndex": 4,
                    "text": {"value": None},
                    "typography": {"sizePx": 18, "color": "#30415A", "maxLines": 2, "alignment": "left"},
                },
            ],
        }
        path = directory / "design.json"
        path.write_text(json.dumps(design), encoding="utf-8")
        return path

    def test_collects_each_unresolved_slot_once_and_records_skip(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            design = load_design(self._fixture(Path(temporary)))
            asked: list[str] = []
            answers = iter(["Uma história curta", "ignorar", "skip"])
            resolutions = collect(design, ask=lambda prompt: (asked.append(prompt), next(answers))[1], emit=lambda _: None)
            self.assertEqual([slot.id for slot in design.slots()], ["title", "portrait", "caption"])
            self.assertEqual(len(asked), 3)
            self.assertEqual(resolutions["title"].value, "Uma história curta")
            self.assertEqual(resolutions["portrait"].status, "skipped")
            self.assertEqual(resolutions["caption"].status, "skipped")

    def test_unknown_image_description_is_still_an_unresolved_photo_slot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "design.json"
            path.write_text(json.dumps({
                "canvas": {"width": 20, "height": 20},
                "elements": [{
                    "id": "photo", "type": "image", "role": "hero", "bbox_px": [0, 0, 20, 20],
                    "image": {"content": "unknown", "fit": "cover"},
                }],
            }), encoding="utf-8")
            design = load_design(path)
            self.assertEqual([slot.id for slot in design.image_slots()], ["photo"])

    def test_renders_text_and_media_and_validates_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            design = load_design(self._fixture(directory))
            source = directory / "source.png"
            Image.new("RGB", (70, 120), "#E46F4A").save(source)
            resolutions = {
                "title": Resolution("filled", "Texto preservado e ajustado"),
                "portrait": Resolution("filled", str(source)),
                "caption": Resolution("skipped"),
            }
            validate_resolutions(design, resolutions)
            output = directory / "post.png"
            result = render(design, output, resolutions)
            validate_output(design, output, result)
            with Image.open(output) as image:
                self.assertEqual(image.size, (320, 240))
            self.assertIn("title", result.rendered_text_ids)
            self.assertNotIn("caption", result.rendered_text_ids)
            self.assertIn("caption", result.skipped_slot_ids)

    def test_text_uses_available_box_before_shrinking(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            design = load_design(self._fixture(Path(temporary)))
            title = next(element for element in design.elements if element.id == "title")
            font, lines, _, line_height, _ = _fit_text(title, "Uma ideia")
            self.assertGreater(font.size, 34)
            self.assertLessEqual(len(lines), 3)
            self.assertGreater(line_height, 0)

    def test_background_gradient_and_shape_rotation_are_rendered_from_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            design_path = directory / "visual-fields.json"
            design_path.write_text(json.dumps({
                "canvas": {"width": 100, "height": 100},
                "background": {"baseColor": "#000000", "gradients": [{
                    "kind": "linear", "colors": ["#000000", "#FFFFFF"], "angleDeg": 0,
                    "approximateOriginPx": [50, 50], "opacity": 1,
                }]},
                "elements": [{
                    "id": "rotated", "type": "shape", "role": "accent", "bbox_px": [30, 40, 40, 20],
                    "zIndex": 1, "shape": {"kind": "rectangle", "fill": "#FFB900", "rotationDeg": 20},
                }],
            }), encoding="utf-8")
            output = directory / "visual-fields.png"
            design = load_design(design_path)
            render(design, output)
            with Image.open(output) as image:
                self.assertLess(image.getpixel((0, 50))[0], image.getpixel((99, 50))[0])
                mask = Image.new("L", image.size, 0)
                pixels = mask.load()
                for y in range(image.height):
                    for x in range(image.width):
                        red, green, blue, _ = image.getpixel((x, y))
                        if red > 220 and 120 < green < 220 and blue < 80:
                            pixels[x, y] = 255
                bounds = mask.getbbox()
                self.assertIsNotNone(bounds)
                assert bounds is not None
                self.assertGreater(bounds[2] - bounds[0], 40)
                self.assertGreater(bounds[3] - bounds[1], 20)

    def test_unresolved_image_cannot_be_silently_rendered_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            design = load_design(self._fixture(Path(temporary)))
            with self.assertRaises(RenderError):
                render(design, Path(temporary) / "missing-image.png", {"title": Resolution("filled", "Texto")})

    def test_image_crop_uses_the_declared_focal_point(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            design_path = directory / "crop.json"
            design_path.write_text(json.dumps({
                "canvas": {"width": 10, "height": 10},
                "elements": [{
                    "id": "photo", "type": "image", "role": "hero", "bbox_px": [0, 0, 10, 10],
                    "image": {"path": None, "fit": "cover", "crop": {"focalX": "right", "focalY": "center"}},
                }],
            }), encoding="utf-8")
            source = directory / "source.png"
            image = Image.new("RGB", (20, 10), "#0000FF")
            for x in range(10):
                for y in range(10):
                    image.putpixel((x, y), (255, 0, 0))
            image.save(source)
            design = load_design(design_path)
            render(design, directory / "crop.png", {"photo": Resolution("filled", str(source))})
            with Image.open(directory / "crop.png") as output:
                red, green, blue, _ = output.convert("RGBA").getpixel((5, 5))
                self.assertGreater(blue, red)

    def test_reads_the_extractor_fact_envelopes_when_available(self) -> None:
        real_design = Path(__file__).resolve().parents[2] / "Extract Estructure Design" / "outputs" / "design.json"
        if not real_design.exists():
            self.skipTest("extractor fixture is not present beside this project")
        design = load_design(real_design)
        self.assertGreater(design.canvas[0], 0)
        self.assertGreater(design.canvas[1], 0)
        self.assertTrue(design.text_slots())
        self.assertTrue(all(slot.id and slot.kind == "text" for slot in design.text_slots()))

    def test_appends_a_uuid_v4_binding_without_removing_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            design_path = self._fixture(directory)
            design = load_design(design_path)
            asset = reserve_generation(design, directory, "Produto A")
            asset.absolute_path.parent.mkdir(parents=True, exist_ok=True)
            Image.new("RGB", design.canvas, "#FFFFFF").save(asset.absolute_path)
            append_generated_asset(design_path, asset)

            document = json.loads(design_path.read_text(encoding="utf-8"))
            self.assertEqual(document["designId"], "design-test-01")
            self.assertEqual(document["generatedAssets"][0]["generationId"], "previous")
            self.assertEqual(document["generatedAssets"][1], {"generationId": asset.generation_id, "designVersionId": asset.design_version_id, "path": asset.relative_path})
            self.assertTrue(asset.relative_path.startswith("generated-content/Produto A/styles/design-test-01/versions/version-test-01/posts/design-test-01--"))
            self.assertTrue(asset.relative_path.endswith(".png"))
            self.assertNotIn("{designId}", asset.relative_path)
            self.assertNotIn("{generationId}", asset.relative_path)


if __name__ == "__main__":
    unittest.main()
