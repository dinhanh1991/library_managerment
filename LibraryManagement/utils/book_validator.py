from LibraryManagement.utils.validators import AppValidator


class BookValidator:
    """Rules validation dành cho sách."""

    @staticmethod
    def is_valid_book_id(value):
        return AppValidator.is_valid_identifier(value)

    @staticmethod
    def is_valid_title(value):
        return AppValidator.is_valid_identifier(value)

    @staticmethod
    def is_valid_author(value):
        return AppValidator.is_valid_identifier(value)

    @staticmethod
    def is_valid_quantity(value):
        return AppValidator.is_non_negative_int(value)

    @staticmethod
    def is_valid_publish_year(value):
        return AppValidator.is_non_negative_int(value)
