from datetime import date

from LibraryManagement.services.book_service import BookService
from LibraryManagement.services.reader_service import ReaderService
from LibraryManagement.services.borrow_service import BorrowService
from LibraryManagement.services.return_service import ReturnService
from LibraryManagement.services.library_state import LibraryState
from LibraryManagement.utils.validators import AppValidator


class LibraryService:
    """Facade giữ API cũ và điều phối các service theo nghiệp vụ."""

    def __init__(
        self,
        repository=None,
        borrower_repo=None,
        queue_repo=None,
        reader_repo=None,
        return_history_repo=None,
    ):
        from LibraryManagement.repositories.book_repo import BookRepository
        from LibraryManagement.repositories.borrower_repo import BorrowerRepository
        from LibraryManagement.repositories.queue_repo import QueueRepository
        from LibraryManagement.repositories.reader_repo import ReaderRepository
        from LibraryManagement.repositories.return_history_repo import ReturnHistoryRepository

        self._repository = repository if repository is not None else BookRepository()
        self._borrower_repo = borrower_repo if borrower_repo is not None else BorrowerRepository()
        self._queue_repo = queue_repo if queue_repo is not None else QueueRepository()
        self._reader_repo = reader_repo if reader_repo is not None else ReaderRepository()
        self._return_history_repo = (
            return_history_repo
            if return_history_repo is not None
            else ReturnHistoryRepository()
        )

        self.state = LibraryState(
            self._repository,
            self._borrower_repo,
            self._queue_repo,
            self._reader_repo,
            self._return_history_repo,
        )

        self._borrow_queue = self.state.borrow_queue
        self._return_stack = self.state.return_stack
        self._book_linked_list = self.state.book_linked_list
        self._book_bst = self.state.book_bst

        self._load_queue()
        self._refresh_structures()

        self.book_service = BookService(
            repository=self._repository,
            borrower_repo=self._borrower_repo,
            normalize_text=self._normalize_text,
            validate_number=self._is_valid_non_negative_number,
            refresh_structures=self._refresh_structures,
        )
        self.reader_service = ReaderService(
            reader_repo=self._reader_repo,
            borrower_repo=self._borrower_repo,
            queue_repo=self._queue_repo,
            return_history_repo=self._return_history_repo,
            borrow_queue=self._borrow_queue,
            normalize_text=self._normalize_text,
            rollback=self._rollback,
        )
        self.borrow_service = BorrowService(
            repository=self._repository,
            borrower_repo=self._borrower_repo,
            reader_repo=self._reader_repo,
            queue_repo=self._queue_repo,
            borrow_queue=self._borrow_queue,
            normalize_text=self._normalize_text,
            ensure_reader=self._ensure_reader,
            refresh_structures=self._refresh_structures,
            rollback=self._rollback,
        )
        self.return_service = ReturnService(
            repository=self._repository,
            borrower_repo=self._borrower_repo,
            queue_repo=self._queue_repo,
            return_history_repo=self._return_history_repo,
            borrow_queue=self._borrow_queue,
            return_stack=self._return_stack,
            normalize_text=self._normalize_text,
            refresh_structures=self._refresh_structures,
            rollback=self._rollback,
        )

    def _sync_service_dependencies(self, **updates):
        """Propagate shared state to the state object and collaborating services."""
        if not updates:
            return

        if hasattr(self, "state"):
            filtered_updates = {
                name: value
                for name, value in updates.items()
                if hasattr(self.state, name)
            }
            if filtered_updates:
                self.state.set_runtime_state(**filtered_updates)

        for service_name in (
            "book_service",
            "reader_service",
            "borrow_service",
            "return_service",
        ):
            service = getattr(self, service_name, None)
            if service is None:
                continue
            for name, value in updates.items():
                if hasattr(service, name):
                    setattr(service, name, value)

    @property
    def repository(self):
        return self._repository

    @repository.setter
    def repository(self, value):
        self._repository = value
        self._sync_service_dependencies(repository=value)

    @property
    def borrower_repo(self):
        return self._borrower_repo

    @borrower_repo.setter
    def borrower_repo(self, value):
        self._borrower_repo = value
        self._sync_service_dependencies(borrower_repo=value)

    @property
    def queue_repo(self):
        return self._queue_repo

    @queue_repo.setter
    def queue_repo(self, value):
        self._queue_repo = value
        self._sync_service_dependencies(queue_repo=value)

    @property
    def reader_repo(self):
        return self._reader_repo

    @reader_repo.setter
    def reader_repo(self, value):
        self._reader_repo = value
        self._sync_service_dependencies(reader_repo=value)

    @property
    def return_history_repo(self):
        return self._return_history_repo

    @return_history_repo.setter
    def return_history_repo(self, value):
        self._return_history_repo = value
        self._sync_service_dependencies(return_history_repo=value)

    @property
    def borrow_queue(self):
        return self._borrow_queue

    @borrow_queue.setter
    def borrow_queue(self, value):
        self._borrow_queue = value
        self._sync_service_dependencies(borrow_queue=value)

    @property
    def return_stack(self):
        return self._return_stack

    @return_stack.setter
    def return_stack(self, value):
        self._return_stack = value
        self._sync_service_dependencies(return_stack=value)

    @property
    def book_linked_list(self):
        return self._book_linked_list

    @book_linked_list.setter
    def book_linked_list(self, value):
        self._book_linked_list = value
        if hasattr(self, "state"):
            self.state.set_runtime_state(book_linked_list=value)

    @property
    def book_bst(self):
        return self._book_bst

    @book_bst.setter
    def book_bst(self, value):
        self._book_bst = value
        if hasattr(self, "state"):
            self.state.set_runtime_state(book_bst=value)

    @staticmethod
    def _normalize_text(value):
        return AppValidator.normalize_text(value)

    @staticmethod
    def _is_valid_non_negative_number(value):
        return AppValidator.is_non_negative_int(value)

    def _load_queue(self):
        self.state.load_queue()
        self.borrow_queue = self.state.borrow_queue

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
        self.state.ensure_reader(borrower)

    def _rollback(self, snapshots):
        self.state.rollback(snapshots)

    def get_overdue_borrowers(self, current_date=None):
        current_date = current_date or date.today()
        return [
            item
            for item in self.borrower_repo.load_borrowers()
            if self._is_overdue(item, current_date)
        ]

    def get_active_borrowers(self):
        return self.borrower_repo.load_borrowers()

    def is_book_borrowed(self, book_id):
        book_id = self._normalize_text(book_id)
        if not book_id:
            return False
        return any(
            self._normalize_text(item.book_id) == book_id
            for item in self.get_active_borrowers()
            if item.status in {"pending", "borrowed"}
        )

    def get_active_reader_ids(self):
        return {
            borrower.borrower_id
            for borrower in self.get_active_borrowers()
            if borrower.status in {"pending", "borrowed"}
        }

    def get_return_history(self):
        return self.return_history_repo.load_history()

    def get_all_books(self):
        return self.book_service.get_all_books()

    def build_book_linked_list(self):
        self.state.refresh_structures()
        self.book_linked_list = self.state.book_linked_list
        self.book_bst = self.state.book_bst
        return self.book_linked_list

    def build_book_bst(self):
        self.state.refresh_structures()
        self.book_linked_list = self.state.book_linked_list
        self.book_bst = self.state.book_bst
        return self.book_bst

    def _refresh_structures(self):
        self.state.refresh_structures()
        self.book_linked_list = self.state.book_linked_list
        self.book_bst = self.state.book_bst

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

    def _get_borrow_service(self):
        """Create BorrowService lazily for legacy tests using LibraryService.__new__()."""
        if hasattr(self, "borrow_service"):
            return self.borrow_service

        self.borrow_service = BorrowService(
            repository=getattr(self, "repository", None),
            borrower_repo=self.borrower_repo,
            reader_repo=getattr(self, "reader_repo", None),
            queue_repo=self.queue_repo,
            borrow_queue=self.borrow_queue,
            normalize_text=self._normalize_text,
            ensure_reader=getattr(self, "_ensure_reader", lambda borrower: None),
            refresh_structures=getattr(self, "_refresh_structures", lambda: None),
            rollback=getattr(self, "_rollback", lambda snapshots: None),
        )
        return self.borrow_service

    # Borrow facade methods
    def book_borrow(self, borrower):
        return self._get_borrow_service().book_borrow(borrower)

    def process_next_borrower(self):
        return self._get_borrow_service().process_next_borrower()

    # Return facade methods
    def return_book(self, borrower):
        return self.return_service.return_book(borrower)
