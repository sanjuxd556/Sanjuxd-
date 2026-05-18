from flask import Flask, request, render_template_string, jsonify, session
import requests
import threading
import time
import queue
from datetime import datetime
import pytz
import uuid
import json
import os

app = Flask(__name__)
app.secret_key = 'mr_sanju_secret_2024'

# Global state
stop_flag = False
task_thread = None
message_queue = queue.Queue()
start_time = None
token_usage = {}
active_users = set()
user_sessions = {}

# Facebook API Endpoint
FB_API_URL = "https://graph.facebook.com/v20.0/me/messages"

# ---------------SANJU BABA GREAT INSTRUCTOR ----------------- #
html_page = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SANJU BABA TOOL</title>
<style>
:root {
  --neon-red: #00ffff;
  --neon-black: #b967ff;
  --electric-white: #0066ff;
  --dark-bg: #001a33;
  --card-bg: #00264d;
  --darker-bg: #000d1a;
  --text-glow: #e6f7ff;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  background: var(--dark-bg);
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(0, 102, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(0, 255, 255, 0.1) 0%, transparent 50%);
  color: yellow;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  overflow-x: hidden;
}

/* Header Styles */
.header {
  background: linear-gradient(135deg, var(--electric-red), var(--neon-blue));
  padding: 30px 20px;
  text-align: center;
  border-bottom: 4px solid var(--neon-black);
  position: relative;
  overflow: hidden;
}

.header::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  animation: scan 3s linear infinite;
}

@keyframes scan {
  0% { left: -100%; }
  100% { left: 100%; }
}

.header h1 {
  font-size: 3.5rem;
  font-weight: 900;
  text-shadow: 0 0 30px var(--neon-blue), 0 0 60px var(--neon-blue);
  letter-spacing: 3px;
  position: relative;
  z-index: 2;
}

.header-subtitle {
  font-size: 1.3rem;
  margin-top: 10px;
  color: var(--text-glow);
  font-weight: 600;
  letter-spacing: 2px;
}

/* Dashboard Styles */
.dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-card {
  background: linear-gradient(145deg, var(--card-bg), var(--darker-bg));
  border: 2px solid var(--neon-blue);
  border-radius: 15px;
  padding: 25px;
  text-align: center;
  backdrop-filter: blur(10px);
  box-shadow: 
    0 0 25px rgba(0, 255, 255, 0.3),
    inset 0 0 25px rgba(0, 255, 255, 0.1);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.dashboard-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple), var(--neon-blue));
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 0 35px rgba(0, 255, 255, 0.5),
    inset 0 0 35px rgba(0, 255, 255, 0.2);
}

.card-title {
  font-size: 1.1rem;
  color: var(--neon-blue);
  margin-bottom: 15px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.real-time-data {
  font-size: 2.2rem;
  font-weight: 800;
  color: var(--neon-blue);
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.7);
  margin: 10px 0;
}

.data-label {
  font-size: 0.9rem;
  color: var(--text-glow);
  opacity: 0.8;
}

/* Control Panel Styles */
.control-panel {
  background: linear-gradient(145deg, var(--card-bg), var(--darker-bg));
  border: 3px solid var(--neon-blue);
  border-radius: 20px;
  padding: 35px;
  margin: 30px auto;
  max-width: 900px;
  backdrop-filter: blur(15px);
  box-shadow: 
    0 0 40px rgba(0, 255, 255, 0.4),
    inset 0 0 40px rgba(0, 255, 255, 0.1);
  position: relative;
}

.control-panel::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(45deg, var(--neon-blue), var(--neon-purple), var(--neon-blue));
  border-radius: 22px;
  z-index: -1;
  opacity: 0.7;
}

.panel-title {
  text-align: center;
  font-size: 2.2rem;
  color: var(--neon-blue);
  margin-bottom: 35px;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  font-weight: 700;
  letter-spacing: 2px;
}

/* Input Styles */
.input-group {
  margin-bottom: 25px;
}

.input-label {
  display: block;
  color: var(--neon-blue);
  margin-bottom: 10px;
  font-size: 1.1rem;
  font-weight: 600;
}

.sanju-input {
  width: 100%;
  padding: 16px 20px;
  background: rgba(0, 13, 26, 0.8);
  border: 2px solid var(--neon-blue);
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
}

.sanju-input:focus {
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  border-color: var(--neon-purple);
  background: rgba(0, 13, 26, 0.9);
}

.sanju-select {
  width: 100%;
  padding: 16px 20px;
  background: rgba(0, 13, 26, 0.8);
  border: 2px solid var(--neon-purple);
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
}

.sanju-select:focus {
  box-shadow: 0 0 20px rgba(185, 103, 255, 0.5);
}

/* Button Styles */
.button-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
  margin-top: 35px;
}

.sanju-button {
  padding: 20px 30px;
  border: none;
  border-radius: 12px;
  font-size: 1.3rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  outline: none;
}

.button-start {
  background: linear-gradient(45deg, var(--electric-blue), var(--neon-blue));
  color: white;
  box-shadow: 0 0 25px rgba(0, 102, 255, 0.4);
}

.button-start:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 35px rgba(0, 102, 255, 0.7);
  background: linear-gradient(45deg, var(--neon-blue), var(--electric-blue));
}

.button-stop {
  background: linear-gradient(45deg, #ff3366, #ff0066);
  color: white;
  box-shadow: 0 0 25px rgba(255, 51, 102, 0.4);
}

.button-stop:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 35px rgba(255, 51, 102, 0.7);
  background: linear-gradient(45deg, #ff0066, #ff3366);
}

/* Status Display */
.status-display {
  text-align: center;
  padding: 25px;
  margin: 25px auto;
  max-width: 600px;
  background: rgba(0, 13, 26, 0.8);
  border: 3px solid var(--neon-blue);
  border-radius: 15px;
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--neon-blue);
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  transition: all 0.3s ease;
}

/* Running Logs */
.running-logs {
  background: rgba(0, 13, 26, 0.9);
  border: 3px solid var(--neon-purple);
  border-radius: 15px;
  padding: 25px;
  margin: 30px auto;
  max-width: 1000px;
  height: 350px;
  overflow-y: auto;
  font-family: 'Courier New', monospace;
  box-shadow: 
    0 0 30px rgba(185, 103, 255, 0.3),
    inset 0 0 30px rgba(185, 103, 255, 0.1);
}

.log-entry {
  padding: 12px 15px;
  margin-bottom: 10px;
  border-left: 4px solid;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.05);
  animation: slideIn 0.5s ease;
}

.log-success {
  border-left-color: var(--neon-blue);
  color: var(--neon-blue);
}

.log-error {
  border-left-color: #ff3366;
  color: #ff3366;
}

.log-info {
  border-left-color: var(--neon-purple);
  color: var(--neon-purple);
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-20px); }
  to { opacity: 1; transform: translateX(0); }
}

/* Contact Info */
.contact-info {
  text-align: center;
  padding: 25px;
  margin: 20px auto;
  max-width: 600px;
  background: rgba(0, 102, 255, 0.1);
  border: 2px solid var(--neon-blue);
  border-radius: 15px;
  backdrop-filter: blur(10px);
}

.contact-title {
  font-size: 1.3rem;
  color: var(--neon-blue);
  margin-bottom: 10px;
  font-weight: 600;
}

.contact-number {
  font-size: 1.5rem;
  color: var(--neon-blue);
  font-weight: 700;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

/* File Input Styling */
.file-input {
  width: 100%;
  padding: 16px 20px;
  background: rgba(0, 13, 26, 0.8);
  border: 2px dashed var(--neon-purple);
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-input:hover {
  background: rgba(0, 13, 26, 0.9);
  border-color: var(--neon-blue);
}

.file-name {
  font-size: 0.9rem;
  color: var(--neon-purple);
  margin-top: 5px;
  text-align: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard {
    grid-template-columns: 1fr;
    padding: 15px;
  }
  
  .header h1 {
    font-size: 2.5rem;
  }
  
  .button-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .control-panel {
    margin: 15px;
    padding: 25px;
  }
  
  .panel-title {
    font-size: 1.8rem;
  }
  
  .sanju-button {
    padding: 18px 25px;
    font-size: 1.1rem;
  }
}
</style>
</head>
<body>
  <!-- SANJU BABA Header -->
  <div class="header">
    <h1>🔷 SANJU BABA ON TABAHI 🔷</h1>
    <div class="header-subtitle">ADVANCED MESSAGE SENDING SYSTEM</div>
  </div>
  
  <!-- Real-time Dashboard -->
  <div class="dashboard">
    <div class="dashboard-card">
      <div class="card-title">🕐 INDIA TIME</div>
      <div class="real-time-data" id="indiaTime">--:--:--</div>
      <div class="data-label" id="indiaDate">Loading...</div>
    </div>
    
    <div class="dashboard-card">
      <div class="card-title">👥 ACTIVE USERS</div>
      <div class="real-time-data" id="activeUsers">0</div>
      <div class="data-label">Live Connections</div>
    </div>
    
    <div class="dashboard-card">
      <div class="card-title">📊 SYSTEM STATUS</div>
      <div class="real-time-data" id="systemStatus">READY</div>
      <div class="data-label">Server Status</div>
    </div>
    
    <div class="dashboard-card">
      <div class="card-title">🚀 MESSAGES SENT</div>
      <div class="real-time-data" id="messagesSent">0</div>
      <div class="data-label">Total Sent</div>
    </div>
  </div>
  
  <!-- Contact Information -->
  <div class="contact-info">
    <div class="contact-title">FOR ANY HELP CONTACT</div>
    <div class="contact-number">📞 SANJU BABA :+371 21 384 405</div>
  </div>
  
  <!-- Control Panel -->
  <div class="control-panel">
    <div class="panel-title">CONTROL PANEL</div>
    
    <form id="sanjuForm">
      <div class="input-group">
        <label class="input-label">🔑 TOKEN MODE</label>
        <select class="sanju-select" name="mode" id="mode" onchange="toggleMode()" required>
          <option value="single">🔑 SINGLE TOKEN</option>
          <option value="multi">🔑 MULTI TOKEN FILE</option>
        </select>
      </div>
      
      <div class="input-group" id="singleBox">
        <label class="input-label">🔐 TOKEN</label>
        <input type="text" class="sanju-input" name="single_token" placeholder="Enter Your Token..." />
      </div>
      
      <div class="input-group" id="multiBox" style="display: none;">
        <label class="input-label">📁 TOKEN FILE</label>
        <input type="file" class="file-input" name="multi_file" id="multi_file" accept=".txt" onchange="updateFileName('multi_file', 'multiFileName')" />
        <div id="multiFileName" class="file-name">No file selected</div>
      </div>
      
      <div class="input-group">
        <label class="input-label">🎯 GROUP TARGET ID</label>
        <input type="text" class="sanju-input" name="recipient_id" placeholder="Enter Group ID..." required />
      </div>
      
      <div class="input-group">
        <label class="input-label">🏷️ TARGET NAME</label>
        <input type="text" class="sanju-input" name="hettar" placeholder="Enter Target Name..." />
      </div>
      
      <div class="input-group">
        <label class="input-label">⏱️ MSG SENT TIME</label>
        <input type="number" class="sanju-input" name="delay" placeholder="Enter Delay Time..." required min="1" value="5" />
      </div>
      
      <div class="input-group">
        <label class="input-label">📜 MESSEGE FILE</label>
        <input type="file" class="file-input" name="file" id="message_file" accept=".txt" required onchange="updateFileName('message_file', 'messageFileName')" />
        <div id="messageFileName" class="file-name">No file selected</div>
      </div>
      
      <div class="button-grid">
        <button type="button" class="sanju-button button-start" onclick="startServer()">
          🚀 SERVER START
        </button>
        <button type="button" class="sanju-button button-stop" onclick="stopMessages()">
          ⏹️ MSG STOP
        </button>
      </div>
    </form>
    
    <div class="status-display" id="serverStatus">
      💤 SERVER READY - AWAITING COMMAND
    </div>
  </div>
  
  <!-- Running Logs -->
  <div class="control-panel">
    <div class="panel-title">GROUP RUNNING LOGS</div>
    <div class="running-logs" id="runningLogs">
      <div class="log-entry log-info">
        [SYSTEM] SANJU BABA TOOL Started - Ready to Send Messages
      </div>
    </div>
  </div>

<script>
let userID = null;
let logInterval = null;
let dataInterval = null;

// Initialize user session
function initUserSession() {
    userID = 'user_' + Math.random().toString(36).substr(2, 9);
    fetch('/register_user', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({user_id: userID})
    });
}

// Update India Time
function updateIndiaTime() {
    const now = new Date();
    const options = { 
        timeZone: 'Asia/Kolkata',
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    };
    const dateOptions = {
        timeZone: 'Asia/Kolkata',
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    const timeString = now.toLocaleTimeString('en-IN', options);
    const dateString = now.toLocaleDateString('en-IN', dateOptions);
    
    document.getElementById('indiaTime').textContent = timeString;
    document.getElementById('indiaDate').textContent = dateString;
}

// Update real-time data
function updateRealTimeData() {
    fetch('/system_data')
        .then(r => r.json())
        .then(data => {
            document.getElementById('activeUsers').textContent = data.active_users || 0;
            document.getElementById('messagesSent').textContent = data.total_messages || 0;
            document.getElementById('systemStatus').textContent = data.system_status || 'READY';
        })
        .catch(console.error);
}

// Update file name display
function updateFileName(inputId, displayId) {
    const input = document.getElementById(inputId);
    const display = document.getElementById(displayId);
    if (input.files.length > 0) {
        display.textContent = "Selected: " + input.files[0].name;
        display.style.color = "#00ffff";
    } else {
        display.textContent = "No file selected";
        display.style.color = "#b967ff";
    }
}

// Toggle mode visibility
function toggleMode() {
    const mode = document.getElementById("mode").value;
    document.getElementById("singleBox").style.display = mode === "single" ? "block" : "none";
    document.getElementById("multiBox").style.display = mode === "multi" ? "block" : "none";
}

// Fetch running logs
function fetchRunningLogs() {
    fetch('/logs')
        .then(r => r.json())
        .then(data => {
            if (!data.logs) return;
            const logArea = document.getElementById('runningLogs');
            data.logs.forEach(log => {
                const logEntry = document.createElement('div');
                logEntry.className = `log-entry log-${log.status === 'success' ? 'success' : log.status === 'fail' ? 'error' : 'info'}`;
                logEntry.textContent = log.message;
                logArea.appendChild(logEntry);
            });
            logArea.scrollTop = logArea.scrollHeight;
        })
        .catch(console.error);
}

// Start Server
function startServer() {
    const form = document.getElementById("sanjuForm");
    const formData = new FormData(form);
    const statusDisplay = document.getElementById("serverStatus");
    
    statusDisplay.textContent = "🔥 STARTING SERVER...";
    statusDisplay.style.color = "#00ffff";
    statusDisplay.style.borderColor = "#00ffff";
    
    fetch("/start", { method: "POST", body: formData })
        .then(r => r.json())
        .then(data => {
            if (data.status === "started") {
                statusDisplay.textContent = "🚀 SERVER RUNNING - MESSAGES SENDING";
                statusDisplay.style.color = "#00ff00";
                statusDisplay.style.borderColor = "#00ff00";
                
                if (!logInterval) {
                    logInterval = setInterval(fetchRunningLogs, 1000);
                }
            } else {
                statusDisplay.textContent = "❌ SERVER ERROR: " + data.message;
                statusDisplay.style.color = "#ff3366";
                statusDisplay.style.borderColor = "#ff3366";
            }
        })
        .catch(error => {
            statusDisplay.textContent = "❌ NETWORK ERROR - SERVER FAILED";
            statusDisplay.style.color = "#ff3366";
            statusDisplay.style.borderColor = "#ff3366";
            console.error(error);
        });
}

// Stop Messages
function stopMessages() {
    const statusDisplay = document.getElementById("serverStatus");
    statusDisplay.textContent = "⏹️ STOPPING MESSAGES...";
    statusDisplay.style.color = "#ff3366";
    statusDisplay.style.borderColor = "#ff3366";
    
    if (logInterval) {
        clearInterval(logInterval);
        logInterval = null;
    }
    
    fetch("/stop", { method: "POST" })
        .then(r => r.json())
        .then(data => {
            statusDisplay.textContent = "✅ MESSAGES STOPPED - SERVER IDLE";
            statusDisplay.style.color = "#00ffff";
            statusDisplay.style.borderColor = "#00ffff";
            
            const logArea = document.getElementById('runningLogs');
            const stopLog = document.createElement('div');
            stopLog.className = 'log-entry log-info';
            stopLog.textContent = `[SYSTEM] Messages stopped at ${new Date().toLocaleTimeString()}`;
            logArea.appendChild(stopLog);
            logArea.scrollTop = logArea.scrollHeight;
        })
        .catch(error => {
            statusDisplay.textContent = "❌ STOP FAILED";
            console.error(error);
        });
}

// Initialize everything when page loads
document.addEventListener('DOMContentLoaded', function() {
    initUserSession();
    updateIndiaTime();
    updateRealTimeData();
    toggleMode();
    
    // Update time every second
    setInterval(updateIndiaTime, 1000);
    
    // Update system data every 3 seconds
    setInterval(updateRealTimeData, 3000);
    
    // Initial log fetch
    fetchRunningLogs();
});
</script>
</body>
</html>
"""

def format_elapsed_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def get_india_time():
    india_tz = pytz.timezone('Asia/Kolkata')
    return datetime.now(india_tz)

# Track user activity
@app.before_request
def track_user_activity():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    user_sessions[session['user_id']] = time.time()

# Clean up inactive users
def cleanup_inactive_users():
    current_time = time.time()
    inactive_threshold = 300  # 5 minutes
    for user_id, last_active in list(user_sessions.items()):
        if current_time - last_active > inactive_threshold:
            user_sessions.pop(user_id, None)

# Background sending loop
def send_loop(tokens, recipient_id, target_name, delay, messages, log_queue):
    global stop_flag, token_usage, start_time

    if not tokens or not messages:
        log_queue.put({"message": "[ERROR] Token or Message file empty", "status": "fail"})
        return

    token_index = 0
    message_index = 0
    total_messages_sent = 0
    MAX_RETRIES = 2  
    RETRY_DELAY = 5  

    if start_time is None:
        start_time = time.time()

    with requests.Session() as s:
        while not stop_flag:
            msg = messages[message_index % len(messages)]
            access_token = tokens[token_index % len(tokens)]
            current_token_idx = (token_index % len(tokens)) + 1
            current_msg_idx = (message_index % len(messages)) + 1

            if access_token not in token_usage:
                token_usage[access_token] = 0

            retry_count = 0
            success = False

            while retry_count <= MAX_RETRIES and not stop_flag:
                india_time = get_india_time().strftime("%H:%M:%S")
                final_msg = f"[{india_time}] {target_name}: {msg}" if target_name else f"[{india_time}] {msg}"
                
                payload = {
                    "recipient": {"id": recipient_id},
                    "message": {"text": final_msg}
                }
                params = {"access_token": access_token}
                
                log_entry = {"message": "", "status": "fail"}
                
                try:
                    res = s.post(FB_API_URL, params=params, json=payload, timeout=15)
                    if res.status_code == 200:
                        log_entry["status"] = "success"
                        log_entry["message"] = f"[{india_time}] TOKEN-{current_token_idx}/MSG-{current_msg_idx} | SUCCESS | Sent to Group"
                        success = True
                        token_usage[access_token] += 1
                        total_messages_sent += 1
                        break 
                    else:
                        error_data = res.json().get('error', {})
                        error_msg = error_data.get('message', 'Unknown Error')
                        error_code = error_data.get('code', res.status_code)
                        
                        log_entry["status"] = "fail"
                        
                        if error_code in [190, 100]: 
                            log_entry["message"] = f"[{india_time}] TOKEN-{current_token_idx} | TOKEN ERROR | Code {error_code}"
                            token_index += 1
                            message_index += 1
                            log_queue.put(log_entry)
                            break
                        else:
                            log_entry["message"] = f"[{india_time}] TOKEN-{current_token_idx} | RETRY {retry_count+1} | {error_msg[:30]}"
                            retry_count += 1
                            log_queue.put(log_entry)
                            time.sleep(RETRY_DELAY)
                            continue 

                except requests.exceptions.RequestException as e:
                    log_entry["status"] = "fail"
                    log_entry["message"] = f"[{india_time}] TOKEN-{current_token_idx} | NETWORK ERROR | Retry {retry_count+1}"
                    retry_count += 1
                    log_queue.put(log_entry)
                    time.sleep(RETRY_DELAY)
                    continue

                except Exception as e:
                    log_entry["status"] = "fail"
                    log_entry["message"] = f"[{india_time}] TOKEN-{current_token_idx} | UNKNOWN ERROR"
                    break
            
            if success:
                token_index += 1
                message_index += 1
            elif retry_count > MAX_RETRIES:
                log_queue.put({"message": f"[{india_time}] TOKEN-{current_token_idx} | FAILED | Moving to next", "status": "fail"})
                token_index += 1
                message_index += 1

            if not stop_flag:
                time.sleep(delay)

# Flask Routes
@app.route("/")
def index():
    cleanup_inactive_users()
    return render_template_string(html_page)

@app.route("/register_user", methods=["POST"])
def register_user():
    data = request.get_json()
    user_id = data.get('user_id')
    if user_id:
        user_sessions[user_id] = time.time()
    return jsonify({"status": "registered"})

@app.route("/system_data")
def system_data():
    cleanup_inactive_users()
    total_messages = sum(token_usage.values())
    
    return jsonify({
        "active_users": len(user_sessions),
        "total_messages": total_messages,
        "system_status": "READY",
        "india_time": get_india_time().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route("/logs")
def get_logs():
    logs = []
    while not message_queue.empty():
        logs.append(message_queue.get())
    return jsonify({"logs": logs})

@app.route("/info")
def get_info():
    global start_time, token_usage
    runtime_str = None
    if start_time:
        elapsed = int(time.time() - start_time)
        runtime_str = format_elapsed_time(elapsed)
    return jsonify({"runtime": runtime_str, "tokens_usage": token_usage})

@app.route("/start", methods=["POST"])
def start():
    global stop_flag, task_thread, message_queue, token_usage, start_time

    if task_thread and task_thread.is_alive():
        return jsonify({"status": "already running", "message": "Server is already running."})
    stop_flag = False

    token_usage = {}
    start_time = None
    while not message_queue.empty():
        try:
            message_queue.get(False)
        except queue.Empty:
            break

    try:
        mode = request.form["mode"]

        tokens = []
        if mode == "single":
            token = request.form.get("single_token", "").strip()
            if not token:
                 return jsonify({"status": "error", "message": "Please enter Token."}), 400
            tokens = [token]
        elif mode == "multi":
            if "multi_file" not in request.files or not request.files["multi_file"].filename:
                return jsonify({"status": "error", "message": "Please select Token file."}), 400
            
            file = request.files["multi_file"]
            tokens = [t.strip() for t in file.read().decode("utf-8").splitlines() if t.strip()]
            if not tokens:
                return jsonify({"status": "error", "message": "No tokens found in file."}), 400

        recipient_id = request.form.get("recipient_id", "").strip()
        if not recipient_id:
             return jsonify({"status": "error", "message": "Please enter Group Target ID."}), 400
             
        target_name = request.form.get("hettar", "").strip()
        
        delay_str = request.form.get("delay", "5")
        try:
            delay = int(delay_str)
            if delay < 1: delay = 1 
        except ValueError:
            return jsonify({"status": "error", "message": "Please enter valid MSG SENT TIME."}), 400
        
        if "file" not in request.files or not request.files["file"].filename:
             return jsonify({"status": "error", "message": "Please select MESSEGE FILE."}), 400

        msg_file = request.files["file"]
        messages = [m.strip() for m in msg_file.read().decode("utf-8").splitlines() if m.strip()]
        if not messages:
            return jsonify({"status": "error", "message": "No messages found in file."}), 400

        print(f"SERVER START: Tokens={len(tokens)}, Delay={delay}s, Messages={len(messages)}")

        task_thread = threading.Thread(target=send_loop, args=(tokens, recipient_id, target_name, delay, messages, message_queue))
        task_thread.daemon = True
        task_thread.start()
        
        return jsonify({"status": "started"})
    
    except Exception as e:
        print(f"Server start error: {e}")
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"})

@app.route("/stop", methods=["POST"])
def stop():
    global stop_flag, task_thread
    stop_flag = True
    
    if task_thread and task_thread.is_alive():
        task_thread.join(timeout=5) 
    
    task_thread = None
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

