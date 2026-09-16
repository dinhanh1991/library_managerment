import sys
import tempfile
import unittest
from pathlib import Path

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


class TestBorrowBusinessRules(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        self.book_repo = BookRepository()
        self.book_repo.FILE_PATH = self.temp_path / "books.json"
        self.book_repo.save_books([
            Book("B001", "Python Basics", "Alice", 2024, 2),
            Book("B002", "Data Structures", "Bob", 2023, 0),
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

    def test_borrow_rejects_invalid_input_without_changing_data(self):
        invalid_inputs = [
            None,
            Borrower("", "Charlie", "B001"),
            Borrower("C001", "", "B001"),
            Borrower("C001", "Charlie", ""),
        ]

        for borrower in invalid_inputs:
            self.assertFalse(self.service.book_borrow(borrower))

        self.assertEqual(self.book_repo.load_books()[0].quantity, 2)
        self.assertEqual(self.borrower_repo.load_borrowers(), [])
        self.assertEqual(self.service.borrow_queue.items, [])
        self.assertEqual(self.reader_repo.load_readers(), [])

    def test_borrow_rejects_unavailable_book_without_changing_data(self):
        borrower = Borrower("C001", "Charlie", "B002")

        self.assertFalse(self.service.book_borrow(borrower))
        self.assertEqual(self.book_repo.load_books()[1].quantity, 0)
        self.assertEqual(self.borrower_repo.load_borrowers(), [])
        self.assertEqual(self.service.borrow_queue.items, [])
        self.assertEqual(self.reader_repo.load_readers(), [])

    def test_pending_borrow_reserves_one_copy_until_return(self):
        borrower = Borrower("  C001  ", "  Charlie  ", " B001 ")

        self.assertTrue(self.service.book_borrow(borrower))

        book = self.book_repo.load_books()[0]
        saved_borrower = self.borrower_repo.load_borrowers()[0]
        saved_queue = self.queue_repo.load_queue()[0]

        self.assertEqual(book.quantity, 1)
        self.assertEqual(saved_borrower.borrower_id, "C001")
        self.assertEqual(saved_borrower.name, "Charlie")
        self.assertEqual(saved_borrower.book_id, "B001")
        self.assertEqual(saved_borrower.status, "pending")
        self.assertEqual(saved_queue.status, "pending")
        self.assertEqual(len(self.reader_repo.load_readers()), 1)

    def test_borrow_does_not_allow_same_reader_to_borrow_another_book(self):
        first = Borrower("C001", "Charlie", "B001")
        second = Borrower("C001", "Charlie", "B002")

        self.assertTrue(self.service.book_borrow(first))
        self.assertFalse(self.service.book_borrow(second))
        self.assertEqual(self.book_repo.load_books()[0].quantity, 1)
        self.assertEqual(self.book_repo.load_books()[1].quantity, 0)
        self.assertEqual(len(self.borrower_repo.load_borrowers()), 1)
        self.assertEqual(len(self.service.borrow_queue.items), 1)


if __name__ == "__main__":
    unittest.main()
