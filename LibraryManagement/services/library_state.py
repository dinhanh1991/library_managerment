from LibraryManagement.data_structures.bts import BinarySearchTree
from LibraryManagement.data_structures.linked_list import BookLinkedList
from LibraryManagement.data_structures.queue import Queue
from LibraryManagement.data_structures.stack import Stack
from LibraryManagement.models.reader import Reader


class LibraryState:
    """Quản lý trạng thái dùng chung của thư viện và thao tác rollback."""

    def __init__(
        self,
        repository,
        borrower_repo,
        queue_repo,
        reader_repo,
        return_history_repo,
    ):
        self.repository = repository
        self.borrower_repo = borrower_repo
        self.queue_repo = queue_repo
        self.reader_repo = reader_repo
        self.return_history_repo = return_history_repo

        self.borrow_queue = Queue()
        self.return_stack = Stack()
        self.book_linked_list = BookLinkedList()
        self.book_bst = BinarySearchTree()

    def load_queue(self):
        self.borrow_queue = Queue()
        for borrower in self.queue_repo.load_queue():
            self.borrow_queue.enqueue(borrower)

    def set_runtime_state(self, **kwargs):
        """Update runtime structures in one place for the library state container."""
        for name, value in kwargs.items():
            if hasattr(self, name):
                setattr(self, name, value)

    def refresh_structures(self):
        books = self.repository.load_books()

        self.book_linked_list = BookLinkedList()
        for book in books:
            self.book_linked_list.add_book(book)

        self.book_bst = BinarySearchTree()
        for book in books:
            self.book_bst.insert(book)

    def ensure_reader(self, borrower):
        readers = self.reader_repo.load_readers()
        if any(reader.reader_id == borrower.borrower_id for reader in readers):
            return
        readers.append(Reader(borrower.borrower_id, borrower.name))
        self.reader_repo.save_readers(readers)

    def rollback(self, snapshots):
        """Restore persisted snapshots and propagate I/O failures to the caller."""
        for repository, data in snapshots:
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
