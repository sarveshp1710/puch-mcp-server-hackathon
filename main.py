import os
from fastapi import FastAPI
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# --- Server Setup ---
app = FastAPI(
    title="My Puch AI MCP Server",
    description="A collection of useful media and document tools.",
)
mcp = FastMCP() # Initialize FastMCP without the app first

# --- Mount the MCP Endpoint ---
# This is the new, crucial line.
# It tells FastAPI to direct all traffic from "/mcp" to the fastmcp library.
app.mount("/mcp", mcp.app)


# --- Mandatory Validation Tool ---
@mcp.tool(
    name="validate",
    description="Validates the server connection for the Puch AI platform."
)
async def validate(token: str) -> str:
    """
    This tool is required for Puch AI to connect to your server.
    It securely loads the phone number from the environment.
    """
    owner_phone_number = os.getenv("OWNER_PHONE_NUMBER")

    if not owner_phone_number:
        raise ValueError("OWNER_PHONE_NUMBER not found in environment!")
    
    print(f"✅ Validation successful for token: {token}")
    return owner_phone_number


# --- Root Endpoint (for easy testing) ---
@app.get("/")
def read_root():
    return {"message": "MCP Server is running! ✨"}