"""Empty unittest runner. Device tests require explicit execution approval."""
import argparse
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--execute-approved", action="store_true", help="Use only after environment and test effects are approved")
a = p.parse_args()
if not a.execute_approved:
    p.exit(2, "Execution blocked: approve scenarios/environment before using --execute-approved.\n")
suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
if suite.countTestCases() == 0:
    p.exit(2, "No test cases configured. No application session opened.\n")
stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
report = ROOT / "reports" / stamp
report.mkdir(parents=True, exist_ok=False)
with (report / "runner.log").open("x") as log:
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
summary = {"tests_run": result.testsRun, "failures": len(result.failures),
           "errors": len(result.errors), "skipped": len(result.skipped),
           "successful": result.wasSuccessful()}
(report / "summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary))
raise SystemExit(0 if result.wasSuccessful() else 1)
