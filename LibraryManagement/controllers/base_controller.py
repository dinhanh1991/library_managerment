class BaseController:
    """Base controller for feature menus.

    Each concrete controller defines the menu actions it owns, while the base class
    ensures the interaction pattern is consistent across the application.
    """

    def __init__(self, view):
        self.view = view

    def get_actions(self):
        raise NotImplementedError

    def dispatch_choice(self, choice, actions):
        """Exit if user requests to leave the menu; otherwise invoke the mapped action."""
        if choice == "0":
            return False

        action = actions.get(choice)
        if action is None:
            self.view.invalid_choice()
            return True

        action()
        return True

    def run(self):
        self.view.run_menu(self.view.show_menu, self.get_actions())
