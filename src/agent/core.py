from agents import Agent, AgentOutputSchema

from agent.guardrails import browser_automation_guardrail
from agent.models import Elements
from agent.tools import playwright_mcp


mcp_agent = Agent(
  name="playwright_mcp_browser_agent",
  handoff_description=(
    "Use this agent for Playwright browser automation, website exploration, "
    "and HTML element identification."
  ),
  instructions=(
    "Use the Playwright MCP tool to explore websites, inspect pages, and "
    "identify HTML elements relevant to the user's target object. Prefer "
    "stable selectors and attributes that will be useful for a BeautifulSoup "
    "scraper later. Return structured Elements with a flat list of matching "
    "elements; do not include child elements or recursive nesting."
  ),
  tools=[playwright_mcp],
  output_type=AgentOutputSchema(Elements, strict_json_schema=False),
)


main_agent = Agent(
  name="web_element_extraction_orchestrator",
  instructions=(
    "Orchestrate browser-based website exploration to identify the specific "
    "HTML elements that best represent the object the user wants to extract. "
    "Handoff website exploration and browser automation requests to the "
    "Playwright MCP browser agent."
  ),
  handoffs=[mcp_agent],
  input_guardrails=[browser_automation_guardrail],
)
