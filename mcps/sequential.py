from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List
import uuid

# In-memory store for thinking sessions
thinking_sessions: Dict[str, Dict] = {}

# Create MCP server
mcp = FastMCP("SequentialThinking")

# Tool: Sequential Thinking
@mcp.tool()
def sequential_thinking(
    thought: str,
    nextThoughtNeeded: bool,
    thoughtNumber: int,
    totalThoughts: int,
    sessionId: Optional[str] = None,
    isRevision: Optional[bool] = False,
    revisesThought: Optional[int] = None,
    branchFromThought: Optional[int] = None,
    branchId: Optional[str] = None,
    needsMoreThoughts: Optional[bool] = False
) -> str:
    """
    Facilitates a step-by-step thinking process for problem-solving.
    
    Args:
        thought: The current thinking step
        nextThoughtNeeded: Whether another thought step is needed
        thoughtNumber: Current thought number
        totalThoughts: Estimated total thoughts needed
        sessionId: Unique identifier for the thinking session
        isRevision: Whether this revises a previous thought
        revisesThought: Which thought number is being revised
        branchFromThought: Thought number to branch from
        branchId: Identifier for the branch
        needsMoreThoughts: If more thoughts are needed beyond totalThoughts
    
    Returns:
        A summary of the current thinking state or an error message
    """
    # Generate or validate session ID
    if not sessionId:
        sessionId = str(uuid.uuid4())
    if sessionId not in thinking_sessions:
        thinking_sessions[sessionId] = {
            "thoughts": [],  # List of (thought_number, thought, branch_id) tuples
            "totalThoughts": totalThoughts,
            "branches": {}  # branch_id -> parent_thought_number
        }

    session = thinking_sessions[sessionId]

    # Validate inputs
    if thoughtNumber < 1:
        return "Error: thoughtNumber must be positive."
    if totalThoughts < thoughtNumber:
        return "Error: totalThoughts cannot be less than thoughtNumber."
    if isRevision and revisesThought is None:
        return "Error: revisesThought must be provided for revisions."
    if branchFromThought is not None and branchId is None:
        return "Error: branchId must be provided when branching."

    # Handle revision
    if isRevision:
        if revisesThought > len(session["thoughts"]) or revisesThought < 1:
            return f"Error: Cannot revise thought {revisesThought}. Invalid thought number."
        # Update the specific thought
        for i, (num, _, branch) in enumerate(session["thoughts"]):
            if num == revisesThought and branch == (branchId or "main"):
                session["thoughts"][i] = (revisesThought, thought, branchId or "main")
                return f"Revised thought {revisesThought} in session {sessionId}: {thought}"

    # Handle branching
    if branchFromThought is not None:
        if branchFromThought > len(session["thoughts"]) or branchFromThought < 1:
            return f"Error: Cannot branch from thought {branchFromThought}. Invalid thought number."
        session["branches"][branchId] = branchFromThought
        session["thoughts"].append((thoughtNumber, thought, branchId))
        return f"Added thought {thoughtNumber} to branch {branchId} from thought {branchFromThought} in session {sessionId}"

    # Handle regular thought
    if thoughtNumber > len(session["thoughts"]) + 1:
        return f"Error: Cannot add thought {thoughtNumber}. Next expected thought is {len(session['thoughts']) + 1}."
    session["thoughts"].append((thoughtNumber, thought, branchId or "main"))

    # Update totalThoughts if needed
    if needsMoreThoughts and totalThoughts > session["totalThoughts"]:
        session["totalThoughts"] = totalThoughts

    # Build summary
    summary = [f"Session {sessionId} Summary:"]
    summary.append(f"Total Thoughts Estimated: {session['totalThoughts']}")
    summary.append("Thoughts:")
    for num, txt, branch in session["thoughts"]:
        branch_info = f"(Branch: {branch})" if branch != "main" else ""
        summary.append(f"  {num}. {txt} {branch_info}")
    if session["branches"]:
        summary.append("Branches:")
        for bid, parent in session["branches"].items():
            summary.append(f"  {bid}: Branched from thought {parent}")
    summary.append(f"Next Thought Needed: {'Yes' if nextThoughtNeeded else 'No'}")

    return "\n".join(summary)

def run(port: int = 8001):
    mcp.run(port=port)

if __name__ == "__main__":
    run()