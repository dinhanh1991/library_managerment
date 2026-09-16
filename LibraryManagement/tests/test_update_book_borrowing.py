import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.models.book import Book
from LibraryManagement.models.borrower import Borrower
from LibraryManagement.repositories.book_repo import BookRepository
from LibraryManagement.repositories.borrower_repo import BorrowerRepository
from LibraryManagement.services.library_service import LibraryService


class TestUpdateBookBorrowing(unittest.TestCase):
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

        self.service = LibraryService()
        self.service.repository = self.book_repo
        self.service.borrower_repo = self.borrower_repo
        self.service._refresh_structures = lambda: None

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_update_book_is_blocked_when_book_has_active_transaction(self):
        borrower = Borrower("C001", "Charlie", "B001", status="borrowed")
        self.borrower_repo.save_borrowers([borrower])

        updated = Book("B001", "Python Advanced", "Bob", 2026, 10)

        self.assertFalse(self.service.update_book(updated))

        books = self.book_repo.load_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].book_id, "B001")
        self.assertEqual(books[0].title, "Python Basics")
        self.assertEqual(books[0].author, "Alice")
        self.assertEqual(books[0].publish_year, 2024)
        self.assertEqual(books[0].quantity, 3)


if __name__ == "__main__":
    unittest.main()
