"""Explicitly authorized APK install/launch and initial UI observation only."""
import argparse
import json
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from framework.config import ROOT, load
from framework.appium_client import Appium
p = argparse.ArgumentParser(description=__doc__)
p.add_argument("--install-launch-approved", action="store_true")
a = p.parse_args()
if not a.install_launch_approved:
    p.exit(2, "APK install/launch requires explicit user instruction.\n")
url, caps = load(ROOT / "config/local.json")
# Allow first-time installation of the Android automation helper on physical devices.
caps["appium:uiautomator2ServerInstallTimeout"] = 120000
caps["appium:adbExecTimeout"] = 120000
caps["appium:uiautomator2ServerLaunchTimeout"] = 90000
out = ROOT / "reports" / ("initial-ui-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ"))
out.mkdir(parents=True, exist_ok=False)
result = {"kind": "initial UI observation, not a functional test", "session_created": False,
          "ui_source_read": False, "functional_tests_run": 0}
driver = Appium(caps, url)
try:
    driver.start()
    result["session_created"] = True
    time.sleep(5)
    source = driver.source()
    (out / "initial-ui.xml").write_text(source)
    nodes = list(ET.fromstring(source).iter())
    result.update(ui_source_read=True, node_count=len(nodes),
                  visible_labels=sorted({n.get("text") or n.get("content-desc") for n in nodes if n.get("text") or n.get("content-desc")}),
                  editable_count=sum(n.get("class") == "android.widget.EditText" for n in nodes),
                  clickable_count=sum(n.get("clickable") == "true" for n in nodes))
except Exception as exc:
    result["error"] = str(exc)
finally:
    try:
        driver.stop()
    except Exception as exc:
        result["cleanup_error"] = str(exc)
    (out / "summary.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
print(json.dumps({"report": str(out), **result}, indent=2, ensure_ascii=False))
raise SystemExit(0 if result["ui_source_read"] and "cleanup_error" not in result else 1)
