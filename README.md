# 🤖 Smart Push Agent

Scans your project folder for problems before pushing to GitHub.

## What it checks
- 🔴 Exposed API keys / secrets
- 🟠 Missing .gitignore
- 🟡 Missing README
- 🟢 Bad Python practices

## How to run
pip install google-generativeai gitpython python-dotenv
python agent.py

## Built with
- GitAgent Standard
- Gemini AI
- GitPython