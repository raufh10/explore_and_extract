import argparse
import asyncio
from pathlib import Path

import yaml
from agents import InputGuardrailTripwireTriggered, Runner
from dotenv import load_dotenv

from agent.core import main_agent
from agent.models import Elements
from agent.yaml_store import save_elements


DEFAULT_OUTPUT_PATH = Path("elements.yaml")


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

    while result.interruptions:
      state = result.to_state()
      state.approve(result.interruptions[0])
      result = await Runner.run(main_agent, state)

    for item in result.new_items:
      print(f"DEBUG - Item Type: {type(item).__name__}")
      if hasattr(item, 'text'):
        print(f"DEBUG - Text: {item.text}")
      if hasattr(item, 'tool_calls'):
        print(f"DEBUG - Tool Calls: {item.tool_calls}")

  except InputGuardrailTripwireTriggered:
    print("Request blocked: prompt must relate to browser automation or website exploration.")
    return

  elements_output = result.final_output
  if elements_output is None:
    print("Agent did not return any elements.")
    return

  if not isinstance(elements_output, Elements):
    elements_output = Elements.model_validate(elements_output)

  print("\nElements:")
  print(yaml.safe_dump(
    elements_output.model_dump(by_alias=True, exclude_none=True),
    sort_keys=False,
    allow_unicode=True,
  ).strip())

  if not prompt_accept():
    print("Element was not saved.")
    return

  save_elements(output_path, name, elements_output)
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
