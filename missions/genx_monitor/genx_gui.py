import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import requests
import socket
from queue import Queue
from datetime import datetime

# --- Configuration ---
DEFAULT_TIMEOUT = 5
MAX_THREADS = 8  # Limited to prevent system overload
LATENCY_GREEN = 200  # ms
LATENCY_YELLOW = 500 # ms

class GenxMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Genx Network Monitor v1.0")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.running = False
        self.threads = []
        self.log_queue = Queue()

        self.create_widgets()
        self.update_log()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#333", height=60)
        header_frame.pack(fill=tk.X)
        header_label = tk.Label(header_frame, text="Genx Network Efficiency Monitor", font=("Helvetica", 18, "bold"), fg="white", bg="#333")
        header_label.pack(pady=10)

        # Control Panel
        control_frame = tk.LabelFrame(self.root, text="Target Configuration", padx=10, pady=10, bg="#f0f0f0")
        control_frame.pack(padx=20, pady=10, fill=tk.X)

        tk.Label(control_frame, text="Target (URL or IP):", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.target_entry = tk.Entry(control_frame, width=40)
        self.target_entry.grid(row=0, column=1, padx=5)
        self.target_entry.insert(0, "http://example.com")

        tk.Label(control_frame, text="Request Interval (ms):", bg="#f0f0f0").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.interval_entry = tk.Entry(control_frame, width=10)
        self.interval_entry.grid(row=0, column=3, padx=5)
        self.interval_entry.insert(0, "1000")

        self.start_button = tk.Button(control_frame, text="Start Monitor", command=self.start_monitoring, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.start_button.grid(row=0, column=4, padx=10)

        self.stop_button = tk.Button(control_frame, text="Stop", command=self.stop_monitoring, bg="#f44336", fg="white", font=("Arial", 10, "bold"), state=tk.DISABLED)
        self.stop_button.grid(row=0, column=5, padx=10)

        # Dashboard
        dashboard_frame = tk.LabelFrame(self.root, text="Live Metrics", padx=10, pady=10, bg="#f0f0f0")
        dashboard_frame.pack(padx=20, pady=5, fill=tk.X)

        self.status_label = tk.Label(dashboard_frame, text="Status: IDLE", font=("Arial", 12, "bold"), bg="#f0f0f0", fg="gray")
        self.status_label.pack(side=tk.LEFT, padx=20)
        
        self.latency_label = tk.Label(dashboard_frame, text="Avg Latency: -- ms", font=("Arial", 12), bg="#f0f0f0")
        self.latency_label.pack(side=tk.LEFT, padx=20)

        # Log Area
        log_frame = tk.LabelFrame(self.root, text="Activity Log", padx=10, pady=10, bg="#f0f0f0")
        log_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(log_frame, state=tk.DISABLED, height=15)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Tags for colored text
        self.log_text.tag_config("INFO", foreground="black")
        self.log_text.tag_config("SUCCESS", foreground="green")
        self.log_text.tag_config("WARNING", foreground="#FFC107") # Amber
        self.log_text.tag_config("ERROR", foreground="red")

    def log_message(self, message, level="INFO"):
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        self.log_queue.put((f"{timestamp} {message}\n", level))

    def update_log(self):
        while not self.log_queue.empty():
            msg, level = self.log_queue.get()
            self.log_text.configure(state=tk.NORMAL)
            self.log_text.insert(tk.END, msg, level)
            self.log_text.see(tk.END)
            self.log_text.configure(state=tk.DISABLED)
        
        self.root.after(100, self.update_log)

    def start_monitoring(self):
        target = self.target_entry.get().strip()
        if not target:
            self.log_message("Please enter a valid target.", "ERROR")
            return

        if not target.startswith("http"):
            target = "http://" + target

        try:
            interval = int(self.interval_entry.get()) / 1000.0
        except ValueError:
            self.log_message("Invalid interval. Defaulting to 1s.", "WARNING")
            interval = 1.0

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: MONITORING", fg="blue")
        
        self.log_message(f"Starting monitor on {target}...", "INFO")

        # Start monitoring threads (max 4 for GUI responsiveness)
        for i in range(4):
            t = threading.Thread(target=self.monitor_task, args=(target, interval, i))
            t.daemon = True
            t.start()
            self.threads.append(t)

    def stop_monitoring(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: STOPPED", fg="gray")
        self.log_message("Monitoring stopped.", "INFO")
        self.threads = []

    def monitor_task(self, target, interval, thread_id):
        while self.running:
            try:
                start_time = time.time()
                response = requests.get(target, timeout=DEFAULT_TIMEOUT)
                latency = int((time.time() - start_time) * 1000)
                
                status_code = response.status_code
                
                # Determine health
                if status_code == 200:
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
                    level = "ERROR"
                    status_text = f"HTTP {status_code}"

                self.log_message(f"[Thread-{thread_id}] {status_text} | Latency: {latency}ms | Code: {status_code}", level)
                
                # Update main latency label (simple average approximation)
                self.root.after(0, lambda l=latency: self.latency_label.config(text=f"Last Latency: {l} ms"))

            except requests.exceptions.RequestException as e:
                self.log_message(f"[Thread-{thread_id}] CONNECTION ERROR: {str(e)}", "ERROR")
                self.root.after(0, lambda: self.status_label.config(text="Status: UNREACHABLE", fg="red"))
            
            time.sleep(interval)

if __name__ == "__main__":
    root = tk.Tk()
    app = GenxMonitorApp(root)
    root.mainloop()
