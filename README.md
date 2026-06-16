# Newtons AI Daily Brief

GitHub Pages site with a dark UI daily brief.

- Repository: https://github.com/shiva45678/newtonsai.github.io
- Pages URL: https://shiva45678.github.io
- Pages source branch: gh-pages

## First deployment status

Add this repo URL to Pages in GitHub Settings → Pages → Source = gh-pages. Since we pushed the `gh-pages` branch, GitHub will render `index.html` within minutes.

## Contents

- `index.html` — dark UI: Morning Brief, Evening Review, Top Action Callout
- `.github/workflows/daily-update.yml` — GitHub Actions workflow that refreshes the site automatically each day
  - Time: 00:00 UTC
  - Trigger mode: schedule + workflow_dispatch
- `update_brief.py` — helper script that refreshes token-stamped content and rewrites `index.html`
- `push-to-github.bat` — exact local workflow runnable from Windows to update and push `main` and `gh-pages`

## Local update workflow (Windows)

From this folder:

```
push-to-github.bat
```

What it does:

```
git pull --rebase origin main
python update_brief.py
git add -A
git commit -m "chore: daily brief update <timestamp>"
git push origin main
git checkout gh-pages
git merge main --no-edit
git push origin gh-pages
git checkout main
```

## Notes

- Repo was created under user account `shiva45678` because the org `Newtons AI` was not found or not accessible with current credentials.
- GitHub Actions has `contents: write` permission and only touches `main`; Pages keeps rendering from `gh-pages`.
