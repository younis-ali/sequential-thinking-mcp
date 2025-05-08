from mcp.server.fastmcp import FastMCP
import leave_manager
import sequential

# Create a single FastMCP server
mcp = FastMCP("CombinedMCP")

# Register Leave Manager tools and resources
mcp.tool()(leave_manager.get_leave_balance)
mcp.tool()(leave_manager.apply_leave)
mcp.tool()(leave_manager.get_leave_history)
mcp.resource("greeting://{name}")(leave_manager.get_greeting)

# Register Sequential Thinking tool
mcp.tool()(sequential.sequential_thinking)

if __name__ == "__main__":
    mcp.run(port=8000)