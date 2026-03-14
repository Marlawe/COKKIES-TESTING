from flask import Flask, render_template_string, request, jsonify
import requests
import json
import time
import threading
import random
import secrets

app = Flask(__name__)

# Global storage for active tasks
tasks = {}

class FBAutomator:
    def __init__(self, task_id, stop_key, auth_list, targets, messages, action_type, delay=5, poll_options=None):
        self.task_id = task_id
        self.stop_key = stop_key
        self.auth_list = auth_list # List of (token, cookie)
        self.targets = targets
        self.messages = messages
        self.action_type = action_type 
        self.delay = delay
        self.poll_options = poll_options or []
        self.running = True
        self.logs = []
        self.session = requests.Session()

    def add_log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")

    def perform_action(self, auth, target_id):
        token, cookie = auth
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        if cookie:
            headers['Cookie'] = cookie
            
        try:
            # Facebook Graph API v17.0 Implementation
            if self.action_type == 'love_react':
                url = f"https://graph.facebook.com/v17.0/{target_id}/reactions?type=LOVE&access_token={token}"
                res = self.session.post(url, headers=headers).json()
                return res.get('success', False) or "id" in res
            
            elif self.action_type == 'message':
                url = f"https://graph.facebook.com/v17.0/me/messages?access_token={token}"
                msg = random.choice(self.messages) if self.messages else "Hello from Raj Gaming Automation"
                payload = {
                    "recipient": {"id": target_id}, 
                    "message": {"text": msg},
                    "messaging_type": "MESSAGE_TAG",
                    "tag": "CONFIRMED_EVENT_UPDATE"
                }
                res = self.session.post(url, json=payload, headers=headers).json()
                return "message_id" in res or "id" in res

            elif self.action_type == 'group_join':
                url = f"https://graph.facebook.com/v17.0/{target_id}/members?access_token={token}"
                res = self.session.post(url, headers=headers).json()
                return res.get('success', False)
                
            elif self.action_type == 'poll_vote':
                option = random.choice(self.poll_options) if self.poll_options else target_id
                url = f"https://graph.facebook.com/v17.0/{option}/votes?access_token={token}"
                res = self.session.post(url, headers=headers).json()
                return res.get('success', False)

            elif self.action_type == 'gaming_boost':
                url = f"https://graph.facebook.com/v17.0/{target_id}/likes?access_token={token}"
                res = self.session.post(url, headers=headers).json()
                return res.get('success', False) or "id" in res

            elif self.action_type == 'autotag':
                url = f"https://graph.facebook.com/v17.0/{target_id}/comments?access_token={token}"
                payload = {"message": f"Tagged for timeline boost! @[{target_id}]"}
                res = self.session.post(url, json=payload, headers=headers).json()
                return "id" in res
                
        except Exception as e:
            self.add_log(f"Error: {str(e)}")
        return False

    def run(self):
        self.add_log(f"🚀 Engine (v17.0) Started. Mode: {self.action_type.upper()}")
        while self.running:
            for auth in self.auth_list:
                if not self.running: break
                for target_id in self.targets:
                    if not self.running: break
                    success = self.perform_action(auth, target_id)
                    status = "✅ Success" if success else "❌ Failed"
                    self.add_log(f"{status} | {self.action_type} | Target: {target_id}")
                    time.sleep(self.delay)
            if not self.running: break
            time.sleep(1)

    def stop(self):
        self.running = False
        self.add_log("🛑 Stopped.")

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔏 OFFLINE MIICKY COKKIES SERVER 🔒</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root { --primary: #00f2fe; --card: rgba(0, 0, 0, 0.5); --neon: #bc13fe; --green: #22c55e; --orange: #ff8c00; --red: #ff0000; }
        body {
            font-family: 'Poppins', sans-serif;
            background-image: url('https://i.postimg.cc/GhcbrCyB/9b63f26ee35e9e789504985c5312975d.jpg');
            background-size: cover; background-position: center; background-attachment: fixed;
            color: #fff; margin: 0; padding: 10px; display: flex; justify-content: center; min-height: 100vh;
        }
        .container {
            width: 100%; max-width: 440px; background: var(--card); backdrop-filter: blur(15px);
            padding: 20px; border-radius: 20px; box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
            border: 1px double rgba(255, 255, 255, 0.4); text-align: center;
        }
        h1 {
            background: linear-gradient(45deg, #00f2fe, #fff, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: 800; margin-bottom: 20px; text-transform: uppercase; font-size: 1.5rem; letter-spacing: 2px;
        }
        
        .input-group { 
            background: rgba(0, 0, 0, 0.4); 
            border: 1.5px double white; 
            padding: 12px; 
            margin-bottom: 12px; 
            border-radius: 12px; 
            box-sizing: border-box; 
            text-align: left;
            transition: 0.3s;
        }
        
        .input-group:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(255,255,255,0.1); }

        .box-neon { border-color: var(--neon) !important; animation: pulse-neon 2s infinite; }
        .box-green { border-color: var(--green) !important; animation: pulse-green-box 2s infinite; }
        .box-orange { border-color: var(--orange) !important; animation: pulse-orange 2s infinite; }
        .box-blue { border-color: var(--primary) !important; animation: pulse-blue 2s infinite; }
        .box-red { border-color: var(--red) !important; animation: pulse-red 2s infinite; }

        @keyframes pulse-neon { 0%, 100% { box-shadow: 0 0 8px var(--neon); } 50% { box-shadow: 0 0 20px var(--neon); } }
        @keyframes pulse-green-box { 0%, 100% { box-shadow: 0 0 8px var(--green); } 50% { box-shadow: 0 0 20px var(--green); } }
        @keyframes pulse-orange { 0%, 100% { box-shadow: 0 0 8px var(--orange); } 50% { box-shadow: 0 0 20px var(--orange); } }
        @keyframes pulse-blue { 0%, 100% { box-shadow: 0 0 8px var(--primary); } 50% { box-shadow: 0 0 20px var(--primary); } }
        @keyframes pulse-red { 0%, 100% { box-shadow: 0 0 8px var(--red); } 50% { box-shadow: 0 0 20px var(--red); } }

        label { display: block; margin-bottom: 5px; font-size: 0.85rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; }
        
        textarea, input, select {
            width: 100%; background: rgba(0, 0, 0, 0.5); border: 1px solid rgba(255,255,255,0.3); color: #fff;
            padding: 10px; margin-top: 5px; border-radius: 8px; box-sizing: border-box; font-weight: 600; outline: none;
        }

        .btn-start { 
            width: 100%; padding: 15px; border-radius: 12px; font-weight: 800; cursor: pointer;
            background: transparent; color: var(--green); border: 2.5px solid var(--green); 
            animation: pulse-green 1.5s infinite; text-transform: uppercase; letter-spacing: 2px;
            font-size: 1rem;
        }
        
        .btn-stop-area { margin-top: 15px; }
        .btn-stop {
            width: 100%; padding: 12px; border-radius: 10px; font-weight: 800; cursor: pointer;
            background: #ff0000; color: #fff; border: none; text-transform: uppercase; letter-spacing: 1px;
        }

        @keyframes pulse-green {
            0% { transform: scale(1); box-shadow: 0 0 5px var(--green); }
            70% { transform: scale(1.02); box-shadow: 0 0 20px rgba(34, 197, 94, 0.3); }
            100% { transform: scale(1); box-shadow: 0 0 5px var(--green); }
        }

        .vip-box {
            background: transparent; border-radius: 15px; padding: 10px 20px; margin: 15px 0;
            color: var(--primary); border: 1.5px solid var(--primary); animation: pulse-blue-anim 2s infinite; display: inline-flex;
            font-weight: 800; text-transform: uppercase; font-size: 0.9rem;
        }
        @keyframes pulse-blue-anim { 0%, 100% { transform: scale(1); box-shadow: 0 0 5px var(--primary); } 50% { transform: scale(1.05); box-shadow: 0 0 15px var(--primary); } }

        .secure-badge {
            display: inline-flex; color: var(--green); font-weight: 900; padding: 12px 25px;
            background: rgba(34, 197, 94, 0.1); border-radius: 50px; border: 2.5px solid var(--green); 
            margin-bottom: 10px; text-transform: uppercase; animation: pulse-green-secure 1.5s infinite;
            font-size: 0.9rem;
        }
        @keyframes pulse-green-secure { 0%, 100% { box-shadow: 0 0 10px var(--green); } 50% { box-shadow: 0 0 25px var(--green); } }

        .social-links-box {
            background: transparent; border-radius: 15px; padding: 12px; margin: 10px auto;
            border: 1.5px solid #ff8c00; display: inline-flex; gap: 15px;
        }
        .social-links-box a { font-size: 1.8rem; filter: drop-shadow(0 0 5px rgba(255,255,255,0.3)); }
        .fa-whatsapp { color: #25d366; } .fa-instagram { color: #e1306c; } .fa-facebook { color: #1877f2; } .fa-youtube { color: #ff0000; }

        #logs {
            margin-top: 15px; background: rgba(0,0,0,0.6); backdrop-filter: blur(5px); height: 160px;
            overflow-y: auto; padding: 10px; border-radius: 10px; font-family: monospace; font-size: 0.75rem;
            text-align: left; border: 1.5px solid #fff; color: #fff;
        }
        .log-entry { border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding: 4px 0; }
        .hidden { display: none; }
        .key-display { background: rgba(0,0,0,0.6); padding: 10px; border-radius: 8px; margin: 10px 0; border: 1px solid var(--primary); color: var(--primary); font-weight: 800; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔏🩵MESSENGER OFFLINE CONVO TOOL 🔒</h1>
        
        <div id="stopKeyDisplay" class="key-display hidden">
            STOP KEY: <span id="keyVal"></span>
        </div>

        <div class="input-group box-neon">
            <label style="color: var(--neon);"><i class="fas fa-gamepad"></i> Action Matrix</label>
            <select id="actionType" onchange="updateUI()">
                <option value="gaming_boost">🎮 Advance Gaming Boost</option>
                <option value="love_react">💖 Love React (All Posts)</option>
                <option value="autotag">🏷️ Autotag + Timeline</option>
                <option value="group_join">🤝 Automatic Group Join</option>
                <option value="poll_vote">🗳️ Poll Voting (Advance)</option>
                <option value="message">💬 Messenger Automation</option>
            </select>
        </div>

        <div id="pollBoxes" class="hidden">
            <div class="input-group box-green">
                <label style="color: var(--green);">Poll Option 1 ID</label>
                <input type="text" id="poll1" placeholder="Option ID 1">
                <label style="color: var(--green);">Poll Option 2 ID</label>
                <input type="text" id="poll2" placeholder="Option ID 2">
            </div>
        </div>

        <div class="input-group box-green">
            <label style="color: var(--green);"><i class="fas fa-shield-alt"></i> Auth System</label>
            <select id="authMode" onchange="toggleAuth()">
                <option value="paste">Paste Tokens/Cookies</option>
                <option value="file">Unlimited File Mode</option>
            </select>
            <div id="authPaste"><textarea id="authInput" rows="3" placeholder="Token|Cookie (One per line)"></textarea></div>
            <div id="authFile" class="hidden"><input type="file" id="fileInput"></div>
        </div>

        <div class="input-group box-orange">
            <label style="color: var(--orange);"><i class="fas fa-crosshairs"></i> Target Database</label>
            <textarea id="targets" rows="2" placeholder="Post/User/Group IDs"></textarea>
        </div>

        <div id="msgBox" class="input-group box-blue">
            <label style="color: var(--primary);"><i class="fas fa-comment-dots"></i> Message Vault</label>
            <textarea id="messages" rows="2" placeholder="Msg1, Msg2, Msg3..."></textarea>
        </div>

        <div class="input-group box-blue">
            <label style="color: var(--primary);"><i class="fas fa-clock"></i> Pulse Delay</label>
            <input type="number" id="delay" value="5">
        </div>

        <button class="btn-start" onclick="startEngine()">🚀 Launch Advance Script</button>

        <div class="btn-stop-area">
            <div class="input-group box-red" style="margin-bottom:0;">
                <label style="color: var(--red);">Process Kill Key</label>
                <input type="text" id="stopKeyInput" placeholder="Enter key here...">
                <button class="btn-stop" onclick="stopEngine()">🛑 Shutdown Engine</button>
            </div>
        </div>

        <div><div class="vip-box">Terms of Service | Facebook Secure🔐</div></div>
        <div><div class="secure-badge">🔏 SECURE BY RAJ HERE 🚀</div></div>

        <div class="social-links-box">
            <a href="#"><i class="fab fa-whatsapp"></i></a>
            <a href="#"><i class="fab fa-facebook"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-youtube"></i></a>
        </div>

        <div id="logs"><div class="log-entry">System Standby (v17.0)...</div></div>
    </div>

    <script>
        let currentTaskId = null;
        let pollInterval = null;

        function updateUI() {
            const action = document.getElementById('actionType').value;
            // Hide/Show Poll Boxes
            document.getElementById('pollBoxes').classList.toggle('hidden', action !== 'poll_vote');
            // Hide/Show Message Box based on action
            const msgBox = document.getElementById('msgBox');
            if (action === 'message' || action === 'autotag') {
                msgBox.classList.remove('hidden');
            } else {
                msgBox.classList.add('hidden');
            }
        }

        function toggleAuth() {
            const isFile = document.getElementById('authMode').value === 'file';
            document.getElementById('authPaste').classList.toggle('hidden', isFile);
            document.getElementById('authFile').classList.toggle('hidden', !isFile);
        }

        async function startEngine() {
            let authList = [];
            if (document.getElementById('authMode').value === 'paste') {
                const lines = document.getElementById('authInput').value.split('\\n').filter(l => l.trim());
                authList = lines.map(l => {
                    const parts = l.split('|');
                    return [parts[0].trim(), parts[1] ? parts[1].trim() : ""];
                });
            } else {
                const file = document.getElementById('fileInput').files[0];
                if (file) {
                    const text = await file.text();
                    authList = text.split('\\n').filter(l => l.trim()).map(l => {
                        const parts = l.split('|');
                        return [parts[0].trim(), parts[1] ? parts[1].trim() : ""];
                    });
                }
            }

            if (authList.length === 0) { alert('Please provide authentication tokens/cookies.'); return; }

            const data = {
                auth_list: authList,
                targets: document.getElementById('targets').value.split('\\n').filter(t => t.trim()),
                messages: document.getElementById('messages').value.split(',').filter(m => m.trim()),
                action_type: document.getElementById('actionType').value,
                delay: parseInt(document.getElementById('delay').value),
                poll_options: [document.getElementById('poll1').value, document.getElementById('poll2').value].filter(o => o)
            };

            const res = await fetch('/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            if (result.stop_key) {
                currentTaskId = result.task_id;
                document.getElementById('stopKeyDisplay').classList.remove('hidden');
                document.getElementById('keyVal').innerText = result.stop_key;
                startPolling(result.task_id);
            }
        }

        async function stopEngine() {
            const key = document.getElementById('stopKeyInput').value;
            if (!key) { alert('Please enter the Stop Key.'); return; }
            const res = await fetch(`/stop/${key}`);
            const result = await res.json();
            alert(result.status || result.error);
        }

        function startPolling(taskId) {
            if (pollInterval) clearInterval(pollInterval);
            pollInterval = setInterval(async () => {
                const res = await fetch(`/logs/${taskId}`);
                const data = await res.json();
                const logBox = document.getElementById('logs');
                logBox.innerHTML = data.logs.map(l => `<div class="log-entry">${l}</div>`).join('');
                logBox.scrollTop = logBox.scrollHeight;
            }, 1000);
        }

        // Initialize UI
        updateUI();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/start', methods=['POST'])
def start_task():
    data = request.json
    task_id = str(int(time.time()))
    stop_key = secrets.token_hex(4).upper()
    tasks[stop_key] = FBAutomator(
        task_id, 
        stop_key, 
        data['auth_list'], 
        data['targets'], 
        data['messages'], 
        data['action_type'], 
        data['delay'], 
        data.get('poll_options')
    )
    threading.Thread(target=tasks[stop_key].run, daemon=True).start()
    return jsonify({"task_id": task_id, "stop_key": stop_key})

@app.route('/stop/<key>')
def stop_task(key):
    if key in tasks:
        tasks[key].stop()
        del tasks[key]
        return jsonify({"status": "Thread Killed Successfully"})
    return jsonify({"error": "Invalid Stop Key"}), 404

@app.route('/logs/<task_id>')
def get_logs(task_id):
    for t in tasks.values():
        if t.task_id == task_id:
            return jsonify({"logs": t.logs})
    return jsonify({"logs": []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
