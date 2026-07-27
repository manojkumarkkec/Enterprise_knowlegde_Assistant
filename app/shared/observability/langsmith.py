import os


def setup_langsmith():


    os.environ[
        "LANGCHAIN_TRACING_V2"
    ] = "true"


    os.environ[
        "LANGCHAIN_PROJECT"
    ] = (
        "enterprise-knowledge-assistant"
    )