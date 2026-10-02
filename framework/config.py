"""Explicit local configuration; no app identity is assumed."""
import json
from pathlib import Path
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parents[1]

def load(path):
    data = json.loads(Path(path).read_text())
    url = data.get("appium_url", "")
    parsed = urlparse(url)
    if parsed.scheme != "http" or parsed.hostname not in ("127.0.0.1", "localhost", "::1"):
        raise ValueError("Only a local HTTP Appium server is supported by this skeleton")
    if not isinstance(data.get("udid"), str) or not data["udid"].strip():
        raise ValueError("Fill udid from adb devices -l")
    raw = data.get("apk_path")
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("APK path is empty; copy your APK into apks/ and set apk_path")
    apk = Path(raw).expanduser()
    apk = (ROOT / apk).resolve() if not apk.is_absolute() else apk.resolve()
    if not apk.is_file() or apk.suffix.lower() != ".apk":
        raise ValueError("Configured APK does not exist or is not an .apk file")
    caps = {"platformName": "Android", "appium:automationName": "UiAutomator2",
            "appium:udid": data["udid"], "appium:app": str(apk),
            "appium:noReset": True, "appium:fullReset": False,
            "appium:autoGrantPermissions": False}
    return url, caps
