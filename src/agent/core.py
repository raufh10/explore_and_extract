from agents import Agent, AgentOutputSchema

from agent.guardrails import browser_automation_guardrail
from agent.models import Elements, APIBlueprint
from agent.tools import playwright_mcp

network_specialist = Agent(
  name="network_discovery_agent",
  instructions=(
    "You are a network protocol analyst. You have access to 'browser_run_code_unsafe'.\n"
    "To capture API data without session errors, write a script that:\n"
    "1. Starts a listener for 'request' events to capture headers and methods.\n"
    "2. Navigates to the target URL and waits for 'networkidle'.\n"
    "3. Filters the captured requests for 'fetch' or 'xhr' types.\n"
    "4. Returns an array of objects containing 'url', 'method', 'headers', and 'postData'.\n"
    "\nUSE THIS CODE PATTERN:\n"
    "async (page) => {\n"
    "  const reqs = [];\n"
    "  page.on('request', r => {\n"
    "    if (['fetch', 'xhr'].includes(r.resourceType())) {\n"
    "      reqs.push({ \n"
    "        url: r.url(), \n"
    "        method: r.method(), \n"
    "        headers: r.headers(), \n"
    "        postData: r.postData() \n"
    "      });\n"
    "    }\n"
    "  });\n"
    "  await page.goto(URL, { waitUntil: 'networkidle' });\n"
    "  return reqs;\n"
    "}"
  ),
  tools=[playwright_mcp],
  output_type=AgentOutputSchema(APIBlueprint, strict_json_schema=False),
)

mcp_agent = Agent(
  name="playwright_mcp_browser_agent",
  instructions=(
    "Use playwright_mcp to visit the site. "
    "Your goal is to identify the TEMPLATE for the requested object, not to scrape every item. "
    "Find the most specific, stable CSS selector that would be used in BeautifulSoup. "
    "MANDATORY: Return ONLY ONE example of each distinct element type requested, "
    "For the value in attributes, do not use specific text from the page (like a book title). Instead, use a placeholder like {text} or {url} to indicate the type of data found there. "
    "If data is nested, return the innermost tag that contains the actual text or target attribute. For titles inside headers, return the 'a' tag directly rather than the 'h3'. "
    "If the user asks for 'prices', find one price element and return its tag, class, and attributes "
    "so that a developer can use that information to write: soup.find_all(tag, class_=...)"
  ),
  tools=[playwright_mcp],
  output_type=AgentOutputSchema(Elements, strict_json_schema=True),
)

main_agent = Agent(
  name="web_element_extraction_orchestrator",
  instructions=(
    "You are the central triage agent for web exploration. Analyze the user's "
    "request and execute an immediate handoff to the appropriate specialist:\n"
    "1. Hand off to 'playwright_mcp_browser_agent' if the user needs HTML tags, "
    "CSS selectors, or visual UI patterns for scrapers like BeautifulSoup.\n"
    "2. Hand off to 'network_discovery_agent' if the user needs to reverse engineer "
    "APIs, inspect network traffic, capture headers, or monitor background requests "
    "for tools like Postman."
  ),
  handoffs=[mcp_agent, network_specialist],
  input_guardrails=[browser_automation_guardrail],
)

