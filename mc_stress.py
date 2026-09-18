import asyncio
import time
import sys

# Interface Colors
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

CONCURRENT_FLOOD = 500  # Number of rapid connections to fire simultaneously

async def rapid_ping(host, port, stats):
    """Fires a rapid TCP connection packet to test network endpoint load."""
    try:
        start = time.time()
        # Open a raw network connection socket stream
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=1.5
        )
        latency = (time.time() - start) * 1000
        stats["success"] += 1
        stats["latencies"].append(latency)
        
        # Cleanly drop the socket connection right away to free the thread
        writer.close()
        await writer.wait_closed()
        sys.stdout.write(f"{GREEN}.{RESET}")
        sys.stdout.flush()
    except Exception:
        stats["failed"] += 1
        sys.stdout.write(f"{RED}x{RESET}")
        sys.stdout.flush()

async def main():
    print(f"{BLUE}========================================================================================={RESET}")
    print("  ███████╗████████╗██████╗ ███████╗███████╗███████╗    ████████╗███████╗███████╗████████╗ ")
    print("  ██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔════╝██╔════╝    ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝ ")
    print("  ███████╗   ██║   ██████╔╝█████╗  ███████╗███████╗       ██║   █████╗  █████╗     ██║    ")
    print("  ╚════██║   ██║   ██╔══██╗██╔══╝  ╚════██║╚════██║       ██║   ██╔══╝  ██╔══╝     ██║    ")
    print("  ███████║   ██║   ██║  ██║███████╗███████║███████║       ██║   ███████╗███████╗   ██║    ")
    print("  ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝       ╚═╝   ╚══════╝╚══════╝   ╚═╝    ")
    print(f"{BLUE}========================================================================================={RESET}")
    
    target = input("Enter server IP or Domain to test: ").strip()
    if not target: return
    
    host, port = (target.split(":") if ":" in target else (target, 25565))
    port = int(port)
    
    print(f"\n{YELLOW}[*] Preparing async connection flood targeting {host}:{port}...{RESET}")
    print(f"[*] Firing {CONCURRENT_FLOOD} rapid socket checks simultaneously. Legend: ({GREEN}.{RESET}=Success, {RED}x{RESET}=Dropped)\n")
    
    stats = {"success": 0, "failed": 0, "latencies": []}
    start_time = time.time()
    
    # Generate and execute the massive wave of connections concurrently
    tasks = [rapid_ping(host, port, stats) for _ in range(CONCURRENT_FLOOD)]
    await asyncio.gather(*tasks)
    
    elapsed = time.time() - start_time
    print(f"\n\n{BLUE}-----------------------------------------------------------------------------------------{RESET}")
    print(f"{GREEN}[+] Network Flood Wave Complete in {elapsed:.2f} seconds!{RESET}")
    print(f"    - Successful Handshakes: {stats['success']}")
    print(f"    - Dropped / Timed Out:    {stats['failed']}")
    if stats["latencies"]:
        avg_lat = sum(stats["latencies"]) / len(stats["latencies"])
        print(f"    - Average Node Latency:   {avg_lat:.1f}ms")
    print(f"{BLUE}-----------------------------------------------------------------------------------------{RESET}")

if __name__ == "__main__":
    if sys.platform == 'win32': asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
