from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from datetime import datetime
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DOMINIC_LAW = False


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received: {data}")
            await websocket.send_text(data)
            logger.info(f"Echoed back: {data}")
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    finally:
        try:
            await websocket.close()
        except RuntimeError:
            # Socket already closed (e.g. after disconnect)
            pass


@app.get("/")
async def root(event: str = None):
    logger.info(f"GET / called with event={event} at {datetime.now()}")
    return {
        "message": "Echo test API is running",
        "you_sent": event,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/echo")
async def echo_post(payload: dict):
    logger.info(f"POST /echo received payload: {payload}")
    return {
        "you_sent": payload,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/dominic")
async def set_dominic(payload: dict):
    global DOMINIC_LAW
    DOMINIC_LAW = payload.get("status", False)
    logger.info(f"DOMINIC_LAW set to {DOMINIC_LAW}")
    return {
        "DOMINIC_LAW": DOMINIC_LAW,
    }


@app.get("/dominic")
async def get_dominic():
    return {
        "status": DOMINIC_LAW,
    }


DOMINIC_UI_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Dominic Law — Registry</title>
<style>
  :root {
    --ink: #12181f;
    --ink-2: #1c2530;
    --parchment: #ece4d3;
    --parchment-dim: #cfc4a8;
    --brass: #b08d3e;
    --brass-bright: #d8b054;
    --red-seal: #8c2f2f;
    --red-seal-bright: #b23a3a;
    --line: rgba(176, 141, 62, 0.35);
  }
  * { box-sizing: border-box; }
  html, body { height: 100%; margin: 0; }
  body {
    background: radial-gradient(ellipse at 50% -10%, #1e2836 0%, var(--ink) 55%, #0b0f14 100%);
    color: var(--parchment);
    font-family: 'Iowan Old Style', 'Palatino Linotype', Georgia, serif;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 32px 20px;
  }
  .registry { width: 100%; max-width: 480px; }
  .eyebrow {
    text-align: center;
    font-family: 'Courier New', ui-monospace, monospace;
    letter-spacing: 0.35em;
    font-size: 11px;
    color: var(--brass);
    text-transform: uppercase;
    margin-bottom: 14px;
  }
  .card {
    background: linear-gradient(180deg, var(--ink-2), #171f28);
    border: 1px solid var(--line);
    border-radius: 4px;
    padding: 40px 36px 32px;
    position: relative;
    box-shadow: 0 30px 60px -20px rgba(0,0,0,0.7), inset 0 1px 0 rgba(255,255,255,0.03);
  }
  .card::before, .card::after {
    content: "";
    position: absolute;
    width: 10px;
    height: 10px;
    border: 1px solid var(--brass);
    opacity: 0.6;
  }
  .card::before { top: 10px; left: 10px; border-right: none; border-bottom: none; }
  .card::after { bottom: 10px; right: 10px; border-left: none; border-top: none; }
  h1 {
    font-size: 30px;
    text-align: center;
    margin: 0 0 4px;
    font-weight: 400;
    letter-spacing: 0.01em;
    color: var(--parchment);
  }
  h1 em { font-style: italic; color: var(--brass-bright); }
  .subtitle {
    text-align: center;
    font-size: 13px;
    color: var(--parchment-dim);
    margin: 0 0 28px;
    font-style: italic;
  }
  .divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--line), transparent);
    margin: 24px 0;
  }
  .seal-wrap { display: flex; justify-content: center; margin: 8px 0 28px; }
  .seal {
    width: 172px;
    height: 172px;
    border-radius: 50%;
    border: 3px double var(--red-seal-bright);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    position: relative;
    transition: border-color 0.5s ease, box-shadow 0.5s ease;
    box-shadow: 0 0 0 6px rgba(140,47,47,0.08), 0 10px 30px -8px rgba(0,0,0,0.6);
  }
  .seal.enacted {
    border-color: var(--brass-bright);
    box-shadow: 0 0 0 6px rgba(176,141,62,0.1), 0 10px 30px -8px rgba(0,0,0,0.6);
  }
  .seal-inner { font-family: 'Courier New', ui-monospace, monospace; letter-spacing: 0.08em; }
  .seal-status {
    font-size: 17px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--red-seal-bright);
    transition: color 0.5s ease;
  }
  .seal.enacted .seal-status { color: var(--brass-bright); }
  .seal-sub {
    font-size: 9px;
    color: var(--parchment-dim);
    margin-top: 6px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }
  .seal-code { font-size: 34px; margin-top: 8px; color: var(--parchment); }
  .control-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-bottom: 8px;
  }
  .switch {
    position: relative;
    width: 64px;
    height: 32px;
    border-radius: 20px;
    border: 1px solid var(--line);
    background: #0c1116;
    cursor: pointer;
    transition: background 0.3s ease;
    flex-shrink: 0;
  }
  .switch.enacted { background: rgba(176,141,62,0.15); }
  .switch:disabled { cursor: wait; opacity: 0.6; }
  .switch .knob {
    position: absolute;
    top: 3px;
    left: 3px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: var(--red-seal-bright);
    transition: transform 0.3s ease, background 0.3s ease;
  }
  .switch.enacted .knob { transform: translateX(32px); background: var(--brass-bright); }
  .control-label {
    font-family: 'Courier New', ui-monospace, monospace;
    font-size: 12px;
    letter-spacing: 0.08em;
    color: var(--parchment-dim);
    text-transform: uppercase;
    min-width: 84px;
  }
  .meta {
    text-align: center;
    font-family: 'Courier New', ui-monospace, monospace;
    font-size: 11px;
    color: var(--parchment-dim);
    margin-top: 22px;
    min-height: 16px;
  }
  .meta.error { color: var(--red-seal-bright); }
  .footnote {
    text-align: center;
    font-size: 11px;
    color: var(--parchment-dim);
    margin-top: 20px;
    font-style: italic;
    line-height: 1.5;
  }
</style>
</head>
<body>

<div class="registry">
  <div class="eyebrow">Registry of Standing Statutes</div>
  <div class="card">
    <h1>The <em>Dominic</em> Law</h1>
    <p class="subtitle">Status as recorded by the office of record</p>

    <div class="seal-wrap">
      <div class="seal" id="seal">
        <div class="seal-inner">
          <div class="seal-status" id="sealStatus">—</div>
          <div class="seal-sub">DOMINIC_LAW</div>
          <div class="seal-code" id="sealCode">?</div>
        </div>
      </div>
    </div>

    <div class="control-row">
      <span class="control-label">Repealed</span>
      <button class="switch" id="switchBtn" role="switch" aria-checked="false" aria-label="Toggle DOMINIC_LAW">
        <span class="knob"></span>
      </button>
      <span class="control-label">In effect</span>
    </div>

    <div class="meta" id="meta">Fetching current status…</div>
  </div>
</div>

<script>
  const seal = document.getElementById('seal');
  const sealStatus = document.getElementById('sealStatus');
  const sealCode = document.getElementById('sealCode');
  const switchBtn = document.getElementById('switchBtn');
  const meta = document.getElementById('meta');

  let currentStatus = null;
  let busy = false;

  function render(status) {
    currentStatus = status;
    seal.classList.toggle('enacted', !!status);
    switchBtn.classList.toggle('enacted', !!status);
    switchBtn.setAttribute('aria-checked', String(!!status));
    sealStatus.textContent = status ? 'In Effect' : 'Repealed';
    sealCode.textContent = status ? 'TRUE' : 'FALSE';
  }

  function setMeta(text, isError = false) {
    meta.textContent = text;
    meta.classList.toggle('error', isError);
  }

  async function fetchStatus() {
    setMeta('Fetching current status…');
    try {
      const res = await fetch('/dominic');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      render(!!data.status);
      setMeta(`Last confirmed ${new Date().toLocaleTimeString()}`);
    } catch (err) {
      setMeta(`Could not reach registry — ${err.message}`, true);
    }
  }

  async function setStatus(next) {
    if (busy) return;
    busy = true;
    switchBtn.disabled = true;
    setMeta('Filing update…');
    try {
      const res = await fetch('/dominic', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: next }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      render(!!data.DOMINIC_LAW);
      setMeta(`Filed ${new Date().toLocaleTimeString()}`);
    } catch (err) {
      setMeta(`Update failed — ${err.message}`, true);
    } finally {
      busy = false;
      switchBtn.disabled = false;
    }
  }

  switchBtn.addEventListener('click', () => {
    if (currentStatus === null) return;
    setStatus(!currentStatus);
  });

  fetchStatus();
</script>

</body>
</html>
"""


@app.get("/dominic/ui", response_class=HTMLResponse)
async def dominic_ui():
    return DOMINIC_UI_HTML
