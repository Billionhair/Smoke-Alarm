import unittest
from unittest.mock import patch

from agent.repository import SheetRepository

class TestRepository(unittest.TestCase):
    @patch("agent.repository.SheetDB")
    def test_sheet_repo_delegates(self, mock_db):
        inst = mock_db.return_value
        repo = SheetRepository()
        repo.list_properties()
        inst.list_properties.assert_called_once()

if __name__ == "__main__":
    unittest.main()
