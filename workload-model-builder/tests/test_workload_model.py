import importlib.util
from pathlib import Path
import unittest

p = Path(__file__).resolve().parents[1] / "scripts" / "workload_model.py"
spec = importlib.util.spec_from_file_location("workload_model", p)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def sample():
    return {"scenario": "Demo", "population_users": 5000, "peak_session_arrivals_per_minute": 120,
        "mean_session_duration_seconds": 180, "mean_requests_per_session": 6,
        "mean_think_time_seconds": 8, "peak_window_minutes": 30}


class WorkloadTests(unittest.TestCase):
    def test_littles_law(self):
        r = module.build(sample())
        self.assertEqual(r["derived"]["mean_concurrent_sessions"], 360)
        self.assertEqual(r["derived"]["requests_per_minute"], 720)
        self.assertEqual(r["derived"]["session_starts_in_peak_window"], 3600)

    def test_population_warning(self):
        d = sample(); d["population_users"] = 30
        self.assertEqual(len(module.build(d)["warnings"]), 1)

    def test_missing_zero_or_boolean_invalid(self):
        d = sample(); del d["mean_requests_per_session"]
        with self.assertRaises(ValueError): module.build(d)
        d = sample(); d["mean_requests_per_session"] = 0
        with self.assertRaises(ValueError): module.build(d)
        d = sample(); d["population_users"] = True
        with self.assertRaises(ValueError): module.build(d)

    def test_invalid_thinktime(self):
        d = sample(); d["mean_think_time_seconds"] = 200
        with self.assertRaises(ValueError): module.build(d)

    def test_nonfinite(self):
        d = sample(); d["peak_window_minutes"] = float("inf")
        with self.assertRaises(ValueError): module.build(d)


    def test_integer_outside_supported_float_range(self):
        with self.assertRaisesRegex(ValueError, "peak_session_arrivals_per_minute"):
            module.build({**sample(), "peak_session_arrivals_per_minute": 10**400})

    def test_derived_overflow_from_finite_inputs(self):
        base = {**sample(), "peak_session_arrivals_per_minute": 1e308,
                "mean_session_duration_seconds": 60,
                "mean_requests_per_session": 1, "peak_window_minutes": 1}
        for field, metric in (
            ("mean_session_duration_seconds", "mean_concurrent_sessions"),
            ("mean_requests_per_session", "requests_per_minute"),
            ("peak_window_minutes", "session_starts_in_peak_window"),
        ):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, metric):
                    module.build({**base, field: 1e308})


if __name__ == "__main__":
    unittest.main()
