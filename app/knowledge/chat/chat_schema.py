from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    conversation_id: str | None = None
    department: str | None = None
    top_k: int = 5


class Source(BaseModel):

    document_id: str | None = None

    filename: str | None = None

    chunk_index: int | None = None

    score: float | None = None


class Metrics(BaseModel):

    retrieval_latency: float

    llm_latency: float

    total_latency: float


class Usage(BaseModel):

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int


class ChatResponse(BaseModel):

    conversation_id: str

    answer: str

    sources: list[Source]

    metrics: Metrics

    usage: Usage | None = None