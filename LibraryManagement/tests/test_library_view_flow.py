import sys
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.models.book import Book
from LibraryManagement.models.borrower import Borrower
from LibraryManagement.views.library_view import LibraryView


class LibraryViewFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.service = Mock()
        self.view = LibraryView(self.service)

    def test_dashboard_stats_are_delegated_to_report_service(self):
        self.view.report_service = Mock()
        self.view.report_service.get_dashboard_stats.return_value = {
            "total_books": 10,
            "total_available": 7,
            "current_borrowed": 3,
            "overdue_count": 1,
            "category_counts": {"Python": 4},
        }

        result = self.view.get_dashboard_stats()

        self.assertEqual(result, (10, 7, 3, 1, {"Python": 4}))
        self.view.report_service.get_dashboard_stats.assert_called_once_with()

    def test_time_window_stats_are_delegated_to_report_service(self):
        self.view.report_service = Mock()
        expected = {"total_active": 5}
        self.view.report_service.get_time_window_stats.return_value = expected

        result = self.view.get_time_window_stats(days=14, as_of=date(2026, 9, 16))

        self.assertEqual(result, expected)
        self.view.report_service.get_time_window_stats.assert_called_once_with(
            14,
            date(2026, 9, 16),
        )

    def test_get_book_status_prioritizes_overdue(self):
        overdue_book = Book("B001", "Python", "Alice", 2024, 2)
        borrower = Borrower(
            "DG001",
            "Nguyen Van A",
            "B001",
            "2026-09-01",
            "2026-09-10",
            "borrowed",
        )
        self.service.get_overdue_borrowers.return_value = [borrower]

        status = self.view.get_book_status(overdue_book)

        self.assertEqual(status, ("Quá hạn", "bold red", "red"))

    def test_get_book_status_uses_quantity_when_not_overdue(self):
        available = Book("B001", "Python", "Alice", 2024, 2)
        unavailable = Book("B002", "Java", "Bob", 2024, 0)
        self.service.get_overdue_borrowers.return_value = []

        self.assertEqual(
            self.view.get_book_status(available),
            ("Có sẵn", "bold green", "green"),
        )
        self.assertEqual(
            self.view.get_book_status(unavailable),
            ("Hết", "bold yellow", "yellow"),
        )

    def test_get_overdue_queue_sorts_by_days_descending(self):
        self.service.get_overdue_borrowers.return_value = [
            Borrower(
                "DG001", "A", "B001", "2026-08-01", "2026-09-10", "borrowed"
            ),
            Borrower(
                "DG002", "B", "B002", "2026-08-01", "2026-09-15", "borrowed"
            ),
        ]

        rows = self.view.get_overdue_queue()

        self.assertEqual([row[0] for row in rows], ["DG001", "DG002"])
        self.assertGreaterEqual(rows[0][4], rows[1][4])


if __name__ == "__main__":
    unittest.main()
