"""Generic W3C transport adapted from appstest/appium_client.py.
No application locators, data or device-specific timeouts are retained.
"""
from __future__ import annotations
import json
import time
import urllib.error
import urllib.request

class AppiumError(RuntimeError):
    pass

class Appium:
    def __init__(self, capabilities: dict, url: str = "http://127.0.0.1:4723"):
        self.url = url.rstrip("/")
        self.capabilities = capabilities
        self.session: str | None = None

    def start(self) -> str:
        caps = {"capabilities": {"alwaysMatch": self.capabilities, "firstMatch": [{}]}}
        value = self._req("POST", "/session", caps).get("value", {})
        if not isinstance(value, dict) or "sessionId" not in value:
            raise AppiumError("Appium did not create a session; inspect local server logs")
        self.session = value["sessionId"]
        return self.session

    def _req(self, method: str, path: str, body: dict | None = None) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(f"{self.url}{path}", data=data, method=method,
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            return json.loads(e.read())

    def _sess(self, method: str, path: str, body: dict | None = None):
        if not self.session:
            raise AppiumError("sesi belum dibuka — panggil start() dulu")
        res = self._req(method, f"/session/{self.session}{path}", body)
        val = res.get("value")
        if isinstance(val, dict) and "error" in val:
            raise AppiumError(f"{val['error']}: {str(val.get('message'))[:200]}")
        return val

    def stop(self) -> None:
        if self.session:
            self._req("DELETE", f"/session/{self.session}")
            self.session = None

    def source(self) -> str:
        return self._sess("GET", "/source")

    def back(self) -> None:
        self._sess("POST", "/back", {})

    def tap(self, x: int, y: int) -> None:
        self._sess("POST", "/actions", {"actions": [{
            "type": "pointer", "id": "finger1",
            "parameters": {"pointerType": "touch"},
            "actions": [
                {"type": "pointerMove", "duration": 0, "x": int(x), "y": int(y)},
                {"type": "pointerDown", "button": 0},
                {"type": "pause", "duration": 60},
                {"type": "pointerUp", "button": 0},
            ]}]})

    def clear(self, element_id: str) -> None:
        self._sess("POST", f"/element/{element_id}/clear", {})

    def type_into(self, element_id: str, text: str) -> None:
        """Isi field. Nilai tidak pernah melewati shell, jadi tidak masuk logcat."""
        self._sess("POST", f"/element/{element_id}/value", {"text": text})

    def hide_keyboard(self) -> None:
        try:
            self._sess("POST", "/appium/device/hide_keyboard", {})
        except AppiumError:
            pass          # keyboard memang sedang tidak tampil

    def __enter__(self):
        self.start()
        time.sleep(1.0)
        return self

    def __exit__(self, *exc):
        self.stop()
        return False
