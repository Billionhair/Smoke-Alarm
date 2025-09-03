import unittest
from unittest.mock import patch, MagicMock

from agent.gmail_client import GmailClient

class TestGmailClient(unittest.TestCase):
    @patch("agent.gmail_client.get_credentials")
    @patch("agent.gmail_client.build")
    def test_send_calls_gmail_api(self, mock_build, _mock_creds):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        client = GmailClient()
        client.send("to@example.com", "Hi", "Body")
        mock_service.users.return_value.messages.return_value.send.assert_called()

if __name__ == "__main__":
    unittest.main()
