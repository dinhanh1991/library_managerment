from copy import deepcopy
from datetime import date, timedelta


class BorrowService:
    def __init__(self, service):
        self.service = service

    def book_borrow(self, borrower):
        if borrower is None:
            return False
        borrower_id = self.service._normalize_text(borrower.borrower_id)
        borrower_name = self.service._normalize_text(borrower.name)
        book_id = self.service._normalize_text(borrower.book_id)
        if not borrower_id or not borrower_name or not book_id:
            return False

        borrowers = self.service.borrower_repo.load_borrowers()
        if any(item.borrower_id == borrower_id for item in borrowers):
            return False
        if any(
            item.borrower_id == borrower_id and item.book_id == book_id
            for item in self.service.borrow_queue.items
        ):
            return False

        books = self.service.repository.load_books()
        readers = self.service.reader_repo.load_readers()
        queue_snapshot = deepcopy(self.service.borrow_queue.items)
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
            self.service._ensure_reader(borrower)
            book.quantity -= 1
            self.service.repository.save_books(books)
            self.service.borrow_queue.enqueue(borrower)
            self.service.queue_repo.save_queue(self.service.borrow_queue.items)
            borrowers.append(borrower)
            self.service.borrower_repo.save_borrowers(borrowers)
        except OSError:
            self.service._rollback([
                (self.service.repository, book_snapshot),
                (self.service.reader_repo, reader_snapshot),
                (self.service.queue_repo, queue_snapshot),
                (self.service.borrower_repo, borrower_snapshot),
            ])
            self.service.borrow_queue.items = queue_snapshot
            raise

        self.service._refresh_structures()
        return True

    def process_next_borrower(self):
        if not self.service.borrow_queue.items:
            return None

        queued_borrower = self.service.borrow_queue.items[0]
        borrowers = self.service.borrower_repo.load_borrowers()
        borrower_snapshot = deepcopy(borrowers)
        queue_snapshot = deepcopy(self.service.borrow_queue.items)

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
        self.service.borrow_queue.dequeue()
        try:
            self.service.borrower_repo.save_borrowers(borrowers)
            self.service.queue_repo.save_queue(self.service.borrow_queue.items)
        except OSError:
            self.service._rollback([
                (self.service.borrower_repo, borrower_snapshot),
                (self.service.queue_repo, queue_snapshot),
            ])
            self.service.borrow_queue.items = queue_snapshot
            raise
        return borrower
