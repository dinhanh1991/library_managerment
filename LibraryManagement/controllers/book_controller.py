from LibraryManagement.controllers.base_controller import BaseController
from LibraryManagement.views.book_view import BookView


class BookController(BaseController):
    """Điều phối menu quản lý sách."""

    def __init__(self, service, view=None):
        super().__init__(view or BookView(service))

    def get_actions(self):
        return {
            "1": self.view.add_book,
            "2": self.view.delete_book,
            "3": self.view.update_book,
            "4": self.view.display_books,
            "5": self.view.search_by_title,
            "6": self.view.search_by_author,
            "7": self.view.search_advanced,
        }
