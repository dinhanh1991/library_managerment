from LibraryManagement.views.book_view import BookView


class BookController:
    """Coordinate the book-management menu and delegate presentation to BookView."""

    def __init__(self, service, view=None):
        # Nhận dependency từ LibraryController thay vì tự tạo service mới.
        self.view = view or BookView(service)

    def get_actions(self):
        # Controller xử lý điều hướng; các thao tác nhập/xuất vẫn nằm trong BookView.
        return {
            "1": self.view.add_book,
            "2": self.view.delete_book,
            "3": self.view.update_book,
            "4": self.view.display_books,
            "5": self.view.search_by_title,
            "6": self.view.search_by_author,
            "7": self.view.search_advanced,
        }

    def run(self):
        # Tái sử dụng vòng lặp menu chung của BaseView.
        self.view.run_menu(self.view.show_menu, self.get_actions())
