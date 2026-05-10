import os
from agents import HostedMCPTool

playwright_mcp = HostedMCPTool(
  tool_config={
    "type": "mcp",
    "server_label": "playwright-mcp",
    "server_url": os.environ.get("PLAYWRIGHT_MCP_SERVER_URL", ""),
    "server_description": "Hosted Playwright MCP server for browser automation.",
  }
)
