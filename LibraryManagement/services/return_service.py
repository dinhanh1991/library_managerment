from copy import deepcopy
from datetime import date


class ReturnService:
    def __init__(self, service):
        self.service = service

    def return_book(self, borrower):
        if borrower is None:
            return False
        borrower_id = self.service._normalize_text(borrower.borrower_id)
        book_id = self.service._normalize_text(borrower.book_id)
        if not borrower_id or not book_id:
            return False

        borrowers = self.service.borrower_repo.load_borrowers()
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

        books = self.service.repository.load_books()
        history = self.service.return_history_repo.load_history()
        queue_snapshot = deepcopy(self.service.borrow_queue.items)
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
            self.service.repository.save_books(books)
            self.service.return_stack.push(active)
            history.append(active)
            self.service.return_history_repo.save_history(history)
            borrowers.remove(active)
            self.service.borrower_repo.save_borrowers(borrowers)
            self.service.borrow_queue.items = [
                item
                for item in self.service.borrow_queue.items
                if not (
                    item.borrower_id == borrower_id and item.book_id == book_id
                )
            ]
            self.service.queue_repo.save_queue(self.service.borrow_queue.items)
        except OSError:
            self.service._rollback([
                (self.service.repository, book_snapshot),
                (self.service.return_history_repo, history_snapshot),
                (self.service.borrower_repo, borrower_snapshot),
                (self.service.queue_repo, queue_snapshot),
            ])
            self.service.borrow_queue.items = queue_snapshot
            if self.service.return_stack.items and self.service.return_stack.items[-1] is active:
                self.service.return_stack.items.pop()
            raise

        self.service._refresh_structures()
        return True
