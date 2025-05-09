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


@router.get("/helloworld")
async def hello_world(request: Request, tz: Optional[str] = Query(None)):
    """
    Return a 'Hello World!' message.

    - Returns plain text or JSON depending on the Accept header.
    - Accepts an optional `tz` query parameter (IANA timezone string).
    - If provided and valid, includes current time in the specified timezone.
    """

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


@router.post("/unravel")
async def unravel(request: Request):
    """
    Recursively flattens a nested JSON object.

    - Accepts a JSON body (must be an object/dict).
    - Returns a flat list of all keys and values, in traversal order.
    - Enforces a maximum recursion depth of 10.
    """

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


@router.post("/roll")
async def roll():
    """
    Triggers a rolling update via GitHub webhook.

    - Responds with HTTP 202 immediately.
    - In the background, pulls the latest code from the `main` branch.
    - Restarts the server if `CONTRAILS_RESTART_ON_UPDATE` is not set to '0'.
    """

    asyncio.create_task(perform_roll_restart())
    return JSONResponse(
        content={"message": "Rolling update triggered"}, status_code=202
    )


async def perform_roll_restart():
    """
    Performs the rolling update logic:

    - Waits briefly to ensure the webhook response is returned cleanly.
    - Runs `git pull` to fetch the latest code from the main branch.
    - Exits the process with code 0 to trigger a restart (when used with a process wrapper).
    - Honors the CONTRAILS_RESTART_ON_UPDATE env var to disable restarts in dev mode.
    """

    print("[roll] checking restart conditions...")
    if os.getenv("CONTRAILS_RESTART_ON_UPDATE", "1") == "0":
        print("[roll] Skipping restart: flag is set to 0")
        return

    await asyncio.sleep(0.5)
    print("[roll] Pulling latest and restarting")
    subprocess.run(["git", "pull", "origin", "main"], check=True)
    sys.exit(0)
