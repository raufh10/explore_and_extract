import asyncio
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from agent import main
from agent.models import Element


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
