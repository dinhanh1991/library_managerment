from LibraryManagement.services.library_service import LibraryService
from LibraryManagement.views.library_view import LibraryView
from LibraryManagement.controllers.book_controller import BookController
from LibraryManagement.controllers.borrow_controller import BorrowController
from LibraryManagement.controllers.reader_controller import ReaderController


class LibraryController:
    """Coordinate application flow without owning console rendering details."""

    def __init__(self, service=None, view=None):
        # Có thể truyền service/view từ bên ngoài để test hoặc thay thế implementation.
        self.service = service or LibraryService()
        self.view = view or LibraryView(self.service)

        # Controller cấp cao giữ các controller chức năng và dùng chung service/view.
        self.book_controller = BookController(self.service, self.view.book_view)
        self.borrow_controller = BorrowController(self.service, self.view.borrow_view)
        self.reader_controller = ReaderController(self.service, self.view.reader_view)

    def get_actions(self):
        # Mỗi phím menu ánh xạ tới một hàm xử lý; không cần if/elif dài trong run().
        return {
            "1": self.book_controller.run,
            "2": self.borrow_controller.run,
            "3": self.view.return_view.run,
            "4": self.view.search_view.run,
            "5": self.view.bst_view.run,
            "6": self.view.linked_list_view.run,
            "7": self.view.sort_view.run,
            "8": self.reader_controller.run,
            "9": self.view.report_view.run,
        }

    def run(self):
        # View chịu trách nhiệm hiển thị; Controller điều phối thứ tự chạy.
        self.view.show_welcome_banner()
        self.view.show_dashboard()
        self.view.run_menu(self.view.show_menu, self.get_actions())
        self.view.console.print(
            "\n[bold green]👋 Cảm ơn bạn đã sử dụng hệ thống![/bold green]"
        )
