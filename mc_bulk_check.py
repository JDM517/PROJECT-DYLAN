import asyncio
import os
import sys
import time
import socket
import struct
import json
from dns.resolver import Resolver as SyncResolver

# Interface Color Variables
GREEN = '\033[92m'
CYAN = '\033[96m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

CONCURRENT_LIMIT = 200  # Number of servers to check at the exact same microsecond

def get_srv_redirect(host):
    """Tracks down enterprise proxy pathways to find hidden custom game ports."""
    try:
        resolver = SyncResolver()
        resolver.timeout = 1.0
        resolver.lifetime = 1.0
        answers = resolver.resolve(f"_minecraft._tcp.{host}", "SRV")
        for r in answers:
            return str(r.target).rstrip("."), int(r.port)
    except Exception:
        pass
    return host, 25565

def read_varint(sock):
    """Securely unrolls protocol tracker bytes."""
    data = 0
    for i in range(5):
        b = sock.recv(1)
        if not b: return 0
        b = b[0] if isinstance(b, bytes) else b
        data |= (b & 0x7F) << (7 * i)
        if not b & 0x80: return data
    return data

def pack_varint(d):
    """Packs raw values into standard VarInt structures."""
    res = b""
    while True:
        b = d & 0x7F
        d >>= 7
        if d != 0: res += struct.pack("B", b | 0x80)
        else:
            res += struct.pack("B", b)
            break
    return res

def ping_minecraft_server(host, port=25565):
    """Fires a modernized protocol 767 network handshake directly to the socket."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)
        sock.connect((host, port))
        
        host_bytes = host.encode('utf-8')
        packet = pack_varint(0x00) + pack_varint(767) + pack_varint(len(host_bytes)) + host_bytes + struct.pack('>H', port) + pack_varint(1)
        sock.send(pack_varint(len(packet)) + packet)
        sock.send(pack_varint(1) + pack_varint(0x00))
        
        _length = read_varint(sock)
        _packet_id = read_varint(sock)
        data_length = read_varint(sock)
        if data_length == 0: return None
        
        data = b""
        while len(data) < data_length:
            chunk = sock.recv(data_length - len(data))
            if not chunk: break
            data += chunk
        sock.close()
        return json.loads(data.decode('utf-8'))
    except Exception:
        return None

async def check_worker(semaphore, target, file_handle):
    """Executes status validation asynchronously."""
    async with semaphore:
        h, p = (target.split(":") if ":" in target else (target, None))
        if p:
            try: p = int(p)
            except ValueError: return
        else:
            loop = asyncio.get_running_loop()
            h, p = await loop.run_in_executor(None, get_srv_redirect, h)

        loop = asyncio.get_running_loop()
        res = await loop.run_in_executor(None, ping_minecraft_server, h, p)

        if res:
            version = res.get('version', {}).get('name', 'Unknown')
            online = res.get('players', {}).get('online', 0)
            max_p = res.get('players', {}).get('max', 0)
            
            output = f"[LIVE] {target} -> Version: {version} | Players: {online}/{max_p}"
            print(f"{GREEN}{output}{RESET}")
            file_handle.write(f"{target} -> Players: {online}/{max_p}\n")
            file_handle.flush()
        else:
            print(f"{RED}[OFFLINE] {target}{RESET}")

async def main():
    # Thick block font banner configured specifically to read "BULK CHECKER"
    print(f"{BLUE}")
    print("=========================================================================================")
    print("  ██████╗ ██╗   ██╗██╗     ██╗  ██╗     ██████╗██╗  ██╗███████╗██████╗██╗  ██╗███████╗██████╗  ")
    print("  ██╔══██╗██║   ██║██║     ██║ ██╔╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║  ██║██╔════╝██╔══██╗ ")
    print("  ██████╔╝██║   ██║██║     █████╔╝     ██║     ███████║█████╗  ██║     ███████║█████╗  ██████╔╝ ")
    print("  ██╔══██╗██║   ██║██║     ██╔═██╗     ██║     ██╔══██║██╔══╝  ██║     ██╔══██║██╔══╝  ██╔══██╗ ")
    print("  ██████╔╝╚██████╔╝███████╗██║  ██╗    ╚██████╗██║  ██║███████╗╚██████╗██║  ██║███████╗██║  ██║ ")
    print("  ╚══════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ")
    print("=========================================================================================")
    print(f"{RESET}")

    if not os.path.exists("found_servers.txt"):
        print(f"{RED}[-] Error: 'found_servers.txt' not found. Run a scanner first!{RESET}")
        return

    print("[*] Harvesting and parsing unique routes from found_servers.txt...")
    unique_servers = set()
    with open("found_servers.txt", "r", encoding="utf-8") as f:
        for line in f:
            if "->" in line:
                cleaned = line.replace("[IP Found]", "").replace("[SRV Found]", "").strip()
                if "->" in cleaned:
                    parts = cleaned.split("->")
                    if len(parts) >= 1:
                        addr = parts[0].strip()
                        if addr: unique_servers.add(addr)

    targets = sorted(list(unique_servers))
    print(f"{GREEN}[+] Found {len(targets)} unique servers. Starting async status scan...{RESET}\n")
    semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)

    with open("live_right_now.txt", "w", encoding="utf-8") as out_f:
        tasks = [check_worker(semaphore, t, out_f) for t in targets]
        await asyncio.gather(*tasks)

    elapsed = round(time.time() - start_time, 2) if 'start_time' in globals() else "0"
    print(f"\n{BLUE}--- Bulk Check Complete ---{RESET}")
    print("All active servers saved to: live_right_now.txt")

if __name__ == "__main__":
    if sys.platform == 'win32': asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
