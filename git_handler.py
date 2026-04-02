import git
import os
from dotenv import load_dotenv

load_dotenv()

def push_to_github(folder_path, repo_url, commit_message):
    try:
        token = os.getenv("GITHUB_TOKEN")

        # Inject token into URL
        # e.g. https://github.com/user/repo → https://TOKEN@github.com/user/repo
        auth_url = repo_url.replace("https://", f"https://{token}@")

        if os.path.exists(os.path.join(folder_path, '.git')):
            repo = git.Repo(folder_path)
        else:
            repo = git.Repo.init(folder_path)
            repo.create_remote('origin', auth_url)

        repo.git.add('--all')
        repo.index.commit(commit_message)

        origin = repo.remote(name='origin')
        origin.set_url(auth_url)
        origin.push(refspec='HEAD:main', force=True)

        return "✅ Successfully pushed to GitHub!"

    except Exception as e:
        return f"❌ Push failed: {str(e)}"