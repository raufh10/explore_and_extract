import argparse
import asyncio
from pathlib import Path
from typing import Any

import yaml
from agents import InputGuardrailTripwireTriggered, Runner
from dotenv import load_dotenv

from agent.core import main_agent
from agent.models import Element


DEFAULT_OUTPUT_PATH = Path("elements.yaml")


def load_elements(path: Path) -> dict[str, Any]:
  if not path.exists():
    return {}

  with path.open("r", encoding="utf-8") as file:
    data = yaml.safe_load(file) or {}

  if not isinstance(data, dict):
    raise ValueError(f"{path} must contain a YAML mapping.")

  return data


def save_element(path: Path, name: str, element: Element) -> None:
  elements = load_elements(path)
  elements[name] = element.model_dump(by_alias=True, exclude_none=True)

  with path.open("w", encoding="utf-8") as file:
    yaml.safe_dump(
      elements,
      file,
      sort_keys=False,
      allow_unicode=True,
    )


def prompt_required(label: str) -> str:
  while True:
    value = input(label).strip()
    if value:
      return value

    print("Value is required.")


def prompt_accept() -> bool:
  value = input("Accept and save this element? [y/N]: ").strip().lower()
  return value in {"y", "yes"}


async def run_cli(output_path: Path) -> None:
  load_dotenv()

  print("Describe the website object you want to extract.")
  name = prompt_required("Element name: ")
  user_prompt = prompt_required("Prompt: ")

  try:
    result = await Runner.run(main_agent, user_prompt)
  except InputGuardrailTripwireTriggered:
    print("Request blocked: prompt must relate to browser automation or website exploration.")
    return

  element = result.final_output
  if not isinstance(element, Element):
    element = Element.model_validate(element)

  print("\nElement:")
  print(yaml.safe_dump(
    element.model_dump(by_alias=True, exclude_none=True),
    sort_keys=False,
    allow_unicode=True,
  ).strip())

  if not prompt_accept():
    print("Element was not saved.")
    return

  save_element(output_path, name, element)
  print(f"Saved '{name}' to {output_path}.")


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    description="Explore a website with Playwright MCP and save an Element YAML entry.",
  )
  parser.add_argument(
    "-o",
    "--output",
    type=Path,
    default=DEFAULT_OUTPUT_PATH,
    help="YAML file to write accepted elements into.",
  )
  return parser.parse_args()


def main() -> None:
  args = parse_args()
  asyncio.run(run_cli(args.output))


if __name__ == "__main__":
  main()
