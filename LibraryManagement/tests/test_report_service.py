import sys
import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.services.report_service import ReportService


class FakeLibraryService:
    def __init__(self):
        self.books = [
            SimpleNamespace(book_id="B001", title="Python Basics", quantity=3, category="Lập trình"),
            SimpleNamespace(book_id="B002", title="Data Structures", quantity=0, category="Cấu trúc dữ liệu"),
            SimpleNamespace(book_id="B003", title="Clean Code", quantity=2, category="Lập trình"),
        ]
        self.active = [
            SimpleNamespace(
                borrower_id="R001",
                name="Nguyễn Văn A",
                book_id="B001",
                borrow_date="2026-09-10",
                due_date="2026-09-20",
                status="borrowed",
            ),
            SimpleNamespace(
                borrower_id="R002",
                name="Trần Văn B",
                book_id="B002",
                borrow_date="2026-09-01",
                due_date="2026-09-10",
                status="pending",
            ),
        ]
        self.overdue = [
            SimpleNamespace(
                borrower_id="R002",
                name="Trần Văn B",
                book_id="B002",
                borrow_date="2026-09-01",
                due_date="2026-09-10",
                status="pending",
            )
        ]
        self.history = [
            SimpleNamespace(
                borrower_id="R001",
                name="Nguyễn Văn A",
                book_id="B003",
                borrow_date="2026-08-01",
                due_date="2026-08-15",
                return_date="2026-08-14",
                status="returned",
            )
        ]
        self.readers = [
            SimpleNamespace(reader_id="R001", name="Nguyễn Văn A"),
            SimpleNamespace(reader_id="R002", name="Trần Văn B"),
        ]

    def get_all_books(self):
        return self.books

    def get_active_borrowers(self):
        return self.active

    def get_overdue_borrowers(self, current_date=None):
        return self.overdue

    def get_return_history(self):
        return self.history

    def get_all_readers(self):
        return self.readers

    def _is_overdue(self, borrower, current_date):
        if not borrower.due_date:
            return False
        try:
            due_date = date.fromisoformat(borrower.due_date)
        except ValueError:
            return False
        return borrower.status in {"borrowed", "pending"} and due_date < current_date


class ReportServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.service = ReportService(FakeLibraryService())

    def test_get_overview(self):
        result = self.service.get_overview()

        self.assertEqual(result["total_books"], 3)
        self.assertEqual(result["available_books"], 2)
        self.assertEqual(result["borrowed"], 1)
        self.assertEqual(result["pending"], 1)
        self.assertEqual(result["overdue"], 1)
        self.assertEqual(result["total_readers"], 2)

    def test_get_dashboard_stats(self):
        result = self.service.get_dashboard_stats()

        self.assertEqual(result["total_books"], 3)
        self.assertEqual(result["total_available"], 2)
        self.assertEqual(result["current_borrowed"], 1)
        self.assertEqual(result["overdue_count"], 1)
        self.assertEqual(result["category_counts"], {"Lập trình": 1})

    def test_get_time_window_stats(self):
        result = self.service.get_time_window_stats(
            days=30,
            as_of=date(2026, 9, 16),
        )

        self.assertEqual(result["total_active"], 2)
        self.assertEqual(result["reader_summary"]["Nguyễn Văn A"], 2)
        self.assertEqual(result["reader_summary"]["Trần Văn B"], 1)
        self.assertEqual(result["category_summary"]["Lập trình"], 2)
        self.assertEqual(result["category_summary"]["Cấu trúc dữ liệu"], 1)
        self.assertEqual(result["status_summary"]["borrowed"], 1)
        self.assertEqual(result["status_summary"]["pending"], 1)
        self.assertEqual(result["status_summary"]["overdue"], 1)
        self.assertEqual(result["status_summary"]["returned"], 1)

    def test_get_book_statistics(self):
        result = self.service.get_book_statistics()

        self.assertEqual(result["total_titles"], 3)
        self.assertEqual(result["total_quantity"], 5)
        self.assertEqual(result["available_quantity"], 5)
        self.assertEqual(result["out_of_stock"], 1)

    def test_get_borrow_statistics(self):
        result = self.service.get_borrow_statistics()

        self.assertEqual(result["borrowed"], 1)
        self.assertEqual(result["pending"], 1)
        self.assertEqual(result["overdue"], 1)
        self.assertEqual(result["returned"], 1)

    def test_get_category_statistics(self):
        result = self.service.get_category_statistics()

        self.assertEqual(result["Lập trình"], 1)
        self.assertEqual(result["Cấu trúc dữ liệu"], 1)

    def test_get_overdue_borrowers(self):
        result = self.service.get_overdue_borrowers(date(2026, 9, 16))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["borrower_id"], "R002")
        self.assertEqual(result[0]["overdue_days"], 6)

    def test_get_most_borrowed_books(self):
        result = self.service.get_most_borrowed_books()

        self.assertEqual(result[0]["book_id"], "B001")
        self.assertEqual(result[0]["borrow_count"], 1)
        self.assertEqual(result[1]["book_id"], "B002")
        self.assertEqual(result[1]["borrow_count"], 1)

    def test_get_most_active_readers(self):
        result = self.service.get_most_active_readers()

        self.assertEqual(result[0]["borrower_id"], "R001")
        self.assertEqual(result[0]["name"], "Nguyễn Văn A")
        self.assertEqual(result[0]["borrow_count"], 2)
        self.assertEqual(result[1]["borrower_id"], "R002")
        self.assertEqual(result[1]["borrow_count"], 1)


if __name__ == "__main__":
    unittest.main()
