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

# Initialize FastMCP, passing the app directly.
# The streamable_http_path argument was removed to fix the DeprecationWarning.
# The library defaults to "/mcp", which is what we need.
mcp = FastMCP(app) 


# --- Mandatory Validation Tool ---
@mcp.tool(
    name="validate",
    description="Validates the server connection for the Puch AI platform."
)
async def validate(token: str) -> str:
    """
    This tool is required by the Puch AI hackathon platform.
    When a user connects, Puch AI calls this tool to verify the server owner.
    It securely loads the owner's phone number from the .env file.
    """
    owner_phone_number = os.getenv("OWNER_PHONE_NUMBER")

    # --- DEBUGGING LOG ---
    print(f"--- VALIDATION CHECK ---")
    if owner_phone_number:
        print(f"Found OWNER_PHONE_NUMBER ending in: ...{owner_phone_number[-4:]}")
    else:
        print(f"CRITICAL ERROR: OWNER_PHONE_NUMBER environment variable is NOT SET or is empty!")
    # --- END DEBUGGING LOG ---

    if not owner_phone_number:
        raise ValueError("OWNER_PHONE_NUMBER not found in environment!")
    
    print(f"✅ Validation successful for token: {token}")
    return owner_phone_number


# --- Root Endpoint (for easy testing) ---
@app.get("/")
def read_root():
    """
    A simple homepage to easily check if the server is running.
    """
    return {"message": "MCP Server is running! ✨"}
