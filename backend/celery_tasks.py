import os, redis, json
from celery import Celery
from .extract_text import extract_text_from_pdf
from .chunking import chunk_text
from .indexing import index_chunks

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

"""
It will publish each progress it track to websocket
"""
def publish(job_id, phase, percent, message):
    r.publish(f"progress_{job_id}", json.dumps({
        "phase": phase,
        "percent": percent,
        "message": message
    }))


"""
celery take task from redis as soon as new task assigned to redis
"""
@celery.task
def process_pdf(pdf_path, job_id):
    # Extract
    txt_path, pages = extract_text_from_pdf(pdf_path)
    for i in range(1, pages + 1):
        publish(job_id, "extraction", int(i / pages * 100), f"Extracted page {i}/{pages}")

    # Chunking
    chunks = chunk_text(txt_path)
    for i, _ in enumerate(chunks, start=1):
        publish(job_id, "chunking", int(i / len(chunks) * 100), f"Chunk {i}/{len(chunks)} ready")

    # Indexing
    total_chunks = len(chunks)
    for i in range(1, total_chunks + 1):
        publish(job_id, "indexing", int(i / total_chunks * 100), f"Indexing chunk {i}/{total_chunks}")

    index_chunks(chunks, source_name=os.path.basename(pdf_path), job_id=job_id)
    publish(job_id, "indexing", 100, "Indexing complete!")
    return {"status": "done"}
