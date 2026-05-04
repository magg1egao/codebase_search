import re
import subprocess
from pathlib import Path
import tempfile
import shutil

from app.config import MAX_FILES, MAX_FILE_SIZE_BYTES, SKIP_DIRS, SUPPORTED

def normalize_github_url(repo_url: str) -> str:
    if not repo_url:
        raise ValueError("Provide a GitHub repository URL.")

    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]
    
    match_url = re.match(r"https://github\.com/([^/]+)/([^/#?]+)", repo_url)
    if not match_url:
        raise ValueError("Please use a public GitHub repo URL (example: https://github.com/psd/requests)")
    owner = match_url.group(1)
    repo = match_url.group(2)

    return f"https://github.com/{owner}/{repo}.git"

def make_repo_id(repo_url):
    normalized_url = repo_url.strip().replace(".git", "")
    match_url = re.match(r"https://github\.com/([^/]+)/([^/#?]+)", normalized_url)
    if not match_url:
        raise ValueError("Invalid GitHub repo URL")
    
    return f"{match_url.group(1)}__{match_url.group(2)}".lower()

def clone_repo(repo_url):
    clone_url = normalize_github_url(repo_url)

    temp_dir = Path(tempfile.mkdtemp(prefix="codebase_search_"))
    repo_dir = temp_dir / "repo"

    result = subprocess.run(
        ["git", "clone", "--depth", "1", clone_url, str(repo_dir)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=90
    )

    if result.returncode != 0:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise RuntimeError(f"Git clone failed:\n{result.stderr}")
    
    return repo_dir

def should_skip(path):
    return any(part in SKIP_DIRS for part in path.parts)

def collect_files(repo_dir):
    files = [] # all paths valid
    for path in repo_dir.rglob("*"):
        if len(files) >= MAX_FILES:
            break
        if not path.is_file():
            continue
        relative_path = path.relative_to(repo_dir)

        if should_skip(relative_path):
            continue

        if path.suffix.lower() not in SUPPORTED:
            continue

        try:
            if path.stat().st_size > MAX_FILE_SIZE_BYTES:
                continue
        except OSError:
            continue

        files.append(path)
    return files

# if __name__ == "__main__":
#     repo_dir = clone_repo("https://github.com/psf/requests")
#     files = collect_files(repo_dir)

#     print(repo_dir)
#     print(len(files))
#     print(files[:10])