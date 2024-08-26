from pathlib import Path

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent.parent.parent
)  # relative to Configuration Manager

CONFIG_FILE_PATH = PROJECT_ROOT / "config" / "config.yml"
