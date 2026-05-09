from agents import Agent

from agent.guardrails import browser_automation_guardrail
from agent.models import Element
from agent.tools import playwright_mcp


mcp_agent = Agent(
  name="Playwright MCP browser agent",
  instructions=(
    "Use the Playwright MCP tool to explore websites, inspect pages, and "
    "identify HTML elements relevant to the user's target object. Prefer "
    "stable selectors and attributes that will be useful for a BeautifulSoup "
    "scraper later."
  ),
  tools=[playwright_mcp],
)


main_agent = Agent(
  name="Web element extraction orchestrator",
  instructions=(
    "Orchestrate browser-based website exploration to identify the specific "
    "HTML element that best represents the object the user wants to extract. "
    "Ask the Playwright MCP browser agent to inspect the website when needed. "
    "Return one structured Element with the tag, class, id, and any other "
    "stable attributes that can guide a later BeautifulSoup scraper."
  ),
  tools=[
    mcp_agent.as_tool(
      tool_name="inspect_website_with_playwright",
      tool_description=(
        "Use Playwright MCP to explore a website and identify relevant HTML "
        "elements for extraction."
      ),
    )
  ],
  input_guardrails=[browser_automation_guardrail],
  output_type=Element,
)
