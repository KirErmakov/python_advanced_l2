from pathlib import Path


def get_file_path(file_name: str) -> Path:
    project_root = Path(__file__).parent.parent.resolve()
    return project_root / file_name
