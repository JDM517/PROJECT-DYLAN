import asyncio
import time
import sys
from dns.asyncresolver import Resolver
from dns.exception import DNSException

GREEN = "\033[92m"
CYAN = "\033[96m"
BLUE = "\033[94m"
RESET = "\033[0m"

TARGET_DOMAIN = "mcserver.us"
TIMEOUT_LIMIT = 120.0       
CONCURRENT_LIMIT = 1000     

def generate_words(choice):
    base_words = [
        "play", "mc", "pvp", "survival", "smp", "vanilla", "factions", "skyblock", 
        "towny", "anarchy", "creative", "prison", "bedwars", "modded", "network", 
        "craft", "lobby", "hub", "pixelmon", "cobblemon", "mine", "block", "realm", 
        "build", "node", "server", "vps", "host", "proxy"
    ]
    if choice == 1:
        return base_words
    elif choice == 2:
        words = list(base_words)
        for i in range(1, 80):
            words.extend([f"mc{i}", f"smp{i}", f"node{i}", f"play{i}", f"server{i}"])
        return words[:500]
    else:
        print("Generating 500,000+ word matrix in memory...")
        words = list(base_words)
        for i in range(1, 50001):
            words.extend([f"mc{i}", f"smp{i}", f"node{i}", f"play{i}", f"server{i}", f"craft{i}"])
        locs = ["us", "eu", "uk", "ca", "au", "na", "sa", "asia"]
        types = ["pvp", "smp", "mc", "play", "vanilla", "craft", "survival"]
        for loc in locs:
            for t in types:
                for num in range(1, 301):
                    words.append(f"{t}-{loc}{num}")
                    words.append(f"{loc}{num}-{t}")
        return words

async def scan_subdomain(resolver, sub, start_time, file_handle):
    if time.time() - start_time >= TIMEOUT_LIMIT: return
    full_host = f"{sub}.{TARGET_DOMAIN}"
    srv_host = f"_minecraft._tcp.{full_host}"
    try:
        a_records = await resolver.resolve(full_host, "A")
        ips = [r.to_text() for r in a_records]
        res_str = f"[IP Found] {full_host} -> " + ", ".join(ips)
        print(f"{GREEN}{res_str}{RESET}")
        file_handle.write(res_str + "\n")
        file_handle.flush()
    except DNSException: pass
    try:
        srv_records = await resolver.resolve(srv_host, "SRV")
        for r in srv_records:
            srv_str = f"[SRV Found] {full_host} -> {r.priority} {r.weight} {r.port} {r.target}"
            print(f"{CYAN}{srv_str}{RESET}")
            file_handle.write(srv_str + "\n")
            file_handle.flush()
    except DNSException: pass

async def main():
    banner = r"""
██████╗ ██████╗  ██████╗  ██████╗███████╗ ██████╗████████╗    ██████╗ ██╗   ██╗██╗      ██████╗ ███╗   ██╗
██╔══██╗██╔══██╗██╔═══██╗ ██╔════╝██╔════╝██╔════╝╚══██╔══╝    ██╔══██╗╚██╗ ██╔╝██║      ██╔══██╗████╗  ██║
██████╔╝██████╔╝██║   ██║ ██║     █████╗  ██║        ██║       ██║  ██║ ╚████╔╝ ██║      ███████║██╔██╗ ██║
██╔═══╝ ██╔══██╗██║   ██║ ██║     ██╔══╝  ██║        ██║       ██║  ██║  ╚██╔╝  ██║      ██╔══██║██║╚██╗██║
██║     ██║  ██║╚██████╔╝ ╚██████╗███████╗╚██████╗   ██║       ██████╔╝   ██║   ███████╗██║  ██║██║ ╚████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═════╝╚══════╝ ╚═════╝   ╚═╝       ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    """
    print(f"{BLUE}{banner}{RESET}")
    print(f"{BLUE}===================================================================================================={RESET}")
    print(" 1. Quick Scan (100 words)")
    print(" 2. Medium Scan (500 words)")
    print(" 3. Deep Scan (500,000+ words)")
    print(f"{BLUE}===================================================================================================={RESET}")
    
    try:
        choice = int(input("Select an option (1-3): "))
        if choice < 1 or choice > 3: raise ValueError
    except (ValueError, KeyboardInterrupt):
        print("\nInvalid choice. Exiting.")
        return

    words = generate_words(choice)
    print(f"Total entries to check: {len(words)}")
    start_time = time.time()
    resolver = Resolver()
    resolver.timeout = 1.0
    resolver.lifetime = 1.0
    
    print("--- Scan Started: Running parallel engine ---")
    with open("found_servers.txt", "a", encoding="utf-8") as f:
        semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)
        async def worker(sub):
            async with semaphore:
                if time.time() - start_time < TIMEOUT_LIMIT:
                    await scan_subdomain(resolver, sub, start_time, f)
        tasks = [worker(word) for word in words]
        for next_task in asyncio.as_completed(tasks):
            if time.time() - start_time >= TIMEOUT_LIMIT:
                print(f"\n{BLUE}--- 2 Minutes Reached! Stopping Scan ---{RESET}")
                break
            await next_task
    print("--- Scan Process Safely Closed ---")

if __name__ == "__main__":
    if sys.platform == "win32": asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
