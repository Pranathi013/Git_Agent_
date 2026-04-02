# 🤖 Smart Push Agent

Scans your project folder for problems before pushing to GitHub.

## What it checks
- 🔴 Exposed API keys / secrets
- 🟠 Missing .gitignore
- 🟡 Missing README
- 🟢 Bad Python practices

## How to run
```bash
pip install groq gitpython python-dotenv
python agent.py
```

## Built with
- GitAgent Standard
- Groq AI (Llama-3)
- GitPython