from LibraryManagement.utils.validators import AppValidator


class ReturnValidator:
    """Rules validation dành cho giao dịch trả sách."""

    @staticmethod
    def is_valid_return_payload(borrower):
        return AppValidator.is_valid_return_payload(borrower)
