@echo off
chcp 65001 >nul
setlocal
cd /d %~dp0

REM Local daily push workflow (PowerShell friendly)
echo [local push] making sure local repo is in sync...
git pull --rebase origin main

echo [local push] regenerating brief...
python update_brief.py

echo [local push] committing and pushing main...
git add -A
git diff --cached --quiet && echo No changes & exit /b 0
git commit -m "chore: daily brief update %date% %time%"
git push origin main

echo [local push] syncing gh-pages from main...
git checkout gh-pages
git merge main --no-edit
git push origin gh-pages
git checkout main

endlocal
