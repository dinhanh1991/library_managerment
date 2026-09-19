from LibraryManagement.utils.project_path import ensure_project_root_on_path

ensure_project_root_on_path()

from LibraryManagement.controllers.library_controller import LibraryController


def bootstrap_application():
    """Configure import paths and return the project root for the application entrypoint."""
    return ensure_project_root_on_path()


def main():
    """Entry point for the library management application."""
    bootstrap_application()
    controller = LibraryController()
    controller.run()


if __name__ == "__main__":
    main()
