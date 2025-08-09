import os
from fastapi import FastAPI
from fastmcp import FastMCP
from dotenv import load_dotenv # Import the new library

# Load all the variables from the .env file
load_dotenv()

# --- Server Setup ---
app = FastAPI(
    title="My Puch AI MCP Server",
    description="A collection of useful media and document tools.",
)
mcp = FastMCP(app)


# --- Mandatory Validation Tool ---
@mcp.tool(
    name="validate",
    description="Validates the server connection for the Puch AI platform."
)
async def validate(token: str) -> str:
    """
    This tool is required for Puch AI to connect to your server.
    It securely loads the phone number from the .env file.
    """
    # Securely get the phone number from the environment variables
    owner_phone_number = os.getenv("OWNER_PHONE_NUMBER")

    if not owner_phone_number:
        # This is a fallback in case the .env file is missing
        raise ValueError("OWNER_PHONE_NUMBER not found in .env file!")
    
    print(f"✅ Validation successful for token: {token}")
    return owner_phone_number


# --- Root Endpoint (for easy testing) ---
@app.get("/")
def read_root():
    return {"message": "MCP Server is running! ✨"}