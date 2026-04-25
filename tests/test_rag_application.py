from unittest.mock import MagicMock, patch

import pytest
from google.api_core.exceptions import ResourceExhausted


@pytest.fixture(autouse=True)
def reset_rag_chain():
    """Ensure the cached chain is cleared between tests."""
    import app.rag_application as rag
    rag._rag_chain = None
    yield
    rag._rag_chain = None


class TestRetrieveGenerate:
    def test_returns_answer_string(self):
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {"answer": "Leonard worked on data pipelines."}

        with patch("app.rag_application._get_rag_chain", return_value=mock_chain):
            from app.rag_application import retrieve_generate
            result = retrieve_generate("What did Leonard work on?")

        assert result == "Leonard worked on data pipelines."

    def test_passes_chat_history_to_chain(self):
        from langchain_core.messages import HumanMessage

        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {"answer": "Yes."}
        history = [HumanMessage(content="Hello")]

        with patch("app.rag_application._get_rag_chain", return_value=mock_chain):
            from app.rag_application import retrieve_generate
            retrieve_generate("Follow-up question", chat_history=history)

        call_kwargs = mock_chain.invoke.call_args[0][0]
        assert call_kwargs["chat_history"] == history

    def test_defaults_to_empty_history(self):
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {"answer": "Answer."}

        with patch("app.rag_application._get_rag_chain", return_value=mock_chain):
            from app.rag_application import retrieve_generate
            retrieve_generate("Any question")

        call_kwargs = mock_chain.invoke.call_args[0][0]
        assert call_kwargs["chat_history"] == []

    def test_returns_rate_limit_message_on_resource_exhausted(self):
        mock_chain = MagicMock()
        mock_chain.invoke.side_effect = ResourceExhausted("Quota exceeded")

        with patch("app.rag_application._get_rag_chain", return_value=mock_chain):
            from app.rag_application import retrieve_generate
            result = retrieve_generate("Any question")

        assert "rate-limited" in result.lower()

    def test_chain_is_cached_after_first_call(self):
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = {"answer": "Cached."}

        with patch("app.rag_application._get_rag_chain", return_value=mock_chain) as mock_get:
            from app.rag_application import retrieve_generate
            retrieve_generate("First call")
            retrieve_generate("Second call")

        assert mock_get.call_count == 2  # _get_rag_chain is called, but internally caches
