from mcp.server.fastmcp import FastMCP
from typing import List
from datetime import datetime
import json
import os

# Constants
DEFAULT_LEAVE_BALANCE = 20
LEAVE_DB_FILE = "employee_leaves.json"

# Load or initialize employee leaves
def load_leaves():
    if os.path.exists(LEAVE_DB_FILE):
        with open(LEAVE_DB_FILE, 'r') as f:
            return json.load(f)
    return {
        "E001": {"balance": 18, "history": ["2024-12-25", "2025-01-01"]},
        "E002": {"balance": 19, "history": []}
    }

def save_leaves(employee_leaves):
    with open(LEAVE_DB_FILE, 'w') as f:
        json.dump(employee_leaves, f, indent=2)

employee_leaves = load_leaves()

# Create MCP server
mcp = FastMCP("LeaveManager")

# Validate date format (YYYY-MM-DD)
def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Tool: Check Leave Balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    print("Getting the leave balance....")
    """Check how many leave days are left for the employee"""
    data = employee_leaves.get(employee_id.strip())
    if data:
        return f"{employee_id} has {data['balance']} leave days remaining."
    return "Employee ID not found."

# Tool: Apply for Leave with specific dates
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
    """
    employee_id = employee_id.strip()
    if employee_id not in employee_leaves:
        return "Employee ID not found."

    # Validate dates
    for date in leave_dates:
        if not is_valid_date(date):
            return f"Invalid date format: {date}. Use YYYY-MM-DD."
        if date in employee_leaves[employee_id]["history"]:
            return f"Date {date} already applied."

    requested_days = len(leave_dates)
    available_balance = employee_leaves[employee_id]["balance"]

    if available_balance < requested_days:
        return f"Insufficient leave balance. You requested {requested_days} day(s) but have only {available_balance}."

    # Deduct balance and add to history
    employee_leaves[employee_id]["balance"] -= requested_days
    employee_leaves[employee_id]["history"].extend(leave_dates)
    save_leaves(employee_leaves)  # Persist changes

    return f"Leave applied for {requested_days} day(s). Remaining balance: {employee_leaves[employee_id]['balance']}."

# Resource: Leave history
@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """Get leave history for the employee"""
    data = employee_leaves.get(employee_id.strip())
    if data:
        history = ', '.join(data['history']) if data['history'] else "No leaves taken."
        return f"Leave history for {employee_id}: {history}"
    return "Employee ID not found."

# Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! How can I assist you with leave management today?"

def run(port: int = 8000):
    import logging
    logging.basicConfig(level=logging.INFO)
    mcp.run(port=port)

if __name__ == "__main__":
    run()