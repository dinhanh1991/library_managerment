import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.models.book import Book
from LibraryManagement.repositories.book_repo import BookRepository
from LibraryManagement.repositories.borrower_repo import BorrowerRepository
from LibraryManagement.repositories.queue_repo import QueueRepository
from LibraryManagement.repositories.reader_repo import ReaderRepository
from LibraryManagement.repositories.return_history_repo import ReturnHistoryRepository
from LibraryManagement.services.library_service import LibraryService


class TestBookNumericValidation(unittest.TestCase):
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

    def test_add_book_rejects_invalid_numeric_values_without_exception(self):
        invalid_books = [
            Book("B002", "Invalid", "Author", 2024, None),
            Book("B003", "Invalid", "Author", 2024, "5"),
            Book("B004", "Invalid", "Author", None, 5),
            Book("B005", "Invalid", "Author", "2024", 5),
            Book("B006", "Invalid", "Author", True, 5),
            Book("B007", "Invalid", "Author", 2024, False),
        ]

        for book in invalid_books:
            self.assertFalse(self.service.add_book(book))

        self.assertEqual([book.book_id for book in self.book_repo.load_books()], ["B001"])

    def test_update_book_rejects_invalid_numeric_values_without_changing_data(self):
        invalid_books = [
            Book("B001", "Changed", "Author", 2024, None),
            Book("B001", "Changed", "Author", 2024, "5"),
            Book("B001", "Changed", "Author", None, 5),
            Book("B001", "Changed", "Author", "2024", 5),
            Book("B001", "Changed", "Author", True, 5),
            Book("B001", "Changed", "Author", 2024, False),
        ]

        for book in invalid_books:
            self.assertFalse(self.service.update_book(book))

        saved_book = self.book_repo.load_books()[0]
        self.assertEqual(saved_book.title, "Python Basics")
        self.assertEqual(saved_book.publish_year, 2024)
        self.assertEqual(saved_book.quantity, 3)


if __name__ == "__main__":
    unittest.main()
