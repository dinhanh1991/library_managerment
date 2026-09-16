import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.data_structures.bts import BinarySearchTree
from LibraryManagement.data_structures.linked_list import BookLinkedList
from LibraryManagement.data_structures.queue import Queue
from LibraryManagement.data_structures.stack import Stack
from LibraryManagement.models.book import Book
from LibraryManagement.repositories.book_repo import BookRepository
from LibraryManagement.repositories.borrower_repo import BorrowerRepository
from LibraryManagement.repositories.queue_repo import QueueRepository
from LibraryManagement.repositories.reader_repo import ReaderRepository
from LibraryManagement.repositories.return_history_repo import ReturnHistoryRepository
from LibraryManagement.services.library_service import LibraryService


class BookIntegerValidationTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        self.book_repo = BookRepository()
        self.book_repo.FILE_PATH = self.temp_path / "books.json"
        self.book_repo.save_books([Book("B001", "Python Basics", "Alice", 2024, 3)])

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
        self.service.book_linked_list = BookLinkedList()
        self.service.book_bst = BinarySearchTree()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_book_rejects_float_quantity_and_publish_year(self):
        self.assertFalse(
            self.service.add_book(Book("B002", "Float Quantity", "Bob", 2024, 1.5))
        )
        self.assertFalse(
            self.service.add_book(Book("B003", "Float Year", "Bob", 2024.5, 1))
        )
        self.assertEqual([book.book_id for book in self.service.get_all_books()], ["B001"])

    def test_update_book_rejects_float_quantity_and_publish_year(self):
        self.assertFalse(
            self.service.update_book(Book("B001", "Python Basics", "Alice", 2024, 1.5))
        )
        self.assertFalse(
            self.service.update_book(Book("B001", "Python Basics", "Alice", 2024.5, 3))
        )

        book = self.service.get_all_books()[0]
        self.assertEqual(book.publish_year, 2024)
        self.assertEqual(book.quantity, 3)

    def test_integer_validation_rejects_bool(self):
        self.assertFalse(
            self.service.add_book(Book("B002", "Boolean Quantity", "Bob", 2024, True))
        )
        self.assertFalse(
            self.service.add_book(Book("B003", "Boolean Year", "Bob", True, 1))
        )


if __name__ == "__main__":
    unittest.main()
