import json
from pathlib import Path

from LibraryManagement.models.borrower import Borrower


class QueueRepository:
    FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "borrow_queue.json"

    def load_queue(self):
        try:
            with self.FILE_PATH.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []

        return [
            Borrower.from_dict(item, default_status="pending")
            for item in data
        ]

    def save_queue(self, borrowers):
        self.FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = [borrower.to_dict() for borrower in borrowers]
        with self.FILE_PATH.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)