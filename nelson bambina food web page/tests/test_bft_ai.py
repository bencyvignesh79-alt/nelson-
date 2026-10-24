import os
import unittest
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from bft_ai import api
from bft_ai.gemini_service import (
    GeminiNotConfiguredError,
    GeminiRequestError,
    generate_reply,
)


class GeminiServiceTests(unittest.TestCase):
    @patch.dict(os.environ, {"GEMINI_API_KEY": ""})
    def test_requires_server_side_api_key(self):
        with self.assertRaises(GeminiNotConfiguredError):
            generate_reply("What does BFT do?")

    @patch("bft_ai.gemini_service.genai.Client")
    @patch.dict(os.environ, {"GEMINI_API_KEY": "test-key", "GEMINI_MODEL": "test-model"})
    def test_uses_configured_model_and_returns_text(self, client_factory):
        client = Mock()
        client.models.generate_content.return_value.text = "BFT offers engineering support."
        client_factory.return_value = client

        answer = generate_reply("What does BFT do?")

        self.assertEqual(answer, "BFT offers engineering support.")
        client_factory.assert_called_once()
        self.assertEqual(
            client.models.generate_content.call_args.kwargs["model"],
            "test-model",
        )

    @patch("bft_ai.gemini_service.genai.Client")
    @patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"})
    def test_sanitizes_gemini_api_errors(self, client_factory):
        from google.genai import errors

        client = Mock()
        client.models.generate_content.side_effect = errors.ClientError(
            403, {"message": "denied"}
        )
        client_factory.return_value = client

        with self.assertRaises(GeminiRequestError):
            generate_reply("What does BFT do?")


class ChatApiTests(unittest.TestCase):
    def setUp(self):
        api._client_requests.clear()
        self.client = TestClient(api.app)

    @patch("bft_ai.api.generate_reply", return_value="BFT offers engineering support.")
    def test_chat_returns_reply_without_exposing_credentials(self, generate_reply_mock):
        response = self.client.post(
            "/api/v1/ai/chat",
            json={"message": "  What does BFT do?  "},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"answer": "BFT offers engineering support."})
        generate_reply_mock.assert_called_once_with("What does BFT do?")

    def test_rejects_blank_and_oversized_questions(self):
        blank = self.client.post("/api/v1/ai/chat", json={"message": "   "})
        oversized = self.client.post("/api/v1/ai/chat", json={"message": "x" * 1201})

        self.assertEqual(blank.status_code, 422)
        self.assertEqual(oversized.status_code, 422)

    def test_enforces_per_client_rate_limit(self):
        with patch.object(api, "RATE_LIMIT_REQUESTS", 1):
            first = self.client.post("/api/v1/ai/chat", json={"message": "first"})
            second = self.client.post("/api/v1/ai/chat", json={"message": "second"})

        self.assertEqual(first.status_code, 503)
        self.assertEqual(second.status_code, 429)


if __name__ == "__main__":
    unittest.main()
