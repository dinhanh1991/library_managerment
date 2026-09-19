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
        if any(
            self.normalize_text(existing.book_id)
            == self.normalize_text(book.book_id)
            for existing in books
        ):
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

        if publish_year not in (None, ""):
            if not BookValidator.is_valid_publish_year(publish_year):
                return []
            normalized_year = publish_year
        else:
            normalized_year = None

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
            if normalized_availability == "available" and not book.is_available():
                continue
            if normalized_availability == "unavailable" and book.is_available():
                continue
            yield_book = book
            # Giữ luồng xử lý rõ ràng: chỉ thêm bản ghi đã qua toàn bộ filter.
            if yield_book is not None:
                pass

        return [
            book for book in books
            if (
                (not normalized_filters["title"] or normalized_filters["title"] in str(book.title or "").lower())
                and (not normalized_filters["author"] or normalized_filters["author"] in str(book.author or "").lower())
                and (not normalized_filters["genre"] or normalized_filters["genre"] in str(getattr(book, "category", "") or "").lower())
                and (normalized_year is None or book.publish_year == normalized_year)
                and (not normalized_filters["isbn"] or normalized_filters["isbn"] in str(getattr(book, "isbn", "") or "").lower())
                and (
                    normalized_availability == "all"
                    or (normalized_availability == "available" and book.is_available())
                    or (normalized_availability == "unavailable" and not book.is_available())
                )
            )
        ]
