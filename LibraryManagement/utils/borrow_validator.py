from LibraryManagement.utils.validators import AppValidator


class BorrowValidator:
    """Rules validation dành cho giao dịch mượn sách."""

    @staticmethod
    def is_valid_borrow_payload(borrower):
        return AppValidator.is_valid_borrower_payload(borrower)
