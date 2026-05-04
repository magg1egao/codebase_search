from pydantic import BaseModel

class IndexRequest(BaseModel):
    repo_url: str

class IndexResponse(BaseModel):
    repo_id: str
    repo_url: str
    file_count: int
    chunk_count: int

class Request(BaseModel):
    repo_id: str
    query: str

class Chunk(BaseModel):
    path: str
    start_line: int
    end_line: int
    score: float | None = None
    text: str

class Response(BaseModel):
    answer: str
    sources: list[Chunk]
    initial_sources: list[Chunk]
    