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
        except json.JSONDecodeError as e:
            raise ValueError(f"File hàng đợi mượn sách không hợp lệ: {e}") from e

        if not isinstance(data, list):
            raise ValueError("Dữ liệu hàng đợi phải có dạng danh sách JSON.")

        queue = []
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Mỗi dữ liệu hàng đợi phải có dạng object JSON.")
            queue.append(Borrower.from_dict(item, default_status="pending"))

        return queue

    def save_queue(self, borrowers):
        self.FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = [borrower.to_dict() for borrower in borrowers]
        with self.FILE_PATH.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)