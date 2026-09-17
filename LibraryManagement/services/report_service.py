from collections import Counter
from datetime import date


class ReportService:
    """Calculate library statistics without handling console rendering."""

    def __init__(self, library_service):
        self.library_service = library_service

    def get_overview(self):
        books = self.library_service.get_all_books()
        borrowers = self.library_service.get_active_borrowers()
        overdue = self.library_service.get_overdue_borrowers()

        return {
            "total_books": len(books),
            "available_books": sum(1 for book in books if book.quantity > 0),
            "borrowed": sum(1 for item in borrowers if item.status == "borrowed"),
            "pending": sum(1 for item in borrowers if item.status == "pending"),
            "overdue": len(overdue),
            "total_readers": len(self.library_service.get_all_readers()),
        }

    def get_book_statistics(self):
        books = self.library_service.get_all_books()
        total_quantity = sum(book.quantity for book in books)
        available_quantity = sum(book.quantity for book in books if book.quantity > 0)

        return {
            "total_titles": len(books),
            "total_quantity": total_quantity,
            "available_quantity": available_quantity,
            "out_of_stock": sum(1 for book in books if book.quantity == 0),
        }

    def get_borrow_statistics(self):
        borrowers = self.library_service.get_active_borrowers()
        history = self.library_service.get_return_history()

        return {
            "borrowed": sum(1 for item in borrowers if item.status == "borrowed"),
            "pending": sum(1 for item in borrowers if item.status == "pending"),
            "overdue": len(self.library_service.get_overdue_borrowers()),
            "returned": len(history),
        }

    def get_category_statistics(self):
        books = self.library_service.get_all_books()
        borrowers = self.library_service.get_active_borrowers()
        books_by_id = {book.book_id: book for book in books}
        counts = Counter()

        for borrower in borrowers:
            if borrower.status not in {"borrowed", "pending"}:
                continue
            book = books_by_id.get(borrower.book_id)
            category = getattr(book, "category", "") or "Chưa phân loại"
            counts[category] += 1

        return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))

    def get_overdue_borrowers(self, current_date=None):
        current_date = current_date or date.today()
        overdue = self.library_service.get_overdue_borrowers(current_date)
        result = []

        for borrower in overdue:
            try:
                due_date = date.fromisoformat(borrower.due_date)
                overdue_days = (current_date - due_date).days
            except (TypeError, ValueError):
                overdue_days = 0

            result.append({
                "borrower_id": borrower.borrower_id,
                "name": borrower.name,
                "book_id": borrower.book_id,
                "due_date": borrower.due_date,
                "overdue_days": overdue_days,
            })

        return sorted(result, key=lambda item: (-item["overdue_days"], item["borrower_id"]))

    def get_most_borrowed_books(self):
        borrowers = self.library_service.get_active_borrowers()
        history = self.library_service.get_return_history()
        counts = Counter()

        for item in borrowers:
            if item.status in {"borrowed", "pending"}:
                counts[item.book_id] += 1

        for item in history:
            counts[item.book_id] += 1

        books = {book.book_id: book for book in self.library_service.get_all_books()}
        result = []

        for book_id, count in counts.most_common():
            book = books.get(book_id)
            result.append({
                "book_id": book_id,
                "title": getattr(book, "title", "Không xác định"),
                "borrow_count": count,
            })

        return result

    def get_most_active_readers(self):
        borrowers = self.library_service.get_active_borrowers()
        history = self.library_service.get_return_history()
        counts = Counter()
        names = {}

        for item in borrowers:
            counts[item.borrower_id] += 1
            names[item.borrower_id] = item.name

        for item in history:
            counts[item.borrower_id] += 1
            names[item.borrower_id] = item.name

        return [
            {
                "borrower_id": borrower_id,
                "name": names.get(borrower_id, "Không xác định"),
                "borrow_count": count,
            }
            for borrower_id, count in counts.most_common()
        ]
