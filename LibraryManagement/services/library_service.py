from copy import deepcopy
from datetime import date, timedelta

from LibraryManagement.models.borrower import Borrower
from LibraryManagement.models.reader import Reader
from LibraryManagement.data_structures.queue import Queue
from LibraryManagement.data_structures.stack import Stack
from LibraryManagement.data_structures.linked_list import BookLinkedList
from LibraryManagement.data_structures.bts import BinarySearchTree


class LibraryService:
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
        self._load_queue()
        self._refresh_structures()

    @staticmethod
    def _normalize_text(value):
        return str(value or "").strip()

    @staticmethod
    def _is_valid_non_negative_number(value):
        return isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0

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
        return [item for item in self.borrower_repo.load_borrowers() if self._is_overdue(item, current_date)]

    def get_all_books(self):
        return self.repository.load_books()

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

    def add_book(self, book):
        if book is None:
            return False
        book_id = self._normalize_text(book.book_id)
        if (
            not book_id
            or not self._is_valid_non_negative_number(book.quantity)
            or not self._is_valid_non_negative_number(book.publish_year)
        ):
            return False
        books = self.repository.load_books()
        for existing in books:
            if self._normalize_text(existing.book_id) == book_id:
                return False
        book.book_id = book_id
        books.append(book)
        self.repository.save_books(books)
        self._refresh_structures()
        return True

    def remove_book(self, book_id):
        book_id = self._normalize_text(book_id)
        if not book_id:
            return False
        books = self.repository.load_books()
        borrowers = self.borrower_repo.load_borrowers()
        if any(self._normalize_text(item.book_id) == book_id for item in borrowers):
            return False
        for book in books:
            if self._normalize_text(book.book_id) == book_id:
                books.remove(book)
                self.repository.save_books(books)
                self._refresh_structures()
                return True
        return False

    def update_book(self, updated_book):
        if (
            updated_book is None
            or not self._is_valid_non_negative_number(updated_book.quantity)
            or not self._is_valid_non_negative_number(updated_book.publish_year)
        ):
            return False
        book_id = self._normalize_text(updated_book.book_id)
        if not book_id:
            return False
        updated_book.book_id = book_id
        books = self.repository.load_books()
        borrowers = self.borrower_repo.load_borrowers()
        if any(self._normalize_text(item.book_id) == book_id for item in borrowers):
            return False
        for i, book in enumerate(books):
            if self._normalize_text(book.book_id) == book_id:
                books[i] = updated_book
                self.repository.save_books(books)
                self._refresh_structures()
                return True
        return False

    def search_books_by_title(self, keyWork):
        keyword = self._normalize_text(keyWork).lower()
        if not keyword:
            return []
        books = self.repository.load_books()
        return [book for book in books if keyword in str(book.title or "").lower()]

    def search_books_by_author(self, author):
        keyword = self._normalize_text(author).lower()
        if not keyword:
            return []
        books = self.repository.load_books()
        return [book for book in books if keyword in str(book.author or "").lower()]

    def search_books_advanced(self, title=None, author=None, genre=None, publish_year=None, isbn=None, availability=None):
        books = self.repository.load_books()
        results = []
        normalized_title = (title or "").strip().lower()
        normalized_author = (author or "").strip().lower()
        normalized_genre = (genre or "").strip().lower()
        normalized_isbn = (isbn or "").strip().lower()
        try:
            normalized_year = int(publish_year) if publish_year not in (None, "") else None
        except (TypeError, ValueError):
            return []
        if normalized_year is not None and normalized_year < 0:
            return []
        normalized_availability = (availability or "all").strip().lower()
        if normalized_availability not in {"all", "available", "unavailable"}:
            return []
        for book in books:
            if normalized_title and normalized_title not in str(book.title or "").lower(): continue
            if normalized_author and normalized_author not in str(book.author or "").lower(): continue
            if normalized_genre and normalized_genre not in str(getattr(book, "category", "") or "").lower(): continue
            if normalized_year is not None and book.publish_year != normalized_year: continue
            if normalized_isbn and normalized_isbn not in str(getattr(book, "isbn", "") or "").lower(): continue
            if normalized_availability == "available" and book.quantity <= 0: continue
            if normalized_availability == "unavailable" and book.quantity > 0: continue
            results.append(book)
        return results

    def get_all_readers(self):
        return self.reader_repo.load_readers()

    def add_reader(self, reader):
        if reader is None: return False
        reader_id = self._normalize_text(reader.reader_id)
        name = self._normalize_text(reader.name)
        if not reader_id or not name: return False
        readers = self.reader_repo.load_readers()
        if any(item.reader_id == reader_id for item in readers): return False
        reader.reader_id, reader.name = reader_id, name
        readers.append(reader)
        self.reader_repo.save_readers(readers)
        return True

    def update_reader(self, updated_reader):
        if updated_reader is None: return False
        reader_id = self._normalize_text(updated_reader.reader_id)
        name = self._normalize_text(updated_reader.name)
        if not reader_id or not name: return False
        readers = self.reader_repo.load_readers()
        for i, reader in enumerate(readers):
            if reader.reader_id == reader_id:
                updated_reader.reader_id, updated_reader.name = reader_id, name
                readers[i] = updated_reader
                self.reader_repo.save_readers(readers)

                borrowers = self.borrower_repo.load_borrowers()
                changed = False
                for borrower in borrowers:
                    if borrower.borrower_id == reader_id:
                        borrower.name = name
                        changed = True
                if changed:
                    self.borrower_repo.save_borrowers(borrowers)

                    for queued_borrower in self.borrow_queue.items:
                        if queued_borrower.borrower_id == reader_id:
                            queued_borrower.name = name
                    self.queue_repo.save_queue(self.borrow_queue.items)
                return True
        return False

    def remove_reader(self, reader_id):
        reader_id = self._normalize_text(reader_id)
        if not reader_id: return False
        borrowers = self.borrower_repo.load_borrowers()
        if any(item.borrower_id == reader_id for item in borrowers): return False
        readers = self.reader_repo.load_readers()
        for reader in readers:
            if reader.reader_id == reader_id:
                readers.remove(reader)
                self.reader_repo.save_readers(readers)
                return True
        return False

    def get_reader_history(self, reader_id):
        reader_id = self._normalize_text(reader_id)
        active = [item for item in self.borrower_repo.load_borrowers() if item.borrower_id == reader_id]
        history = [item for item in self.return_history_repo.load_history() if item.borrower_id == reader_id]
        return active + history

    def book_borrow(self, borrower):
        if borrower is None: return False
        borrower_id = self._normalize_text(borrower.borrower_id)
        borrower_name = self._normalize_text(borrower.name)
        book_id = self._normalize_text(borrower.book_id)
        if not borrower_id or not borrower_name or not book_id: return False
        borrowers = self.borrower_repo.load_borrowers()
        if any(item.borrower_id == borrower_id for item in borrowers): return False
        if any(item.borrower_id == borrower_id and item.book_id == book_id for item in self.borrow_queue.items): return False
        books = self.repository.load_books()
        readers = self.reader_repo.load_readers()
        queue_snapshot = deepcopy(self.borrow_queue.items)
        borrower_snapshot = deepcopy(borrowers)
        book_snapshot = deepcopy(books)
        reader_snapshot = deepcopy(readers)
        book = next((item for item in books if item.book_id == book_id), None)
        if book is None or book.quantity <= 0: return False
        borrower.borrower_id, borrower.name, borrower.book_id = borrower_id, borrower_name, book_id
        borrower.borrow_date = date.today().isoformat()
        borrower.due_date = (date.today() + timedelta(days=14)).isoformat()
        borrower.return_date = None
        borrower.status = "pending"
        try:
            self._ensure_reader(borrower)
            book.quantity -= 1
            self.repository.save_books(books)
            self.borrow_queue.enqueue(borrower)
            self.queue_repo.save_queue(self.borrow_queue.items)
            borrowers.append(borrower)
            self.borrower_repo.save_borrowers(borrowers)
        except OSError:
            self._rollback([
                (self.repository, book_snapshot),
                (self.reader_repo, reader_snapshot),
                (self.queue_repo, queue_snapshot),
                (self.borrower_repo, borrower_snapshot),
            ])
            self.borrow_queue.items = queue_snapshot
            raise
        self._refresh_structures()
        return True

    def process_next_borrower(self):
        if not self.borrow_queue.items:
            return None

        queued_borrower = self.borrow_queue.items[0]
        borrowers = self.borrower_repo.load_borrowers()
        borrower_snapshot = deepcopy(borrowers)
        queue_snapshot = deepcopy(self.borrow_queue.items)

        borrower = None
        for item in borrowers:
            if (
                item.borrower_id == queued_borrower.borrower_id
                and item.book_id == queued_borrower.book_id
            ):
                borrower = item
                break

        if borrower is None or borrower.status != "pending":
            return None

        borrower.status = "borrowed"
        self.borrow_queue.dequeue()
        try:
            self.borrower_repo.save_borrowers(borrowers)
            self.queue_repo.save_queue(self.borrow_queue.items)
        except OSError:
            self._rollback([
                (self.borrower_repo, borrower_snapshot),
                (self.queue_repo, queue_snapshot),
            ])
            self.borrow_queue.items = queue_snapshot
            raise
        return borrower

    def return_book(self, borrower):
        if borrower is None: return False
        borrower_id = self._normalize_text(borrower.borrower_id)
        book_id = self._normalize_text(borrower.book_id)
        if not borrower_id or not book_id: return False
        borrowers = self.borrower_repo.load_borrowers()
        active = next((item for item in borrowers if item.borrower_id == borrower_id and item.book_id == book_id), None)
        if active is None or active.status not in {"pending", "borrowed"}: return False
        books = self.repository.load_books()
        history = self.return_history_repo.load_history()
        queue_snapshot = deepcopy(self.borrow_queue.items)
        borrower_snapshot = deepcopy(borrowers)
        book_snapshot = deepcopy(books)
        history_snapshot = deepcopy(history)
        book = next((item for item in books if item.book_id == book_id), None)
        if book is None: return False
        book.quantity += 1
        active.return_date = date.today().isoformat()
        active.status = "returned"
        try:
            self.repository.save_books(books)
            self.return_stack.push(active)
            history.append(active)
            self.return_history_repo.save_history(history)
            borrowers.remove(active)
            self.borrower_repo.save_borrowers(borrowers)
            self.borrow_queue.items = [item for item in self.borrow_queue.items if not (item.borrower_id == borrower_id and item.book_id == book_id)]
            self.queue_repo.save_queue(self.borrow_queue.items)
        except OSError:
            self._rollback([
                (self.repository, book_snapshot),
                (self.return_history_repo, history_snapshot),
                (self.borrower_repo, borrower_snapshot),
                (self.queue_repo, queue_snapshot),
            ])
            self.borrow_queue.items = queue_snapshot
            if self.return_stack.items and self.return_stack.items[-1] is active:
                self.return_stack.items.pop()
            raise
        self._refresh_structures()
        return True
