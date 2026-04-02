import os
import re

def scan_project(folder_path):
    problems = []

    files = os.listdir(folder_path)

    # 1. Check for missing README
    if "README.md" not in files and "README.txt" not in files:
        problems.append({
            "type": "missing_readme",
            "severity": "medium",
            "message": "No README file found",
            "file": None
        })

    # 2. Check for missing .gitignore
    if ".gitignore" not in files:
        problems.append({
            "type": "missing_gitignore",
            "severity": "high",
            "message": "No .gitignore file found",
            "file": None
        })

    # 3. Check for exposed secrets
    secret_patterns = [
        r'api_key\s*=\s*["\'][\w-]+["\']',
        r'password\s*=\s*["\'][\w-]+["\']',
        r'secret\s*=\s*["\'][\w-]+["\']',
        r'token\s*=\s*["\'][\w-]+["\']',
        r'sk-[a-zA-Z0-9]{40,}',
        r'ghp_[a-zA-Z0-9]{36}',
    ]

    for root, dirs, filenames in os.walk(folder_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')
                   and d not in ['venv', 'node_modules', '__pycache__']]

        for filename in filenames:
            if filename.endswith(('.py', '.js', '.env', '.txt', '.yaml', '.json')):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                        # Remove dummy placeholders from content before scanning so we don't flag our own auto-fixes
                        content = content.replace("YOUR_SECRET_HERE", "").replace("YOUR_TOKEN_HERE", "").replace("YOUR_PASSWORD_HERE", "")

                        for pattern in secret_patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                problems.append({
                                    "type": "exposed_secret",
                                    "severity": "critical",
                                    "message": "Possible secret/API key found",
                                    "file": filepath
                                })
                                break
                except Exception:
                    pass

    # 4. Check for bad Python practices
    for root, dirs, filenames in os.walk(folder_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')
                   and d not in ['venv', 'node_modules', '__pycache__']]

        for filename in filenames:
            if filename.endswith('.py'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for i, line in enumerate(lines, 1):
                            if re.search(r'except\s*:', line):
                                problems.append({
                                    "type": "bad_practice",
                                    "severity": "low",
                                    "message": "Bare 'except Exception as e:' found (catches ALL errors, risky)",
                                    "file": f"{filepath} (line {i})"
                                })
                except Exception:
                    pass

    return problems