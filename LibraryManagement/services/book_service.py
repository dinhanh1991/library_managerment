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

    def get_book_by_id(self, book_id):
        normalized_id = self.normalize_text(book_id)
        if not normalized_id:
            return None
        for book in self.repository.load_books():
            if self.normalize_text(book.book_id) == normalized_id:
                return book
        return None

    @staticmethod
    def _validate_book(book):
        if book is None:
            return False
        return (
            BookValidator.is_valid_book_id(book.book_id)
            and BookValidator.is_valid_title(book.title)
            and BookValidator.is_valid_author(book.author)
            and BookValidator.is_valid_quantity(book.quantity)
            and BookValidator.is_valid_publish_year(book.publish_year)
        )

    def _normalize_book(self, book):
        book.book_id = self.normalize_text(book.book_id)
        book.title = self.normalize_text(book.title)
        book.author = self.normalize_text(book.author)
        return book

    def add_book(self, book):
        if not self._validate_book(book):
            return False
        books = self.repository.load_books()
        if any(self.normalize_text(existing.book_id) == self.normalize_text(book.book_id) for existing in books):
            return False
        self._normalize_book(book)
        books.append(book)
        self.repository.save_books(books)
        self.refresh_structures()
        return True

    def remove_book(self, book_id):
        book_id = self.normalize_text(book_id)
        if not book_id:
            return "not_found"
        books = self.repository.load_books()
        borrowers = self.borrower_repo.load_borrowers()
        if not any(self.normalize_text(book.book_id) == book_id for book in books):
            return "not_found"
        if any(self.normalize_text(item.book_id) == book_id for item in borrowers):
            return "borrowed"
        for book in books:
            if self.normalize_text(book.book_id) == book_id:
                books.remove(book)
                self.repository.save_books(books)
                self.refresh_structures()
                return "deleted"
        return "not_found"

    def update_book(self, updated_book):
        if not self._validate_book(updated_book):
            return False
        book_id = self.normalize_text(updated_book.book_id)
        books = self.repository.load_books()
        borrowers = self.borrower_repo.load_borrowers()
        if any(self.normalize_text(item.book_id) == book_id for item in borrowers):
            return False
        for i, book in enumerate(books):
            if self.normalize_text(book.book_id) == book_id:
                books[i] = self._normalize_book(updated_book)
                self.repository.save_books(books)
                self.refresh_structures()
                return True
        return False

    def search_books_by_title(self, keyword):
        key_word = self.normalize_text(keyword).lower()
        if not key_word:
            return []
        return [book for book in self.repository.load_books() if key_word in str(book.title or "").lower()]

    def search_books_by_author(self, author):
        keyword = self.normalize_text(author).lower()
        if not keyword:
            return []
        return [book for book in self.repository.load_books() if keyword in str(book.author or "").lower()]

    def search_books_advanced(self, title=None, author=None, genre=None, publish_year=None, isbn=None, availability=None):
        books = self.repository.load_books()
        text_filters = {"title": title, "author": author, "genre": genre, "isbn": isbn}
        normalized_filters = {}
        for field, value in text_filters.items():
            if value is None:
                normalized_filters[field] = ""
            elif isinstance(value, str):
                normalized_filters[field] = value.strip().lower()
            else:
                return []

        if publish_year in (None, ""):
            normalized_year = None
        elif BookValidator.is_valid_publish_year(publish_year):
            normalized_year = publish_year
        else:
            return []

        if availability is None:
            normalized_availability = "all"
        elif isinstance(availability, str):
            normalized_availability = availability.strip().lower()
        else:
            return []

        if normalized_availability not in {"all", "available", "unavailable"}:
            return []

        results = []
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
            if normalized_availability == "available" and not book.is_available():
                continue
            if normalized_availability == "unavailable" and book.is_available():
                continue
            results.append(book)
        return results
