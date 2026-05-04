import numpy as np
from app.models import CodeChunk
import re

def get_top_chunks(query, query_emb, chunks, chunk_embeddings, top_k):
    if not chunks:
        return []

    if chunk_embeddings.shape[0] != len(chunks):
        raise ValueError(
            f"Got {chunk_embeddings.shape[0]} embeddings for {len(chunks)} chunks"
        )

    scores = np.dot(chunk_embeddings, query_emb)
    scores = normalize_scores(scores)

    keyword_scores = np.array(
        [keyword_score(query, chunk) for chunk in chunks],
        dtype=np.float32
    )
    keyword_scores = normalize_scores(keyword_scores)

    combined_scores = 0.7*scores + 0.3*keyword_scores

    top_k = min(top_k, len(chunks))
    top_indices = np.argsort(combined_scores)[::-1][:top_k]

    ret = []
    for i in top_indices:
        ret.append((chunks[int(i)], float(combined_scores[int(i)])))
    return ret

def extract_query_terms(query):
    terms = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", query)
    return [term.lower() for term in terms if len(term) >= 3]

def keyword_score(query, chunk):
    terms = extract_query_terms(query)
    if not terms: return 0.0

    searchable_text = f"{chunk.path}\n{chunk.text}".lower()
    score = 0.0

    for t in terms:
        if t in searchable_text:
            score += 1.0
            if "_" in t:
                score += 3.0
    return score

def normalize_scores(scores):
    min_s = float(np.min(scores))
    max_s = float(np.max(scores))

    if max_s == min_s:
        return np.zeros_like(scores)

    return (scores - min_s) / (max_s - min_s)

if __name__ == "__main__":
    from app.cohere import embed_texts, get_cohere_client
    from app.github_load import clone_repo, collect_files, make_repo_id
    from app.chunker import chunk_files
    from app.config import RETRIEVAL_TOP_K

    repo_url = "https://github.com/psf/requests"

    client = get_cohere_client()

    repo_id = make_repo_id(repo_url)
    repo_dir = clone_repo(repo_url)

    files = collect_files(repo_dir)
    chunks = chunk_files(repo_id, repo_dir, files)

    chunk_embeddings = embed_texts(
        client=client,
        texts=[chunk.as_document() for chunk in chunks],
        input_type="search_document",
    )

    question = "Where is resolve_redirects implemented?"

    question_embedding = embed_texts(
        client=client,
        texts=[question],
        input_type="search_query",
    )[0]

    results = get_top_chunks(
        query=question,
        query_emb=question_embedding,
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
        top_k=RETRIEVAL_TOP_K,
    )

    for chunk, score in results:
        print(score, chunk.label())

    from app.cohere import rerank

    candidate_chunks = [chunk for chunk, _ in results]

    reranked_results = rerank(
        client=client,
        query=question,
        chunks=candidate_chunks,
    )

    print("\nRERANKED RESULTS")
    for chunk, score in reranked_results:
        print(score, chunk.label())