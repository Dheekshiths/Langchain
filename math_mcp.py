from fastmcp import FastMCP
import math

mcp = FastMCP("Math")


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def square_root(num: float) -> float:
    """Calculate the square root of a number."""
    if num < 0:
        raise ValueError("Cannot calculate the square root of a negative number.")
    return math.sqrt(num)


if __name__ == "__main__":
    mcp.run(transport="stdio")