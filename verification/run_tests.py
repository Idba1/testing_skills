#!/usr/bin/env python3
"""Discover and run the four standard-library unittest suites from repository root."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("test-case-generator", "coverage-gap-auditor", "workload-model-builder",
          "nine-dimension-output-evaluator")
loader = unittest.TestLoader()
suite = unittest.TestSuite()
for folder in SKILLS:
    suite.addTests(loader.discover(str(ROOT / folder / "tests"), pattern="test_*.py"))
result = unittest.TextTestRunner(verbosity=2).run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
