import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import monitor_engine

app = FastAPI(title="IntelAgent API")

# Static files (dashboard)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def index():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/api/targets")
def api_get_targets():
    return JSONResponse(content=monitor_engine.load_targets())

@app.post("/api/targets")
async def api_add_target(request: Request):
    payload = await request.json()
    url = payload.get("url")
    if not url:
        return JSONResponse({"error": "url required"}, status_code=400)
    t = {"url": url, "id": payload.get("id", url), "notes": payload.get("notes", "")}
    monitor_engine.add_target(t)
    return {"ok": True, "target": t}

@app.post("/api/check")
def api_check():
    new_alerts = monitor_engine.check_once()
    return {"ok": True, "new_alerts": new_alerts}

@app.get("/api/alerts")
def api_alerts(limit: int = 50):
    lines = monitor_engine.get_recent_alerts(limit)
    return {"alerts": lines}

@app.post("/api/start")
async def api_start(request: Request):
    body = await request.json()
    interval = int(body.get("interval", 60))
    started = monitor_engine.start_background(interval)
    return {"started": started, "interval": interval}

@app.post("/api/stop")
def api_stop():
    stopped = monitor_engine.stop_background()
    return {"stopped": stopped}

@app.post("/api/alerts/clear")
def api_clear_alerts():
    open("alerts.log", "w", encoding="utf-8").close()  # empty file
    return {"ok": True}