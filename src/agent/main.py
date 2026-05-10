import argparse
import asyncio
from pathlib import Path

import yaml
from agents import InputGuardrailTripwireTriggered, Runner
from dotenv import load_dotenv

from agent.core import main_agent
from agent.models import Elements, APIBlueprint
from agent.yaml_store import save_pattern

DEFAULT_OUTPUT_PATH = Path("patterns.yaml")

def prompt_required(label: str) -> str:
  while True:
    value = input(label).strip()
    if value.lower() in {"q", "exit"}:
      return "EXIT_SIGNAL"
    if value:
      return value
    print("Value is required.")

def prompt_accept() -> bool:
  value = input("Accept and save this pattern? [y/N]: ").strip().lower()
  return value in {"y", "yes"}

async def run_cli(output_path: Path) -> None:
  load_dotenv()
  print("--- Web Pattern Explorer (Type 'q' or 'exit' to quit) ---")

  while True:
    print("\nDescribe the website object or API you want to analyze.")

    name = prompt_required("Pattern name: ")
    if name == "EXIT_SIGNAL": break

    user_prompt = prompt_required("Prompt: ")
    if user_prompt == "EXIT_SIGNAL": break

    try:
      result = await Runner.run(
        main_agent, 
        user_prompt, 
        tool_approval_callback=lambda x: "approve"
      )

      while result.interruptions:
        state = result.to_state()
        state.approve(result.interruptions[0])
        result = await Runner.run(main_agent, state)

    except InputGuardrailTripwireTriggered:
      print("Request blocked: prompt must relate to browser automation.")
      continue
    except Exception as e:
      print(f"An error occurred: {e}")
      continue

    output_data = result.final_output
    if output_data is None:
      print("Agent did not return any data.")
      continue

    if not isinstance(output_data, (Elements, APIBlueprint)):
      try:
        # Attempt to figure out which model it is based on the keys
        if isinstance(output_data, dict) and "endpoints" in output_data:
          output_data = APIBlueprint.model_validate(output_data)
        else:
          output_data = Elements.model_validate(output_data)
      except Exception:
        print("Error: Received data that does not match known pattern schemas.")
        continue

    print("\nExtracted Pattern:")
    formatted_yaml = yaml.safe_dump(
      output_data.model_dump(by_alias=True, exclude_none=True),
      sort_keys=False,
      allow_unicode=True,
    ).strip()
    print(formatted_yaml)

    if prompt_accept():
      save_pattern(output_path, name, output_data)
      print(f"Saved '{name}' to {output_path}.")
    else:
      print("Pattern was not saved.")

  print("Exiting...")

def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(
    description="Explore websites and APIs using Playwright MCP and save YAML blueprints.",
  )
  parser.add_argument(
    "-o", "--output", type=Path, default=DEFAULT_OUTPUT_PATH,
    help="YAML file to write accepted patterns into.",
  )
  return parser.parse_args()

def main() -> None:
  args = parse_args()
  asyncio.run(run_cli(args.output))

if __name__ == "__main__":
  main()
