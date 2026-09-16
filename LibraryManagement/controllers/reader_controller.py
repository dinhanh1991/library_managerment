from LibraryManagement.views.reader_view import ReaderView


class ReaderController:
    """Coordinate reader-management workflows and delegate presentation to ReaderView."""

    def __init__(self, service, view=None):
        # Có thể truyền mock/view thay thế khi kiểm thử mà không đổi controller.
        self.view = view or ReaderView(service)

    def get_actions(self):
        # Tách bảng ánh xạ menu khỏi phần hiển thị và xử lý vòng lặp.
        return {
            "1": self.view.add_reader,
            "2": self.view.update_reader,
            "3": self.view.delete_reader,
            "4": self.view.display_readers,
            "5": self.view.display_history,
            "6": self.view.display_overdue,
        }

    def run(self):
        # ReaderView tập trung vào prompt, bảng Rich và thông báo cho người dùng.
        self.view.run_menu(self.view.show_menu, self.get_actions())
