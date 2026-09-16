import sys
import tempfile
import unittest
from datetime import date, timedelta
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
from LibraryManagement.views.library_view import LibraryView


class LibraryServiceTestCase(unittest.TestCase):
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

        books = [
            Book("B001", "Python Basics", "Alice", 2024, 3),
            Book("B002", "Data Structures", "Bob", 2023, 2),
        ]
        self.book_repo.save_books(books)

        self.service = LibraryService()
        self.service.repository = self.book_repo
        self.service.borrower_repo = self.borrower_repo
        self.service.queue_repo = self.queue_repo
        self.service.reader_repo = self.reader_repo
        self.service.return_history_repo = self.return_history_repo
        self.service.borrow_queue = __import__("LibraryManagement.data_structures.queue", fromlist=["Queue"]).Queue()
        self.service.return_stack = __import__("LibraryManagement.data_structures.stack", fromlist=["Stack"]).Stack()
        self.service.book_linked_list = __import__("LibraryManagement.data_structures.linked_list", fromlist=["BookLinkedList"]).BookLinkedList()
        self.service.book_bst = __import__("LibraryManagement.data_structures.bts", fromlist=["BinarySearchTree"]).BinarySearchTree()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_all_books_returns_data_from_repo(self):
        books = self.service.get_all_books()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0].book_id, "B001")

    def test_search_books_advanced_filters_by_fields_and_availability(self):
        books = [
            Book("B001", "Python Basics", "Alice", 2024, 0, "Khoa học máy tính", "978-1-2345-6789-0"),
            Book("B002", "Data Structures", "Bob", 2023, 2, "Cấu trúc dữ liệu", "978-1-2345-6789-1"),
            Book("B003", "Python for Beginners", "Alice", 2024, 3, "Khoa học máy tính", "978-1-2345-6789-2"),
        ]
        self.book_repo.save_books(books)

        results = self.service.search_books_advanced(
            title="python",
            author="alice",
            genre="khoa học",
            publish_year=2024,
            isbn="978-1-2345-6789-2",
            availability="available",
        )
        self.assertEqual([book.book_id for book in results], ["B003"])

        unavailable = self.service.search_books_advanced(
            title="python",
            author="alice",
            availability="unavailable",
        )
        self.assertEqual([book.book_id for book in unavailable], ["B001"])

    def test_borrow_and_return_updates_quantity(self):
        borrower = Borrower("C001", "Charlie", "B001")

        result = self.service.book_borrow(borrower)
        self.assertTrue(result)
        self.assertEqual(self.service.get_all_books()[0].quantity, 2)
        self.assertEqual(len(self.service.borrow_queue.items), 1)
        self.assertEqual(borrower.borrow_date, date.today().isoformat())
        self.assertEqual(
            borrower.due_date,
            (date.today() + timedelta(days=14)).isoformat(),
        )
        self.assertEqual(borrower.status, "pending")

        return_result = self.service.return_book(borrower)
        self.assertTrue(return_result)
        self.assertEqual(self.service.get_all_books()[0].quantity, 3)
        self.assertEqual(len(self.service.return_stack.items), 1)

    def test_return_rejects_non_active_loan(self):
        borrower = Borrower("C001", "Charlie", "B001")

        self.assertFalse(self.service.return_book(borrower))
        self.assertEqual(self.service.get_all_books()[0].quantity, 3)
        self.assertEqual(self.borrower_repo.load_borrowers(), [])
        self.assertTrue(self.service.return_stack.is_empty())

    def test_return_rejects_empty_input_without_changing_data(self):
        self.assertFalse(self.service.return_book(None))
        self.assertFalse(self.service.return_book(Borrower("", "Charlie", "B001")))
        self.assertFalse(self.service.return_book(Borrower("C001", "Charlie", "")))
        self.assertEqual(self.service.get_all_books()[0].quantity, 3)
        self.assertEqual(self.borrower_repo.load_borrowers(), [])
        self.assertTrue(self.service.return_stack.is_empty())

    def test_return_uses_stored_borrower_data_not_return_input_name(self):
        borrower = Borrower("C001", "Stored Name", "B001")
        self.assertTrue(self.service.book_borrow(borrower))

        returned = Borrower("  C001  ", "Wrong Input Name", " B001 ")
        self.assertTrue(self.service.return_book(returned))

        history = self.return_history_repo.load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].borrower_id, "C001")
        self.assertEqual(history[0].name, "Stored Name")
        self.assertEqual(history[0].book_id, "B001")
        self.assertEqual(history[0].status, "returned")

    def test_return_cannot_be_done_twice(self):
        borrower = Borrower("C001", "Charlie", "B001")
        self.assertTrue(self.service.book_borrow(borrower))
        self.assertTrue(self.service.return_book(borrower))

        self.assertFalse(self.service.return_book(borrower))
        self.assertEqual(self.service.get_all_books()[0].quantity, 3)
        self.assertEqual(len(self.return_history_repo.load_history()), 1)
        self.assertEqual(self.borrower_repo.load_borrowers(), [])

    def test_return_rejects_missing_book_without_finishing_transaction(self):
        borrower = Borrower("C001", "Charlie", "B001")
        self.assertTrue(self.service.book_borrow(borrower))

        self.book_repo.save_books([Book("B002", "Data Structures", "Bob", 2023, 2)])
        self.assertFalse(self.service.return_book(borrower))

        active = self.borrower_repo.load_borrowers()
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0].status, "pending")
        self.assertEqual(len(self.return_history_repo.load_history()), 0)
        self.assertEqual(self.service.get_all_books()[0].book_id, "B002")

    def test_return_removes_only_matching_transaction_from_queue(self):
        first = Borrower("C001", "Charlie", "B001")
        second = Borrower("C002", "Diana", "B002")
        self.assertTrue(self.service.book_borrow(first))
        self.assertTrue(self.service.book_borrow(second))

        self.assertTrue(self.service.return_book(first))
        self.assertEqual(
            [(item.borrower_id, item.book_id) for item in self.service.borrow_queue.items],
            [("C002", "B002")],
        )

    def test_return_removes_queue_entry_and_persists_history(self):
        borrower = Borrower("C001", "Stored Name", "B001")
        self.assertTrue(self.service.book_borrow(borrower))

        returned = Borrower("C001", "Wrong Input Name", "B001")
        self.assertTrue(self.service.return_book(returned))

        self.assertEqual(self.service.borrow_queue.items, [])
        self.assertEqual(self.borrower_repo.load_borrowers(), [])
        history = self.return_history_repo.load_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].name, "Stored Name")
        self.assertEqual(history[0].status, "returned")
        self.assertEqual(history[0].return_date, date.today().isoformat())

    def test_borrow_queue_is_fifo_and_persisted(self):
        first = Borrower("C001", "Charlie", "B001")
        second = Borrower("C002", "Diana", "B002")

        self.assertTrue(self.service.book_borrow(first))
        self.assertTrue(self.service.book_borrow(second))

        saved_queue = self.queue_repo.load_queue()
        self.assertEqual(
            [item.borrower_id for item in saved_queue],
            ["C001", "C002"],
        )

        processed = self.service.process_next_borrower()
        self.assertEqual(processed.borrower_id, "C001")
        self.assertEqual(processed.status, "borrowed")
        self.assertEqual(
            [item.borrower_id for item in self.queue_repo.load_queue()],
            ["C002"],
        )

    def test_duplicate_active_borrower_is_rejected(self):
        borrower = Borrower("C001", "Charlie", "B001")

        self.assertTrue(self.service.book_borrow(borrower))
        self.assertFalse(self.service.book_borrow(borrower))
        self.assertEqual(self.service.get_all_books()[0].quantity, 2)
        self.assertEqual(len(self.service.borrow_queue.items), 1)

    def test_reader_crud_and_delete_guard(self):
        reader = Reader("R001", "Reader One")
        self.assertTrue(self.service.add_reader(reader))
        self.assertFalse(self.service.add_reader(reader))

        self.assertTrue(self.service.update_reader(Reader("R001", "Updated Name")))
        self.assertEqual(self.service.get_all_readers()[0].name, "Updated Name")

        active = Borrower("R001", "Updated Name", "B001", status="borrowed")
        self.borrower_repo.save_borrowers([active])
        self.assertFalse(self.service.remove_reader("R001"))

        self.borrower_repo.save_borrowers([])
        self.assertTrue(self.service.remove_reader("R001"))

    def test_reader_history_and_overdue_lookup(self):
        self.service.add_reader(Reader("R001", "Reader One"))
        overdue = Borrower(
            "R001",
            "Reader One",
            "B001",
            borrow_date="2026-01-01",
            due_date="2026-01-10",
            status="borrowed",
        )
        returned = Borrower(
            "R001",
            "Reader One",
            "B002",
            borrow_date="2025-01-01",
            due_date="2025-01-15",
            return_date="2025-01-14",
            status="returned",
        )
        self.borrower_repo.save_borrowers([overdue])
        self.return_history_repo.save_history([returned])

        overdue_result = self.service.get_overdue_borrowers(date(2026, 9, 16))
        self.assertEqual([item.book_id for item in overdue_result], ["B001"])
        history = self.service.get_reader_history("R001")
        self.assertEqual({item.book_id for item in history}, {"B001", "B002"})

    def test_overdue_reader_cannot_borrow_again(self):
        overdue = Borrower(
            "R001",
            "Reader One",
            "B001",
            borrow_date="2026-01-01",
            due_date="2026-01-10",
            status="borrowed",
        )
        self.borrower_repo.save_borrowers([overdue])

        self.assertFalse(self.service.book_borrow(Borrower("R001", "Reader One", "B002")))
        self.assertEqual(self.service.get_all_books()[1].quantity, 2)

    def test_dashboard_analytics_include_reader_category_and_status_summary(self):
        self.service.repository.save_books([
            Book("B001", "Python Basics", "Alice", 2024, 3, "Khoa học máy tính", "978-1-2345-6789-0"),
            Book("B002", "Data Structures", "Bob", 2023, 2, "Cấu trúc dữ liệu", "978-1-2345-6789-1"),
        ])

        self.service.borrower_repo.save_borrowers([
            Borrower("R001", "Alice", "B001", borrow_date=(date.today() - timedelta(days=5)).isoformat(), due_date=(date.today() + timedelta(days=4)).isoformat(), status="borrowed"),
            Borrower("R002", "Bob", "B001", borrow_date=(date.today() - timedelta(days=20)).isoformat(), due_date=(date.today() - timedelta(days=2)).isoformat(), status="pending"),
            Borrower("R003", "Carol", "B002", borrow_date=(date.today() - timedelta(days=40)).isoformat(), due_date=(date.today() - timedelta(days=10)).isoformat(), status="borrowed"),
        ])

        view = LibraryView(self.service)
        stats = view.get_time_window_stats(days=30)

        self.assertIn("total_active", stats)
        self.assertIn("reader_summary", stats)
        self.assertIn("category_summary", stats)
        self.assertIn("status_summary", stats)
        self.assertGreaterEqual(stats["total_active"], 1)
        self.assertIn("Alice", stats["reader_summary"])
        self.assertIn("Khoa học máy tính", stats["category_summary"])
        self.assertIn("borrowed", stats["status_summary"])


if __name__ == "__main__":
    unittest.main()
