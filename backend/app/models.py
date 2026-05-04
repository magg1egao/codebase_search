from dataclasses import dataclass

@dataclass
class CodeChunk:
    repo_id: str
    path: str
    start_line: int
    end_line: int
    text: str

    def label(self):
        return f"{self.path}:{self.start_line}-{self.end_line}"
    def as_document(self):
        return f"File: {self.path}\n"
        f"Lines: {self.start_line}-{self.end_line}\n"
        f"{self.text}"
