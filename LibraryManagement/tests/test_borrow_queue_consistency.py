import unittest

from LibraryManagement.models.borrower import Borrower
from LibraryManagement.services.library_service import LibraryService


class FakeBorrowerRepository:
    def __init__(self, borrowers):
        self.borrowers = borrowers
        self.saved_borrowers = None

    def load_borrowers(self):
        return list(self.borrowers)

    def save_borrowers(self, borrowers):
        self.saved_borrowers = list(borrowers)
        self.borrowers = list(borrowers)


class FakeQueueRepository:
    def __init__(self):
        self.saved_queue = None

    def save_queue(self, borrowers):
        self.saved_queue = list(borrowers)


class TestQueue:
    def __init__(self):
        self.items = []

    def dequeue(self):
        if not self.items:
            return None
        return self.items.pop(0)


class TestBorrowQueueConsistency(unittest.TestCase):
    def setUp(self):
        self.service = LibraryService.__new__(LibraryService)
        self.service.borrow_queue = TestQueue()
        self.service.borrower_repo = FakeBorrowerRepository([])
        self.service.queue_repo = FakeQueueRepository()

    def test_process_next_borrower_keeps_queue_when_borrower_is_missing(self):
        queued_borrower = Borrower("DG001", "Nguyen Van A", "S001")
        queued_borrower.status = "pending"
        self.service.borrow_queue.items = [queued_borrower]

        result = self.service.process_next_borrower()

        self.assertIsNone(result)
        self.assertEqual(len(self.service.borrow_queue.items), 1)
        self.assertEqual(self.service.borrow_queue.items[0].borrower_id, "DG001")
        self.assertIsNone(self.service.borrower_repo.saved_borrowers)
        self.assertIsNone(self.service.queue_repo.saved_queue)

    def test_process_next_borrower_updates_matching_pending_borrower(self):
        borrower = Borrower("DG001", "Nguyen Van A", "S001")
        borrower.status = "pending"
        self.service.borrower_repo.borrowers = [borrower]
        self.service.borrow_queue.items = [borrower]

        result = self.service.process_next_borrower()

        self.assertIsNotNone(result)
        self.assertEqual(result.borrower_id, "DG001")
        self.assertEqual(result.book_id, "S001")
        self.assertEqual(result.status, "borrowed")
        self.assertEqual(self.service.borrower_repo.borrowers[0].status, "borrowed")
        self.assertEqual(self.service.borrow_queue.items, [])
        self.assertEqual(self.service.queue_repo.saved_queue, [])


if __name__ == "__main__":
    unittest.main()
