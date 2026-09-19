import tempfile
import unittest

from LibraryManagement.utils.project_path import ensure_project_root_on_path

ensure_project_root_on_path()

from LibraryManagement.models.book import Book
from LibraryManagement.repositories.book_repo import BookRepository
from LibraryManagement.repositories.borrower_repo import BorrowerRepository
from LibraryManagement.repositories.queue_repo import QueueRepository
from LibraryManagement.repositories.reader_repo import ReaderRepository
from LibraryManagement.repositories.return_history_repo import ReturnHistoryRepository
from LibraryManagement.services.library_service import LibraryService


class TestBookTextValidation(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        self.book_repo = BookRepository()
        self.book_repo.FILE_PATH = self.temp_path / "books.json"
        self.book_repo.save_books([
            Book("B001", "Python Basics", "Alice", 2024, 3),
        ])

        self.borrower_repo = BorrowerRepository()
        self.borrower_repo.FILE_PATH = self.temp_path / "borrowers_list.json"
        self.queue_repo = QueueRepository()
        self.queue_repo.FILE_PATH = self.temp_path / "borrow_queue.json"
        self.reader_repo = ReaderRepository()
        self.reader_repo.FILE_PATH = self.temp_path / "readers.json"
        self.return_history_repo = ReturnHistoryRepository()
        self.return_history_repo.FILE_PATH = self.temp_path / "return_history.json"

        self.service = LibraryService()
        self.service.repository = self.book_repo
        self.service.borrower_repo = self.borrower_repo
        self.service.queue_repo = self.queue_repo
        self.service.reader_repo = self.reader_repo
        self.service.return_history_repo = self.return_history_repo

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_book_rejects_invalid_title_and_author(self):
        invalid_books = [
            Book("B002", "", "Author", 2024, 5),
            Book("B003", "   ", "Author", 2024, 5),
            Book("B004", 123, "Author", 2024, 5),
            Book("B005", "Valid", "", 2024, 5),
            Book("B006", "Valid", "   ", 2024, 5),
            Book("B007", "Valid", 123, 2024, 5),
        ]

        for book in invalid_books:
            self.assertFalse(self.service.add_book(book))

        self.assertEqual([book.book_id for book in self.book_repo.load_books()], ["B001"])

    def test_update_book_rejects_invalid_title_and_author(self):
        invalid_books = [
            Book("B001", "", "Author", 2024, 3),
            Book("B001", "Valid", "", 2024, 3),
            Book("B001", 123, "Author", 2024, 3),
            Book("B001", "Valid", 123, 2024, 3),
        ]

        for book in invalid_books:
            self.assertFalse(self.service.update_book(book))

        saved_book = self.book_repo.load_books()[0]
        self.assertEqual(saved_book.title, "Python Basics")
        self.assertEqual(saved_book.author, "Alice")

    def test_from_dict_rejects_invalid_optional_text_fields(self):
        base_data = {
            "book_id": "B002",
            "title": "Python",
            "author": "Alice",
            "publish_year": 2024,
            "quantity": 2,
        }

        invalid_category = dict(base_data, category=123)
        invalid_isbn = dict(base_data, isbn=123)

        with self.assertRaises(ValueError):
            Book.from_dict(invalid_category)

        with self.assertRaises(ValueError):
            Book.from_dict(invalid_isbn)

    def test_normalize_text_rejects_non_string_values(self):
        self.assertEqual(self.service._normalize_text(123), "")
        self.assertEqual(self.service._normalize_text(True), "")
        self.assertEqual(self.service._normalize_text(None), "")
        self.assertEqual(self.service._normalize_text("  B001  "), "B001")


if __name__ == "__main__":
    unittest.main()
