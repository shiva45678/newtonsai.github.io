#!/usr/bin/env python3
"""Generate or refresh the daily brief and write index.html.

Behavior for this template:
- Update header datetime to now.
- Rotate today's focus items to simulate a fresh daily brief.
"""
from __future__ import annotations

import datetime
import random
import html as ihtml
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "index.html"

MORNING = [
    ("KPI", "Overnight pipeline: <strong>{n}</strong> new opportunities"),
    ("Alert", "{n} deals &gt;$10k move to next stage"),
    ("Action", "Outreach cadence review at 10:00"),
    ("Focus", "Q3 pipeline coverage back on target"),
]
EVENING = [
    ("Meetings", "{n} demos completed"),
    ("Won", "Alpha — $18,500 annual contract"),
    ("Blocked", "Beta lab testing delayed by {n} days"),
    ("Score", "Team attainment: <strong>{pct}%</strong> of monthly goal"),
]
CALLOUT = [
    "Follow up with <strong>Beta</strong> by EOD to unlock Q3 close",
    "Send updated proposal to <strong>Gamma</strong> and book technical review",
]


def pick(items, n=2):
    return random.sample(items, k=min(n, len(items)))


def build_section(items):
    return "\n".join(
        f'<li><span class="pill">{tag}</span> {text}</li>' for tag, text in items
    )


def main() -> int:
    now = datetime.datetime.now(datetime.timezone.utc)
    random.seed(now.date().isoformat())
    morning = build_section([(t, v.format(n=random.randint(1,7), pct=random.randint(55,92))) for t,v in pick(MORNING)])
    evening = build_section([(t, v.format(n=random.randint(1,5), pct=random.randint(55,92))) for t,v in pick(EVENING)])
    callout = "\n".join(f"<li>{i}</li>" for i in random.sample(CALLOUT, k=min(2, len(CALLOUT))))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Newton's AI Daily Brief</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: #0f1115;
    color: #e6e8eb;
  }}
  header {{
    padding: 24px;
    text-align: center;
    border-bottom: 1px solid #23262d;
    background: linear-gradient(180deg, #161a24 0%, #0f1115 100%);
  }}
  h1 {{
    margin: 0;
    font-size: 22px;
    letter-spacing: 0.5px;
  }}
  .sub {{
    margin-top: 6px;
    color: #9aa0a6;
    font-size: 13px;
  }}
  .container {{
    max-width: 960px;
    margin: 0 auto;
    padding: 24px 16px 64px;
  }}
  .grid {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
  }}
  @media (min-width: 900px) {{ .grid {{ grid-template-columns: 1fr 1fr; }} }}
  .card {{
    background: #161a24;
    border: 1px solid #23262d;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 4px 0 rgba(0,0,0,0.25);
  }}
  .card h2 {{
    margin: 0 0 10px;
    font-size: 16px;
    color: #ffd54a;
  }}
  .card ul {{
    margin: 0;
    padding-left: 18px;
    line-height: 1.6;
    color: #d8dce2;
  }}
  .callout {{
    margin-top: 20px;
    background: #1c2230;
    border-left: 4px solid #60c0f8;
    padding: 16px 18px;
    border-radius: 8px;
  }}
  .callout h2 {{
    margin: 0 0 8px;
    color: #60c0f8;
  }}
  footer {{
    text-align: center;
    padding: 20px;
    color: #9aa0a6;
    font-size: 12px;
  }}
  .pill {{
    display: inline-block;
    background: #23262d;
    color: #e6e8eb;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 11px;
    margin-right: 6px;
    vertical-align: middle;
  }}
</style>
</head>
<body>
<header>
  <h1>Newton's AI — Daily Brief</h1>
  <div class="sub">{now.strftime('%A, %d %b %Y · %H:%M:%S UTC')}</div>
</header>
<main class="container">
  <div class="grid">
    <div class="card">
      <h2>Morning Brief</h2>
      <ul>
        {morning}
      </ul>
    </div>
    <div class="card">
      <h2>Evening Review</h2>
      <ul>
        {evening}
      </ul>
    </div>
  </div>

  <div class="callout">
    <h2>Action Callout</h2>
    <ul>
        {callout}
    </ul>
  </div>
</main>
<footer>
  © {now.year} Newton's AI · Generated for Newtons AI (shiva452648)
</footer>
</body>
</html>
"""
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
