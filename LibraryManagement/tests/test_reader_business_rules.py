import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.models.book import Book
from LibraryManagement.models.borrower import Borrower
from LibraryManagement.models.reader import Reader
from LibraryManagement.repositories.book_repo import BookRepository
from LibraryManagement.repositories.borrower_repo import BorrowerRepository
from LibraryManagement.repositories.queue_repo import QueueRepository
from LibraryManagement.repositories.reader_repo import ReaderRepository
from LibraryManagement.repositories.return_history_repo import ReturnHistoryRepository
from LibraryManagement.services.library_service import LibraryService


class ReaderBusinessRulesTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        self.book_repo = BookRepository()
        self.book_repo.FILE_PATH = self.temp_path / "books.json"
        self.borrower_repo = BorrowerRepository()
        self.borrower_repo.FILE_PATH = self.temp_path / "borrowers_list.json"
        self.queue_repo = QueueRepository()
        self.queue_repo.FILE_PATH = self.temp_path / "borrow_queue.json"
        self.reader_repo = ReaderRepository()
        self.reader_repo.FILE_PATH = self.temp_path / "readers.json"
        self.return_history_repo = ReturnHistoryRepository()
        self.return_history_repo.FILE_PATH = self.temp_path / "return_history.json"

        self.book_repo.save_books([
            Book("B001", "Python Basics", "Alice", 2024, 3),
            Book("B002", "Data Structures", "Bob", 2023, 2),
        ])

        self.service = LibraryService()
        self.service.repository = self.book_repo
        self.service.borrower_repo = self.borrower_repo
        self.service.queue_repo = self.queue_repo
        self.service.reader_repo = self.reader_repo
        self.service.return_history_repo = self.return_history_repo
        self.service.borrow_queue.items = []

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_borrow_creates_reader_automatically(self):
        borrower = Borrower("R001", "Reader One", "B001")

        self.assertTrue(self.service.book_borrow(borrower))

        readers = self.reader_repo.load_readers()
        self.assertEqual(len(readers), 1)
        self.assertEqual(readers[0].reader_id, "R001")
        self.assertEqual(readers[0].name, "Reader One")

    def test_borrow_does_not_create_duplicate_reader(self):
        self.reader_repo.save_readers([Reader("R001", "Reader One")])

        borrower = Borrower("R001", "Reader One", "B001")
        self.assertTrue(self.service.book_borrow(borrower))

        readers = self.reader_repo.load_readers()
        self.assertEqual(len(readers), 1)
        self.assertEqual(readers[0].reader_id, "R001")

    def test_reader_can_borrow_again_after_return(self):
        first = Borrower("R001", "Reader One", "B001")

        self.assertTrue(self.service.book_borrow(first))
        self.assertTrue(self.service.return_book(first))

        second = Borrower("R001", "Reader One", "B002")
        self.assertTrue(self.service.book_borrow(second))

        readers = self.reader_repo.load_readers()
        self.assertEqual(len(readers), 1)
        self.assertEqual(readers[0].reader_id, "R001")
        self.assertEqual(self.borrower_repo.load_borrowers()[0].book_id, "B002")

    def test_reader_history_contains_active_and_returned_transactions(self):
        first = Borrower("R001", "Reader One", "B001")
        second = Borrower("R001", "Reader One", "B002")

        self.assertTrue(self.service.book_borrow(first))
        self.assertTrue(self.service.return_book(first))
        self.assertTrue(self.service.book_borrow(second))

        history = self.service.get_reader_history("R001")

        self.assertEqual(len(history), 2)
        self.assertEqual({item.book_id for item in history}, {"B001", "B002"})
        returned = next(item for item in history if item.book_id == "B001")
        active = next(item for item in history if item.book_id == "B002")
        self.assertEqual(returned.status, "returned")
        self.assertEqual(active.status, "pending")

    def test_remove_reader_is_blocked_while_transaction_is_active(self):
        borrower = Borrower("R001", "Reader One", "B001")
        self.assertTrue(self.service.book_borrow(borrower))

        self.assertFalse(self.service.remove_reader("R001"))
        self.assertEqual(len(self.reader_repo.load_readers()), 1)

        self.assertTrue(self.service.return_book(borrower))
        self.assertTrue(self.service.remove_reader("R001"))
        self.assertEqual(self.reader_repo.load_readers(), [])


if __name__ == "__main__":
    unittest.main()
