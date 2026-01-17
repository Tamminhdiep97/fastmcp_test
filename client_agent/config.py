import os

host = "localhost"
port = 10000

os.environ["model_source"] = "OpenAi"
os.environ["TOOL_LLM_URL"] = "http://localhost:11434/v1"
# os.environ["TOOL_LLM_NAME"] = "qwen3-next:80b-cloud"
# os.environ["TOOL_LLM_NAME"] = "qwen3:4b"
os.environ["TOOL_LLM_NAME"] = "gemini-3-flash-preview:cloud"
# os.environ["TOOL_LLM_NAME"] = "nemotron-3-nano:30b-cloud"

os.environ["API_KEY"] = "hi"

mcp_host = "http://0.0.0.0"

weather_port = 8081
math_port = 7999

SYSTEM_INSTRUCTION = """
You are a helpful agent who can use tools to get result to answer question of user
"""
