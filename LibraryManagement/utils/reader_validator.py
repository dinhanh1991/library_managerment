from LibraryManagement.utils.validators import AppValidator


class ReaderValidator:
    """Rules validation dành cho độc giả."""

    @staticmethod
    def is_valid_reader_id(value):
        return AppValidator.is_valid_identifier(value)

    @staticmethod
    def is_valid_name(value):
        return AppValidator.is_valid_identifier(value)

    @staticmethod
    def is_valid_reader_payload(reader):
        return AppValidator.is_valid_reader_payload(reader)
