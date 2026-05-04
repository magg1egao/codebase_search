from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.pipeline import index_repository, ask_query
from app.schemas import Request, Response, IndexRequest, IndexResponse, Chunk

app = FastAPI(title = "Codebase Search")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/check")
def check():
    return {"status": "ok"}

@app.post("/index", response_model=IndexResponse)
def index_repo(request: IndexRequest):
    try:
        repo_index = index_repository(request.repo_url)
        return IndexResponse(
            repo_id=repo_index.repo_id,
            repo_url=repo_index.repo_url,
            file_count=repo_index.file_count,
            chunk_count=len(repo_index.chunks)
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/ask", response_model=Response)
def ask_repo_query(request: Request):
    try:
        answer, reranked_results, initial_results = ask_query(repo_id=request.repo_id, query=request.query)
    
        sources = [Chunk(
            path=chunk.path,
            start_line=chunk.start_line,
            end_line=chunk.end_line,
            score=score,
            text=chunk.text,
        ) for chunk,score in reranked_results]

        initial_sources = [Chunk(
            path=chunk.path,
            start_line=chunk.start_line,
            end_line=chunk.end_line,
            score=score,
            text=chunk.text,
        ) for chunk,score in initial_results]

        return Response(
            answer=answer, sources=sources, initial_sources=initial_sources
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
