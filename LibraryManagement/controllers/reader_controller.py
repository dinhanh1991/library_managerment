from LibraryManagement.controllers.base_controller import BaseController
from LibraryManagement.views.reader_view import ReaderView


class ReaderController(BaseController):
    """Điều phối menu quản lý độc giả."""

    def __init__(self, service, view=None):
        super().__init__(view or ReaderView(service))

    def get_actions(self):
        return {
            "1": self.view.add_reader,
            "2": self.view.update_reader,
            "3": self.view.delete_reader,
            "4": self.view.display_readers,
            "5": self.view.display_history,
            "6": self.view.display_overdue,
        }
