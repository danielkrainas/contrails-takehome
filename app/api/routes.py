import asyncio
import subprocess
import sys
import os
from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import Optional, Any, List
from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter()


# Responds with "Hello World!" in plain text or JSON.
# If a valid 'tz' query parameter is provided, includes the current time in that timezone.
@router.get("/helloworld")
async def hello_world(request: Request, tz: Optional[str] = Query(None)):
    accept = request.headers.get("accept", "")
    message = "Hello World!"
    if tz:
        # If a timezone is provided, convert the current time to that timezone
        try:
            tz_info = ZoneInfo(tz)
            current_time = datetime.now(tz_info).isoformat()
            message += f" It is {current_time} in timezone {tz}."
        except Exception as e:
            return JSONResponse(
                content={"error": f"Invalid timezone '{tz}'."}, status_code=400
            )

    # handles compound values in the accept header
    if "application/json" in accept:
        return JSONResponse({"message": message})
    else:
        return PlainTextResponse(message)


# Recursively traverses a nested JSON object and returns a flat list containing all keys and values.
# Lists and nested dictionaries are fully unpacked in traversal order.
@router.post("/unravel")
async def unravel(request: Request):
    try:
        payload = await request.json()
        if not isinstance(payload, dict):
            return JSONResponse(
                content={"error": "Request payload must be a JSON object."},
                status_code=400,
            )
    except Exception:
        return JSONResponse(content={"error": "Invalid JSON payload."}, status_code=400)

    def flatten(obj: Any, depth: int = 0, max_depth: int = 10) -> List[Any]:
        if depth > max_depth:
            raise ValueError(f"Maximum recursion depth of {max_depth} exceeded.")

        result = []
        if isinstance(obj, dict):
            for key, value in obj.items():
                result.append(key)
                result.extend(flatten(value, depth + 1, max_depth))
        elif isinstance(obj, list):
            for item in obj:
                result.extend(flatten(item, depth + 1, max_depth))
        else:
            result.append(obj)

        return result

    flattened = []
    try:
        flattened = flatten(payload)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

    return JSONResponse(content=flattened)


# POST /roll endpoint used by a GitHub webhook to trigger a rolling update.
# It schedules a background task to pull the latest code and restart the server,
# and responds immediately with 202 to avoid breaking the webhook request.
@router.post("/roll")
async def roll():
    asyncio.create_task(perform_roll_restart())
    return JSONResponse(
        content={"message": "Rolling update triggered"}, status_code=202
    )


# Performs the rolling update logic:
# - Waits briefly to ensure the webhook caller receives a response
# - Runs `git pull` to fetch the latest code
# - Exits the process to trigger a restart loop (if enabled)
# Respects the CONTRAILS_RESTART_ON_UPDATE env var to allow dev-mode override.
async def perform_roll_restart():
    if os.getenv("CONTRAILS_RESTART_ON_UPDATE", "1") == "0":
        print("Skipping restart: CONTRAILS_RESTART_ON_UPDATE is set to 0")
        return

    await asyncio.sleep(0.5)
    subprocess.run(["git", "pull", "origin", "main"], check=True)
    try:
        sys.exit(0)
    except SystemExit:
        # This is expected when the process exits
        pass
