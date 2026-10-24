# BFT website and Gemini assistant

The existing BFT site remains a public marketing page. Its optional Bambina AI
widget answers general questions about public BFT services only. It is not
connected to production equipment, customer accounts, finance, HR, or private
business records. Questions submitted to the widget are sent to Google Gemini;
visitors are warned not to include personal or confidential information.

## Local setup (Windows PowerShell)

1. Create a Google Gemini API key in Google AI Studio. Do not paste it into the
   HTML, source control, chat, or `.vscode/mcp.json`.
2. Add the key to the ignored root `.env` file as `GEMINI_API_KEY=...`.
   `GEMINI_MODEL` is optional and defaults to `gemini-2.5-flash`. The existing
   `vbs` environment entry is separate and is not read by this integration.
3. From the project root, create an environment and install the dependencies:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. Start the website and API on the local machine:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn bft_ai.api:app --host 127.0.0.1 --port 8000
   ```

5. Open `http://127.0.0.1:8000`. The chat widget sends requests to the local
   backend; opening the HTML directly as a `file://` page will not connect.

## VS Code MCP

`.vscode/mcp.json` registers the `vbs-bft-gemini` stdio MCP server. Install the
requirements above, then start or reconnect the server from VS Code's MCP
controls. VS Code asks for the Gemini key through a password-masked input; the
key is passed to the local MCP process and is not written into the JSON file.
The MCP tool accepts only a question and has no tools for accessing files,
databases, machines, or other MCP servers.

## Security and deployment notes

- The Gemini key is read only by the Python process. Never expose it in
  browser JavaScript or a public repository.
- `.env` is ignored by Git; `.env.example` contains placeholders only.
- The public chat endpoint limits input to 1,200 characters and 8 requests per
  client IP per minute. This in-memory limit is for local demonstration, not a
  production abuse-control boundary.
- Run locally on `127.0.0.1`. Before public deployment, add a trusted reverse
  proxy/WAF with shared rate limiting, abuse protection, TLS, monitoring, and
  Gemini quota/billing limits. Do not trust client-supplied forwarded-IP
  headers as identity.
- Do not submit confidential, personal, financial, employee, or machine-control
  data to this public assistant. The assistant does not have access to such
  records and cannot execute machine commands.
- Gemini responses can be incorrect. Confirm technical, commercial, and safety
  details with BFT before acting.
- Never configure production hardware-control access through this public API
  or the MCP tool.
