import unittest
from unittest.mock import Mock

from LibraryManagement.services.return_service import ReturnService


class ReturnServiceTest(unittest.TestCase):
    def test_get_return_history_delegates_to_repository(self):
        history = [Mock()]
        return_history_repo = Mock()
        return_history_repo.load_history.return_value = history

        service = ReturnService(
            repository=Mock(),
            borrower_repo=Mock(),
            queue_repo=Mock(),
            return_history_repo=return_history_repo,
            borrow_queue=Mock(),
            return_stack=Mock(),
            normalize_text=Mock(),
            refresh_structures=Mock(),
            rollback=Mock(),
        )

        result = service.get_return_history()

        self.assertIs(result, history)
        return_history_repo.load_history.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
