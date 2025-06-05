from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from . import tasks
import httpx
import asyncio
from urllib.parse import quote
from . import helpers
from contextlib import asynccontextmanager
from . import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect redis
    await redis_client.connect_redis()
    yield
    # disconnect redis
    await redis_client.disconnect_redis()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SESSION_HEADERS = {
    "Referer": "https://megacloud.blog/",
    "Origin": "https://megacloud.blog",
}


@app.get("/getSource")
async def get_stream_url(path: str):
    base_url = "https://hianimez.to"
    page_url = f"{base_url}/{path}"

    encoded_id = helpers.encode_safe_string(path)

    # Check if the task is already in progress or completed or queued
    task = await redis_client.redis.get(encoded_id)
    if task and task != "failure":
        return {
            "task_id": encoded_id,
        }

    task = tasks.get_stream_url.apply_async(
        args=[page_url, encoded_id],
        task_id=encoded_id,
        queue="celery",
        expires=3600 * 12,
    )

    await redis_client.redis.set(task.id, "queued", ex=3600 * 12)
    return {"task_id": task.id}


@app.get("/task/{task_id}")
async def get_source_result(task_id: str):
    task = tasks.get_stream_url.AsyncResult(task_id)
    return {
        "task_id": task.id,
        "state": task.state,
        "result": task.result if task.ready() else None,
        "error": str(task.info) if task.failed() else None,
    }


@app.get("/proxy_hls/{path}")
async def proxy_hls(request: Request, path: str, base_url: str):
    try:
        return await stream_proxy(path, base_url, request)

    except httpx.RequestError as e:
        return StreamingResponse(f"Error: {str(e)}", status_code=502)



async def stream_proxy(path: str, base_url: str, request: Request):
    url = f"{base_url}/{path}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Propagate User-Agent + custom session headers
        headers = {
            "User-Agent": request.headers.get("User-Agent", ""),
            **SESSION_HEADERS,
        }

        # Make the streaming request
        resp = await client.get(url, headers=headers, timeout=10.0)

        # Raise if 4xx or 5xx
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "application/octet-stream")

        headers = {"Cache-Control": "public, max-age=86400"}

        # Check if it's an .m3u8 playlist
        if "application/vnd.apple.mpegurl" in content_type or path.endswith(".m3u8"):
            base = base_url
            original_lines = resp.text.splitlines()

            async def m3u8_stream():
                for line in original_lines:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        safe_path = quote(line.split("/")[-1])
                        proxy_line = f"/proxy_hls/{safe_path}?base_url={quote(base)}"
                        yield proxy_line + "\n"
                    else:
                        yield line + "\n"
                    await asyncio.sleep(0)  # yield control for cooperative multitasking

            return StreamingResponse(
                m3u8_stream(),
                media_type="application/vnd.apple.mpegurl",
                headers=headers,
            )

        # For .ts and other media chunks
        return StreamingResponse(
            resp.aiter_bytes(), media_type=content_type, headers=headers
        )


