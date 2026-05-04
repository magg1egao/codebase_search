SUPPORTED = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    "tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".scala",
    ".kt",
    ".swift",
    ".txt",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".md"
}

SKIP_DIRS = {
    ".git", 
    "venv",
    ".venv",
    "node_modules",
    "__pycache__",
    "build",
    ".vs_code",
    ".cache"
}

MAX_FILES = 300
MAX_FILE_SIZE_BYTES = 120_000

CHUNK_LINE_COUNT = 80
CHUNK_OVERLAP = 20

RETRIEVAL_TOP_K = 20
RERANK_TOP_N = 5
EMBED_BATCH_SIZE = 64

EMBED_MODEL = "embed-v4.0"
RERANK_MODEL = "rerank-v4.0-pro"
CHAT_MODEL = "command-a-03-2025"

