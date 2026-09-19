class BaseController:
    """Base controller cho các menu con."""

    def __init__(self, view):
        self.view = view

    def get_actions(self):
        raise NotImplementedError

    def run(self):
        self.view.run_menu(self.view.show_menu, self.get_actions())
