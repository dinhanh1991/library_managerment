class ReaderService:
    def __init__(self, service):
        self.service = service

    def get_all_readers(self):
        return self.service.reader_repo.load_readers()

    def add_reader(self, reader):
        if reader is None:
            return False
        reader_id = self.service._normalize_text(reader.reader_id)
        name = self.service._normalize_text(reader.name)
        if not reader_id or not name:
            return False
        readers = self.service.reader_repo.load_readers()
        if any(item.reader_id == reader_id for item in readers):
            return False
        reader.reader_id, reader.name = reader_id, name
        readers.append(reader)
        self.service.reader_repo.save_readers(readers)
        return True

    def update_reader(self, updated_reader):
        if updated_reader is None:
            return False
        reader_id = self.service._normalize_text(updated_reader.reader_id)
        name = self.service._normalize_text(updated_reader.name)
        if not reader_id or not name:
            return False
        readers = self.service.reader_repo.load_readers()
        for i, reader in enumerate(readers):
            if reader.reader_id == reader_id:
                updated_reader.reader_id, updated_reader.name = reader_id, name
                readers[i] = updated_reader
                self.service.reader_repo.save_readers(readers)

                borrowers = self.service.borrower_repo.load_borrowers()
                changed = False
                for borrower in borrowers:
                    if borrower.borrower_id == reader_id:
                        borrower.name = name
                        changed = True
                if changed:
                    self.service.borrower_repo.save_borrowers(borrowers)
                    for queued_borrower in self.service.borrow_queue.items:
                        if queued_borrower.borrower_id == reader_id:
                            queued_borrower.name = name
                    self.service.queue_repo.save_queue(self.service.borrow_queue.items)
                return True
        return False

    def remove_reader(self, reader_id):
        reader_id = self.service._normalize_text(reader_id)
        if not reader_id:
            return False
        borrowers = self.service.borrower_repo.load_borrowers()
        if any(item.borrower_id == reader_id for item in borrowers):
            return False
        readers = self.service.reader_repo.load_readers()
        for reader in readers:
            if reader.reader_id == reader_id:
                readers.remove(reader)
                self.service.reader_repo.save_readers(readers)
                return True
        return False

    def get_reader_history(self, reader_id):
        reader_id = self.service._normalize_text(reader_id)
        active = [
            item
            for item in self.service.borrower_repo.load_borrowers()
            if item.borrower_id == reader_id
        ]
        history = [
            item
            for item in self.service.return_history_repo.load_history()
            if item.borrower_id == reader_id
        ]
        return active + history
