from LibraryManagement.views.borrow_view import BorrowView


class BorrowController:
    """Coordinate borrowing workflows and delegate presentation to BorrowView."""

    def __init__(self, service, view=None):
        # Dùng cùng service với các chức năng khác để dữ liệu luôn nhất quán.
        self.view = view or BorrowView(service)

    def get_actions(self):
        # Ánh xạ lựa chọn menu mượn sách tới phương thức tương ứng của view.
        return {
            "1": self.view.borrow_book,
            "2": self.view.display_queue,
            "3": self.view.process_next_borrower,
        }

    def run(self):
        # Controller điều phối vòng lặp; BorrowView chịu trách nhiệm giao diện.
        self.view.run_menu(self.view.show_menu, self.get_actions())
