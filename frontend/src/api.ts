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