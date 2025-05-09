from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, PlainTextResponse

router = APIRouter()


# Responds with "Hello World!" in plain text or JSON based on the client's Accept header
@router.get("/helloworld")
async def hello_world(request: Request):
    accept = request.headers.get("accept", "")

    # handles compound values in the accept header
    if "application/json" in accept:
        return JSONResponse({"message": "Hello World!"})
    else:
        return PlainTextResponse("Hello World!")
