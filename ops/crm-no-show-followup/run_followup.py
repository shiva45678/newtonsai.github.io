#!/usr/bin/env python3
"""
CRM No-Show Follow-Up Ops Runner
Dashboard item: o2 | Owner: Newtons AI Team
"""

import json, os, sys, textwrap
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).parent
CONFIG_PATH = BASE / "schedule.json"
STATE_PATH = BASE / "state" / "run_state.json"
LOG_PATH = BASE / "state" / "run.log"
DRY_RUN = os.environ.get("CRM_NO_DRY_RUN", "").lower() not in ("0", "false", "no", "")

PLACEHOLDERS = {
    "{{rep_name}}": "Newtons AI Team",
    "{{company}}": "Newtons AI",
    "{{product}}": "Easy HMS",
    "{{booking_link}}": "https://calendly.com/newtonsai/demo",
}

def log(msg):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")
    print(line)

def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)

def load_state():
    if STATE_PATH.exists():
        with open(STATE_PATH) as f:
            return json.load(f)
    return {"runs": [], "leads": {}, "last_run_ts": None}

def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2, default=str)

def is_business_day(dt):
    return dt.weekday() < 5

def next_business_morning(dt, hour=9):
    d = dt.replace(hour=hour, minute=0, second=0, microsecond=0)
    while not is_business_day(d):
        d += timedelta(days=1)
    return d

def within_quiet_hours(ts, quiet_start="21:00", quiet_end="09:00"):
    t = ts.strftime("%H:%M")
    if quiet_start <= quiet_end:
        return quiet_start <= t <= quiet_end
    return t >= quiet_start or t <= quiet_end

def fill_template(template, lead):
    data = dict(PLACEHOLDERS)
    data["{{target_name}}"] = lead.get("target_name", lead.get("chat_id", "there"))
    data["{{demo_date}}"] = lead.get("demo_date", "")
    data["{{demo_slot}}"] = lead.get("demo_slot", "")
    text = template
    for k, v in data.items():
        text = text.replace(k, v)
    return text

def build_fake_crm_leads():
    """Simulated CRM query — replace this hook with your real CRM integration."""
    return [
        {
            "chat_id": "chat_1001",
            "target_name": "Dr. Mehta - City Hospital",
            "demo_date": datetime.now().strftime("%Y-%m-%d"),
            "demo_slot": "11:00",
            "language": "en",
            "preferred_time_window": "morning",
            "touch_sent": [False, False, False, False],
        },
        {
            "chat_id": "chat_1002",
            "target_name": "Clinic Apollo Admin",
            "demo_date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "demo_slot": "15:30",
            "language": "en",
            "preferred_time_window": "afternoon",
            "touch_sent": [False, False, False, False],
        },
        {
            "chat_id": "chat_1003",
            "target_name": "NovaCare Ops Lead",
            "demo_date": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"),
            "demo_slot": "10:00",
            "language": "en",
            "preferred_time_window": "morning",
            "touch_sent": [True, False, False, False],
        },
    ]

def run():
    print("=" * 70)
    print("CRM No-Show Follow-Up Runner (o2) | Newtons AI Team")
    print("=" * 70)
    print(f"DRY RUN : {DRY_RUN}")
    print(f"CONFIG  : {CONFIG_PATH}")
    print(f"STATE    : {STATE_PATH}")
    print("=" * 70)

    config = load_config()
    state = load_state()

    leads = build_fake_crm_leads()
    sched = config["followup"]["schedule"]
    touches = sched["touches"]
    quiet = sched.get("quiet_hours", {})

    summary = {
        "run_ts": datetime.now().isoformat(),
        "dry_run": DRY_RUN,
        "leads_processed": 0,
        "messages_queued": [],
        "escalated": [],
        "errors": [],
    }

    for idx, lead in enumerate(leads):
        lead_key = lead["chat_id"]
        record = state.setdefault("leads", {}).setdefault(lead_key, {"touch_sent": [False, False, False, False], "history": []})

        # sync sent-touch shelf from state if first run
        if len(record.get("touch_sent", [])) < len(touches):
            record["touch_sent"] += [False] * (len(touches) - len(record["touch_sent"]))
        lead["touch_sent"] = record["touch_sent"]
        summary["leads_processed"] += 1

        for t in touches:
            idx_t = t["touch"] - 1
            if lead["touch_sent"][idx_t]:
                continue

            queue = {
                "lead": lead_key,
                "target_name": lead["target_name"],
                "touch": t["touch"],
                "channel": t["channel"],
                "template": t["template_ref"],
                "demo_date": lead.get("demo_date"),
                "demo_slot": lead.get("demo_slot"),
            }

            if not DRY_RUN:
                #在这儿 你可以调用实际的发送API
                pass

            lead["touch_sent"][idx_t] = True
            record["touch_sent"] = lead["touch_sent"]
            record["history"].append({
                "ts": datetime.now().isoformat(),
                "touch": t["touch"],
                "status": "queued" if DRY_RUN else "sent",
            })
            summary["messages_queued"].append(queue)
            log(f"QUEUED touch {t['touch']} -> {lead['target_name']} ({lead_key}) via {t['channel']}")

        # escalation logic
        if all(lead["touch_sent"]):
            summary["escalated"].append(lead_key)
            record["escalated"] = True
            record["escalated_at"] = datetime.now().isoformat()
            log(f"ESCALATE -> {lead['target_name']} ({lead_key}): flag for SDR review")

    state["last_run_ts"] = datetime.now().isoformat()
    state["leads"] = {k: v for k, v in state.get("leads", {}).items() if k in {l["chat_id"] for l in leads}}
    save_state(state)

    # Persist structured run summary
    summary_path = BASE / "state" / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    latest_summary = BASE / "state" / "latest_run_summary.json"
    with open(latest_summary, "w") as f:
        json.dump(summary, f, indent=2, default=str)

    log(f"Run complete. Summary -> {latest_summary}")
    log(f"State saved at -> {STATE_PATH}")
    print(f"\n[OUTPUT] Latest run state: {latest_summary}")

if __name__ == "__main__":
    run()
