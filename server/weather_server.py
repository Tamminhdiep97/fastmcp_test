from fastmcp import FastMCP
from loguru import logger

import config as cfg

mcp = FastMCP("Weather")


@mcp.tool
async def get_weather(location: str) -> str:
    """Get weather for location."""
    logger.info("running weather tools")
    return f"It's always sunny in {location}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=cfg.weather_port, host=cfg.mcp_host)
