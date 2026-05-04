import shutil
from dataclasses import dataclass
import numpy as np

from app.chunker import chunk_files
from app.cohere import embed_texts, get_cohere_client, rerank, prompt_answer
from app.config import RETRIEVAL_TOP_K
from app.github_load import clone_repo, collect_files, make_repo_id
from app.models import CodeChunk
from app.search import get_top_chunks

@dataclass
class RepoIdx:
    repo_id: str
    repo_url: str
    file_count: int
    chunks: list[CodeChunk]
    embeddings: np.ndarray

INDEXED_REPOS = {}

def index_repository(repo_url):
    client = get_cohere_client()
    repo_id = make_repo_id(repo_url)
    repo_dir = clone_repo(repo_url)

    try:
        files = collect_files(repo_dir)
        chunks = chunk_files(repo_id = repo_id, repo_dir=repo_dir, files =files)

        if not chunks:
            raise RuntimeError("No supported files found in this repository")
        embeddings = embed_texts(
            client=client,
            texts=[c.as_document() for c in chunks],
            input_type = "search_document"
        )

        repo_index = RepoIdx(
            repo_id = repo_id,
            repo_url=repo_url,
            file_count = len(files),
            chunks=chunks,
            embeddings = embeddings
        )

        INDEXED_REPOS[repo_id] = repo_index
        return repo_index
    finally:
        shutil.rmtree(repo_dir.parent, ignore_errors = True)

def get_indexed_repo(repo_id: str):
    if repo_id not in INDEXED_REPOS:
        raise KeyError(
            f"Repository '{repo_id}' has not been indexed yet. "
        )

    return INDEXED_REPOS[repo_id]

def ask_query(repo_id, query):
    client = get_cohere_client()
    repo_index = get_indexed_repo(repo_id)

    query_embeddings = embed_texts(
        client=client,
        texts = [query],
        input_type="search_query"
    )[0]

    initial_results = get_top_chunks(
        query = query,
        query_emb = query_embeddings,
        chunks = repo_index.chunks,
        chunk_embeddings = repo_index.embeddings, 
        top_k = RETRIEVAL_TOP_K
    )

    chunks = [c for c,_ in initial_results]
    reranked_results = rerank(
        client=client, query=query, chunks = chunks
    )

    final_chunks = [c for c,_ in reranked_results]
    answer = prompt_answer(client=client, query=query, chunks=final_chunks)

    return answer, reranked_results, initial_results