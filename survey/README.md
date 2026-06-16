# Newtons AI — Doctor Onboarding Survey
Dashboard item: `b3`
Owner: Newtons AI Team
Due: 2026-06-18
Status: Executed

## What this is
A 5-question day-1 post-onboarding survey to catch doctor friction fast.
Artifact: `survey/index.html`

## Questions
1. Setup speed
2. Clarity of first task
3. Biggest friction point
4. Confidence using Notes / Orders
5. Open feedback (one thing to fix before next shift)

Optional fields: Doctor ID/Name, Facility/Location.

## Local use
Open the file directly in a browser:

- `start "" "C:\Users\chandu\newtonsai-daily-brief\survey\index.html"`

## Deploy
This is a static HTML page. You can deploy it by copying `survey/index.html` (and optional assets) to any static host, such as:
- GitHub Pages (new repo or `/docs` or `/survey` folder in this repo)
- Cloudflare Pages
- Any web server serving static files

No build step, backend, or database is required. Responses are stored locally via `localStorage` for demo/testing.

## Exported data
Use the built-in **Export JSON** button in the UI to export responses as a JSON file.
