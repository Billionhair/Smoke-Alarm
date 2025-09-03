import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from agent.scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    @patch("agent.scheduler.get_credentials")
    @patch("agent.scheduler.build")
    def test_schedule_calls_calendar(self, mock_build, _mock_creds):
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        s = Scheduler()
        s.schedule_inspection("Test", datetime.utcnow())
        mock_service.events.return_value.insert.return_value.execute.assert_called()

if __name__ == "__main__":
    unittest.main()
