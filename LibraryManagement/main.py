from LibraryManagement.utils.project_path import ensure_project_root_on_path
from LibraryManagement.controllers.library_controller import LibraryController

ensure_project_root_on_path()


def main():
    # main chỉ khởi động ứng dụng; điều phối menu được giao cho Controller.
    controller = LibraryController()
    controller.run()


if __name__ == "__main__":
    main()
