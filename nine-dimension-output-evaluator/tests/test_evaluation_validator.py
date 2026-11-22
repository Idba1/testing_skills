import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "scripts" / "evaluation_validator.py"
spec = importlib.util.spec_from_file_location("evaluation_validator", p)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def evaluation(risk="high"):
    return {"artifact_id": "A1", "risk_level": risk,
        "evaluations": {d: {"status": "pass", "evidence": "Reviewed against cited requirement"} for d in module.REQUIRED[risk]}}


class ValidatorTests(unittest.TestCase):
    def test_high_complete(self):
        self.assertEqual(module.validate(evaluation())["structural_status"], "complete")

    def test_high_missing_is_incomplete(self):
        d = evaluation(); del d["evaluations"]["Security"]
        r = module.validate(d)
        self.assertEqual(r["missing_dimensions"], ["Security"])
        self.assertEqual(r["structural_status"], "incomplete")

    def test_medium_three_dimensions(self):
        self.assertEqual(module.validate(evaluation("medium"))["required_dimensions"],
            ["Correctness", "Completeness", "Traceability"])

    def test_critical_requires_review_record(self):
        d = evaluation("critical")
        self.assertEqual(module.validate(d)["structural_status"], "incomplete")
        d["independent_human_review"] = {"reviewer": "Example QA reviewer", "independent_attested": True,
            "decision": "changes_requested", "notes": "Missing real execution verification"}
        self.assertEqual(module.validate(d)["structural_status"], "complete")

    def test_low_requires_sanity(self):
        d = evaluation("low")
        self.assertEqual(module.validate(d)["structural_status"], "incomplete")
        d["sanity_check"] = {"status": "concern", "evidence": "Unverified assumption found"}
        self.assertEqual(module.validate(d)["structural_status"], "complete")

    def test_status_evidence_and_name_validation(self):
        d = evaluation(); d["evaluations"]["Bias"]["status"] = "not_checked"
        self.assertIn("Bias", module.validate(d)["incomplete_dimension_evidence"])
        d["evaluations"]["Bias"]["status"] = "bad"
        with self.assertRaises(ValueError): module.validate(d)
        d = evaluation(); d["evaluations"]["Accuracy"] = {"status": "pass", "evidence": "x"}
        with self.assertRaises(ValueError): module.validate(d)

    def test_concern_recorded_without_approval(self):
        d = evaluation(); d["evaluations"]["Correctness"]["status"] = "concern"
        r = module.validate(d)
        self.assertIn("Correctness", r["concern_dimensions"])
        self.assertIn("not output correctness or approval", r["advisory"])


if __name__ == "__main__":
    unittest.main()
