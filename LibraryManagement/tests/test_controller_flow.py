import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.controllers.book_controller import BookController
from LibraryManagement.controllers.borrow_controller import BorrowController
from LibraryManagement.controllers.reader_controller import ReaderController


class ControllerFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.service = Mock()

    def test_book_controller_maps_menu_to_view_actions(self):
        view = Mock()
        controller = BookController(self.service, view)

        actions = controller.get_actions()

        self.assertIs(actions["1"], view.add_book)
        self.assertIs(actions["2"], view.delete_book)
        self.assertIs(actions["3"], view.update_book)
        self.assertIs(actions["4"], view.display_books)
        self.assertIs(actions["5"], view.search_by_title)
        self.assertIs(actions["6"], view.search_by_author)
        self.assertIs(actions["7"], view.search_advanced)

    def test_borrow_controller_maps_menu_to_view_actions(self):
        view = Mock()
        controller = BorrowController(self.service, view)

        actions = controller.get_actions()

        self.assertIs(actions["1"], view.borrow_book)
        self.assertIs(actions["2"], view.display_queue)
        self.assertIs(actions["3"], view.process_next_borrower)

    def test_reader_controller_maps_menu_to_view_actions(self):
        view = Mock()
        controller = ReaderController(self.service, view)

        actions = controller.get_actions()

        self.assertIs(actions["1"], view.add_reader)
        self.assertIs(actions["2"], view.update_reader)
        self.assertIs(actions["3"], view.delete_reader)
        self.assertIs(actions["4"], view.display_readers)
        self.assertIs(actions["5"], view.display_history)
        self.assertIs(actions["6"], view.display_overdue)

    def test_controller_run_delegates_to_view_menu(self):
        view = Mock()
        controller = BookController(self.service, view)

        controller.run()

        view.run_menu.assert_called_once_with(
            view.show_menu,
            controller.get_actions(),
        )


if __name__ == "__main__":
    unittest.main()
