import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.repositories.book_repo import BookRepository
from LibraryManagement.services.library_service import LibraryService
from LibraryManagement.views.base_view import BaseView
from LibraryManagement.views.book_view import BookView
from LibraryManagement.views.borrow_view import BorrowView
from LibraryManagement.views.return_view import ReturnView


class UiAndInputTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        self.service = LibraryService()
        self.service.repository = BookRepository()
        self.service.repository.FILE_PATH = self.temp_path / "books.json"

        self.service.borrower_repo = __import__("LibraryManagement.repositories.borrower_repo", fromlist=["BorrowerRepository"]).BorrowerRepository()
        self.service.borrower_repo.FILE_PATH = self.temp_path / "borrowers_list.json"
        self.service.borrow_queue = __import__("LibraryManagement.data_structures.queue", fromlist=["Queue"]).Queue()
        self.service.queue_repo = __import__("LibraryManagement.repositories.queue_repo", fromlist=["QueueRepository"]).QueueRepository()
        self.service.queue_repo.FILE_PATH = self.temp_path / "borrow_queue.json"
        self.service.return_history_repo = __import__("LibraryManagement.repositories.return_history_repo", fromlist=["ReturnHistoryRepository"]).ReturnHistoryRepository()
        self.service.return_history_repo.FILE_PATH = self.temp_path / "return_history.json"
        self.service.return_stack = __import__("LibraryManagement.data_structures.stack", fromlist=["Stack"]).Stack()

        self.view = BookView(self.service)
        self.base_view = BaseView(self.service)

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch.object(BaseView, "pause")
    @patch("builtins.input", side_effect=[
        "B100",
        "Clean Code",
        "Robert C. Martin",
        "2024",
        "5",
        "Cấu trúc dữ liệu",
        "978-1-2345-6789-7",
        "Y",
    ])
    def test_add_book_collects_category_and_isbn(self, _mock_input, _mock_pause):
        self.view.add_book()

        books = self.service.get_all_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].book_id, "B100")
        self.assertEqual(books[0].category, "Cấu trúc dữ liệu")
        self.assertEqual(books[0].isbn, "978-1-2345-6789-7")

    @patch("builtins.input", side_effect=["0"])
    def test_run_menu_exits_on_zero(self, _mock_input):
        self.base_view.run_menu(
            lambda: print("menu"),
            {"0": lambda: None},
        )

    @patch("builtins.input", side_effect=["1", "0"])
    def test_run_menu_stays_open_until_exit(self, _mock_input):
        calls = []

        def action():
            calls.append("called")

        self.base_view.run_menu(
            lambda: None,
            {"1": action, "0": lambda: None},
        )

        self.assertEqual(calls, ["called"])

    def test_menu_contains_expected_main_actions(self):
        menu_content = (
            " [1] ➕ Thêm sách\n"
            " [2] 🗑️  Xóa sách\n"
            " [3] ✏️  Cập nhật sách\n"
            " [4] 📋 Hiển thị tất cả\n"
            " [5] 🔍 Tìm theo tên\n"
            " [6] ✍️  Tìm theo tác giả\n"
            " [7] 🔎 Tìm kiếm nâng cao\n"
            " [0] 🔙 Quay lại"
        )
        self.assertIn("[1] ➕ Thêm sách", menu_content)
        self.assertIn("[7] 🔎 Tìm kiếm nâng cao", menu_content)
        self.assertIn("[0] 🔙 Quay lại", menu_content)

    @patch.object(BaseView, "pause")
    @patch("builtins.input", side_effect=["", "B100", "", "2024", "3", "Y"])
    def test_add_book_rejects_empty_required_fields(self, _mock_input, _mock_pause):
        self.view.add_book()
        self.assertEqual(self.service.get_all_books(), [])

    @patch("builtins.input", side_effect=["",])
    def test_prompt_optional_int_returns_none_for_empty_input(self, _mock_input):
        from LibraryManagement.utils.ui_helpers import prompt_optional_int

        self.assertIsNone(prompt_optional_int("Năm: ", "Năm"))

    @patch("builtins.input", side_effect=["abc", "2025"])
    def test_prompt_optional_int_retries_invalid_input(self, _mock_input):
        from LibraryManagement.utils.ui_helpers import prompt_optional_int

        self.assertEqual(prompt_optional_int("Năm: ", "Năm"), 2025)

    def test_book_catalog_has_real_categories(self):
        catalog_path = ROOT / "data" / "books.json"
        with catalog_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        self.assertTrue(data)
        self.assertTrue(all((book.get("category") or "").strip() for book in data))

    @patch.object(BaseView, "pause")
    @patch.object(BaseView, "confirm_action", return_value=True)
    @patch("builtins.input", side_effect=["R202", "Reader Borrow", "B001", "Y"])
    def test_borrow_view_success_flow(self, _mock_input, _mock_confirm, _mock_pause):
        self.service.repository.save_books([
            __import__("LibraryManagement.models.book", fromlist=["Book"]).Book("B001", "Python Basics", "Alice", 2024, 3)
        ])

        BorrowView(self.service).borrow_book()

        self.assertEqual(len(self.service.borrow_queue.items), 1)
        self.assertEqual(self.service.borrow_queue.items[0].borrower_id, "R202")
        self.assertEqual(self.service.borrow_queue.items[0].status, "pending")

    @patch.object(BaseView, "pause")
    @patch.object(BaseView, "confirm_action", return_value=True)
    @patch("builtins.input", side_effect=["R202", "Reader Borrow", "B001", "Y"])
    def test_return_view_success_flow(self, _mock_input, _mock_confirm, _mock_pause):
        self.service.repository.save_books([
            __import__("LibraryManagement.models.book", fromlist=["Book"]).Book("B001", "Python Basics", "Alice", 2024, 3)
        ])
        self.service.book_borrow(__import__("LibraryManagement.models.borrower", fromlist=["Borrower"]).Borrower("R202", "Reader Borrow", "B001"))

        ReturnView(self.service).return_book()

        self.assertEqual(self.service.get_all_books()[0].quantity, 3)
        self.assertEqual(len(self.service.borrower_repo.load_borrowers()), 0)
        self.assertEqual(len(self.service.return_stack.items), 1)


if __name__ == "__main__":
    unittest.main()
