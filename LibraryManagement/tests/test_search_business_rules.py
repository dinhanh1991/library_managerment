import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.models.book import Book
from LibraryManagement.repositories.book_repo import BookRepository
from LibraryManagement.services.library_service import LibraryService


class SearchBusinessRulesTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.book_repo = BookRepository()
        self.book_repo.FILE_PATH = Path(self.temp_dir.name) / "books.json"
        self.book_repo.save_books([
            Book("B001", "Python Basics", "Alice", 2024, 3, "Khoa hoc", "978-001"),
            Book("B002", "Data Structures", "Bob", 2023, 0, "Cau truc du lieu", "978-002"),
            Book("B003", "Python Advanced", "Alice", 2024, 2, "Khoa hoc", "978-003"),
        ])

        self.service = LibraryService()
        self.service.repository = self.book_repo

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_search_advanced_filters_all_supported_fields(self):
        results = self.service.search_books_advanced(
            title="python",
            author="alice",
            genre="khoa",
            publish_year="2024",
            isbn="978-003",
            availability="available",
        )
        self.assertEqual([book.book_id for book in results], ["B003"])

    def test_search_advanced_filters_available_and_unavailable(self):
        available = self.service.search_books_advanced(availability="available")
        unavailable = self.service.search_books_advanced(availability="unavailable")

        self.assertEqual({book.book_id for book in available}, {"B001", "B003"})
        self.assertEqual({book.book_id for book in unavailable}, {"B002"})

    def test_invalid_publish_year_does_not_match_all_books(self):
        self.assertEqual(self.service.search_books_advanced(publish_year="abc"), [])
        self.assertEqual(self.service.search_books_advanced(publish_year="-1"), [])

    def test_invalid_availability_is_rejected_by_service(self):
        self.assertEqual(
            self.service.search_books_advanced(availability="something"),
            [],
        )

    def test_empty_filters_return_all_books(self):
        results = self.service.search_books_advanced()
        self.assertEqual([book.book_id for book in results], ["B001", "B002", "B003"])

    def test_title_and_author_search_reject_blank_keyword(self):
        self.assertEqual(self.service.search_books_by_title("   "), [])
        self.assertEqual(self.service.search_books_by_author("   "), [])


if __name__ == "__main__":
    unittest.main()
