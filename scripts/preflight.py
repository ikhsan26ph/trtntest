"""Read-only local checks: never creates a session or installs an APK."""
import argparse
import json
import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from framework.config import ROOT, load
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--config", default=str(ROOT / "config/local.json"))
a = p.parse_args()
checks = {"python": sys.version.split()[0], "tools": {x: bool(shutil.which(x)) for x in ("adb", "appium", "node", "java")},
          "apks_in_project": len(list(ROOT.rglob("*.apk")))}
try:
    load(a.config)
    checks["configuration"] = "valid (session not opened)"
except (OSError, ValueError, TypeError) as e:
    checks["configuration"] = str(e)
print(json.dumps(checks, indent=2))
sys.exit(0 if checks["configuration"].startswith("valid") and all(checks["tools"].values()) else 1)
