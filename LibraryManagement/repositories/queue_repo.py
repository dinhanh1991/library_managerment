from pathlib import Path

from LibraryManagement.models.borrower import Borrower
from LibraryManagement.repositories.base_repository import JsonRepository


class QueueRepository(JsonRepository):
    FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "borrow_queue.json"
    ENTITY_NAME = "hàng đợi mượn sách"

    def load_queue(self):
        return self._load_json_list(
            factory=lambda item: Borrower.from_dict(item, default_status="pending")
        )

    def save_queue(self, borrowers):
        self._save_json_list(borrowers)