from datetime import date, timedelta

from LibraryManagement.models.reader import Reader


class LibraryService:

    def __init__(self):
        # Existing initialization remains unchanged.
        pass

    @staticmethod
    def _normalize_text(value):
        return str(value or "").strip()

    # Add book
    def add_book(self, book):
        if book is None:
            return False

        book_id = self._normalize_text(book.book_id)
        if not book_id:
            return False

        books = self.repository.load_books()
        for existing in books:
            if self._normalize_text(existing.book_id) == book_id:
                return False

        book.book_id = book_id
        books.append(book)

        self.repository.save_books(books)
        self._refresh_structures()
        return True

    # Remove book by ID
    def remove_book(self, book_id):
        book_id = self._normalize_text(book_id)
        if not book_id:
            return False

        books = self.repository.load_books()
        borrowers = self.borrower_repo.load_borrowers()

        if any(self._normalize_text(item.book_id) == book_id for item in borrowers):
            return False

        for book in books:
            if self._normalize_text(book.book_id) == book_id:
                books.remove(book)
                self.repository.save_books(books)
                self._refresh_structures()
                return True

        return False

    # Update book information
    def update_book(self, updated_book):
        if updated_book is None:
            return False
        if updated_book.quantity < 0 or updated_book.publish_year < 0:
            return False

        book_id = self._normalize_text(updated_book.book_id)
        if not book_id:
            return False
        updated_book.book_id = book_id

        books = self.repository.load_books()

        for i, book in enumerate(books):
            if self._normalize_text(book.book_id) == book_id:
                books[i] = updated_book
                self.repository.save_books(books)
                self._refresh_structures()
                return True

        return False

    # Search books by title
    def search_books_by_title(self, keyWork):
        keyword = self._normalize_text(keyWork).lower()
        if not keyword:
            return []

        books = self.repository.load_books()
        results = []

        for book in books:
            if keyword in str(book.title or "").lower():
                results.append(book)

        return results

    # Search books by author
    def search_books_by_author(self, author):
        keyword = self._normalize_text(author).lower()
        if not keyword:
            return []

        books = self.repository.load_books()
        results = []

        for book in books:
            if keyword in str(book.author or "").lower():
                results.append(book)

        return results

    # Advanced search
    def search_books_advanced(
        self,
        title=None,
        author=None,
        genre=None,
        publish_year=None,
        isbn=None,
        availability=None,
    ):
        books = self.repository.load_books()
        results = []

        normalized_title = (title or "").strip().lower()
        normalized_author = (author or "").strip().lower()
        normalized_genre = (genre or "").strip().lower()
        normalized_isbn = (isbn or "").strip().lower()

        try:
            normalized_year = int(publish_year) if publish_year not in (None, "") else None
        except (TypeError, ValueError):
            normalized_year = None

        normalized_availability = (availability or "all").strip().lower()

        for book in books:
            if normalized_title and normalized_title not in str(book.title).lower():
                continue
            if normalized_author and normalized_author not in str(book.author).lower():
                continue
            if normalized_genre and normalized_genre not in str(getattr(book, "category", "")).lower():
                continue
            if normalized_year is not None and book.publish_year != normalized_year:
                continue
            if normalized_isbn and normalized_isbn not in str(getattr(book, "isbn", "")).lower():
                continue

            if normalized_availability == "available" and book.quantity <= 0:
                continue
            if normalized_availability == "unavailable" and book.quantity > 0:
                continue

            results.append(book)

        return results
