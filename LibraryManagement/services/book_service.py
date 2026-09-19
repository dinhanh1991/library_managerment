from LibraryManagement.utils.book_validator import BookValidator


class BookService:
    def __init__(self, repository, borrower_repo, normalize_text, validate_number, refresh_structures):
        self.repository = repository
        self.borrower_repo = borrower_repo
        self.normalize_text = normalize_text
        self.validate_number = validate_number
        self.refresh_structures = refresh_structures

    def get_all_books(self):
        return self.repository.load_books()

    @staticmethod
    def _is_valid_text(value):
        return BookValidator.is_valid_title(value)

    def add_book(self, book):
        if book is None:
            return False
        if not self._is_valid_text(book.book_id):
            return False
        if not self._is_valid_text(book.title):
            return False
        if not self._is_valid_text(book.author):
            return False
        if (
            not self.validate_number(book.quantity)
            or not self.validate_number(book.publish_year)
        ):
            return False

        book_id = book.book_id.strip()
        books = self.repository.load_books()
        for existing in books:
            if self.normalize_text(existing.book_id) == book_id:
                return False

        book.book_id = book_id
        book.title = book.title.strip()
        book.author = book.author.strip()
        books.append(book)
        self.repository.save_books(books)
        self.refresh_structures()
        return True

    def remove_book(self, book_id):
        book_id = self.normalize_text(book_id)
        if not book_id:
            return False
        books = self.repository.load_books()
        borrowers = self.borrower_repo.load_borrowers()
        if any(self.normalize_text(item.book_id) == book_id for item in borrowers):
            return False
        for book in books:
            if self.normalize_text(book.book_id) == book_id:
                books.remove(book)
                self.repository.save_books(books)
                self.refresh_structures()
                return True
        return False

    def update_book(self, updated_book):
        if updated_book is None:
            return False
        if not self._is_valid_text(updated_book.book_id):
            return False
        if not self._is_valid_text(updated_book.title):
            return False
        if not self._is_valid_text(updated_book.author):
            return False
        if (
            not self.validate_number(updated_book.quantity)
            or not self.validate_number(updated_book.publish_year)
        ):
            return False

        book_id = updated_book.book_id.strip()
        updated_book.book_id = book_id
        updated_book.title = updated_book.title.strip()
        updated_book.author = updated_book.author.strip()
        books = self.repository.load_books()
        borrowers = self.borrower_repo.load_borrowers()
        if any(self.normalize_text(item.book_id) == book_id for item in borrowers):
            return False
        for i, book in enumerate(books):
            if self.normalize_text(book.book_id) == book_id:
                books[i] = updated_book
                self.repository.save_books(books)
                self.refresh_structures()
                return True
        return False

    def search_books_by_title(self, keyword):
        key_word = self.normalize_text(keyword).lower()
        if not key_word:
            return []
        books = self.repository.load_books()
        return [book for book in books if key_word in str(book.title or "").lower()]

    def search_books_by_author(self, author):
        keyword = self.normalize_text(author).lower()
        if not keyword:
            return []
        books = self.repository.load_books()
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
        books = self.repository.load_books()
        results = []

        text_filters = {
            "title": title,
            "author": author,
            "genre": genre,
            "isbn": isbn,
        }
        normalized_filters = {}
        for field, value in text_filters.items():
            if value is None:
                normalized_filters[field] = ""
            elif not isinstance(value, str):
                return []
            else:
                normalized_filters[field] = value.strip().lower()

        try:
            normalized_year = int(publish_year) if publish_year not in (None, "") else None
        except (TypeError, ValueError):
            return []
        if normalized_year is not None and normalized_year < 0:
            return []

        if availability is None:
            normalized_availability = "all"
        elif not isinstance(availability, str):
            return []
        else:
            normalized_availability = availability.strip().lower()

        if normalized_availability not in {"all", "available", "unavailable"}:
            return []

        for book in books:
            if normalized_filters["title"] and normalized_filters["title"] not in str(book.title or "").lower():
                continue
            if normalized_filters["author"] and normalized_filters["author"] not in str(book.author or "").lower():
                continue
            if normalized_filters["genre"] and normalized_filters["genre"] not in str(getattr(book, "category", "") or "").lower():
                continue
            if normalized_year is not None and book.publish_year != normalized_year:
                continue
            if normalized_filters["isbn"] and normalized_filters["isbn"] not in str(getattr(book, "isbn", "") or "").lower():
                continue
            if normalized_availability == "available" and book.quantity <= 0:
                continue
            if normalized_availability == "unavailable" and book.quantity > 0:
                continue
            results.append(book)
        return results
