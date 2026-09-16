import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

from rich.console import Console

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.models.book import Book
from LibraryManagement.utils.ui_helpers import add_book_to_table, create_book_table
from LibraryManagement.views.book_view import BookView


class BookViewTestCase(unittest.TestCase):
    def test_create_book_table_has_status_column(self):
        table = create_book_table("DANH SÁCH SÁCH")

        headers = [column.header for column in table.columns]

        self.assertEqual(
            headers,
            ["MÃ SÁCH", "TÊN SÁCH", "TÁC GIẢ", "NĂM", "SL", "TÌNH TRẠNG"],
        )

    def test_add_book_to_table_displays_status(self):
        table = create_book_table("DANH SÁCH SÁCH")
        book = Book("B001", "Python Basics", "Alice", 2024, 3)
        console = Console(record=True)

        add_book_to_table(table, book, status="Có sẵn")
        console.print(table)
        output = console.export_text()

        self.assertIn("B001", output)
        self.assertIn("Python Basics", output)
        self.assertIn("Có sẵn", output)

    def test_book_view_status_depends_on_quantity(self):
        available = Book("B001", "Python Basics", "Alice", 2024, 2)
        unavailable = Book("B002", "Data Structures", "Bob", 2023, 0)

        self.assertEqual(BookView.get_book_status(available), "Có sẵn")
        self.assertEqual(BookView.get_book_status(unavailable), "Hết")

    def test_display_books_shows_books_and_status(self):
        service = Mock()
        service.get_all_books.return_value = [
            Book("B001", "Python Basics", "Alice", 2024, 3),
            Book("B002", "Data Structures", "Bob", 2023, 0),
        ]

        view = BookView(service)
        view.console = Console(record=True)
        view.pause = Mock()

        view.display_books()
        output = view.console.export_text()

        service.get_all_books.assert_called_once_with()
        self.assertIn("DANH SÁCH SÁCH", output)
        self.assertIn("B001", output)
        self.assertIn("B002", output)
        self.assertIn("Có sẵn", output)
        self.assertIn("Hết", output)
        view.pause.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
