"""MCP client — connection to Model Context Protocol servers.

The Model Context Protocol (MCP) is an open standard for connecting LLM
applications to external tools and data sources via a unified interface.

This file is the integration point for any MCP servers your agents use.

If you define an MCPClient Protocol in domain/interfaces.py, implement it here.
Otherwise, use this as a standalone client injected into agents that need it.

What MCP enables:
    - Your agents can call tools exposed by MCP servers (e.g., web search,
      code execution, database access, file system) without baking the
      integration into the agent itself.
    - Servers can be local (stdio) or remote (SSE / HTTP).

Conventions:
    - All server URLs, tokens, and config come from config.py (Settings).
    - Catch MCP-specific exceptions and re-raise as domain exceptions.
    - Keep this client thin — just transport and serialization, no business logic.

SDK options:
    - Official Python MCP SDK (pip install mcp)
      Docs: https://modelcontextprotocol.io/introduction
    - Claude's built-in MCP support via the Anthropic SDK (>=0.40)

Example servers to connect to:
    - Filesystem server (read/write local files)
    - Brave Search / Tavily (web search)
    - GitHub (repo access)
    - PostgreSQL (database queries)
    - Any custom MCP server your organization builds
"""

from {{ cookiecutter.project_slug }}.config import settings

# TODO: Install the MCP SDK and import it here.
# Example: from mcp import ClientSession, StdioServerParameters


class MCPClient:
    """Client for connecting to and calling tools on an MCP server.

    Args:
        server_url: URL or command for the MCP server.
            For stdio servers, this is the command to launch the server.
            For SSE servers, this is the HTTP endpoint URL.
    """

    def __init__(self, server_url: str | None = None) -> None:
        # TODO: Initialize the MCP session here.
        pass

    async def call_tool(self, tool_name: str, args: dict) -> dict:
        """Call a tool exposed by the MCP server.

        Args:
            tool_name: The name of the tool as declared by the server.
            args: Arguments to pass to the tool (schema defined by the server).

        Returns:
            The tool's response as a dict. Map to domain models in the agent.

        Raises:
            ProviderError: If the MCP server is unreachable or the tool fails.
        """
        # TODO: Invoke the tool via the MCP SDK session.
        raise NotImplementedError("Implement call_tool() for your MCP server.")

    async def list_tools(self) -> list[dict]:
        """List the tools available on the connected MCP server.

        Returns:
            List of tool descriptors (name, description, input schema).
        """
        # TODO: Call the MCP server's tools/list endpoint.
        raise NotImplementedError("Implement list_tools() for your MCP server.")
