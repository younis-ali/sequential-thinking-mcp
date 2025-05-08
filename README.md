# Model Context Protocol (MCP) Servers: Sequential Thinking with bonus Leave Management server. 

This project implements two **Model Context Protocol (MCP)** servers using the `FastMCP` framework:
- **Sequential Thinking**: A tool for structured problem-solving, ideal for tasks like supply chain management planning.
- **Leave Manager**: An AI tool for HR to manage employee leave tasks, interacting with a mock leave database.

The servers are launched concurrently using a `main.py` script and can be queried via **Claude Desktop**, which integrates with the MCP servers for sending API requests using the Model Context Protocol.

## Project Structure

```
directory/
├── main.py              # Launches both MCP servers
├── leave_manager.py     # Leave Manager MCP server
├── sequential.py        # Sequential Thinking MCP server
```

## Features

### Sequential Thinking MCP Server
- **Purpose**: Facilitates structured, step-by-step problem-solving using the Model Context Protocol, ideal for planning complex tasks like supply chain management.
- **Tool**: `sequential_thinking`
  - Breaks down problems into sequential thoughts.
  - Supports revising thoughts, branching for alternative strategies, and dynamically adjusting the number of steps.
  - Maintains context via a `sessionId`.
- **Use Case**: Plan supply chains, projects, or any task requiring iterative reasoning.
- **Port**: Runs on `http://localhost:8001`.

### Leave Manager MCP Server
- **Purpose**: Assists HR with employee leave management using the Model Context Protocol.
- **Tools**:
  - `get_leave_balance`: Check an employee’s remaining leave days.
  - `apply_leave`: Apply for leave on specific dates.
  - `get_leave_history`: View an employee’s leave history.
- **Resource**: `greeting://{name}` for personalized greetings.
- **Port**: Runs on `http://localhost:8000`.


### Main Launcher
- **main.py**: Uses `multiprocessing` to run both servers concurrently on their respective ports.

## Prerequisites

- **Python**: Version 3.8 or higher.
- **Claude Desktop**: For sending MCP queries to the servers.
- **uv**: Package manager for installing dependencies.
- **Operating System**: Tested on Linux (e.g., Ubuntu).

## Setup Steps

Follow these steps to set up the project:

1. **Install Claude Desktop**:
   - Download and install Claude Desktop from the official source.
   - Ensure it’s configured to send API queries (e.g., via a query input field).

2. **Install uv**:
   ```bash
   pip install uv
   ```

3. **Create Project Directory**:
   ```bash
   uv init my-first-mcp-server
   cd my-first-mcp-server
   ```

4. **Add MCP CLI**:
   ```bash
   uv add "mcp[cli]"
   ```

5. **Add Server Code**:
   - Place the following files in `my-first-mcp-server/`:
     - `main.py`: Launcher for both servers.
     - `leave_manager.py`: Leave Manager server code.
     - `sequential.py`: Sequential Thinking server code.
   - Ensure the code matches the provided implementations (see project repository or documentation).

6. **Run the Servers**:
   - Instead of `uv run mcp install main.py` (which may fail due to multiple servers), run:
     ```bash
     uv run python main.py
     ```

7. **Restart Claude Desktop** (if needed):
   - Kill any running Claude Desktop instances via Task Manager (Windows) or `killall` (Linux).
   - Restart Claude Desktop to ensure it recognizes the running servers.

## Usage

### Running the Servers
Start both servers using:
```bash
cd ~/my-first-mcp-server
uv run python main.py
```
This launches:
- Leave Manager on `http://localhost:8000`.
- Sequential Thinking on `http://localhost:8001`.

**Note**: Keep the terminal open to maintain server uptime.

### Interacting via Claude Desktop
Use Claude Desktop’s query input field to send JSON queries to the servers via the Model Context Protocol. Below are examples for both servers, with a focus on **supply chain management** using the Sequential Thinking server.

#### Sequential Thinking MCP Server
- **Endpoint**: `http://localhost:8001/tool/sequential_thinking`
- **Purpose**: Plan a supply chain by breaking it into steps, revising plans, or exploring alternatives using MCP.
- **Input**: Paste JSON queries into Claude Desktop’s query field and submit.

**Example: Plan a Supply Chain for a Smartwatch**

1. **Define Objective**:
   ```json
   {
     "thought": "Define objective: Plan a cost-efficient supply chain for a new smartwatch, ensuring global delivery within 5 months.",
     "nextThoughtNeeded": true,
     "thoughtNumber": 1,
     "totalThoughts": 8
   }
   ```
   - Submit in Claude Desktop (e.g., paste into the query field and click “Send”).
   - Copy the `sessionId` (e.g., `123e4567-...`) from the response.

2. **Select Suppliers**:
   ```json
   {
     "sessionId": "<sessionId>",
     "thought": "Select suppliers: Source microchips from Supplier X (Taiwan), displays from Supplier Y (South Korea), batteries from Supplier Z (China).",
     "nextThoughtNeeded": true,
     "thoughtNumber": 2,
     "totalThoughts": 8
   }
   ```
   - Replace `<sessionId>` with the ID from Step 1.

3. **Plan Manufacturing**:
   ```json
   {
     "sessionId": "<sessionId>",
     "thought": "Plan manufacturing: Assemble smartwatches in Factory A (Vietnam) for low labor costs and supplier proximity.",
     "nextThoughtNeeded": true,
     "thoughtNumber": 3,
     "totalThoughts": 8
   }
   ```

4. **Revise Supplier**:
   ```json
   {
     "sessionId": "<sessionId>",
     "thought": "Revised: Switch battery supplier to Supplier W (Japan) for better quality, despite 10% higher cost.",
     "nextThoughtNeeded": true,
     "thoughtNumber": 2,
     "totalThoughts": 8,
     "isRevision": true,
     "revisesThought": 2
   }
   ```

5. **Explore Alternative Logistics (Branch)**:
   ```json
   {
     "sessionId": "<sessionId>",
     "thought": "Alternative: Use air freight for distribution to Europe to ensure 7-day delivery.",
     "nextThoughtNeeded": true,
     "thoughtNumber": 4,
     "totalThoughts": 8,
     "branchFromThought": 3,
     "branchId": "air_freight"
   }
   ```

6. **Plan Inventory**:
   ```json
   {
     "sessionId": "<sessionId>",
     "thought": "Plan inventory: Maintain 20,000 units in regional warehouses (USA, Europe, Asia) with just-in-time delivery.",
     "nextThoughtNeeded": true,
     "thoughtNumber": 5,
     "totalThoughts": 8
   }
   ```

7. **Mitigate Risks**:
   ```json
   {
     "sessionId": "<sessionId>",
     "thought": "Mitigate risks: Dual-source microchips and maintain 15% buffer inventory for supply disruptions.",
     "nextThoughtNeeded": true,
     "thoughtNumber": 6,
     "totalThoughts": 10,
     "needsMoreThoughts": true
   }
   ```

8. **Set Timeline**:
   ```json
   {
     "sessionId": "<sessionId>",
     "thought": "Set timeline: Supplier contracts by Month 1, manufacturing by Month 3, distribution by Month 4.",
     "nextThoughtNeeded": false,
     "thoughtNumber": 7,
     "totalThoughts": 10
   }
   ```

**Tips**:
- **Session ID**: Save the `sessionId` after the first query for use in subsequent queries.
- **Claude Desktop Format**: If required, prepend the JSON with:
  ```
  POST http://localhost:8001/tool/sequential_thinking
  ```
  Example:
  ```
  POST http://localhost:8001/tool/sequential_thinking
  {
    "thought": "Define objective: Plan a cost-efficient supply chain for a new smartwatch, ensuring global delivery within 5 months.",
    "nextThoughtNeeded": true,
    "thoughtNumber": 1,
    "totalThoughts": 8
  }
  ```
- **Customization**: Modify `thought` content for other supply chains (e.g., food, pharmaceuticals). Example for food:
  ```json
  {
    "thought": "Define objective: Plan a cold-chain supply chain for fresh produce, ensuring delivery within 48 hours.",
    "nextThoughtNeeded": true,
    "thoughtNumber": 1,
    "totalThoughts": 8
  }
  ```

#### Leave Manager MCP Server
- **Endpoint**: `http://localhost:8000`
- **Purpose**: Manage employee leaves via a mock database (`employee_leaves.json`) using MCP.
- **Example Queries**:
  - Check leave balance:
    ```json
    {
      "employee_id": "E001"
    }
    ```
    Send to `http://localhost:8000/tool/get_leave_balance`.
  - Apply for leave:
    ```json
    {
      "employee_id": "E001",
      "leave_dates": ["2025-06-01", "2025-06-02"]
    }
    ```
    Send to `http://localhost:8000/tool/apply_leave`.
  - Get leave history:
    ```json
    {
      "employee_id": "E001"
    }
    ```
    Send to `http://localhost:8000/tool/get_leave_history`.

## Extending the Project

- **Persistence for Sequential Thinking**: Add JSON or database storage to save supply chain plans, similar to `employee_leaves.json`.
- **Claude Desktop Automation**: Create a script to manage `sessionId` and streamline query input.
- **Visualization**: Generate supply chain flowcharts or timelines from Sequential Thinking data.
- **Metrics**: Enhance `sequential_thinking` to calculate costs or lead times from thoughts.