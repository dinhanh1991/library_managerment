class AppValidator:
    """Shared validation rules used across models, services, and views."""

    @staticmethod
    def is_non_empty_text(value):
        return isinstance(value, str) and bool(value.strip())

    @staticmethod
    def is_valid_identifier(value):
        return AppValidator.is_non_empty_text(value)

    @staticmethod
    def is_non_negative_int(value):
        return isinstance(value, int) and not isinstance(value, bool) and value >= 0

    @staticmethod
    def normalize_text(value):
        if not isinstance(value, str):
            return ""
        return value.strip()

    @staticmethod
    def is_valid_borrower_payload(borrower):
        if borrower is None:
            return False
        return (
            AppValidator.is_valid_identifier(getattr(borrower, "borrower_id", None))
            and AppValidator.is_valid_identifier(getattr(borrower, "name", None))
            and AppValidator.is_valid_identifier(getattr(borrower, "book_id", None))
        )

    @staticmethod
    def is_valid_return_payload(borrower):
        if borrower is None:
            return False
        return (
            AppValidator.is_valid_identifier(getattr(borrower, "borrower_id", None))
            and AppValidator.is_valid_identifier(getattr(borrower, "book_id", None))
        )

    @staticmethod
    def is_valid_reader_payload(reader):
        if reader is None:
            return False
        return (
            AppValidator.is_valid_identifier(getattr(reader, "reader_id", None))
            and AppValidator.is_valid_identifier(getattr(reader, "name", None))
        )
