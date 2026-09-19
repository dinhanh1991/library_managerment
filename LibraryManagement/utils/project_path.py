import sys
from pathlib import Path


def ensure_project_root_on_path():
    """Ensure the project root is available on sys.path for package imports."""
    project_parent = Path(__file__).resolve().parents[2]
    root_str = str(project_parent)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return project_parent
