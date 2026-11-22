import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "scripts" / "boundary_helper.py"
spec = importlib.util.spec_from_file_location("boundary_helper", p)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BoundaryTests(unittest.TestCase):
    def test_inclusive_bounds(self):
        report = module.generate({"requirements": [{"id": "R1", "minimum": 2, "maximum": 5,
            "min_inclusive": True, "max_inclusive": True}]})
        probes = {x["value"]: x["range_expected"] for x in report["requirements"][0]["candidate_values"]}
        self.assertEqual(probes[1], "outside_range")
        self.assertEqual(probes[2], "within_range")
        self.assertEqual(probes[5], "within_range")
        self.assertEqual(probes[6], "outside_range")

    def test_exclusive_bounds(self):
        probes = module.generate({"requirements": [{"id": "R2", "minimum": 1, "maximum": 5,
            "min_inclusive": False, "max_inclusive": False}]})["requirements"][0]["candidate_values"]
        status = {p["value"]: p["range_expected"] for p in probes}
        self.assertEqual(status[1], "outside_range")
        self.assertEqual(status[5], "outside_range")
        self.assertEqual(status[2], "within_range")

    def test_equal_inclusive_bounds(self):
        v = module.generate({"requirements": [{"id": "R1", "minimum": 0, "maximum": 0,
            "min_inclusive": True, "max_inclusive": True}]})
        self.assertEqual(len(v["requirements"][0]["candidate_values"]), 3)

    def test_invalid_empty_and_bool(self):
        with self.assertRaises(ValueError):
            module.generate({"requirements": []})
        with self.assertRaises(ValueError):
            module.generate({"requirements": [{"id": "R1", "minimum": True, "maximum": 3,
                "min_inclusive": True, "max_inclusive": True}]})

    def test_invalid_duplicate_and_exclusive_equal(self):
        r = {"id": "R1", "minimum": 1, "maximum": 3, "min_inclusive": True, "max_inclusive": True}
        with self.assertRaises(ValueError):
            module.generate({"requirements": [r, r]})
        with self.assertRaises(ValueError):
            module.generate({"requirements": [{**r, "maximum": 1, "min_inclusive": False}]})

    def test_custom_probe_distance_not_claimed_as_valid_step(self):
        r = module.generate({"requirements": [{"id": "R1", "minimum": 0, "maximum": 100,
            "min_inclusive": True, "max_inclusive": True, "step": 10}]})
        self.assertEqual(r["requirements"][0]["candidate_values"][0]["value"], -10)


if __name__ == "__main__":
    unittest.main()
