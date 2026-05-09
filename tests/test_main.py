import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from agent import main
from agent.models import Element


def test_load_elements_returns_empty_dict_for_missing_file(tmp_path: Path) -> None:
  assert main.load_elements(tmp_path / "missing.yaml") == {}


def test_load_elements_rejects_non_mapping_yaml(tmp_path: Path) -> None:
  path = tmp_path / "elements.yaml"
  path.write_text("- tag: div\n", encoding="utf-8")

  with pytest.raises(ValueError, match="must contain a YAML mapping"):
    main.load_elements(path)


def test_save_element_appends_and_overwrites_by_name(tmp_path: Path) -> None:
  path = tmp_path / "elements.yaml"

  main.save_element(
    path,
    "title",
    Element(tag="h1", css_class="product-title"),
  )
  main.save_element(
    path,
    "price",
    Element(tag="span", css_class="price", other_attrs={"data-role": "price"}),
  )
  main.save_element(
    path,
    "title",
    Element(tag="h2", id="replacement-title"),
  )

  assert yaml.safe_load(path.read_text(encoding="utf-8")) == {
    "title": {
      "tag": "h2",
      "id": "replacement-title",
      "other_attrs": {},
    },
    "price": {
      "tag": "span",
      "class": "price",
      "other_attrs": {"data-role": "price"},
    },
  }


def test_prompt_accept_accepts_yes(monkeypatch: pytest.MonkeyPatch) -> None:
  monkeypatch.setattr("builtins.input", lambda _: "yes")

  assert main.prompt_accept() is True


def test_prompt_accept_rejects_blank(monkeypatch: pytest.MonkeyPatch) -> None:
  monkeypatch.setattr("builtins.input", lambda _: "")

  assert main.prompt_accept() is False


def test_prompt_required_retries_until_value(
  monkeypatch: pytest.MonkeyPatch,
  capsys: pytest.CaptureFixture[str],
) -> None:
  answers = iter(["", "product title"])
  monkeypatch.setattr("builtins.input", lambda _: next(answers))

  assert main.prompt_required("Prompt: ") == "product title"
  assert "Value is required." in capsys.readouterr().out


def test_run_cli_saves_accepted_agent_output(
  tmp_path: Path,
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  output_path = tmp_path / "elements.yaml"
  answers = iter(["product_title", "Find the product title on https://example.com", "y"])
  element = Element(tag="h1", css_class="product-title")

  async def fake_run(*_args: object, **_kwargs: object) -> SimpleNamespace:
    return SimpleNamespace(final_output=element)

  monkeypatch.setattr("builtins.input", lambda _: next(answers))
  monkeypatch.setattr(main.Runner, "run", fake_run)

  asyncio.run(main.run_cli(output_path))

  assert yaml.safe_load(output_path.read_text(encoding="utf-8")) == {
    "product_title": {
      "tag": "h1",
      "class": "product-title",
      "other_attrs": {},
    }
  }


def test_run_cli_skips_save_when_user_rejects(
  tmp_path: Path,
  monkeypatch: pytest.MonkeyPatch,
) -> None:
  output_path = tmp_path / "elements.yaml"
  answers = iter(["product_title", "Find the product title on https://example.com", "n"])

  async def fake_run(*_args: object, **_kwargs: object) -> SimpleNamespace:
    return SimpleNamespace(final_output=Element(tag="h1", css_class="product-title"))

  monkeypatch.setattr("builtins.input", lambda _: next(answers))
  monkeypatch.setattr(main.Runner, "run", fake_run)

  asyncio.run(main.run_cli(output_path))

  assert not output_path.exists()
