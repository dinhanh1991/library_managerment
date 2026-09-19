import sys
from pathlib import Path

PROJECT_PARENT = Path(__file__).resolve().parents[1]
if str(PROJECT_PARENT) not in sys.path:
    sys.path.insert(0, str(PROJECT_PARENT))

from LibraryManagement.utils.project_path import ensure_project_root_on_path
from LibraryManagement.controllers.library_controller import LibraryController

ensure_project_root_on_path()


def main():
    # main chỉ khởi động ứng dụng; điều phối menu được giao cho Controller.
    controller = LibraryController()
    controller.run()


if __name__ == "__main__":
    main()
