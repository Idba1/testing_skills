import importlib.util
from pathlib import Path
import tempfile
import unittest

p = Path(__file__).resolve().parents[1] / "scripts" / "coverage_audit.py"
spec = importlib.util.spec_from_file_location("coverage_audit", p)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def req(rid, kinds="positive|negative"):
    return {"requirement_id": rid, "requirement_text": "Illustrative requirement", "required_kinds": kinds}


def test(tid, rid, kind="positive"):
    return {"test_id": tid, "requirement_id": rid, "kind": kind, "expected_result": "Explicit outcome"}


class CoverageTests(unittest.TestCase):
    def test_covered_partial_uncovered(self):
        r = module.audit([req("A"), req("B"), req("C")], [test("T1", "A"), test("T2", "A", "negative"), test("T3", "B")])
        self.assertEqual([x["status"] for x in r["requirements"]], ["covered", "partial", "uncovered"])
        self.assertEqual(r["summary"]["covered"], 1)

    def test_orphan_and_unlinked(self):
        r = module.audit([req("A")], [test("T1", "UNKNOWN"), test("T2", "")])
        self.assertEqual(len(r["orphan_tests"]), 1)
        self.assertEqual(r["unlinked_tests"], ["T2"])

    def test_missing_reqs_and_unknown_kind(self):
        with self.assertRaises(ValueError):
            module.audit([], [])
        with self.assertRaises(ValueError):
            module.audit([req("A")], [test("T", "A", "equivalence")])

    def test_duplicate_ids(self):
        with self.assertRaises(ValueError):
            module.audit([req("A"), req("A")], [])
        with self.assertRaises(ValueError):
            module.audit([req("A")], [test("T1", "A"), test("T1", "A")])

    def test_unknown_requirement_kinds(self):
        with self.assertRaises(ValueError):
            module.audit([req("A", "positive|performance")], [])

    def test_csv_schema_error(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "bad.csv"
            f.write_text("bad,header\nfoo,bar\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                module._read_csv(f, {"requirement_id"})


if __name__ == "__main__":
    unittest.main()
