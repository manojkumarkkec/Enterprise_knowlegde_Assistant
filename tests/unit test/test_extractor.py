import pytest

from app.knowledge.ingestion.extractor import DocumentExtractor


@pytest.mark.asyncio
async def test_extractor_returns_text():

    extractor = DocumentExtractor()

    result = await extractor.extract(
        "tests/sample.pdf"
    )

    assert result is not None
    assert isinstance(result, str)