from pathlib import Path

import pytest
import yaml

from agent.models import Element, Elements
from agent.yaml_store import load_elements, save_elements


def test_load_elements_returns_empty_dict_for_missing_file(tmp_path: Path) -> None:
  assert load_elements(tmp_path / "missing.yaml") == {}


def test_load_elements_rejects_non_mapping_yaml(tmp_path: Path) -> None:
  path = tmp_path / "elements.yaml"
  path.write_text("- tag: div\n", encoding="utf-8")

  with pytest.raises(ValueError, match="must contain a YAML mapping"):
    load_elements(path)


def test_save_elements_appends_and_overwrites_by_name(tmp_path: Path) -> None:
  path = tmp_path / "elements.yaml"

  save_elements(
    path,
    "title",
    Elements(elements=[Element(tag="h1", css_class="product-title")]),
  )
  save_elements(
    path,
    "price",
    Elements(elements=[
      Element(tag="span", css_class="price", other_attrs={"data-role": "price"}),
      Element(tag="p", css_class="price_color"),
    ]),
  )
  save_elements(
    path,
    "title",
    Elements(elements=[Element(tag="h2", id="replacement-title")]),
  )

  assert yaml.safe_load(path.read_text(encoding="utf-8")) == {
    "title": {
      "elements": [
        {
          "tag": "h2",
          "id": "replacement-title",
          "other_attrs": {},
        }
      ],
    },
    "price": {
      "elements": [
        {
          "tag": "span",
          "class": "price",
          "other_attrs": {"data-role": "price"},
        },
        {
          "tag": "p",
          "class": "price_color",
          "other_attrs": {},
        },
      ],
    },
  }
