from fastapi import FastAPI, Request, HTTPException
from sse_starlette.sse import EventSourceResponse
from config import settings
from client_a2a import stream

app = FastAPI(
    title="KGraph Agent",
    description="An agent for querying using KGraph",
    version=getattr(settings, "APP_VERSION", "0.0.1")
)


@app.post("/chat")
async def query_chat_kgraph(request: Request):
    """
    Query the KGraph with user input.
    Args:
        request: The HTTP request containing the user input.
    """
    try:

        data = await request.json()
        user_input = data.get("user_input")

        if not user_input:
            raise HTTPException(
                status_code=400,
                detail="Query parameter 'query' is required."
            )
        return EventSourceResponse(stream(query=user_input))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
