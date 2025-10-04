import os, json, time, hashlib, logging, threading
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from summarizer import summarize_change

ROOT = os.path.dirname(__file__)
TARGETS_FILE = os.path.join(ROOT, "targets.json")
STATE_FILE = os.path.join(ROOT, "state.json")
ALERTS_FILE = os.path.join(ROOT, "alerts.log")

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

# ----------------- helpers -----------------
def _load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_targets():
    return _load_json(TARGETS_FILE) or []

def add_target(obj):
    targets = load_targets()
    targets.append(obj)
    _save_json(TARGETS_FILE, targets)
    return obj

def fetch_html(url, timeout=10, retries=3, backoff=1.5):
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            r = requests.get(url, timeout=timeout, headers={"User-Agent":"Mozilla/5.0"})
            r.raise_for_status()
            return r.text
        except Exception as e:
            last_exc = e
            if attempt < retries:
                time.sleep(backoff * attempt)
    logging.error("fetch failed %s -> %s", url, last_exc)
    return None

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style", "noscript"]):
        s.decompose()
    return soup.get_text(separator=" ", strip=True)

def text_hash(t):
    return hashlib.sha256(t.encode("utf-8")).hexdigest()

# ----------------- core check function -----------------
def check_once():
    """
    Run a single check across targets.
    Returns list of new alert dicts (timestamp, id, url, summary).
    """
    targets = load_targets()
    state = _load_json(STATE_FILE) or {}
    new_alerts = []

    for t in targets:
        url = t.get("url")
        tid = t.get("id", url)
        html = fetch_html(url)
        if not html:
            continue
        txt = extract_text(html)
        h = text_hash(txt)
        prev = state.get(tid, {})
        prev_hash = prev.get("hash")
        prev_text = prev.get("text", "")
        if prev_hash != h:
            summary = summarize_change(prev_text, txt)
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            alert = {"timestamp": ts, "id": tid, "url": url, "summary": summary}
            new_alerts.append(alert)
            # append to alerts.log
            with open(ALERTS_FILE, "a", encoding="utf-8") as f:
                f.write(f"[{ts}] {tid} {url} -> {summary}\n")
            # update state
            state[tid] = {"hash": h, "text": txt, "last_seen": time.time()}
        else:
            logging.info("no change: %s", tid)

    _save_json(STATE_FILE, state)
    return new_alerts

# ----------------- alerts helper -----------------
def get_recent_alerts(limit=50):
    if not os.path.exists(ALERTS_FILE):
        return []
    with open(ALERTS_FILE, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    return lines[-limit:][::-1]

# ----------------- background worker -----------------
_bg_thread = None
_stop_event = None

def start_background(interval=60):
    global _bg_thread, _stop_event
    if _bg_thread and _bg_thread.is_alive():
        return False
    _stop_event = threading.Event()
    def loop():
        while not _stop_event.is_set():
            try:
                check_once()
            except Exception as e:
                logging.exception("Background monitor error: %s", e)
            _stop_event.wait(interval)
    _bg_thread = threading.Thread(target=loop, daemon=True)
    _bg_thread.start()
    return True

def stop_background():
    global _bg_thread, _stop_event
    if _stop_event:
        _stop_event.set()
    if _bg_thread:
        _bg_thread.join(timeout=2)
    _bg_thread = None
    _stop_event = None
    return True
