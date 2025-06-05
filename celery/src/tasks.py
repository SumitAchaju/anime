from celery import Celery
import platform
from playwright.sync_api import sync_playwright
from redis import Redis
from . import helpers
import os

redis_url = os.getenv("REDIS_URL", "redis://redis:6379")


app = Celery("tasks", broker=redis_url, backend=redis_url)

if platform.system() == "Windows":
    app.conf.worker_pool = "solo"


redis_client = Redis(host="redis", port=6379, decode_responses=True)


def setRedisValue(task_id: str, status: str):
    redis_client.set(task_id, status, ex=3600 * 10)


@app.task(name="tasks.get_stream_url")
def get_stream_url(url: str, task_id: str) -> str | None:
    setRedisValue(task_id, "running")
    try:
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            context = browser.new_context(
                storage_state="state.json",
                user_agent=(
                    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0"
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 800},
            )

            context.add_init_script(helpers.init_script)

            page = context.new_page()
            request_urls = []
            tracks = []

                # Start listening for response
            def handle_response(response):
                if "getSources?id=" in response.url:
                    if "tracks" in response.json():
                        tracks.extend(response.json()["tracks"])

            page.on("request", lambda request: request_urls.append(request.url))
            page.on("response", handle_response)
            page.goto(url, wait_until="domcontentloaded", timeout=20_000)

            elapsed = 0
            m3u8_url = None
            page.wait_for_timeout(5_000)



            def find_m3u8():
                nonlocal m3u8_url
                for req_url in request_urls:
                    if "master.m3u8" in req_url:
                        m3u8_url = req_url
                        return True
                return False

            while elapsed <= 50_000:
                if find_m3u8():
                    break
                page.wait_for_timeout(5_000)
                elapsed += 5_000

            browser.close()
            setRedisValue(task_id, "finished")
            if m3u8_url is None:
                setRedisValue(task_id, "failure")
                return None
            return {"url": m3u8_url, "tracks": tracks}

    except Exception as e:
        setRedisValue(task_id, "failure")
        return str(e)
