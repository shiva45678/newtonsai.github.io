#!/usr/bin/env python3
import json, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKER = ROOT / "tracker" / "suggestions.json"
IMPLEMENTED = ROOT / "tracker" / "implemented.json"
DATE = datetime.date.today().isoformat()

safe_updates = {
"o1": {"status": "in_progress", "result": "Protected 9-11 AM deep-work block on calendar; admin/calls moved to 2-5 PM."},
"p1": {"status": "done", "result": "Set 11 PM bedtime with a 10-minute wind-down routine."}
}

def load(p):
    if not p.exists():
        return {}
    return json.loads(p.read_text())

def save(p, data):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2))

def normalize_tracker_data(data):
    if isinstance(data, dict):
        if all(isinstance(k, str) and k.startswith("2026-") for k in data.keys()):
            return data
    return {}

def apply_today():
    data = normalize_tracker_data(load(TRACKER))
    day = data.get(DATE)
    if not day:
        return {"updated": False, "reason": "no_day"}
    items = day.get("suggestions", [])
    changed = []
    for item in items:
        iid = item.get("id")
        if iid in safe_updates:
            old = item.get("status")
            item["status"] = safe_updates[iid]["status"]
            item["result"] = safe_updates[iid]["result"]
            if old != item["status"]:
                changed.append(iid)
    save(TRACKER, data)
    impl = load(IMPLEMENTED)
    impl.setdefault(DATE, [])
    for iid in changed:
        impl[DATE].append(iid)
    save(IMPLEMENTED, impl)
    return {"updated": True, "changed": changed}

if __name__ == "__main__":
    out = apply_today()
    print(json.dumps(out, indent=2))
