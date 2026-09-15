import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

from extractor import build_design
from validator import validate_document


class DesignExtractionTests(unittest.TestCase):
    def make_reference(self, directory: Path) -> Path:
        path = directory / "reference.png"
        image = Image.new("RGB", (800, 1000), "#202028")
        draw = ImageDraw.Draw(image)
        draw.rectangle((60, 520, 740, 900), fill="#8A6D55")
        draw.text((80, 90), "VISIBLE TEXT", fill="#FFFFFF")
        image.save(path)
        return path

    def digest(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def test_image_becomes_valid_design_json_without_mutating_input(self):
        with tempfile.TemporaryDirectory() as directory:
            reference = self.make_reference(Path(directory))
            before = self.digest(reference)
            design = build_design(reference)
            self.assertEqual(validate_document(design), [])
            self.assertEqual(self.digest(reference), before)
            self.assertEqual(design["canvas"]["widthPx"]["value"], 800)
            self.assertEqual(design["source"]["value"]["filename"], "reference.png")
            self.assertNotIn("VISIBLE TEXT", json.dumps(design, ensure_ascii=False))

    def test_validator_rejects_an_invented_font(self):
        with tempfile.TemporaryDirectory() as directory:
            design = build_design(self.make_reference(Path(directory)))
            design["typography"]["fontFamily"]["value"] = "Arial"
            self.assertIn("fontFamily must be unknown unless the user provided it", validate_document(design))

    def test_visual_agent_analysis_adds_semantic_elements(self):
        with tempfile.TemporaryDirectory() as directory:
            analysis = {
                "elements": [{
                    "id": "headline", "type": "text", "role": "headline", "bounds": [80, 90, 300, 40],
                    "zIndex": 10, "confidence": "medium", "note": "The visual agent identified the headline.",
                    "text": "VISIBLE TEXT",
                    "typography": {"fontFamily": "unknown", "fontCandidates": []}
                }]
            }
            design = build_design(self.make_reference(Path(directory)), analysis)
            self.assertEqual(validate_document(design), [])
            self.assertEqual(design["elements"][0]["role"]["value"], "headline")
            self.assertIsNone(design["elements"][0]["text"]["value"])

    def test_schema_is_valid_json(self):
        schema = Path(__file__).resolve().parents[1] / "schema" / "design.schema.json"
        self.assertEqual(json.loads(schema.read_text())["$id"], "design/1.0.0")


if __name__ == "__main__":
    unittest.main()
