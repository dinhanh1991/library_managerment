from LibraryManagement.data_structures.bts import BinarySearchTree
from LibraryManagement.data_structures.linked_list import BookLinkedList
from LibraryManagement.data_structures.queue import Queue
from LibraryManagement.data_structures.stack import Stack


class LibraryState:
    """Runtime state holder for the library: queue, stack, book structures, and rollback snapshots.

    This class intentionally manages only runtime and persistence-state concerns. Business
    decisions remain in the service layer.
    """

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

        self.reset_runtime_state()

    def reset_runtime_state(self):
        """Reset the runtime-only data structures to their empty initial state."""
        self.borrow_queue = Queue()
        self.return_stack = Stack()
        self.book_linked_list = BookLinkedList()
        self.book_bst = BinarySearchTree()

    def load_queue(self):
        """Load queue items from the queue repository into the runtime queue."""
        self.borrow_queue = Queue()
        for borrower in self.queue_repo.load_queue():
            self.borrow_queue.enqueue(borrower)

    def set_runtime_state(self, **kwargs):
        """Update runtime structures in one place for the library state container."""
        for name, value in kwargs.items():
            if hasattr(self, name):
                setattr(self, name, value)

    def get_borrow_queue_items(self):
        return list(self.borrow_queue.items)

    def get_return_stack_items(self):
        return list(self.return_stack.items)

    def get_linked_list_books(self):
        books = []
        current = self.book_linked_list.head
        while current is not None:
            books.append(current.data)
            current = current.next
        return books

    def search_linked_list(self, book_id):
        return self.book_linked_list.search_book(book_id)

    def search_bst(self, book_id):
        return self.book_bst.search(book_id)

    def get_bst_inorder(self):
        result = []

        def visit(node):
            if node is None:
                return
            visit(node.left)
            result.append(node.book)
            visit(node.right)

        visit(self.book_bst.root)
        return result

    def get_bst_preorder(self):
        result = []

        def visit(node):
            if node is None:
                return
            result.append(node.book)
            visit(node.left)
            visit(node.right)

        visit(self.book_bst.root)
        return result

    def get_bst_postorder(self):
        result = []

        def visit(node):
            if node is None:
                return
            visit(node.left)
            visit(node.right)
            result.append(node.book)

        visit(self.book_bst.root)
        return result

    def rebuild_book_structures(self):
        """Rebuild the linked-list and BST views of books from repository data."""
        books = self.repository.load_books()

        self.book_linked_list = BookLinkedList()
        for book in books:
            self.book_linked_list.add_book(book)

        self.book_bst = BinarySearchTree()
        for book in books:
            self.book_bst.insert(book)

    def refresh_structures(self):
        """Compatibility wrapper that keeps the public API while isolating state rebuild logic."""
        self.rebuild_book_structures()

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
