from copy import deepcopy
from datetime import date

from LibraryManagement.models.reader import Reader
from LibraryManagement.data_structures.queue import Queue
from LibraryManagement.data_structures.stack import Stack
from LibraryManagement.data_structures.linked_list import BookLinkedList
from LibraryManagement.data_structures.bts import BinarySearchTree
from LibraryManagement.services.book_service import BookService
from LibraryManagement.services.reader_service import ReaderService
from LibraryManagement.services.borrow_service import BorrowService
from LibraryManagement.services.return_service import ReturnService


class LibraryService:
    """Facade giữ API cũ và điều phối các service theo nghiệp vụ."""

    def __init__(self):
        from LibraryManagement.repositories.book_repo import BookRepository
        from LibraryManagement.repositories.borrower_repo import BorrowerRepository
        from LibraryManagement.repositories.queue_repo import QueueRepository
        from LibraryManagement.repositories.reader_repo import ReaderRepository
        from LibraryManagement.repositories.return_history_repo import ReturnHistoryRepository

        self.repository = BookRepository()
        self.borrower_repo = BorrowerRepository()
        self.queue_repo = QueueRepository()
        self.reader_repo = ReaderRepository()
        self.return_history_repo = ReturnHistoryRepository()

        self.borrow_queue = Queue()
        self.return_stack = Stack()
        self.book_linked_list = BookLinkedList()
        self.book_bst = BinarySearchTree()

        self.book_service = BookService(self)
        self.reader_service = ReaderService(self)
        self.borrow_service = BorrowService(self)
        self.return_service = ReturnService(self)

        self._load_queue()
        self._refresh_structures()

    @staticmethod
    def _normalize_text(value):
        return str(value or "").strip()

    @staticmethod
    def _is_valid_non_negative_number(value):
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and value >= 0
        )

    def _load_queue(self):
        self.borrow_queue = Queue()
        for borrower in self.queue_repo.load_queue():
            self.borrow_queue.enqueue(borrower)

    @staticmethod
    def _is_overdue(borrower, as_of):
        if borrower.status not in {"pending", "borrowed"} or not borrower.due_date:
            return False
        try:
            due_date = date.fromisoformat(borrower.due_date)
        except ValueError:
            return False
        return due_date < as_of

    def _ensure_reader(self, borrower):
        readers = self.reader_repo.load_readers()
        if any(reader.reader_id == borrower.borrower_id for reader in readers):
            return
        readers.append(Reader(borrower.borrower_id, borrower.name))
        self.reader_repo.save_readers(readers)

    def _rollback(self, snapshots):
        for repository, data in snapshots:
            try:
                if repository is self.repository:
                    repository.save_books(data)
                elif repository is self.borrower_repo:
                    repository.save_borrowers(data)
                elif repository is self.queue_repo:
                    repository.save_queue(data)
                elif repository is self.reader_repo:
                    repository.save_readers(data)
                elif repository is self.return_history_repo:
                    repository.save_history(data)
            except OSError:
                pass

    def get_overdue_borrowers(self, current_date=None):
        current_date = current_date or date.today()
        return [
            item
            for item in self.borrower_repo.load_borrowers()
            if self._is_overdue(item, current_date)
        ]

    def get_active_borrowers(self):
        return self.borrower_repo.load_borrowers()

    def get_return_history(self):
        return self.return_history_repo.load_history()

    def get_all_books(self):
        return self.book_service.get_all_books()

    def build_book_linked_list(self):
        books = self.repository.load_books()
        self.book_linked_list = BookLinkedList()
        for book in books:
            self.book_linked_list.add_book(book)
        return self.book_linked_list

    def build_book_bst(self):
        books = self.repository.load_books()
        self.book_bst = BinarySearchTree()
        for book in books:
            self.book_bst.insert(book)
        return self.book_bst

    def _refresh_structures(self):
        self.book_linked_list = self.build_book_linked_list()
        self.book_bst = self.build_book_bst()

    # Book facade methods
    def add_book(self, book):
        return self.book_service.add_book(book)

    def remove_book(self, book_id):
        return self.book_service.remove_book(book_id)

    def update_book(self, updated_book):
        return self.book_service.update_book(updated_book)

    def search_books_by_title(self, key_work):
        return self.book_service.search_books_by_title(key_work)

    def search_books_by_author(self, author):
        return self.book_service.search_books_by_author(author)

    def search_books_advanced(
        self,
        title=None,
        author=None,
        genre=None,
        publish_year=None,
        isbn=None,
        availability=None,
    ):
        return self.book_service.search_books_advanced(
            title=title,
            author=author,
            genre=genre,
            publish_year=publish_year,
            isbn=isbn,
            availability=availability,
        )

    # Reader facade methods
    def get_all_readers(self):
        return self.reader_service.get_all_readers()

    def add_reader(self, reader):
        return self.reader_service.add_reader(reader)

    def update_reader(self, updated_reader):
        return self.reader_service.update_reader(updated_reader)

    def remove_reader(self, reader_id):
        return self.reader_service.remove_reader(reader_id)

    def get_reader_history(self, reader_id):
        return self.reader_service.get_reader_history(reader_id)

    # Borrow facade methods
    def book_borrow(self, borrower):
        return self.borrow_service.book_borrow(borrower)

    def process_next_borrower(self):
        return self.borrow_service.process_next_borrower()

    # Return facade methods
    def return_book(self, borrower):
        return self.return_service.return_book(borrower)
