from pathlib import Path
from typing import Any, Union

import yaml
from pydantic import BaseModel

from agent.models import Elements, APIBlueprint

def load_patterns(path: Path) -> dict[str, Any]:
  """Loads the existing pattern repository from YAML."""
  if not path.exists():
    return {}

  with path.open("r", encoding="utf-8") as file:
    data = yaml.safe_load(file) or {}

  if not isinstance(data, dict):
    raise ValueError(f"{path} must contain a YAML mapping.")

  return data

def save_pattern(path: Path, name: str, output_data: Union[Elements, APIBlueprint]) -> None:
  """
  Saves a named pattern (either UI Elements or API Blueprints) 
  into the central YAML store.
  """
  store = load_patterns(path)
  
  # model_dump ensures we get the clean dict representation 
  # by_alias=True handles the 'class' -> 'css_class' mapping
  store[name] = output_data.model_dump(by_alias=True, exclude_none=True)

  with path.open("w", encoding="utf-8") as file:
    yaml.safe_dump(
      store,
      file,
      sort_keys=False,
      allow_unicode=True,
    )
