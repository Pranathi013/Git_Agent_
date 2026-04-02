import os
import re

def apply_fixes(problems, folder_path):
    for p in problems:
        if p["type"] == "missing_readme":
            with open(os.path.join(folder_path, "README.md"), "w", encoding="utf-8") as f:
                name = os.path.basename(os.path.normpath(folder_path))
                f.write(f"# {name}\n\nProject description goes here. This was auto-generated.\n")
        
        elif p["type"] == "missing_gitignore":
            with open(os.path.join(folder_path, ".gitignore"), "w", encoding="utf-8") as f:
                f.write("node_modules/\nvenv/\n__pycache__/\n.env\n*.pyc\n.DS_Store\n")
        
        elif p["type"] == "exposed_secret" and p["file"]:
            filepath = p["file"]
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace exact string matches for exposed secrets so they aren't pushed to github
                content = re.sub(r'(api_key\s*=\s*)["\'][\w-]+["\']', r'\1"YOUR_SECRET_HERE"', content, flags=re.IGNORECASE)
                content = re.sub(r'(password\s*=\s*)["\'][\w-]+["\']', r'\1"YOUR_PASSWORD_HERE"', content, flags=re.IGNORECASE)
                content = re.sub(r'(secret\s*=\s*)["\'][\w-]+["\']', r'\1"YOUR_SECRET_HERE"', content, flags=re.IGNORECASE)
                content = re.sub(r'(token\s*=\s*)["\'][\w-]+["\']', r'\1"YOUR_TOKEN_HERE"', content, flags=re.IGNORECASE)
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception:
                pass
                
        elif p["type"] == "bad_practice" and p["file"]:
            # filename format is "path/to/file (line N)"
            match = re.match(r"(.*) \(line (\d+)\)", p["file"])
            if match:
                filepath = match.group(1)
                line_idx = int(match.group(2)) - 1
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    
                    if 0 <= line_idx < len(lines):
                        lines[line_idx] = re.sub(r'except\s*:', 'except Exception as e:', lines[line_idx])
                    
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.writelines(lines)
                except Exception:
                    pass
