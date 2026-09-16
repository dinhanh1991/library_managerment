import json
import tempfile
import unittest
from pathlib import Path

from LibraryManagement.models.book import Book
from LibraryManagement.models.borrower import Borrower
from LibraryManagement.models.reader import Reader
from LibraryManagement.repositories.book_repo import BookRepository
from LibraryManagement.repositories.borrower_repo import BorrowerRepository
from LibraryManagement.repositories.queue_repo import QueueRepository
from LibraryManagement.repositories.reader_repo import ReaderRepository
from LibraryManagement.repositories.return_history_repo import ReturnHistoryRepository


class RepositoryTestCase(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)
        self.original_paths = {
            BookRepository: BookRepository.FILE_PATH,
            BorrowerRepository: BorrowerRepository.FILE_PATH,
            QueueRepository: QueueRepository.FILE_PATH,
            ReaderRepository: ReaderRepository.FILE_PATH,
            ReturnHistoryRepository: ReturnHistoryRepository.FILE_PATH,
        }
        BookRepository.FILE_PATH = self.temp_path / "books.json"
        BorrowerRepository.FILE_PATH = self.temp_path / "borrowers.json"
        QueueRepository.FILE_PATH = self.temp_path / "queue.json"
        ReaderRepository.FILE_PATH = self.temp_path / "readers.json"
        ReturnHistoryRepository.FILE_PATH = self.temp_path / "history.json"

    def tearDown(self):
        for repository_class, file_path in self.original_paths.items():
            repository_class.FILE_PATH = file_path
        self.temp_dir.cleanup()

    def test_missing_files_return_empty_lists(self):
        self.assertEqual(BookRepository().load_books(), [])
        self.assertEqual(BorrowerRepository().load_borrowers(), [])
        self.assertEqual(QueueRepository().load_queue(), [])
        self.assertEqual(ReaderRepository().load_readers(), [])
        self.assertEqual(ReturnHistoryRepository().load_history(), [])

    def test_invalid_json_raises_value_error(self):
        repositories = [
            (BookRepository, "books.json"),
            (BorrowerRepository, "borrowers.json"),
            (QueueRepository, "queue.json"),
            (ReaderRepository, "readers.json"),
            (ReturnHistoryRepository, "history.json"),
        ]

        for repository_class, filename in repositories:
            with self.subTest(repository=repository_class.__name__):
                path = self.temp_path / filename
                path.write_text("{invalid", encoding="utf-8")
                repository_class.FILE_PATH = path

                with self.assertRaises(ValueError):
                    self._load(repository_class)

    def test_json_root_must_be_list(self):
        repositories = [
            (BookRepository, "books.json"),
            (BorrowerRepository, "borrowers.json"),
            (QueueRepository, "queue.json"),
            (ReaderRepository, "readers.json"),
            (ReturnHistoryRepository, "history.json"),
        ]

        for repository_class, filename in repositories:
            with self.subTest(repository=repository_class.__name__):
                path = self.temp_path / filename
                path.write_text(json.dumps({"data": []}), encoding="utf-8")
                repository_class.FILE_PATH = path

                with self.assertRaises(ValueError):
                    self._load(repository_class)

    def test_json_items_must_be_objects(self):
        repositories = [
            (BookRepository, "books.json"),
            (BorrowerRepository, "borrowers.json"),
            (QueueRepository, "queue.json"),
            (ReaderRepository, "readers.json"),
            (ReturnHistoryRepository, "history.json"),
        ]

        for repository_class, filename in repositories:
            with self.subTest(repository=repository_class.__name__):
                path = self.temp_path / filename
                path.write_text(json.dumps(["invalid"]), encoding="utf-8")
                repository_class.FILE_PATH = path

                with self.assertRaises(ValueError):
                    self._load(repository_class)

    def test_book_repository_round_trip(self):
        path = self.temp_path / "books.json"
        BookRepository.FILE_PATH = path
        books = [Book("B001", "Python", "Anh", 2024, 5, "IT", "123")]

        repository = BookRepository()
        repository.save_books(books)
        loaded = repository.load_books()

        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].book_id, "B001")
        self.assertEqual(loaded[0].category, "IT")
        self.assertEqual(loaded[0].isbn, "123")

    def test_borrower_repository_round_trip(self):
        path = self.temp_path / "borrowers.json"
        BorrowerRepository.FILE_PATH = path
        borrowers = [
            Borrower(
                "DG001",
                "Nguyen Van A",
                "B001",
                "2026-09-01",
                "2026-09-15",
                None,
                "borrowed",
            )
        ]

        repository = BorrowerRepository()
        repository.save_borrowers(borrowers)
        loaded = repository.load_borrowers()

        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].borrower_id, "DG001")
        self.assertEqual(loaded[0].status, "borrowed")

    def test_reader_repository_round_trip(self):
        path = self.temp_path / "readers.json"
        ReaderRepository.FILE_PATH = path
        readers = [Reader("DG001", "Nguyen Van A")]

        repository = ReaderRepository()
        repository.save_readers(readers)
        loaded = repository.load_readers()

        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].reader_id, "DG001")
        self.assertEqual(loaded[0].name, "Nguyen Van A")

    def test_book_and_borrower_save_errors_are_propagated(self):
        book_path = self.temp_path / "book_directory"
        borrower_path = self.temp_path / "borrower_directory"
        book_path.mkdir()
        borrower_path.mkdir()
        BookRepository.FILE_PATH = book_path
        BorrowerRepository.FILE_PATH = borrower_path

        with self.assertRaises(OSError):
            BookRepository().save_books([])

        with self.assertRaises(OSError):
            BorrowerRepository().save_borrowers([])

    @staticmethod
    def _load(repository_class):
        repository = repository_class()
        if repository_class is BookRepository:
            return repository.load_books()
        if repository_class is BorrowerRepository:
            return repository.load_borrowers()
        if repository_class is QueueRepository:
            return repository.load_queue()
        if repository_class is ReaderRepository:
            return repository.load_readers()
        return repository.load_history()


if __name__ == "__main__":
    unittest.main()
