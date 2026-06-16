# CRM No-Show Follow-Up Automation — Process Doc

> Owner: Newtons AI Team  
> Area: Workflow  
> Dashboard Item: **o2** — Automate follow-up reminders for demo-no-show leads in CRM  
> Package Path: `newtonsai-daily-brief/ops/crm-no-show-followup/`

---

## What This Package Does

- Pulls CRM leads with `demo_status = no_show` and `followup_sent = false`.
- Sends up to 4 configurable in-app follow-up touches at T+2h, next business morning, day 3, and day 7.
- Quiet hours respected (21:00–09:00 configurable).
- After 4 touches with no response → auto-escalate to SDR review queue.
- Idempotent per-lead: re-running never double-sends the same touch.
- All run state and output written to local files.

---

## Package Layout

```
newtonsai-daily-brief/
  ops/
    crm-no-show-followup/
      run_followup.py           # main runner
      schedule.json             # configurable schedule + owner metadata
      templates/
        touch1_t0_immediate.txt
        touch2_t1_next_day.txt
        touch3_t3_followup.txt
        touch4_t7_winback.txt
      state/
        run.log                 # human-readable execution log
        run_state.json          # per-lead state shelf (which touches sent)
        latest_run_summary.json # last run structured output
        <timestamp>_run.json    # timestamped snapshot of each run
```

---

## Placeholders (filled at send time)

| Placeholder | Source | Example |
|---|---|---|
| `{{target_name}}` | `chat_id` or `target_name` from CRM lead | Dr. Mehta - City Hospital |
| `{{demo_date}}` | lead.demo_date | 2026-06-15 |
| `{{demo_slot}}` | lead.demo_slot | 11:00 |
| `{{rep_name}}` | config (static) | Newtons AI Team |
| `{{company}}` | config (static) | Newtons AI |
| `{{product}}` | config (static) | Easy HMS |
| `{{booking_link}}` | config (static) | https://calendly.com/newtonsai/demo |

> Note: leads are addressed by **chat/target names only** — no personal names.

---

## How to Run It Now

### Prerequisites
- Python 3.9+ available in PATH (already available).
- No extra packages required.

### One-command run (dry-run by default)

```bash
cd /c/Users/chandu/newtonsai-daily-brief/ops/crm-no-show-followup
python run_followup.py
```

Output files created on every run:
- `state/latest_run_summary.json` — structured JSON of the latest run
- `state/run.log` — human-readable append-only log
- `state/run_state.json` — persistent shelf of touch status per lead

### Disable dry-run (real sends)

Daily brief workflow runs dry-run first. To actually send:

```bash
python -c "import os; os.environ['CRM_NO_DRY_RUN']='1'" && python run_followup.py
```

---

## Configurable Schedule

Edit `schedule.json` to tune timing, message count, or channels:

- **Touches**: `schedule.touches` — add, remove, or reorder. Minimum: keep field names `touch`, `delay_hours`, `channel`, `template_ref`.
- **Quiet Hours**: `schedule.quiet_hours.start` / `.end` — 24h format (`HH:MM`).
- **Escalation**: `schedule.escalation` — configure what happens after touch N with no response.
- **Owner / Area / Dashboard item**: top-level `followup.owner`, `followup.area`, `followup.dashboard_item`.

---

## Integrating a Real CRM

The script currently uses a simulated lead source (`build_fake_crm_leads()`). To wire your CRM:

1. Locate `build_fake_crm_leads()` in `run_followup.py`.
2. Replace its body with a call to your CRM fetch logic (API/SDK/CSV).
3. Return a list of dicts matching `lead_schema` from `schedule.json`.
4. Set `CRM_NO_DRY_RUN=1` for real sends and hook actual message dispatch in the `if not DRY_RUN:` block inside the loop.

---

## Verifying the Run

```bash
# View last run output
cat newtonsai-daily-brief/ops/crm-no-show-followup/state/latest_run_summary.json

# View per-lead state (touches sent / escalated)
cat newtonsai-daily-brief/ops/crm-no-show-followup/state/run_state.json

# View execution log
cat newtonsai-daily-brief/ops/crm-no-show-followup/state/run.log
```

---

## Status (as of this run)

| Run # | Timestamp | Leads | Touches Queued | Escalated | Mode |
|---|---|---|---|---|---|
| 1 | 2026-06-17T00:36:39 | 3 | 12 | 3 | dry_run=False (demo) |
| 2 | 2026-06-17T00:36:55 | 3 | 0 | 3 | idempotent re-run |

Artifacts saved to:
- `ops/crm-no-show-followup/state/latest_run_summary.json`
- `ops/crm-no-show-followup/state/run_state.json`
- `ops/crm-no-show-followup/state/run.log`
