from fastapi.testclient import TestClient
from types import SimpleNamespace

def test_chat_endpoint(mocker):

    from app.main import app

    from app.knowledge.dependencies import (
        get_chat_service
    )

    from app.auth.security.jwt_auth import (
        get_current_user
    )


    mock_service = mocker.Mock()


    mock_service.ask = (
        mocker.AsyncMock(
            return_value={
                "conversation_id": "123",
                "answer":
                    "Company provides 20 leave days.",
                "sources": [],
                "metrics": {
                    "retrieval_latency": 0.05,
                    "llm_latency": 0.15,
                    "total_latency": 0.2
                },
                "usage": None
            }
        )
    )


    # Mock Chat Service
    app.dependency_overrides[
        get_chat_service
    ] = lambda: mock_service


    # Mock JWT user
    app.dependency_overrides[
        get_current_user
     ] = lambda: SimpleNamespace(
            id="test-user",
            username="test",
    )


    client = TestClient(app)


    response = client.post(
        "/api/v1/chat",
        json={
            "question": "Leave policy"
        }
    )

    print(response.json())

    assert response.status_code == 200


    data = response.json()

    assert (
        data["answer"]
        ==
        "Company provides 20 leave days."
    )


    app.dependency_overrides.clear()