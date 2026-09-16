import json
from pathlib import Path

from LibraryManagement.models.reader import Reader


class ReaderRepository:
    FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "readers.json"

    def load_readers(self):
        try:
            with self.FILE_PATH.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            raise ValueError(f"File dữ liệu người đọc không hợp lệ: {e}") from e

        if not isinstance(data, list):
            raise ValueError("Dữ liệu người đọc phải có dạng danh sách JSON.")

        readers = []
        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Mỗi dữ liệu người đọc phải có dạng object JSON.")
            readers.append(Reader.from_dict(item))

        return readers

    def save_readers(self, readers):
        self.FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        data = [reader.to_dict() for reader in readers]
        with self.FILE_PATH.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
