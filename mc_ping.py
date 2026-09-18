import socket
import struct
import json
import time
import sys

# Crucial fix: Dynamically load the resolver we already installed on your system
try:
    from dns.resolver import Resolver
    HAS_DNS = True
except ImportError:
    HAS_DNS = False

GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

def get_srv_redirect(host):
    """Checks if a network uses an SRV redirect to hide its actual game servers."""
    if not HAS_DNS:
        return host, 25565
    try:
        resolver = Resolver()
        resolver.timeout = 1.5
        resolver.lifetime = 1.5
        answers = resolver.resolve(f"_minecraft._tcp.{host}", "SRV")
        for r in answers:
            # Extract the actual target routing node and custom port
            target = str(r.target).rstrip(".")
            return target, int(r.port)
    except Exception:
        pass
    return host, 25565

def read_varint(sock):
    """Reads standard Minecraft VarInt tracking bytes securely."""
    data = 0
    for i in range(5):
        b = sock.recv(1)
        if not b:
            return 0
        b = b[0]
        data |= (b & 0x7F) << (7 * i)
        if not b & 0x80:
            return data
    return data

def pack_varint(d):
    """Packs standard integer metrics into a VarInt byte layout."""
    res = b""
    while True:
        b = d & 0x7F
        d >>= 7
        if d != 0:
            res += struct.pack("B", b | 0x80)
        else:
            res += struct.pack("B", b)
            break
    return res

def ping_minecraft_server(host, port=25565):
    """Pings a Minecraft server using standard modern protocol handshakes."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(4.0)
        sock.connect((host, port))

        # Protocol 767 handles all modern 1.21+ enterprise network structures smoothly
        host_bytes = host.encode('utf-8')
        packet = pack_varint(0x00) + pack_varint(767) + pack_varint(len(host_bytes)) + host_bytes + struct.pack('>H', port) + pack_varint(1)
        sock.send(pack_varint(len(packet)) + packet)

        # Send Status Request packet
        sock.send(pack_varint(1) + pack_varint(0x00))

        # Unpack the response
        _length = read_varint(sock)
        _packet_id = read_varint(sock)
        data_length = read_varint(sock)

        if data_length == 0:
            sock.close()
            return None

        data = b""
        while len(data) < data_length:
            chunk = sock.recv(data_length - len(data))
            if not chunk:
                break
            data += chunk

        sock.close()
        return json.loads(data.decode('utf-8'))
    except Exception:
        return None

def main():
    print(f"{BLUE}========================================{RESET}")
    print(f"{BLUE}       PROJECT DYLAN: LIVE CHECKER      {RESET}")
    print(f"{BLUE}========================================{RESET}")
    
    target = input("Enter server address (e.g., hypixel.net): ").strip()
    if not target:
        return

    # 1. Parse out custom user ports if manually entered
    if ":" in target:
        host, port_str = target.split(":")
        port = int(port_str)
        print(f"{BLUE}[*] Connecting directly to user port {host}:{port}...{RESET}")
    else:
        host = target
        print(f"{BLUE}[*] Resolving game network layout maps for {host}...{RESET}")
        # Run the tracking fix to locate hidden enterprise routing hosts
        host, port = get_srv_redirect(host)

    start = time.time()
    response = ping_minecraft_server(host, port)
    latency = int((time.time() - start) * 1000)

    if response:
        print(f"\n{GREEN}███████████████████████████████████████████{RESET}")
        print(f"{GREEN}  [+] SERVER IS ONLINE!{RESET}")
        print(f"  Connected to: {host}:{port}")
        print(f"  Latency: {latency}ms")
        
        version = response.get("version", {}).get("name", "Unknown")
        online = response.get("players", {}).get("online", 0)
        max_players = response.get("players", {}).get("max", 0)
        
        print(f"  Version: {version}")
        print(f"  Players: {online:,} / {max_players:,}")
        print(f"{GREEN}███████████████████████████████████████████{RESET}\n")
    else:
        print(f"\n{RED}[-] SERVER IS OFFLINE or UNREACHABLE{RESET}\n")

if __name__ == "__main__":
    main()
