# FastestVPN WireGuard Config Generator

Automatically generate WireGuard configuration files for all FastestVPN servers.

## 🎯 Goal

When FastestVPN support sends you a default WireGuard configuration file (typically `fastestvpn.conf`) with only one
server configured, this tool helps you quickly generate individual configuration files for **all available servers**
across all locations worldwide.

Instead of manually editing the configuration file each time you want to connect to a different server,
you'll have a complete library of ready-to-use config files organized by country, city, and server type.

## 🚀 Features

- **Automatic Server Discovery**: Fetches the complete list of available VPN servers from FastestVPN support page
- **Bulk Config Generation**: Creates individual `.conf` file for every server location
- **Smart Naming**: Files are named by country, city, and server type (e.g., `united-states-new-york.conf`, `united-kingdom-london-streaming.conf`)
- **Server Type Support**: Recognizes and labels specialized servers:
  - Standard servers
  - Streaming optimized servers
  - P2P servers
  - Double VPN servers
- **Multi-Protocol Support**: Can fetch servers from TCP, UDP, and IKEv2 protocols

## 📋 Prerequisites

- Python 3.14 or higher
- A WireGuard configuration file from FastestVPN support (with your credentials)

## 🔧 Installation

1. Clone or download this repository:
```bash
git clone https://github.com/marcelorodrigo/fastestvpn-config-generator.git
cd fastestvpn-config-generator
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
```

3. Activate the virtual environment:
   - **macOS/Linux**:
   ```bash
   source venv/bin/activate
   ```
   - **Windows**:
   ```bash
   venv\Scripts\activate
   ```

4. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 📝 Setup

1. **Obtain your FastestVPN WireGuard configuration file**:
   - Send an email to **support@fastestvpn.com** with the subject: "WireGuard Configuration Request"
   - In your email, request a WireGuard configuration file for your account
   - FastestVPN support will respond with a `.conf` file containing your credentials

2. **Set up your configuration file**:
   - Copy your configuration file received in the email to the project directory
   - Rename it to `fastestvpn.conf`
    
Example `fastestvpn.conf` (after filling in your keys):
```ini
[Interface]
PrivateKey = your-actual-private-key-here
Address = 172.16.254.254/32
DNS = 10.8.8.8

[Peer]
PublicKey = actual-public-key-from-fastestvpn
AllowedIPs = 0.0.0.0/0
Endpoint = ca-01.jumptoserver.com:51820
```

## 🎬 Usage

### Generate All Server Configs

Run the main script to generate configuration files for all available servers:

```bash
python3 generate_configs.py
```

This will:
1. Fetch the complete list of VPN servers from FastestVPN
2. Generate individual `.conf` files for each server
3. Save all files in the `output/` directory

### Example Output

After running the script, your `output/` folder will contain files like:

```text
output/
├── united-states-new-york.conf
├── united-states-los-angeles.conf
├── united-kingdom-london.conf
├── united-kingdom-london-streaming.conf
├── canada-toronto.conf
├── australia-sydney.conf
├── germany-frankfurt.conf
├── netherlands-amsterdam-p2p.conf
└── ... (100+ more servers)
```

### View Available Servers

To see the list of all available servers without generating configs:

```bash
python3 fetch_vpn_servers.py
```

For servers across all protocols:

```bash
python3 fetch_all_protocols.py
```

## 📱 Using the Configuration Files

### On Desktop/Laptop (Standard WireGuard Client)

1. Install the official [WireGuard client](https://www.wireguard.com/install/)
2. Import a configuration file:
   - **Windows/macOS**: Click "Import tunnel(s) from file" and select a `.conf` file from the `output/` folder
   - **Linux**: Copy the file to `/etc/wireguard/` and activate with `wg-quick up <filename>`

3. Activate the VPN connection

### On Mobile Devices

1. Install the WireGuard app from your app store
2. Transfer the desired `.conf` file to your device
3. Open the WireGuard app and import the configuration
4. Activate the VPN tunnel

### On Routers

Many modern routers support WireGuard (e.g., GL.iNet, Ubiquiti, pfSense, OpenWrt):

1. Access your router's admin interface
2. Navigate to the WireGuard/VPN section
3. Upload or paste the contents of your chosen `.conf` file
4. Enable the WireGuard connection

Consult your router's documentation for specific instructions.

## 🎯 Choosing the Right Server

- **Regular browsing**: Use any standard server (e.g., `country-city.conf`)
- **Streaming**: Use `-streaming` servers for better performance with Netflix, Hulu, etc.
- **Torrenting/P2P**: Use `-p2p` servers for optimal peer-to-peer connections
- **Extra privacy**: Use `-via-` Double VPN servers for multi-hop connections

## 🔄 Updating Server Configs

FastestVPN may add new servers or update existing ones. To refresh your configuration files:

1. Run the generator again:
```bash
python3 generate_configs.py
```

2. The script will fetch the latest server list and regenerate all files

## 🧪 Testing

Run the test suite to verify functionality:

```bash
pytest
```

With coverage report:

```bash
pytest --cov=utils --cov-report=term-missing
```

## ⚠️ Important Notes

- **Keep your keys private**: Never share your `PrivateKey` or commit it to version control
- **One connection at a time**: Most VPN providers limit simultaneous connections per account
- **Server availability**: Not all servers may work at all times; try different locations if you experience issues

## 🤝 Support

If you encounter issues:

1. Ensure your `fastestvpn.conf` template file has valid credentials
2. Check that you have an active FastestVPN subscription
3. Verify your internet connection
4. Contact FastestVPN support for account-related issues

## 📄 License

This is an unofficial tool for FastestVPN users. Please respect FastestVPN's terms of service.

---

**Note**: This tool is not affiliated with or endorsed by FastestVPN.
It's a community project to help users manage their WireGuard configurations more easily.
