import os
from fastapi import FastAPI
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# --- Server Setup ---
# Create the main FastAPI web application instance. This is the core of our server.
app = FastAPI(
    title="My Puch AI MCP Server",
    description="A collection of useful media and document tools.",
)

# Initialize the FastMCP library, passing our FastAPI app directly to it.
# This is the most stable way to integrate the two and avoids the mounting bug.
# The library will automatically create the /mcp endpoint for us.
mcp = FastMCP(app) 


# --- Mandatory Validation Tool ---
# The @mcp.tool() decorator registers the function below as an AI tool.
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
    # os.getenv() safely reads the secret variable we set on Render (or from .env locally).
    # It will NOT be exposed in our code or on GitHub.
    owner_phone_number = os.getenv("OWNER_PHONE_NUMBER")

    # A safety check in case the environment variable isn't set.
    if not owner_phone_number:
        print("ERROR: OWNER_PHONE_NUMBER environment variable not found!")
        raise ValueError("OWNER_PHONE_NUMBER not found in environment!")
    
    # A log message to help us debug. This will show up in the Render logs.
    print(f"✅ Validation successful for token: {token}")
    return owner_phone_number


# --- Root Endpoint (for easy testing) ---
# The @app.get("/") decorator creates a simple homepage for our server.
@app.get("/")
def read_root():
    """
    A simple homepage to easily check if the server is running.
    You can visit this page in your web browser.
    """
    return {"message": "MCP Server is running! ✨"}
