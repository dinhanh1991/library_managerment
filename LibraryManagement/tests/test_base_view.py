import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from LibraryManagement.views.base_view import BaseView


class BaseViewMenuTestCase(unittest.TestCase):
    def setUp(self):
        self.view = BaseView(Mock())

    def test_run_menu_exits_when_user_enters_zero(self):
        self.view.prompt_choice = Mock(return_value="0")
        show_menu = Mock()
        actions = {"1": Mock()}

        self.view.run_menu(show_menu, actions)

        show_menu.assert_called_once_with()
        actions["1"].assert_not_called()

    def test_run_menu_executes_selected_action(self):
        self.view.prompt_choice = Mock(side_effect=["1", "0"])
        show_menu = Mock()
        action = Mock()

        self.view.run_menu(show_menu, {"1": action})

        action.assert_called_once_with()
        self.assertEqual(show_menu.call_count, 2)

    def test_run_menu_rejects_invalid_choice_and_continues(self):
        self.view.prompt_choice = Mock(side_effect=["99", "0"])
        self.view.invalid_choice = Mock()
        show_menu = Mock()
        action = Mock()

        self.view.run_menu(show_menu, {"1": action})

        self.view.invalid_choice.assert_called_once_with()
        action.assert_not_called()
        self.assertEqual(show_menu.call_count, 2)

    def test_run_menu_does_not_require_zero_in_actions(self):
        self.view.prompt_choice = Mock(return_value="0")
        action = Mock()

        self.view.run_menu(Mock(), {"1": action})

        action.assert_not_called()


if __name__ == "__main__":
    unittest.main()
