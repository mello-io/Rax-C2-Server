<h1> Rax : C2 Server </h1>


A compact C2 (Command-and-Control) server and Agent deployment package for advanced cybersecurity research that can be done cost-effectively using open-source tools and virtualization, reviewing and implementing protocol design, encryption and evasion technique. Here’s a full step-by-step breakdown, tailored for realistic adversary simulation and EDR evasion research.

<h2> ⚙️ GOAL </h2>

Build a custom C2 framework that:
- Runs in a VM/lab setup
- Supports multiple agents (Windows/Linux)
- Has encrypted communication
- Offers modular payloads, execution, and exfiltration
- Avoids cloud or paid infrastructure

<br>


<h2> 🔨 1. Set Up the C2 Host (on Kali or Ubuntu VM) </h2>

```bash

sudo apt update && sudo apt install python3 python3-pip git
pip3 install flask flask-socketio cryptography

mkdir ~/RaxC2
cd ~/RaxC2

```

<br>


<h2> 🧠 2. Design Architecture </h2>

```perl

RaxC2/
├── server.py       # Flask + SocketIO
├── agent.py        # Implants/agents to run on targets
├── modules/        # Payload modules & features
├── logs/
└── keys/

```
```bash
mkdir -p logs keys modules
touch server.py agent.py
```

<br>


<h2> 🖥️ 3. Basic C2 Server Template (server.py) </h2>

Use the server.py file with the repo.

<br>


<h2> 🧬 4. Sample Agent Implant (agent.py for Windows/Linux) </h2>

Use the agent.py file with the repo.

<br>

<h2> 🔐 5. Generate SSL Certs </h2>

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
```

<br>


<h2> 🧪 6. Testing on Target </h2>

- Deploy agent.exe (compiled) on Windows VM.
```bash
pip install pyinstaller
pyinstaller --onefile agent.py

⚠️ Transfer the compiled agent.exe to the Windows target machine and execute it.
```
- Run C2 (python3 server.py) and issue commands.
```bash
python3 server.py
```  
- Exfiltrated data appears in the server console or saved logs. 

<br>

<h2>🔹 How to Send Commands </h2>
Currentl stage: Hardcoded support only – listen for connections and watch outputs.

Advanced - feature development ⚠️ : Create an admin console that sends commands like:

```bash
curl -X POST https://<C2-IP>:443/send_command -d 'whoami'
```

<br>

<h2> 🔧 Extend Functionality </h2>

- modules/screenshot.py: take screenshot and send back   :  Feature to add ⚠️
- modules/keylogger.py: live keystroke capture           :  Feature to add ⚠️
- modules/persistence.py: registry or startup hijacks    :  Feature to add ⚠️ 

<br>


<h2> 🧰 VM Setup Tips </h2>

- Kali/Ubuntu (for C2)
- Windows 11 with Entra ID and EDR (for agent testing)
- Use NAT or Host-only Adapter for isolation
- Use Fakenet-NG or Wireshark for traffic monitoring
- Use snapshots before malware testing

