#!/usr/init/env python3
"""
Project Dylan - Consolidated Master Recon & Utility Toolkit (Upgraded Edition)
Author: Dylan
Repository: JDM517/PROJECT-DYLAN
"""

import asyncio
import socket
import sys
import time
import urllib.request
import json
import ipaddress
import base64
from concurrent.futures import ThreadPoolExecutor

try:
    from dns.asyncresolver import Resolver
    from dns.exception import DNSException
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False


# ANSI Color Codes for Output Styling
RESET = "\033[0m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
BOLD = "\033[1m"


def banner():
    print(f"""{CYAN}{BOLD}
    ╔══════════════════════════════════════════════════╗
    ║                 PROJECT DYLAN                    ║
    ║      Consolidated Master Recon Toolkit (v2.0)    ║
    ╚══════════════════════════════════════════════════╝
    {RESET}""")


# --- TOOL 1: Advanced Async Minecraft & Subdomain Scanner with SLP Pinger ---
def generate_words(choice):
    """Dynamically builds intelligent word list permutations based on the chosen tier choice."""
    base_words = [
        'play', 'mc', 'pvp', 'survival', 'smp', 'vanilla', 'factions', 'skyblock', 
        'towny', 'anarchy', 'creative', 'prison', 'bedwars', 'modded', 'network', 
        'craft', 'lobby', 'hub', 'pixelmon', 'cobblemon', 'mine', 'block', 'realm', 
        'build', 'node', 'server', 'vps', 'host', 'proxy'
    ]
    if choice == 1:
        return base_words
    elif choice == 2:
        words = set(base_words)
        locs = ['us', 'eu', 'na', 'au', 'east', 'west']
        for w in base_words:
            for l in locs:
                words.add(f"{w}-{l}")
                words.add(f"{l}-{w}")
            for i in range(1, 50):
                words.add(f"{w}{i}")
        return list(words)[:1000]
    else:
        print(f'{YELLOW}Generating high-density permutation matrix in memory...{RESET}')
        words = set(base_words)
        locs = ['us', 'eu', 'uk', 'ca', 'au', 'na', 'sa', 'asia', 'east', 'west', 'de', 'fr']
        types = ['pvp', 'smp', 'mc', 'play', 'vanilla', 'craft', 'survival', 'hub', 'network', 'skyblock']
        
        for loc in locs:
            for t in types:
                words.add(f'{t}-{loc}')
                words.add(f'{loc}-{t}')
                for num in range(1, 150):
                    words.add(f'{t}-{loc}{num}')
                    words.add(f'{loc}{num}-{t}')
                    words.add(f'{t}{num}-{loc}')
        
        for i in range(1, 10000):
            words.add(f'mc{i}')
            words.add(f'smp{i}')
            words.add(f'node{i}')
            words.add(f'play{i}')
            
        return list(words)

async def ping_minecraft_server(host, port=25565, timeout=2.0):
    """Pings a Minecraft server using the modern TCP SLP protocol to extract status & MOTD."""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
        
        host_bytes = host.encode('utf-8')
        packet = (
            b'\x00'
            b'\xff\x05'
            + bytes([len(host_bytes)]) + host_bytes
            + int(port).to_bytes(2, 'big')
            + b'\x01'
        )
        packet = len(packet).to_bytes(1, 'big') + packet
        writer.write(packet)
        writer.write(b'\x01\x00')
        await writer.drain()
        
        _ = await reader.read(1)
        data_len = await reader.read(1)
        if not data_len:
            writer.close()
            return None
            
        json_len = await reader.read(1)
        response_data = await reader.read(int.from_bytes(json_len, 'big'))
        
        writer.close()
        await writer.wait_closed()
        
        return json.loads(response_data.decode('utf-8', errors='ignore'))
    except Exception:
        return None

async def scan_subdomain_async(resolver, sub, target_domain, start_time, timeout_limit, file_handle):
    """Performs parallel async resolution checks and pings active Minecraft ports."""
    if time.time() - start_time >= timeout_limit:
        return
    full_host = f'{sub}.{target_domain}'
    
    ips = []
    if DNS_AVAILABLE and resolver:
        for rtype in ['A', 'AAAA']:
            try:
                records = await resolver.resolve(full_host, rtype)
                for r in records:
                    ips.append(r.to_text())
            except DNSException:
                pass
    
    if not ips:
        try:
            result = socket.getaddrinfo(full_host, None)
            for item in result:
                ip = item[4][0]
                if ip not in ips:
                    ips.append(ip)
        except socket.gaierror:
            pass
            
    if ips:
        res_str = f'[IP Found] {full_host} -> ' + ', '.join(ips)
        print(f"{GREEN}{res_str}{RESET}")
        file_handle.write(res_str + '\n')
        file_handle.flush()
        
        server_status = await ping_minecraft_server(full_host, 25565)
        if server_status:
            version = server_status.get('version', {}).get('name', 'Unknown')
            players = server_status.get('players', {})
            online = players.get('online', 0)
            max_players = players.get('max', 0)
            status_str = f"  -> [MC ONLINE] Ver: {version} | Players: {online}/{max_players}"
            print(f"{YELLOW}{status_str}{RESET}")
            file_handle.write(status_str + '\n')
            file_handle.flush()

def run_advanced_scanner():
    print(f"\n{BLUE}--- ADVANCED MINECRAFT & SUBDOMAIN SCANNER ---{RESET}")
    print(" 1. Quick Scan (Base wordlist)")
    print(" 2. Medium Scan (Expanded permutations)")
    print(" 3. Deep Scan (High-density matrix generator)")
    
    try:
        choice = int(input(f"\n{YELLOW}> Select wordlist size (1-3): {RESET}"))
        if choice < 1 or choice > 3:
            raise ValueError
            
        print(f"\n{BLUE}--- SELECT TARGET HOSTING NETWORK ---{RESET}")
        print(" 1. mcserver.us")
        print(" 2. aternos.me")
        print(" 3. falixsrv.me")
        print(" 4. playit.gg")
        print(" 5. minekeep.gg")
        print(" 6. bisect.host")
        print(" 7. wisehost.gg")
        print(" 8. apexmc.co")
        print(" 9. scalacube.media")
        print(" 10. nodecraft.gg")
        print(" 11. SCAN ALL")
        print(" 12. Custom Domain")
        
        net_choice = int(input(f"\n{YELLOW}> Select hosting network (1-12): {RESET}"))
        if net_choice < 1 or net_choice > 12:
            raise ValueError
            
        target_domains = []
        if net_choice == 1: target_domains.append("mcserver.us")
        elif net_choice == 2: target_domains.append("aternos.me")
        elif net_choice == 3: target_domains.append("falixsrv.me")
        elif net_choice == 4: target_domains.append("playit.gg")
        elif net_choice == 5: target_domains.append("minekeep.gg")
        elif net_choice == 6: target_domains.append("bisect.host")
        elif net_choice == 7: target_domains.append("wisehost.gg")
        elif net_choice == 8: target_domains.append("apexmc.co")
        elif net_choice == 9: target_domains.append("scalacube.media")
        elif net_choice == 10: target_domains.append("nodecraft.gg")
        elif net_choice == 11: 
            target_domains = [
                "mcserver.us", "aternos.me", "falixsrv.me", "playit.gg", "minekeep.gg", 
                "bisect.host", "wisehost.gg", "apexmc.co", "scalacube.media", "nodecraft.gg"
            ]
        else:
            custom_domain = input(f"{YELLOW}> Enter custom target domain: {RESET}").strip()
            target_domains.append(custom_domain if custom_domain else "mcserver.us")
            
    except (ValueError, KeyboardInterrupt):
        print(f"{RED}[!] Invalid input or cancelled.{RESET}")
        return

    words = generate_words(choice)
    total_checks = len(words) * len(target_domains)
    print(f"\n{CYAN}[*] Total entries to check: {total_checks}{RESET}")
    
    timeout_limit = 120.0
    concurrent_limit = 1000
    start_time = time.time()
    
    resolver = None
    if DNS_AVAILABLE:
        resolver = Resolver()
        resolver.timeout = 1.0
        resolver.lifetime = 1.0
        
    print(f"{CYAN}--- Scan Started targeting: {', '.join(target_domains)} ---{RESET}")
    
    async def async_wrapper():
        with open("found_servers.txt", "a", encoding="utf-8") as f:
            semaphore = asyncio.Semaphore(concurrent_limit)
            async def worker(sub, dom):
                async with semaphore:
                    if time.time() - start_time < timeout_limit:
                        await scan_subdomain_async(resolver, sub, dom, start_time, timeout_limit, f)
                        
            tasks = [worker(word, domain) for word in words for domain in target_domains]
            for next_task in asyncio.as_completed(tasks):
                if time.time() - start_time >= timeout_limit:
                    print(f"\n{BLUE}--- 2 Minutes Reached! Stopping Scan ---{RESET}")
                    break
                await next_task

    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(async_wrapper())
    print(f"{CYAN}--- Scan Process Safely Closed. Results saved to found_servers.txt ---{RESET}")


# --- TOOL 2: Port & Subnet Sweeper with CIDR Support ---
def check_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1.0)
        result = sock.connect_ex((target_ip, port))
        sock.close()
        if result == 0:
            print(f"{GREEN}[OPEN]{RESET} {target_ip}:{port}")
            return True
    except Exception:
        pass
    return False

def run_port_sweeper():
    print(f"\n{BLUE}--- ADVANCED PORT & SUBNET SWEEPER ---{RESET}")
    target_input = input(f"{YELLOW}> Enter target IP or CIDR range (e.g. 192.168.1.5 or 192.168.1.0/24): {RESET}").strip()
    port_input = input(f"{YELLOW}> Enter ports (comma-separated, e.g. 25565,80,443,22): {RESET}").strip()
    
    try:
        ports = [int(p.strip()) for p in port_input.split(',')]
        
        if '/' in target_input:
            targets = [str(ip) for ip in ipaddress.ip_network(target_input, strict=False).hosts()]
        else:
            targets = [target_input]
            
        print(f"\n{CYAN}[*] Sweeping {len(targets)} target(s) across {len(ports)} port(s)...{RESET}")
        with ThreadPoolExecutor(max_workers=200) as executor:
            for ip in targets:
                executor.map(lambda p: check_port(ip, p), ports)
                
    except ValueError:
        print(f"{RED}[!] Invalid IP, CIDR, or port format entered.{RESET}")


# --- TOOL 3: Mojang Player, UUID & Skin Tracker ---
def track_mojang_uuid():
    print(f"\n{BLUE}--- MOJANG PLAYER & SKIN TRACKER ---{RESET}")
    username = input(f"{YELLOW}> Enter Minecraft username: {RESET}").strip()
    if not username:
        return
    print(f"\n{CYAN}[*] Fetching profile data for player: {username}{RESET}")
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            name = data.get('name')
            uuid = data.get('id')
            print(f"{GREEN}[+] Username:{RESET} {name}")
            print(f"{GREEN}[+] UUID:{RESET} {uuid}")
            
            session_url = f"https://sessionserver.mojang.com/sessionserver/minecraft/profile/{uuid}"
            req_sess = urllib.request.Request(session_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_sess) as sess_resp:
                sess_data = json.loads(sess_resp.read().decode())
                for prop in sess_data.get('properties', []):
                    if prop.get('name') == 'textures':
                        decoded_texture = json.loads(base64.b64decode(prop.get('value')).decode())
                        skin_url = decoded_texture.get('textures', {}).get('SKIN', {}).get('url')
                        if skin_url:
                            print(f"{GREEN}[+] Skin URL:{RESET} {skin_url}")
    except Exception as e:
        print(f"{RED}[!] Failed to retrieve player profile: {e}{RESET}")


# --- MAIN MENU ---
def main():
    banner()
    while True:
        print(f"\n{BOLD}Select a tool utility:{RESET}")
        print("  1. Advanced Minecraft & Subdomain Scanner (with Live SLP Ping)")
        print("  2. Port & Subnet Sweeper (CIDR supported)")
        print("  3. Mojang Player & Skin Tracker")
        print("  4. Exit")
        
        choice = input(f"\n{YELLOW}> {RESET}").strip()
        
        if choice == '1':
            run_advanced_scanner()
        elif choice == '2':
            run_port_sweeper()
        elif choice == '3':
            track_mojang_uuid()
        elif choice == '4':
            print(f"{CYAN}Exiting Project Dylan.{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}[!] Invalid selection, try again.{RESET}")


if __name__ == "__main__":
    main()