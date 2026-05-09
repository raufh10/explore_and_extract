from typing import Annotated

from pydantic import BaseModel, Field

from agents import (
  Agent,
  GuardrailFunctionOutput,
  RunContextWrapper,
  Runner,
  TResponseInputItem,
  input_guardrail,
)


class BrowserAutomationOutput(BaseModel):
  is_browser_automation_request: bool
  reasoning: Annotated[
    str,
    Field(
      description="One sentence explaining the classification.",
      max_length=120,
    ),
  ]


browser_automation_guardrail_agent = Agent(
  name="Browser automation check",
  instructions=(
    "Determine whether the user's prompt is related to Playwright browser "
    "automation, website exploration, web navigation, browser testing, "
    "web scraping, or automating actions on a website. Return true only when "
    "the request is clearly about using a browser or website automation. "
    "Keep reasoning to exactly one sentence and no more than 120 characters."
  ),
  output_type=BrowserAutomationOutput,
)


@input_guardrail
async def browser_automation_guardrail(
  ctx: RunContextWrapper[None],
  agent: Agent,
  input: str | list[TResponseInputItem],
) -> GuardrailFunctionOutput:
  result = await Runner.run(
    browser_automation_guardrail_agent,
    input,
    context=ctx.context,
  )

  return GuardrailFunctionOutput(
    output_info=result.final_output,
    tripwire_triggered=not result.final_output.is_browser_automation_request,
  )
