from copy import deepcopy

from LibraryManagement.models.reader import Reader
from LibraryManagement.utils.reader_validator import ReaderValidator


class ReaderService:
    def __init__(
        self,
        reader_repo,
        borrower_repo,
        queue_repo,
        return_history_repo,
        borrow_queue,
        normalize_text,
        rollback,
    ):
        self.reader_repo = reader_repo
        self.borrower_repo = borrower_repo
        self.queue_repo = queue_repo
        self.return_history_repo = return_history_repo
        self.borrow_queue = borrow_queue
        self.normalize_text = normalize_text
        self.rollback = rollback

    def get_all_readers(self):
        return self.reader_repo.load_readers()

    def get_active_reader_ids(self):
        return {
            borrower.borrower_id
            for borrower in self.borrower_repo.load_borrowers()
            if borrower.is_active()
        }

    def ensure_reader(self, borrower):
        readers = self.reader_repo.load_readers()
        if any(reader.reader_id == borrower.borrower_id for reader in readers):
            return
        readers.append(Reader(borrower.borrower_id, borrower.name))
        self.reader_repo.save_readers(readers)

    def add_reader(self, reader):
        if not ReaderValidator.is_valid_reader_payload(reader):
            return False
        reader_id = self.normalize_text(reader.reader_id)
        name = self.normalize_text(reader.name)
        readers = self.reader_repo.load_readers()
        if any(item.reader_id == reader_id for item in readers):
            return False
        reader.reader_id, reader.name = reader_id, name
        readers.append(reader)
        self.reader_repo.save_readers(readers)
        return True

    def update_reader(self, updated_reader):
        if not ReaderValidator.is_valid_reader_payload(updated_reader):
            return False
        reader_id = self.normalize_text(updated_reader.reader_id)
        name = self.normalize_text(updated_reader.name)

        readers = self.reader_repo.load_readers()
        borrowers = self.borrower_repo.load_borrowers()
        queue_snapshot = deepcopy(self.borrow_queue.items)
        reader_snapshot = deepcopy(readers)
        borrower_snapshot = deepcopy(borrowers)

        for i, reader in enumerate(readers):
            if reader.reader_id == reader_id:
                updated_reader.reader_id, updated_reader.name = reader_id, name
                readers[i] = updated_reader

                changed = False
                for borrower in borrowers:
                    if borrower.borrower_id == reader_id:
                        borrower.name = name
                        changed = True

                queue_items = deepcopy(self.borrow_queue.items)
                for queued_borrower in queue_items:
                    if queued_borrower.borrower_id == reader_id:
                        queued_borrower.name = name

                try:
                    self.reader_repo.save_readers(readers)
                    if changed:
                        self.borrower_repo.save_borrowers(borrowers)
                    self.queue_repo.save_queue(queue_items)
                except OSError:
                    self.rollback([
                        (self.reader_repo, reader_snapshot),
                        (self.borrower_repo, borrower_snapshot),
                        (self.queue_repo, queue_snapshot),
                    ])
                    self.borrow_queue.items = queue_snapshot
                    raise

                self.borrow_queue.items = queue_items
                return True
        return False

    def remove_reader(self, reader_id):
        reader_id = self.normalize_text(reader_id)
        if not ReaderValidator.is_valid_reader_id(reader_id):
            return False
        borrowers = self.borrower_repo.load_borrowers()
        if any(item.borrower_id == reader_id for item in borrowers):
            return False
        readers = self.reader_repo.load_readers()
        for reader in readers:
            if reader.reader_id == reader_id:
                readers.remove(reader)
                self.reader_repo.save_readers(readers)
                return True
        return False

    def get_reader_history(self, reader_id):
        reader_id = self.normalize_text(reader_id)
        active = [
            item
            for item in self.borrower_repo.load_borrowers()
            if item.borrower_id == reader_id
        ]
        history = [
            item
            for item in self.return_history_repo.load_history()
            if item.borrower_id == reader_id
        ]
        return active + history
