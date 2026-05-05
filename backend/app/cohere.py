import os
import cohere
import numpy as np
from dotenv import load_dotenv
import time

from app.config import EMBED_MODEL, CHAT_MODEL, RERANK_MODEL, RERANK_TOP_N, EMBED_BATCH_SIZE
from app.models import CodeChunk


load_dotenv()

def get_cohere_client():
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing COHERE_API_KEY")
    return cohere.ClientV2(api_key=api_key)

def embed_texts(client, texts, input_type):
    vectors = []
    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[i: i+EMBED_BATCH_SIZE]

        response = client.embed(
            texts = batch,
            model=EMBED_MODEL,
            input_type = input_type,
            # output_dimension=1024,
            embedding_types = ["float"]
        )
        vectors.extend(response.embeddings.float)
        # time.sleep(1)
    embeddings = np.array(vectors, dtype=np.float32)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms==0] =1
    return embeddings/norms

def rerank(client, query, chunks):
    docs = [c.as_document() for c in chunks]
    results = client.rerank(model=RERANK_MODEL, query=query, documents=docs, top_n = min(len(docs),RERANK_TOP_N))

    ret = []
    for r in results.results:
        ret.append((chunks[r.index], float(r.relevance_score)))

    return ret

def extract_text(response):
    content = response.message.content
    if isinstance(content, list):
        return "\n".join(getattr(item, "text", str(item)) for item in content)
    return str(content)

def prompt_answer(client, query, chunks):
    context = "\n\n---\n\n".join(c.as_document() for c in chunks)
    prompt = f"""
    You are a Codebase Search tool. A tool that explains unfamiliar GitHub repositories.

    Answer the user's question using the provided code context.

    Rules:
    - Be specific and practical
    - Cite the file paths and line ranges like 'path/to/file.py:10-30'
    - If the context is insufficient, say what is missing and do not guess

    User question: {query}

    Code context: {context}"""

    res = client.chat(
        model=CHAT_MODEL,
        messages = [{
            "role":"user",
            "content":prompt
        }]
    )
    return extract_text(res)

# if __name__ == "__main__":
#     client = get_cohere_client()
#     embeddings = embed_texts(
#         client=client,
#         texts=["def hello(): return 'world'"],
#         input_type="search_document",
#     )

#     print(embeddings.shape)
#     print(embeddings[0][:5])