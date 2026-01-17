# MCP Project

This is a Model Context Protocol (MCP) project split into two main components:

## Structure

- `server/`: Contains server-side implementations
- `client_agent/`: Contains client-side implementations

## Prerequisites

### Installing uv

This project uses `uv` for package management (not using anaconda). Install `uv` using the following commands:

```bash
# On Unix-like systems (Linux/macOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Or using pip (cross-platform)
pip install uv
```

For more information about uv, visit [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

## Setup

All components in this repository use uv for dependency management:

```bash
# Install dependencies for server
cd server
uv sync

# Install dependencies for client
cd ../client_agent
uv sync
```

## Model Configuration

This repository is configured to use Ollama as the language model service running locally. To use this project, you need to:

1. Install Ollama locally on your machine from [https://ollama.com](https://ollama.com)
2. Pull the required model(s) using `ollama pull <model-name>`
3. Ensure the Ollama service is running on `http://localhost:11434`

The model configuration is located in `client_agent/config.py` where you can adjust the model settings as needed. By default, it uses `gemini-3-flash-preview:cloud` but you can uncomment other models as needed.

### Site note

Model use in this repo is called **cloud model**, which is a special type of model that ollama will host on their cloud server somewhere and allow your cli to connect and get result from it

To use it

    1. First you have to signup an accound on ollama.com, use this link [ollama signup](https://signin.ollama.com/sign-up?)

    2. Then process to signin on your machine

```bash
ollama signin
```

    3. Pull your model

```bash
ollama pull gemini-3-flash-preview:cloud
```

## Running Examples

### Example 1: Math Server with Single Client

1. Start the math server:

```bash
cd server
uv run math_server.py
```

2. In a new terminal, run the client to test:

```bash
cd client_agent
uv run client.py
```

This example demonstrates communication between the math server and a single client, calculating `(11 + 17) x 19`.

### Example 2: Multiple Servers with Multi-Server Client

1. Start both servers in **separate** terminals:

```bash
# Terminal 1 - Start math server
cd server
uv run math_server.py
```


```bash
# Terminal 2 - Start weather server
cd server
uv run weather_server.py
```

2. In a third terminal, run the multi-server client:

```bash
cd client_agent
uv run multi_server_mcp.py
```

This example demonstrates how a single client can connect to multiple MCP servers simultaneously, performing both mathematical calculations and weather queries.
