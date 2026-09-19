from pathlib import Path

from LibraryManagement.models.borrower import Borrower
from LibraryManagement.repositories.base_repository import JsonRepository


class ReturnHistoryRepository(JsonRepository):
    FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "return_history.json"
    ENTITY_NAME = "lịch sử trả sách"

    def load_history(self):
        return self._load_json_list(
            factory=lambda item: Borrower.from_dict(item, default_status="returned")
        )

    def save_history(self, borrowers):
        self._save_json_list(borrowers)
