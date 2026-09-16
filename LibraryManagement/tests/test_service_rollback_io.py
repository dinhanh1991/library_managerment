import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.data_structures.queue import Queue
from LibraryManagement.data_structures.stack import Stack
from LibraryManagement.models.book import Book
from LibraryManagement.models.borrower import Borrower
from LibraryManagement.repositories.book_repo import BookRepository
from LibraryManagement.repositories.borrower_repo import BorrowerRepository
from LibraryManagement.repositories.queue_repo import QueueRepository
from LibraryManagement.repositories.reader_repo import ReaderRepository
from LibraryManagement.repositories.return_history_repo import ReturnHistoryRepository
from LibraryManagement.services.library_service import LibraryService


class ServiceRollbackIOTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        self.book_repo = BookRepository()
        self.book_repo.FILE_PATH = self.temp_path / "books.json"
        self.book_repo.save_books([
            Book("B001", "Python Basics", "Alice", 2024, 2),
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
        self.service.borrow_queue = Queue()
        self.service.return_stack = Stack()
        self.service._refresh_structures = lambda: None

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_borrow_rolls_back_when_book_save_fails(self):
        borrower = Borrower("C001", "Charlie", "B001")
        original_save = self.book_repo.save_books
        calls = 0

        def fail_once(data):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise OSError("book save failure")
            return original_save(data)

        with patch.object(self.book_repo, "save_books", side_effect=fail_once):
            with self.assertRaises(OSError):
                self.service.book_borrow(borrower)

        self.assertEqual(self.book_repo.load_books()[0].quantity, 2)
        self.assertEqual(self.borrower_repo.load_borrowers(), [])
        self.assertEqual(self.queue_repo.load_queue(), [])
        self.assertEqual(self.reader_repo.load_readers(), [])
        self.assertEqual(self.service.borrow_queue.items, [])

    def test_borrow_rolls_back_when_queue_save_fails(self):
        borrower = Borrower("C001", "Charlie", "B001")
        original_save = self.queue_repo.save_queue
        calls = 0

        def fail_once(data):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise OSError("queue save failure")
            return original_save(data)

        with patch.object(self.queue_repo, "save_queue", side_effect=fail_once):
            with self.assertRaises(OSError):
                self.service.book_borrow(borrower)

        self.assertEqual(self.book_repo.load_books()[0].quantity, 2)
        self.assertEqual(self.borrower_repo.load_borrowers(), [])
        self.assertEqual(self.queue_repo.load_queue(), [])
        self.assertEqual(self.reader_repo.load_readers(), [])
        self.assertEqual(self.service.borrow_queue.items, [])

    def test_return_rolls_back_when_history_save_fails(self):
        borrower = Borrower("C001", "Charlie", "B001")
        self.assertTrue(self.service.book_borrow(borrower))
        original_save = self.return_history_repo.save_history
        calls = 0

        def fail_once(data):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise OSError("history save failure")
            return original_save(data)

        with patch.object(self.return_history_repo, "save_history", side_effect=fail_once):
            with self.assertRaises(OSError):
                self.service.return_book(borrower)

        self.assertEqual(self.book_repo.load_books()[0].quantity, 1)
        active = self.borrower_repo.load_borrowers()
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].status, "pending")
        self.assertEqual(self.return_history_repo.load_history(), [])
        self.assertEqual(self.queue_repo.load_queue()[0].borrower_id, "C001")
        self.assertTrue(self.service.return_stack.is_empty())

    def test_return_rolls_back_when_queue_save_fails(self):
        borrower = Borrower("C001", "Charlie", "B001")
        self.assertTrue(self.service.book_borrow(borrower))
        original_save = self.queue_repo.save_queue
        calls = 0

        def fail_once(data):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise OSError("queue save failure")
            return original_save(data)

        with patch.object(self.queue_repo, "save_queue", side_effect=fail_once):
            with self.assertRaises(OSError):
                self.service.return_book(borrower)

        self.assertEqual(self.book_repo.load_books()[0].quantity, 1)
        active = self.borrower_repo.load_borrowers()
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].status, "pending")
        self.assertEqual(self.return_history_repo.load_history(), [])
        self.assertEqual(self.queue_repo.load_queue()[0].borrower_id, "C001")
        self.assertEqual(len(self.service.borrow_queue.items), 1)
        self.assertTrue(self.service.return_stack.is_empty())


if __name__ == "__main__":
    unittest.main()
