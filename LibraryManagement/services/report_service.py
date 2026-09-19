from collections import Counter
from datetime import date, timedelta


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

    def get_dashboard_stats(self):
        books = self.library_service.get_all_books()
        borrowers = self.library_service.get_active_borrowers()
        overdue = self.library_service.get_overdue_borrowers()
        book_by_id = {book.book_id: book for book in books}
        categories = Counter()

        for borrower in borrowers:
            if borrower.status != "borrowed":
                continue
            book = book_by_id.get(borrower.book_id)
            category = getattr(book, "category", "") or "Chưa phân loại"
            categories[category] += 1

        return {
            "total_books": len(books),
            "total_available": sum(1 for book in books if book.quantity > 0),
            "current_borrowed": sum(
                1 for borrower in borrowers if borrower.status == "borrowed"
            ),
            "overdue_count": len(overdue),
            "category_counts": dict(
                sorted(categories.items(), key=lambda item: item[1], reverse=True)
            ),
        }

    def get_time_window_stats(self, days=30, as_of=None):
        as_of = as_of or date.today()
        active_borrowers = self.library_service.get_active_borrowers()
        returned_borrowers = self.library_service.get_return_history()
        books = {book.book_id: book for book in self.library_service.get_all_books()}

        active_window = []
        returned_window = []
        window = timedelta(days=days)

        for borrower in active_borrowers:
            if not borrower.borrow_date:
                continue
            try:
                borrow_date = date.fromisoformat(borrower.borrow_date)
            except (TypeError, ValueError):
                continue

            days_since_borrow = as_of - borrow_date
            if timedelta(0) <= days_since_borrow <= window:
                active_window.append(borrower)

        for borrower in returned_borrowers:
            if not borrower.return_date:
                continue
            try:
                return_date = date.fromisoformat(borrower.return_date)
            except (TypeError, ValueError):
                continue

            days_since_return = as_of - return_date
            if timedelta(0) <= days_since_return <= window:
                returned_window.append(borrower)

        category_summary = Counter()
        reader_summary = Counter()
        status_summary = {
            "borrowed": 0,
            "pending": 0,
            "overdue": 0,
            "returned": 0,
        }
        overdue_ids = {
            borrower.borrower_id
            for borrower in self.library_service.get_overdue_borrowers(as_of)
        }

        for borrower in active_window:
            status = borrower.status

            if status in {"borrowed", "pending"}:
                status_summary[status] += 1

            if (
                status in {"borrowed", "pending"}
                and borrower.borrower_id in overdue_ids
            ):
                status_summary["overdue"] += 1

            book = books.get(borrower.book_id)
            category = getattr(book, "category", "") or "Chưa phân loại"
            category_summary[category] += 1
            reader_summary[borrower.name] += 1

        for borrower in returned_window:
            status_summary["returned"] += 1

            book = books.get(borrower.book_id)
            category = getattr(book, "category", "") or "Chưa phân loại"
            category_summary[category] += 1
            reader_summary[borrower.name] += 1

        return {
            "days": days,
            "total_active": len(active_window),
            "reader_summary": dict(
                sorted(reader_summary.items(), key=lambda item: item[1], reverse=True)
            ),
            "category_summary": dict(
                sorted(category_summary.items(), key=lambda item: item[1], reverse=True)
            ),
            "status_summary": dict(
                sorted(
                    status_summary.items(),
                    key=lambda item: (item[0] != "borrowed", -item[1]),
                )
            ),
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

        # Sắp xếp theo lượt mượn giảm dần, sau đó theo mã sách tăng dần.
        for book_id, count in sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0]),
        ):
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
