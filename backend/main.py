import os, uuid, redis, json, asyncio, threading
from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import Request
from .rag_qa import ask_question
from .celery_tasks import process_pdf

app = FastAPI()
app.mount("/static", StaticFiles(directory="backend/templates"), name="static")
templates = Jinja2Templates(directory="backend/templates")

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile):
    job_id = str(uuid.uuid4())
    out_path = os.path.join(UPLOAD_FOLDER, f"{job_id}_{file.filename}")
    with open(out_path, "wb") as f:
        f.write(await file.read())
    process_pdf.delay(out_path, job_id)
    return {"job_id": job_id}


@app.post("/ask")
async def ask_question_endpoint(data: dict):
    question = data.get("question")
    if not question:
        return {"answer": "No question provided"}
    answer = ask_question(question)
    return {"answer": answer}


@app.websocket("/ws/{job_id}")
async def websocket_endpoint(ws: WebSocket, job_id: str):
    await ws.accept()
    pubsub = r.pubsub()
    pubsub.subscribe(f"progress_{job_id}")

    try:
        while True:
            msg = pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if msg:
                data = json.loads(msg["data"])
                await ws.send_text(json.dumps({"update": data}))
            await asyncio.sleep(0.1)
    except Exception as e:
        print("WebSocket error:", e)
    finally:
        await ws.close()
