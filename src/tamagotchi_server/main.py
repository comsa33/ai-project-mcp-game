from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("weather")

@mcp.tool()
async def main():
    print("Hello from ai-project-mcp-game!")


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
