from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from typing import Optional
from datetime import datetime
from zoneinfo import ZoneInfo

router = APIRouter()


# Responds with "Hello World!" in plain text or JSON.
#   If a valid 'tz' query parameter is provided, includes the current time in that timezone.
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
            return JSONResponse({"error": f"Invalid timezone '{tz}'."}, status_code=400)

    # handles compound values in the accept header
    if "application/json" in accept:
        return JSONResponse({"message": message})
    else:
        return PlainTextResponse(message)
