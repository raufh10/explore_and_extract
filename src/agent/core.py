from agents import Agent, AgentOutputSchema

from agent.guardrails import browser_automation_guardrail
from agent.models import Elements
from agent.tools import playwright_mcp

mcp_agent = Agent(
  name="playwright_mcp_browser_agent",
  instructions=(
    "Use playwright_mcp to visit the site. "
    "Your goal is to identify the TEMPLATE for the requested object, not to scrape every item. "
    "Find the most specific, stable CSS selector that would be used in BeautifulSoup. "
    "MANDATORY: Return ONLY ONE example of each distinct element type requested, "
    "If the user asks for 'prices', find one price element and return its tag, class, and attributes "
    "so that a developer can use that information to write: soup.find_all(tag, class_=...)"
  ),
  tools=[playwright_mcp],
  output_type=AgentOutputSchema(Elements, strict_json_schema=True),
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
