from pathlib import Path
from app.config import CHUNK_LINE_COUNT, CHUNK_OVERLAP
from app.models import CodeChunk

def read_text_file(path): 
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1", errors="ignore")

def chunk_file(repo_id, repo_dir, file_path):
    relative_path = str(file_path.relative_to(repo_dir))
    text = read_text_file(file_path)
    lines = text.splitlines()

    chunks = []
    step = max(1, CHUNK_LINE_COUNT  - CHUNK_OVERLAP)

    for i in range(0, len(lines), step):
        j = min(i + CHUNK_LINE_COUNT, len(lines))
        chunk_text = "\n".join(lines[i:j]).strip()

        if len(chunk_text) < 80:
            continue
        
        chunks.append(
            CodeChunk(
                repo_id = repo_id,
                path = relative_path,
                start_line = i+1,
                end_line = j,
                text = chunk_text
            )
        )
    return chunks

def chunk_files(repo_id, repo_dir, files):
    chunks = []
    for path in files:
        chunks.extend(chunk_file(repo_id, repo_dir, path))
    return chunks

# if __name__ == "__main__":
#     from app.github_load import clone_repo, collect_files, make_repo_id

#     repo_url = "https://github.com/psf/requests"
#     repo_id = make_repo_id(repo_url)
#     repo_dir = clone_repo(repo_url)
#     files = collect_files(repo_dir)
#     chunks = chunk_files(repo_id, repo_dir, files)

#     print("repo_id:", repo_id)
#     print("files:", len(files))
#     print("chunks:", len(chunks))
#     print()
#     print(chunks[0].label())
#     print(chunks[0].text[:500])