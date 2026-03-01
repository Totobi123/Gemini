import http.server, socketserver, json, threading, time, os, socket, sys
import requests
from datetime import datetime

# --- Configuration (from genx_gui.py) ---
DEFAULT_TIMEOUT = 5
LATENCY_GREEN = 200  # ms
LATENCY_YELLOW = 500 # ms
DEFAULT_INTERVAL = 1.0 # s

state = {
    "status": "IDLE",
    "target": "http://example.com",
    "interval": DEFAULT_INTERVAL,
    "last_latency": 0,
    "total_checks": 0,
    "success_checks": 0,
    "failed_checks": 0,
    "health_pct": 100,
    "log": [],
    "running": False
}

def monitor_task():
    while state["running"]:
        try:
            start_time = time.time()
            response = requests.get(state["target"], timeout=DEFAULT_TIMEOUT)
            latency = int((time.time() - start_time) * 1000)
            
            state["last_latency"] = latency
            state["total_checks"] += 1
            
            timestamp = datetime.now().strftime("[%H:%M:%S]")
            
            if response.status_code == 200:
                state["success_checks"] += 1
                if latency < LATENCY_GREEN:
                    level = "SUCCESS"
                    status_text = "HEALTHY"
                elif latency < LATENCY_YELLOW:
                    level = "WARNING"
                    status_text = "SLOW"
                else:
                    level = "ERROR"
                    status_text = "LAGGING"
            else:
                state["failed_checks"] += 1
                level = "ERROR"
                status_text = f"HTTP {response.status_code}"

            msg = f"{timestamp} [MONITOR] {status_text} | Latency: {latency}ms | Code: {response.status_code}"
            state["log"].append({"msg": msg, "level": level})
            if len(state["log"]) > 100: state["log"].pop(0)

        except requests.exceptions.RequestException as e:
            state["failed_checks"] += 1
            state["total_checks"] += 1
            timestamp = datetime.now().strftime("[%H:%M:%S]")
            msg = f"{timestamp} [ERROR] CONNECTION ERROR: {str(e)}"
            state["log"].append({"msg": msg, "level": "ERROR"})
            if len(state["log"]) > 100: state["log"].pop(0)
        
        # Calculate health percentage
        if state["total_checks"] > 0:
            state["health_pct"] = int((state["success_checks"] / state["total_checks"]) * 100)

        time.sleep(state["interval"])

# --- WEB SERVER ---
def get_free_port(start_port=8080):
    port = start_port
    while port < 65535:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            port += 1
    return 0

PORT = get_free_port()

HTML_DASHBOARD = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenX Network Monitor</title>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; padding: 20px; overflow-x: hidden; }
        .container { max-width: 900px; margin: 0 auto; border: 2px solid #0f0; padding: 20px; box-shadow: 0 0 30px rgba(0,255,0,0.1); position: relative; }
        .scanline { position: absolute; top: 0; left: 0; width: 100%; height: 5px; background: rgba(0,255,0,0.2); opacity: 0.5; animation: scan 3s linear infinite; pointer-events: none; }
        @keyframes scan { 0% { top: 0%; } 100% { top: 100%; } }
        
        h1 { text-align: center; border-bottom: 1px solid #0f0; padding-bottom: 15px; text-shadow: 0 0 10px #0f0; letter-spacing: 2px; }
        
        .control-panel { border: 1px solid #333; padding: 15px; margin-bottom: 20px; display: flex; gap: 10px; align-items: center; }
        input { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px; font-family: monospace; flex-grow: 1; }
        button { background: #000; border: 1px solid #0f0; color: #0f0; padding: 10px 20px; font-family: monospace; cursor: pointer; font-weight: bold; }
        button:hover { background: #0f0; color: #000; }
        
        .log-box { height: 300px; overflow-y: scroll; border: 1px solid #333; padding: 10px; font-size: 12px; margin-top: 20px; background: rgba(0,20,0,0.3); box-shadow: inset 0 0 20px #000; }
        .log-box div { margin-bottom: 4px; border-bottom: 1px solid rgba(0,255,0,0.1); padding-bottom: 2px; }
        
        .liquid-container { display: flex; justify-content: center; margin: 30px 0; }
        .liquid-gauge {
            width: 150px; height: 150px; border-radius: 50%; border: 4px solid #333;
            position: relative; overflow: hidden; background: #000;
            box-shadow: 0 0 30px rgba(0,255,0,0.2);
        }
        .liquid {
            position: absolute; left: 0; bottom: 0; width: 100%; height: 100%;
            background: #0f0; opacity: 0.8;
            transition: height 0.5s ease-in-out;
            box-shadow: 0 0 50px #0f0;
        }
        .liquid::before {
            content: ''; position: absolute; left: -50%; top: -10px; width: 200%; height: 20px;
            background: #000; opacity: 0.3; border-radius: 50%;
            animation: wave 2s linear infinite;
        }
        @keyframes wave { 0% { transform: translateX(0); } 100% { transform: translateX(50%); } }
        
        .gauge-text {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            z-index: 10; font-size: 24px; font-weight: bold; color: #fff; text-shadow: 0 0 10px #000;
        }
        
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 20px; text-align: center; }
        .stat-box { border: 1px solid #333; padding: 10px; }
        .stat-val { font-size: 20px; font-weight: bold; margin-top: 5px; }
        
        .grid-bg { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: repeating-linear-gradient(0deg, transparent, transparent 1px, #001100 1px, #001100 2px); z-index: -1; pointer-events: none; }
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="container">
        <div class="scanline"></div>
        <h1>// GENX NETWORK MONITOR v1.0 //</h1>
        
        <div class="control-panel">
            <input type="text" id="target" value="http://example.com" placeholder="Target URL or IP">
            <input type="number" id="interval" value="1000" style="width: 80px;" placeholder="ms">
            <button id="start-btn" onclick="toggleMonitor()">>> START <<</button>
        </div>
        
        <div class="liquid-container">
            <div class="liquid-gauge">
                <div id="liquid-fill" class="liquid"></div>
                <div id="gauge-text" class="gauge-text">100%</div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-box">
                <div style="color:#0f0">SUCCESS</div>
                <div id="val-success" class="stat-val">0</div>
            </div>
            <div class="stat-box">
                <div style="color:red">FAILED</div>
                <div id="val-failed" class="stat-val">0</div>
            </div>
            <div class="stat-box">
                <div style="color:yellow">LATENCY</div>
                <div id="val-latency" class="stat-val">0 ms</div>
            </div>
            <div class="stat-box">
                <div style="color:#888">STATUS</div>
                <div id="val-status" class="stat-val">IDLE</div>
            </div>
        </div>

        <div class="log-box" id="logs"></div>
    </div>

    <script>
        async function toggleMonitor() {
            const btn = document.getElementById('start-btn');
            const target = document.getElementById('target').value;
            const interval = document.getElementById('interval').value;

            if(btn.innerText === ">> START <<") {
                await fetch('/start', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target, interval})
                });
                btn.innerText = ">> STOP <<";
                btn.style.borderColor = "red";
                btn.style.color = "red";
            } else {
                await fetch('/stop', { method: 'POST' });
                btn.innerText = ">> START <<";
                btn.style.borderColor = "#0f0";
                btn.style.color = "#0f0";
            }
        }

        async function pollStatus() {
            const res = await fetch('/status');
            const data = await res.json();
            
            document.getElementById('liquid-fill').style.height = data.health_pct + '%';
            document.getElementById('gauge-text').innerText = data.health_pct + '%';
            document.getElementById('val-success').innerText = data.success_checks;
            document.getElementById('val-failed').innerText = data.failed_checks;
            document.getElementById('val-latency').innerText = data.last_latency + ' ms';
            document.getElementById('val-status').innerText = data.status;
            
            const logBox = document.getElementById('logs');
            const isScrolledToBottom = logBox.scrollHeight - logBox.clientHeight <= logBox.scrollTop + 10;
            
            logBox.innerHTML = data.log.map(l => {
                let color = "#0f0";
                if(l.level === "ERROR") color = "red";
                if(l.level === "WARNING") color = "yellow";
                return `<div style="color:${color}">${l.msg}</div>`;
            }).reverse().join('');
            
            // if(isScrolledToBottom) logBox.scrollTop = logBox.scrollHeight;
        }

        setInterval(pollStatus, 1000);
    </script>
</body>
</html>
"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode())
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(state).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        if self.path == '/start':
            data = json.loads(post_data)
            state["target"] = data.get("target", "http://example.com")
            state["interval"] = int(data.get("interval", 1000)) / 1000.0
            state["running"] = True
            state["status"] = "MONITORING"
            threading.Thread(target=monitor_task, daemon=True).start()
            self.send_response(200)
            self.end_headers()
        elif self.path == '/stop':
            state["running"] = False
            state["status"] = "STOPPED"
            self.send_response(200)
            self.end_headers()

if __name__ == "__main__":
    httpd = None
    curr_port = PORT
    while curr_port < 65535:
        try:
            httpd = socketserver.TCPServer(("", curr_port), Handler)
            break
        except OSError:
            curr_port += 1

    if httpd:
        print(f"[*] Starting GenX Monitor on http://localhost:{curr_port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Shutting down...")
            httpd.server_close()
    else:
        print("[!] Error: Could not find an available port.")
