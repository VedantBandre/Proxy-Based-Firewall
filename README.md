# Proxy-Based-Firewall

A proxy-based custom firewall using Squid, a Bottle.py REST API, and a DearPyGUI desktop interface.

## Overview

This project provides:
- **Squid proxy** for network access control
- **REST API** (`api.py`) to manage domains, ports, and MAC addresses
- **GUI** (`dpgui.py`) for easy management

## Prerequisites

### 1. Install Squid

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install squid
```

**CentOS/RHEL/Fedora:**
```bash
sudo dnf install squid
# or
sudo yum install squid
```

**Arch Linux:**
```bash
sudo pacman -S squid
```

### 2. Create Required Configuration Files

The API expects these files to exist. Create them if they don't:

```bash
sudo touch /etc/squid/ban_domains.txt
sudo touch /etc/squid/allowed_ports.txt
sudo touch /etc/squid/allowed_mac.txt
sudo chown -R squid:squid /etc/squid/*.txt  # or proxy:proxy depending on your distro
```

### 3. Configure Squid

Edit `/etc/squid/squid.conf` to include the generated files:

```conf
# Deny banned domains
acl banned_domains dstdomain "/etc/squid/ban_domains.txt"
http_access deny banned_domains

# Allow specific ports
acl allowed_ports port "/etc/squid/allowed_ports.txt"
http_access allow allowed_ports

# Allow specific MAC addresses
acl allowed_macs arp "/etc/squid/allowed_mac.txt"
http_access allow allowed_macs
```

After editing, test and restart Squid:
```bash
sudo squid -k parse          # Test configuration
sudo systemctl restart squid
sudo systemctl enable squid   # Auto-start on boot
```

## Installation

### 1. Clone/Navigate to the Project

```bash
cd Proxy-Based-Firewall
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Requirements

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install bottle dearpygui requests
```

## Usage

### Start the API Server

```bash
python3 api.py
```

The API will run on `http://0.0.0.0:7505/`

### Start the GUI (in another terminal)

```bash
source venv/bin/activate  # if not already activated
python3 dpgui.py
```

The GUI will connect to the API at `127.0.0.1:7505` by default.

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /service/<oper>` | Manage Squid service (`start`, `stop`, `restart`, `reload`) |
| `GET /domain/<stat>/<domain>` | Manage banned domains (`add`, `remove`, `show`) |
| `GET /port/<stat>/<port>` | Manage allowed ports (`add`, `remove`, `show`) |
| `GET /arp/<stat>/<mac>` | Manage allowed MAC addresses (`add`, `remove`, `show`) |

## File Structure

```
.
├── api.py           # Bottle.py REST API server
├── dpgui.py         # DearPyGUI management interface
├── requirements.txt # Python dependencies
├── squid.conf      # Example Squid configuration
└── README.md       # This file
```

## Troubleshooting

### API Error: "No such file or directory"
Ensure the Squid configuration files exist:
```bash
sudo mkdir -p /etc/squid
sudo touch /etc/squid/ban_domains.txt /etc/squid/allowed_ports.txt /etc/squid/allowed_mac.txt
```

### Permission Denied
Run API with sudo if managing system services:
```bash
sudo $(which python3) api.py
```

### GUI Won't Connect
Verify the API is running and check the IP/port in the GUI (default: `127.0.0.1:7505`).

## Security Notes

- The API runs on all interfaces (`0.0.0.0`) by default. Restrict access with firewall rules if needed.
- No authentication is implemented. Run only on trusted networks.
- The API executes `systemctl` commands - ensure proper permissions.
