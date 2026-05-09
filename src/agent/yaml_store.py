from pathlib import Path
from typing import Any

import yaml

from agent.models import Elements


def load_elements(path: Path) -> dict[str, Any]:
  if not path.exists():
    return {}

  with path.open("r", encoding="utf-8") as file:
    data = yaml.safe_load(file) or {}

  if not isinstance(data, dict):
    raise ValueError(f"{path} must contain a YAML mapping.")

  return data


def save_elements(path: Path, name: str, elements_output: Elements) -> None:
  elements = load_elements(path)
  elements[name] = elements_output.model_dump(by_alias=True, exclude_none=True)

  with path.open("w", encoding="utf-8") as file:
    yaml.safe_dump(
      elements,
      file,
      sort_keys=False,
      allow_unicode=True,
    )
