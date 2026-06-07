import asyncio

if hasattr(asyncio, "WindowsProactorEventLoopPolicy"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsProactorEventLoopPolicy()
    )

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.search import google_search


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Serve frontend assets under /static to avoid conflicting with API routes
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class SearchRequest(BaseModel):
    query: str


@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html", media_type="text/html")


@app.get("/api/status")
def health():
    return {"status": "ok"}

@app.post("/search")
async def search(request: SearchRequest):

    results = await google_search(
        request.query
    )

    return {
        "query": request.query,
        "results": results
    }

