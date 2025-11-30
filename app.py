import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import monitor_engine
from monitor_engine import TARGETS_FILE, ALERTS_FILE, STATE_FILE, _save_json

app = FastAPI(title="IntelAgent API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

# -------- API ROUTES --------

@app.get("/api/targets")
def api_get_targets():
    return JSONResponse(content=monitor_engine.load_targets())

@app.post("/api/targets")
async def api_add_target(request: Request):
    payload = await request.json()
    url = payload.get("url")
    if not url:
        return JSONResponse({"error": "missing URL"}, status_code=400)
    t = {"url": url, "id": url}
    monitor_engine.add_target(t)
    return {"ok": True, "target": t}

@app.post("/api/check")
def api_check():
    alerts = monitor_engine.check_once()
    return {"ok": True, "new_alerts": alerts}

@app.get("/api/alerts")
def api_alerts(limit: int = 50):
    lines = monitor_engine.get_recent_alerts(limit)
    return {"alerts": lines}

@app.post("/api/start")
async def api_start(request: Request):
    body = await request.json()
    interval = int(body.get("interval", 60))
    started = monitor_engine.start_background(interval)
    return {"started": started}

@app.post("/api/stop")
def api_stop():
    stopped = monitor_engine.stop_background()
    return {"stopped": stopped}

from monitor_engine import TARGETS_FILE, ALERTS_FILE, STATE_FILE, _save_json

@app.post("/api/clear-all")
async def clear_all():
    _save_json(TARGETS_FILE, [])
    open(ALERTS_FILE, "w").close()
    _save_json(STATE_FILE, {})
    return {"ok": True}
