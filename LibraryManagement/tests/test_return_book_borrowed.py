import sys
import tempfile
import unittest
from datetime import date
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
from LibraryManagement.repositories.return_history_repo import ReturnHistoryRepository
from LibraryManagement.services.library_service import LibraryService


class TestReturnBookBorrowed(unittest.TestCase):
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

        self.return_history_repo = ReturnHistoryRepository()
        self.return_history_repo.FILE_PATH = self.temp_path / "return_history.json"

        self.service = LibraryService()
        self.service.repository = self.book_repo
        self.service.borrower_repo = self.borrower_repo
        self.service.queue_repo = self.queue_repo
        self.service.return_history_repo = self.return_history_repo
        self.service.borrow_queue = Queue()
        self.service.return_stack = Stack()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_return_borrowed_book_updates_all_related_structures(self):
        borrower = Borrower("C001", "Charlie", "B001")

        self.assertTrue(self.service.book_borrow(borrower))
        processed = self.service.process_next_borrower()
        self.assertIsNotNone(processed)
        self.assertEqual(processed.status, "borrowed")

        self.assertTrue(self.service.return_book(Borrower("C001", "Wrong Name", "B001")))

        book = self.book_repo.load_books()[0]
        self.assertEqual(book.quantity, 3)
        self.assertEqual(self.borrower_repo.load_borrowers(), [])
        self.assertEqual(self.service.borrow_queue.items, [])
        self.assertEqual(self.queue_repo.load_queue(), [])

        history = self.return_history_repo.load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].borrower_id, "C001")
        self.assertEqual(history[0].name, "Charlie")
        self.assertEqual(history[0].status, "returned")
        self.assertEqual(history[0].return_date, date.today().isoformat())

        self.assertEqual(len(self.service.return_stack.items), 1)
        returned = self.service.return_stack.items[0]
        self.assertEqual(returned.borrower_id, "C001")
        self.assertEqual(returned.book_id, "B001")
        self.assertEqual(returned.status, "returned")
        self.assertEqual(returned.return_date, date.today().isoformat())

    def test_return_rolls_back_when_borrower_save_fails(self):
        borrower = Borrower("C001", "Charlie", "B001")
        self.assertTrue(self.service.book_borrow(borrower))
        self.assertIsNotNone(self.service.process_next_borrower())

        original_save = self.borrower_repo.save_borrowers
        calls = 0

        def fail_once(data):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise OSError("simulated borrower save failure")
            return original_save(data)

        with patch.object(self.borrower_repo, "save_borrowers", side_effect=fail_once):
            with self.assertRaises(OSError):
                self.service.return_book(Borrower("C001", "Wrong Name", "B001"))

        book = self.book_repo.load_books()[0]
        self.assertEqual(book.quantity, 2)
        active = self.borrower_repo.load_borrowers()
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].status, "borrowed")
        self.assertEqual(self.return_history_repo.load_history(), [])
        self.assertEqual(len(self.service.borrow_queue.items), 0)
        self.assertEqual(self.queue_repo.load_queue(), [])
        self.assertEqual(self.service.return_stack.items, [])


if __name__ == "__main__":
    unittest.main()
