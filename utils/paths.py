from pathlib import Path
import sys

def get_proj_root(current_dir=None) -> Path:
    if current_dir is None:
        current_dir = Path.cwd()

    while not (current_dir / "pyproject.toml").exists():
        current_dir = current_dir.parent

        if current_dir == Path.home():
            # Fallback
            return Path(__file__).resolve().parent.parent.parent
        
def get_module_path(module_name: str) -> Path:
    return Path(sys.modules[module_name].__file__).resolve()
