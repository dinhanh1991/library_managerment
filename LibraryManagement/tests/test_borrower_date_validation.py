import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.models.borrower import Borrower


class BorrowerDateValidationTestCase(unittest.TestCase):
    def setUp(self):
        self.base_data = {
            "borrower_id": "C001",
            "name": "Charlie",
            "book_id": "B001",
            "borrow_date": "2026-09-01",
            "due_date": "2026-09-15",
            "return_date": None,
            "status": "borrowed",
        }

    def test_valid_iso_dates_are_accepted(self):
        borrower = Borrower.from_dict(self.base_data)

        self.assertEqual(borrower.borrow_date, "2026-09-01")
        self.assertEqual(borrower.due_date, "2026-09-15")
        self.assertIsNone(borrower.return_date)

    def test_invalid_date_string_is_rejected(self):
        for field in ["borrow_date", "due_date", "return_date"]:
            data = self.base_data.copy()
            data[field] = "2026-99-99"

            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    Borrower.from_dict(data)

    def test_non_string_date_is_rejected(self):
        for field in ["borrow_date", "due_date", "return_date"]:
            data = self.base_data.copy()
            data[field] = 20260901

            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    Borrower.from_dict(data)

    def test_empty_date_string_is_rejected(self):
        for field in ["borrow_date", "due_date", "return_date"]:
            data = self.base_data.copy()
            data[field] = "   "

            with self.subTest(field=field):
                with self.assertRaises(ValueError):
                    Borrower.from_dict(data)

    def test_none_date_is_allowed(self):
        data = self.base_data.copy()
        data["borrow_date"] = None
        data["due_date"] = None
        data["return_date"] = None

        borrower = Borrower.from_dict(data)

        self.assertIsNone(borrower.borrow_date)
        self.assertIsNone(borrower.due_date)
        self.assertIsNone(borrower.return_date)


if __name__ == "__main__":
    unittest.main()
