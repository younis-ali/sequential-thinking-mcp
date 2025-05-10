from mcp.server.fastmcp import FastMCP
from mcps import sequential

# Create a single FastMCP server
mcp = FastMCP("SequentialThinkingMCP")

# Register Sequential Thinking tool
mcp.tool()(sequential.sequential_thinking)

if __name__ == "__main__":
    mcp.run()