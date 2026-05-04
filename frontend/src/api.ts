const API_BASE_URL = "http://127.0.0.1:8000";

export async function checkHealth(): Promise<{ status:string}> {
    const response = await fetch(`${API_BASE_URL}/check`);
    if (!response.ok) {
        throw new Error("Backend health checkpoint failed");
    }
    return response.json();
}

export type IndexResponse = {
    repo_id: string;
    repo_url: string;
    file_count: number;
    chunk_count:number;
};

export type Chunk = {
    path: string;
    start_line: number;
    end_line: number;
    score: number | null;
    text: string;
};

export type Response = {
    answer: string;
    sources: Chunk[];
    initial_sources: Chunk[];
}
    
    

export async function indexRepo(repoUrl:string): Promise<IndexResponse> {
    const response = await fetch(`${API_BASE_URL}/index`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            repo_url: repoUrl
        })
    });

    if (!response.ok) {
        const err = await response.json().catch(()=>null);
        throw new Error(err?.detail || "Failed to index repo");
    }
    return response.json();
}

export async function answerQuery(repoId: string, query: string): Promise<Response> {
    const response = await fetch(`${API_BASE_URL}/ask`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            repo_id: repoId,
            query: query
        })
    })

    if (!response.ok) {
        const err = await response.json().catch(()=>null);
        throw new Error(err?.detail || "Failed to ask query");
    }

    return response.json();
}