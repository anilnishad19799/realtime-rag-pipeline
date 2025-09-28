import os, uuid, redis, json
from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from .celery_tasks import process_pdf

app = FastAPI()
app.mount("/static", StaticFiles(directory="backend/templates"), name="static")
templates = Jinja2Templates(directory="backend/templates")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile):
    job_id = str(uuid.uuid4())
    out_path = f"uploads_{job_id}_{file.filename}"
    with open(out_path, "wb") as f:
        f.write(await file.read())
    process_pdf.delay(out_path, job_id)
    return {"job_id": job_id}

@app.websocket("/ws/{job_id}")
async def websocket_endpoint(ws: WebSocket, job_id: str):
    await ws.accept()
    pubsub = r.pubsub()
    pubsub.subscribe(f"progress_{job_id}")
    for msg in pubsub.listen():
        if msg["type"] == "message":
            await ws.send_text(json.dumps({"update": json.loads(msg["data"])}))
