from LibraryManagement.controllers.base_controller import BaseController
from LibraryManagement.views.borrow_view import BorrowView


class BorrowController(BaseController):
    """Điều phối menu quản lý mượn sách."""

    def __init__(self, service, view=None):
        super().__init__(view or BorrowView(service))

    def get_actions(self):
        return {
            "1": self.view.borrow_book,
            "2": self.view.display_queue,
            "3": self.view.process_next_borrower,
        }
