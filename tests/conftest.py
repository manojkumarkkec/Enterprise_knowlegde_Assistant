import pytest
import os

os.environ["DATABASE_URL"] = (
    "postgresql+asyncpg://postgres:postgres@localhost:5432/testdb"
)

os.environ["SECRET_KEY"] = "test-secret"

os.environ["AZURE_OPENAI_ENDPOINT"] = (
    "https://test.openai.azure.com"
)

os.environ["AZURE_OPENAI_KEY"] = "test-key"

os.environ["AZURE_OPENAI_API_VERSION"] = (
    "2025-01-01-preview"
)

os.environ["AZURE_OPENAI_DEPLOYMENT"] = (
    "gpt-test"
)


@pytest.fixture(scope="session", autouse=True)
def load_models():

    from app.knowledge.models.document_chunk import DocumentChunk
    from app.knowledge.models.vector_embedding import VectorEmbedding
    from app.knowledge.models.conversation import Conversation
    from app.knowledge.models.message import Message

    return True

@pytest.fixture
def sample_contexts():

    return [
        {
            "content": "Employees get 20 annual leaves.",
            "metadata": {
                "filename": "HR_policy.pdf",
                "chunk_index": 1,
            },
        }
    ]



@pytest.fixture
def sample_history():

    return []

