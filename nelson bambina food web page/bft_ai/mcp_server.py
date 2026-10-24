import os
import logging

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from bft_ai.gemini_service import GeminiRequestError, generate_reply

mcp = FastMCP("VBS BFT Gemini Assistant")
logger = logging.getLogger("bft_ai.mcp")


@mcp.tool()
def ask_bambina_ai(
    question: str = Field(
        description="A public, non-sensitive question about BFT's described services."
    ),
) -> str:
    """Ask Gemini about BFT's public services; do not provide confidential data."""
    question = question.strip()
    if not question or len(question) > 1200:
        raise ValueError("Question must contain 1 to 1200 characters.")
    if not os.getenv("GEMINI_API_KEY", "").strip():
        raise ValueError("Set GEMINI_API_KEY in the MCP server environment.")
    try:
        return generate_reply(question)
    except GeminiRequestError as error:
        logger.warning("Gemini MCP request failed")
        raise ValueError("Gemini could not answer right now. Check configuration and try again.") from error


if __name__ == "__main__":
    mcp.run(transport="stdio")
