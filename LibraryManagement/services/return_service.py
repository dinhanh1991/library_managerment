from copy import deepcopy
from datetime import date

from LibraryManagement.utils.return_validator import ReturnValidator


class ReturnService:
    def __init__(
        self,
        repository,
        borrower_repo,
        queue_repo,
        return_history_repo,
        borrow_queue,
        return_stack,
        normalize_text,
        refresh_structures,
        rollback,
    ):
        self.repository = repository
        self.borrower_repo = borrower_repo
        self.queue_repo = queue_repo
        self.return_history_repo = return_history_repo
        self.borrow_queue = borrow_queue
        self.return_stack = return_stack
        self.normalize_text = normalize_text
        self.refresh_structures = refresh_structures
        self.rollback = rollback

    def get_return_history(self):
        return self.return_history_repo.load_history()

    def return_book(self, borrower):
        if not ReturnValidator.is_valid_return_payload(borrower):
            return False
        borrower_id = self.normalize_text(borrower.borrower_id)
        book_id = self.normalize_text(borrower.book_id)

        borrowers = self.borrower_repo.load_borrowers()
        active = next(
            (
                item
                for item in borrowers
                if item.borrower_id == borrower_id and item.book_id == book_id
            ),
            None,
        )
        if active is None or active.status not in {"pending", "borrowed"}:
            return False

        books = self.repository.load_books()
        history = self.return_history_repo.load_history()
        queue_snapshot = deepcopy(self.borrow_queue.items)
        borrower_snapshot = deepcopy(borrowers)
        book_snapshot = deepcopy(books)
        history_snapshot = deepcopy(history)

        book = next((item for item in books if item.book_id == book_id), None)
        if book is None:
            return False

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
            self.borrow_queue.items = [
                item
                for item in self.borrow_queue.items
                if not (
                    item.borrower_id == borrower_id and item.book_id == book_id
                )
            ]
            self.queue_repo.save_queue(self.borrow_queue.items)
        except OSError:
            self.rollback([
                (self.repository, book_snapshot),
                (self.return_history_repo, history_snapshot),
                (self.borrower_repo, borrower_snapshot),
                (self.queue_repo, queue_snapshot),
            ])
            self.borrow_queue.items = queue_snapshot
            if self.return_stack.items and self.return_stack.items[-1] is active:
                self.return_stack.items.pop()
            raise

        self.refresh_structures()
        return True
