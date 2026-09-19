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
    def normalize_identifier(value, field_name="identifier"):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} phải là chuỗi.")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{field_name} không được để trống.")
        return normalized

    @staticmethod
    def normalize_optional_text(value, field_name="text"):
        if value is None:
            return ""
        if not isinstance(value, str):
            raise ValueError(f"{field_name} phải là chuỗi hoặc rỗng.")
        return value.strip()

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
