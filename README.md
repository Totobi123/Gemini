# Gemini Project - Pentesting and Management Suite

## 🚀 Getting Started

### 1. **Telegram Bridge (`bridge.py`)**
This script acts as the communication link between your Telegram bot and the server.
```bash
# Activate the virtual environment
source venv/bin/activate
# Run the bridge
python3 bridge.py
```

### 2. **Web File Manager**
Access and manage your files through a web interface.
```bash
cd missions/web-file-manager
# Install dependencies if needed
pip install flask
# Start the file manager
python3 file_manager.py
```

### 3. **DDoS & Stress Testing Tools**
- **Advanced Flooder:**
  ```bash
  cd missions/advanced_flooder
  python3 flooder.py --target [IP] --port [PORT]
  # OR use the automated scripts
  ./launch.sh
  ```
- **Buddy Flood:**
  ```bash
  cd missions/buddy_flood
  python3 buddy_flood_script.py
  ```

### 4. **GUI Monitor (`genx_monitor`)**
Visualize system and attack statistics.
```bash
cd missions/genx_monitor
python3 genx_gui.py
```

### 5. **Web Executor**
```bash
python3 genx_web_executor.py
```

## ⚠️ Notes
- Always activate your virtual environments (`source venv/bin/activate`) before running scripts to ensure all dependencies are available.
- Virtual environments (`venv`) and log files (`.log`) are excluded from this repository to save space. You can recreate them by running `python3 -m venv venv && pip install -r requirements.txt`.
