# Newton's AI Daily Brief

This repo feeds the GitHub Pages site at:
- Repo: https://github.com/shiva45678/newtonsai.github.io
- Pages: https://shiva45678.github.io
- Branch used by Pages: `gh-pages`

## Repo contents
- `index.html` — dark UI with Morning Brief, Evening Review, Action Callout
- `daily-update.yml` — GitHub Actions to refresh the brief daily
- `update_brief.py` — optional helper to regenerate/timestamp the file

## First setup
1. Push the included `gh-pages` branch to remote (see script in `push-to-github.sh` / instructions below).
2. In the repo settings → Pages → set Source to `gh-pages`.

Workflow will run automatically once push is complete.
