from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List
import uuid

# In-memory store for thinking sessions
thinking_sessions: Dict[str, Dict] = {}

# Create MCP server
mcp = FastMCP("SequentialThinking")

# NEW: Define reflection strategies inspired by the paper
REFLECTION_STRATEGIES = [
    "error_analysis",  # Analyze why the thought was incorrect
    "alternative_approach",  # Suggest a different method
    "clarify_assumptions",  # Re-evaluate assumptions
    "break_down_problem",  # Decompose into smaller parts
]

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
    needsMoreThoughts: Optional[bool] = False,
    # NEW: Parameters for self-reflection
    reflectionNeeded: Optional[bool] = False,
    reflectionStrategy: Optional[str] = None,
    performanceFeedback: Optional[str] = None
) -> str:
    """
    Facilitates a step-by-step thinking process for problem-solving with self-reflection.
    
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
        reflectionNeeded: Whether to perform self-reflection on the thought
        reflectionStrategy: Type of reflection (e.g., error_analysis)
        performanceFeedback: Feedback on thought effectiveness (e.g., correct/incorrect)
    
    Returns:
        A summary of the current thinking state or an error message
    """
    
    print("\n🔄 [MCP CALL RECEIVED] ------------------------")

    # Generate or validate session ID
    if not sessionId:
        sessionId = str(uuid.uuid4())
    if sessionId not in thinking_sessions:
        thinking_sessions[sessionId] = {
            "thoughts": [],  # List of (thought_number, thought, branch_id, reflection) tuples
            "totalThoughts": totalThoughts,
            "branches": {},  # branch_id -> parent_thought_number
            "reflections": [],  # NEW: Store reflection outcomes
            "performance": []  # NEW: Track performance metrics
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
    # NEW: Validate reflection inputs
    if reflectionNeeded and reflectionStrategy not in REFLECTION_STRATEGIES:
        return f"Error: Invalid reflectionStrategy. Choose from {REFLECTION_STRATEGIES}."

    # NEW: Handle self-reflection
    reflection_output = ""
    if reflectionNeeded:
        if not performanceFeedback:
            return "Error: performanceFeedback required for reflection."
        # Simulate reflection based on strategy (call Claude Desktop for actual LLM reflection)
        reflection_prompt = f"Reflect on thought {thoughtNumber}: '{thought}' with feedback: '{performanceFeedback}' using strategy: {reflectionStrategy}."
        # Placeholder: In practice, send reflection_prompt to Claude Desktop
        reflection_output = f"Reflection ({reflectionStrategy}): Analyzed thought {thoughtNumber}. Feedback: {performanceFeedback}."
        session["reflections"].append((thoughtNumber, reflectionStrategy, reflection_output))
        # If reflection suggests revision, trigger isRevision
        if "incorrect" in performanceFeedback.lower():
            isRevision = True
            revisesThought = thoughtNumber

    # Handle revision
    if isRevision:
        if revisesThought > len(session["thoughts"]) or revisesThought < 1:
            return f"Error: Cannot revise thought {revisesThought}. Invalid thought number."
        for i, (num, _, branch, _) in enumerate(session["thoughts"]):
            if num == revisesThought and branch == (branchId or "main"):
                session["thoughts"][i] = (revisesThought, thought, branchId or "main", reflection_output)
                # NEW: Log performance improvement
                session["performance"].append((revisesThought, performanceFeedback or "Revised"))
                return f"Revised thought {revisesThought} in session {sessionId}: {thought}\n{reflection_output}"

    # Handle branching
    if branchFromThought is not None:
        if branchFromThought > len(session["thoughts"]) or branchFromThought < 1:
            return f"Error: Cannot branch from thought {branchFromThought}. Invalid thought number."
        session["branches"][branchId] = branchFromThought
        session["thoughts"].append((thoughtNumber, thought, branchId, reflection_output))
        # NEW: Log performance
        session["performance"].append((thoughtNumber, performanceFeedback or "Branched"))
        return f"Added thought {thoughtNumber} to branch {branchId} from thought {branchFromThought} in session {sessionId}\n{reflection_output}"

    # Handle regular thought
    if thoughtNumber > len(session["thoughts"]) + 1:
        return f"Error: Cannot add thought {thoughtNumber}. Next expected thought is {len(session['thoughts']) + 1}."
    session["thoughts"].append((thoughtNumber, thought, branchId or "main", reflection_output))
    # NEW: Log performance
    session["performance"].append((thoughtNumber, performanceFeedback or "Added"))

    # Update totalThoughts if needed
    if needsMoreThoughts and totalThoughts > session["totalThoughts"]:
        session["totalThoughts"] = totalThoughts

    # Build summary
    summary = [f"Session {sessionId} Summary:"]
    summary.append(f"Total Thoughts Estimated: {session['totalThoughts']}")
    summary.append("Thoughts:")
    for num, txt, branch, ref in session["thoughts"]:
        branch_info = f"(Branch: {branch})" if branch != "main" else ""
        ref_info = f"(Reflection: {ref})" if ref else ""
        summary.append(f"  {num}. {txt} {branch_info} {ref_info}")
    if session["branches"]:
        summary.append("Branches:")
        for bid, parent in session["branches"].items():
            summary.append(f"  {bid}: Branched from thought {parent}")
    if session["reflections"]:
        summary.append("Reflections:")
        for num, strat, ref in session["reflections"]:
            summary.append(f"  Thought {num}: {strat} - {ref}")
    if session["performance"]:
        summary.append("Performance:")
        for num, feedback in session["performance"]:
            summary.append(f"  Thought {num}: {feedback}")
    summary.append(f"Next Thought Needed: {'Yes' if nextThoughtNeeded else 'No'}")

    # print("[THOUGHT STORED] Current session state:")
    # print("\n".join(summary))

    return "\n".join(summary)

def run(port: int = 8001):
    mcp.run(port=port)

if __name__ == "__main__":
    run()