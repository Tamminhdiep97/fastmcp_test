# Create server
import os
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from loguru import logger


import config as cfg


async def main():
    # Use configuration from config.py
    model_name = os.getenv("TOOL_LLM_NAME", "gpt-4.1")
    api_key = os.getenv("API_KEY", "empty")
    base_url = os.getenv("TOOL_LLM_URL", "empty")

    # Create the model with the configured parameters
    model = ChatOpenAI(
        model=model_name,
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0,
    )

    # The streamablehttp_client connects to the MCP server, not the LLM API
    async with streamablehttp_client(f"{cfg.mcp_host}:{cfg.math_port}/mcp") as (
        read,
        write,
        _,
    ):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create agent with the configured model
            agent = create_agent(
                model,
                tools,
                system_prompt=cfg.SYSTEM_INSTRUCTION,
            )
            math_response = await agent.ainvoke({"messages": "what's (11 + 17) x 19?"})
            logger.info(f"math response: {math_response}")
            logger.info(f"message response: {math_response['messages']}")
            for ith, item in enumerate(math_response["messages"]):
                logger.info(f"ith: {ith}, message: {item}")


if __name__ == "__main__":
    asyncio.run(main())
