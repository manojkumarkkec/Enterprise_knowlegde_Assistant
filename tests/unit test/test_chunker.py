from app.knowledge.ingestion.chunker import TextChunker


def test_text_chunker_creates_chunks():

    text = """
    This is a sample enterprise document.
    It contains multiple sentences.
    The chunker should split this text.
    """

    chunker = TextChunker(
        chunk_size=50,
        overlap=10
    )

    chunks = chunker.split(text)


    assert len(chunks) > 0
    assert isinstance(chunks[0], str)