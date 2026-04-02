from scanner import scan_project
from suggester import get_suggestions
from git_handler import push_to_github
import os

def run_agent():
    print("=" * 50)
    print("🤖 Smart Push Agent — Powered by GitAgent + Gemini")
    print("=" * 50)

    # Step 1: Get folder path
    folder_path = input("\n📁 Enter your project folder path: ").strip().strip('"\'')

    if not folder_path or not os.path.exists(folder_path):
        print("❌ Folder not found. Please check the path.")
        return

    # Step 2: Scan
    print("\n🔍 Scanning your project for problems...\n")
    problems = scan_project(folder_path)

    if not problems:
        print("✅ Your project looks clean! No problems found.")
    else:
        print(f"⚠️  Found {len(problems)} issue(s). Let me explain...\n")
        print("-" * 50)
        suggestions = get_suggestions(problems)
        print(suggestions)
        print("-" * 50)
        
        # Auto-fix feature
        fix_it = input("\n🛠️ Would you like me to automatically fix these issues? (yes/no): ").strip().lower()
        if fix_it == "yes":
            from auto_fixer import apply_fixes
            apply_fixes(problems, folder_path)
            print("✅ I applied fixes to your project!")
            
            # Re-scan to ensure they're fixed
            problems = scan_project(folder_path)
            if problems:
                print(f"⚠️ Still found {len(problems)} issue(s) that I couldn't fix automatically. Here is what is remaining:")
                for p in problems:
                    file_msg = f" in {p['file']}" if p['file'] else ""
                    print(f"   - [{p['type']}] {p['message']}{file_msg}")
            else:
                print("✅ All clean now! Ready to push.")

    # Step 3: Ask to proceed
    proceed = input("\n🚀 Do you still want to push to GitHub? (yes/no): ").strip().lower()

    if proceed != "yes":
        print("\n👍 Smart move! Fix the issues first, then run me again.")
        return

    # Step 4: Get GitHub details
    repo_url = input("\n🔗 Enter your GitHub repo URL (https://github.com/you/repo): ").strip()
    commit_msg = input("💬 Enter commit message (or press Enter for default): ").strip()

    if not commit_msg:
        commit_msg = "chore: pushed via smart-push-agent"

    # Step 5: Push!
    print("\n⏳ Pushing to GitHub...")
    result = push_to_github(folder_path, repo_url, commit_msg)
    print(result)

if __name__ == "__main__":
    run_agent()