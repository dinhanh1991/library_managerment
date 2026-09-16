from copy import deepcopy
from datetime import date, timedelta


class BorrowService:
    def __init__(
        self,
        repository,
        borrower_repo,
        reader_repo,
        queue_repo,
        borrow_queue,
        normalize_text,
        ensure_reader,
        refresh_structures,
        rollback,
    ):
        self.repository = repository
        self.borrower_repo = borrower_repo
        self.reader_repo = reader_repo
        self.queue_repo = queue_repo
        self.borrow_queue = borrow_queue
        self.normalize_text = normalize_text
        self.ensure_reader = ensure_reader
        self.refresh_structures = refresh_structures
        self.rollback = rollback

    def book_borrow(self, borrower):
        if borrower is None:
            return False
        borrower_id = self.normalize_text(borrower.borrower_id)
        borrower_name = self.normalize_text(borrower.name)
        book_id = self.normalize_text(borrower.book_id)
        if not borrower_id or not borrower_name or not book_id:
            return False

        borrowers = self.borrower_repo.load_borrowers()
        if any(item.borrower_id == borrower_id for item in borrowers):
            return False
        if any(
            item.borrower_id == borrower_id and item.book_id == book_id
            for item in self.borrow_queue.items
        ):
            return False

        books = self.repository.load_books()
        readers = self.reader_repo.load_readers()
        queue_snapshot = deepcopy(self.borrow_queue.items)
        borrower_snapshot = deepcopy(borrowers)
        book_snapshot = deepcopy(books)
        reader_snapshot = deepcopy(readers)

        book = next((item for item in books if item.book_id == book_id), None)
        if book is None or book.quantity <= 0:
            return False

        borrower.borrower_id = borrower_id
        borrower.name = borrower_name
        borrower.book_id = book_id
        borrower.borrow_date = date.today().isoformat()
        borrower.due_date = (date.today() + timedelta(days=14)).isoformat()
        borrower.return_date = None
        borrower.status = "pending"

        try:
            self.ensure_reader(borrower)
            book.quantity -= 1
            self.repository.save_books(books)
            self.borrow_queue.enqueue(borrower)
            self.queue_repo.save_queue(self.borrow_queue.items)
            borrowers.append(borrower)
            self.borrower_repo.save_borrowers(borrowers)
        except OSError:
            self.rollback([
                (self.repository, book_snapshot),
                (self.reader_repo, reader_snapshot),
                (self.queue_repo, queue_snapshot),
                (self.borrower_repo, borrower_snapshot),
            ])
            self.borrow_queue.items = queue_snapshot
            raise

        self.refresh_structures()
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
            self.rollback([
                (self.borrower_repo, borrower_snapshot),
                (self.queue_repo, queue_snapshot),
            ])
            self.borrow_queue.items = queue_snapshot
            raise
        return borrower
