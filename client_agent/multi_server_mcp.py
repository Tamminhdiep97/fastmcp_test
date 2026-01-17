import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient

# from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from loguru import logger

import config as cfg


async def main():
    memory = MemorySaver()
    client = MultiServerMCPClient(
        {
            "mcp_server_1": {
                "url": f"{cfg.mcp_host}:{cfg.math_port}/mcp",
                "transport": "streamable-http",
            },
            "mcp_server_2": {
                "url": f"{cfg.mcp_host}:{cfg.weather_port}/mcp",
                "transport": "streamable-http",
            },
        }
    )
    tools = await client.get_tools()
    model = ChatOpenAI(
        model=os.getenv("TOOL_LLM_NAME"),
        openai_api_key=os.getenv("API_KEY", "EMPTY"),
        openai_api_base=os.getenv("TOOL_LLM_URL"),
        temperature=0,
    )

    agent = create_react_agent(
        model,
        prompt=cfg.SYSTEM_INSTRUCTION,
        tools=tools,
        checkpointer=memory,
    )

    math_response = await agent.ainvoke(
        {"messages": "what's (393 + 57) x 12?"},
        config={"configurable": {"thread_id": "id_1"}},
    )
    weather_response = await agent.ainvoke(
        {"messages": "what is the weather in nyc?"},
        config={"configurable": {"thread_id": "id_2"}},
    )

    # Convert complex objects to dictionaries and format as JSON
    def serialize_response(response):
        if isinstance(response, dict):
            result = {}
            for key, value in response.items():
                if hasattr(value, "__dict__") or isinstance(value, list):
                    if isinstance(value, list):
                        result[key] = [
                            serialize_response(item)
                            if isinstance(item, (dict, list))
                            else str(item)
                            for item in value
                        ]
                    else:
                        result[key] = {
                            k: serialize_response(v)
                            if isinstance(v, (dict, list))
                            else str(v)
                            for k, v in value.__dict__.items()
                        }
                else:
                    result[key] = value
            return result
        return str(response)

    serialized_math = serialize_response(math_response)
    serialized_weather = serialize_response(weather_response)

    logger.info("math response:")
    # logger.info(json.dumps(serialized_math, indent=2))
    for i in range(len(serialized_math["messages"])):
        logger.info(serialized_math["messages"][i])
    logger.info("weather response:")
    for i in range(len(serialized_weather["messages"])):
        logger.info(serialized_weather["messages"][i])


if __name__ == "__main__":
    asyncio.run(main())
