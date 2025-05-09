from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter()


# This is a simple example of a FastAPI route that returns "Hello World!".
@router.get("/helloworld", response_class=PlainTextResponse)
async def hello_world():
    return "Hello World!"
