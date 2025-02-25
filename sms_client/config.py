import tomli
from typing import Dict, Any


def load_config(config_path: str) -> Dict[str, Any]:
    """Загружает конфигурацию из TOML-файла."""
    with open(config_path, "rb") as f:
        return tomli.load(f)
