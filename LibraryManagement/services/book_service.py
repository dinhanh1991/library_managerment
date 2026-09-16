class BookService:
    def __init__(self, service):
        self.service = service

    def get_all_books(self):
        return self.service.repository.load_books()

    def add_book(self, book):
        if book is None:
            return False
        book_id = self.service._normalize_text(book.book_id)
        if (
            not book_id
            or not self.service._is_valid_non_negative_number(book.quantity)
            or not self.service._is_valid_non_negative_number(book.publish_year)
        ):
            return False
        books = self.service.repository.load_books()
        for existing in books:
            if self.service._normalize_text(existing.book_id) == book_id:
                return False
        book.book_id = book_id
        books.append(book)
        self.service.repository.save_books(books)
        self.service._refresh_structures()
        return True

    def remove_book(self, book_id):
        book_id = self.service._normalize_text(book_id)
        if not book_id:
            return False
        books = self.service.repository.load_books()
        borrowers = self.service.borrower_repo.load_borrowers()
        if any(self.service._normalize_text(item.book_id) == book_id for item in borrowers):
            return False
        for book in books:
            if self.service._normalize_text(book.book_id) == book_id:
                books.remove(book)
                self.service.repository.save_books(books)
                self.service._refresh_structures()
                return True
        return False

    def update_book(self, updated_book):
        if (
            updated_book is None
            or not self.service._is_valid_non_negative_number(updated_book.quantity)
            or not self.service._is_valid_non_negative_number(updated_book.publish_year)
        ):
            return False
        book_id = self.service._normalize_text(updated_book.book_id)
        if not book_id:
            return False
        updated_book.book_id = book_id
        books = self.service.repository.load_books()
        borrowers = self.service.borrower_repo.load_borrowers()
        if any(self.service._normalize_text(item.book_id) == book_id for item in borrowers):
            return False
        for i, book in enumerate(books):
            if self.service._normalize_text(book.book_id) == book_id:
                books[i] = updated_book
                self.service.repository.save_books(books)
                self.service._refresh_structures()
                return True
        return False

    def search_books_by_title(self, key_work):
        keyword = self.service._normalize_text(key_work).lower()
        if not keyword:
            return []
        books = self.service.repository.load_books()
        return [book for book in books if keyword in str(book.title or "").lower()]

    def search_books_by_author(self, author):
        keyword = self.service._normalize_text(author).lower()
        if not keyword:
            return []
        books = self.service.repository.load_books()
        return [book for book in books if keyword in str(book.author or "").lower()]

    def search_books_advanced(
        self,
        title=None,
        author=None,
        genre=None,
        publish_year=None,
        isbn=None,
        availability=None,
    ):
        books = self.service.repository.load_books()
        results = []
        normalized_title = (title or "").strip().lower()
        normalized_author = (author or "").strip().lower()
        normalized_genre = (genre or "").strip().lower()
        normalized_isbn = (isbn or "").strip().lower()
        try:
            normalized_year = int(publish_year) if publish_year not in (None, "") else None
        except (TypeError, ValueError):
            return []
        if normalized_year is not None and normalized_year < 0:
            return []
        normalized_availability = (availability or "all").strip().lower()
        if normalized_availability not in {"all", "available", "unavailable"}:
            return []
        for book in books:
            if normalized_title and normalized_title not in str(book.title or "").lower():
                continue
            if normalized_author and normalized_author not in str(book.author or "").lower():
                continue
            if normalized_genre and normalized_genre not in str(getattr(book, "category", "") or "").lower():
                continue
            if normalized_year is not None and book.publish_year != normalized_year:
                continue
            if normalized_isbn and normalized_isbn not in str(getattr(book, "isbn", "") or "").lower():
                continue
            if normalized_availability == "available" and book.quantity <= 0:
                continue
            if normalized_availability == "unavailable" and book.quantity > 0:
                continue
            results.append(book)
        return results
