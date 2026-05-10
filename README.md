## explore-and-extract 🕵️‍♂️🤖
A modular AI agent suite designed to automate the discovery of web patterns and internal API endpoints. By leveraging an orchestrator and specialized sub-agents, it bridges the gap between traditional browser automation and modern API reverse engineering.
This tool triages requests into two primary workflows:
 1. **DOM Exploration:** Identifies stable CSS selectors and HTML structures for scraping.
 2. **Network Discovery:** Sniffs background traffic to capture URLs, methods, and headers for direct API interaction (Postman-ready).
### 🚀 Features
 * **Intelligent Triage:** A central orchestrator that routes prompts to either a Visual or Network specialist based on intent.
 * **Network Protocol Analysis:** Automatically identifies fetch and xhr calls, capturing critical headers and payloads.
 * **Pattern Persistence:** Saves all discoveries into a centralized patterns.yaml file for future use in data pipelines.
 * **Atomic Scripting:** Uses unsafe code execution to handle complex browser interactions in a single, high-performance operation.
 * **Built-in Guardrails:** Protects against non-automation prompts to keep the agents focused and secure.
### 📂 Project Structure
```text
.
├── src/
│   ├── agent/
│   │   ├── core.py          # Agent definitions & orchestrator logic
│   │   ├── guardrails.py    # Input validation logic
│   │   ├── models.py        # Pydantic schemas (Elements, APIBlueprint)
│   │   ├── tools.py         # Specialized tool configurations
│   │   ├── yaml_store.py    # Pattern loading and saving
│   │   └── main.py          # CLI entry point
├── patterns.yaml            # The generated pattern library
└── pyproject.toml           # Project metadata

```
### 📥 Setup
 1. **Clone the repository:**
   ```bash
   git clone https://github.com/raufh10/explore_and_extract
   cd explore_and_extract
   
   ```
 2. **Environment Configuration:**
   Create a .env file and add your GPT API key:
   ```env
   OPENAI_API_KEY=your_key_here
   
   ```
 3. **Requirements:**
   This project requires a running **Playwright MCP** server. Use the following deployment for the browser automation backend:
   👉[raufh10/playwright-mcp](https://github.com/raufh10/playwright-mcp)
### 💻 Usage Examples
Run the CLI tool using uv:
```bash
uv run explore-and-extract

```
#### 1. Visual Element Extraction
**Prompt:** *"get ongoing, upcoming, & completed missions elements from the web complete with its date and mission name"*
```yaml
spacex_launches_elements:
  elements:
    - tag: div
      class: mission-card
      attributes:
        - name: data-status
          value: '{ongoing|upcoming|completed}'
      description: Mission item container
    - tag: span
      class: mission-date
      description: Mission date text
    - tag: a
      class: mission-name
      attributes:
        - name: href
          value: '{url}'
      description: Mission name link

```
#### 2. Network API Discovery
**Prompt:** *"Go to SpaceX.com/launches and find the background fetch request that loads the list of upcoming missions."*
```yaml
spacex_launches_api:
  endpoints:
    - url: "https://content.spacex.com/api/spacex-website/launches-page-tiles/upcoming"
      method: "GET"
      headers:
        - name: "accept"
          value: "application/json, text/plain, */*"
        - name: "referer"
          value: "https://www.spacex.com/"
      resource_type: "fetch"
  summary: "Direct API endpoint for upcoming mission data."

```
### ⚖️ Note
This tool is intended for ethical reverse engineering and development purposes. Always ensure you have permission to analyze target websites and comply with their Terms of Service.

