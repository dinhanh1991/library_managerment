from pathlib import Path

from LibraryManagement.models.borrower import Borrower
from LibraryManagement.repositories.base_repository import JsonRepository


class BorrowerRepository(JsonRepository):
    FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "borrowers_list.json"
    ENTITY_NAME = "người mượn"

    def load_borrowers(self):
        return self._load_json_list(
            factory=lambda item: Borrower.from_dict(item, default_status="borrowed")
        )

    def save_borrowers(self, borrowers):
        self._save_json_list(borrowers)
