from pathlib import Path

from LibraryManagement.models.reader import Reader
from LibraryManagement.repositories.base_repository import JsonRepository


class ReaderRepository(JsonRepository):
    FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "readers.json"
    ENTITY_NAME = "người đọc"

    def load_readers(self):
        return self._load_json_list(factory=Reader.from_dict)

    def save_readers(self, readers):
        self._save_json_list(readers)
