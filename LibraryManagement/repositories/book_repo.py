from pathlib import Path

from LibraryManagement.models.book import Book
from LibraryManagement.repositories.base_repository import JsonRepository


class BookRepository(JsonRepository):
    FILE_PATH = Path(__file__).resolve().parents[1] / "data" / "books.json"
    ENTITY_NAME = "sách"

    def load_books(self):
        return self._load_json_list(factory=Book.from_dict)

    def save_books(self, books):
        self._save_json_list(books)
