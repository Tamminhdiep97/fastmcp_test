# math_server.py
from fastmcp import FastMCP
from loguru import logger

import config as cfg

mcp = FastMCP("Math")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    logger.info("Run add Tool")
    return a + b


@mcp.tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    logger.info("Run multiply Tool")
    return a * b


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=cfg.math_port, host=cfg.mcp_host)
