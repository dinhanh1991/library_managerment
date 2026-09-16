import sys
from pathlib import Path

if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from LibraryManagement.controllers.library_controller import LibraryController


def main():
    # main chỉ khởi động ứng dụng; điều phối menu được giao cho Controller.
    controller = LibraryController()
    controller.run()


if __name__ == "__main__":
    main()
