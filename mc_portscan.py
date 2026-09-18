import asyncio
import socket
import time
import sys

# Interface Color Variables
GREEN = '\033[92m'
CYAN = '\033[96m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

async def check_port(host, port):
    """Attempts a rapid TCP handshake on a specific port mapping."""
    try:
        # Run a native low-level socket stream connection
        conn = asyncio.open_connection(host, port)
        # Force a strict 1-second timeout so it runs fast
        reader, writer = await asyncio.wait_for(conn, timeout=1.0)
        print(f"{GREEN}  [+] PORT OPEN: {port} (Active Minecraft Node Candidate){RESET}")
        writer.close()
        await writer.wait_closed()
        return port
    except Exception:
        return None

async def main():
    # Thick block font banner configured specifically to read "PORT SWEEPER"
    print(f"{BLUE}")
    print("=========================================================================================")
    print("  ██████╗  ██████╗ ██████╗ ████████╗    ███████╗██╗    ██╗███████╗███████╗██████╗  ███████╗ ")
    print("  ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝    ██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗██╔════╝ ")
    print("  ██████╔╝██║   ██║██████╔╝   ██║       ███████╗██║ █╗ ██║█████╗  █████╗  ██████╔╝█████╗   ")
    print("  ██╔═══╝ ██║   ██║██╔══██╗   ██║       ╚════██║██║███╗██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝   ")
    print("  ██║     ╚██████╔╝██║  ██║   ██║       ███████║╚███╔███╔╝███████╗███████╗██║     ███████╗ ")
    print("  ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝     ╚══════╝ ")
    print("=========================================================================================")
    print(f"{RESET}")
    
    host = input("Enter server IP or Domain to sweep (e.g., node1.mcserver.us): ").strip()
    if not host:
        print("No target entered. Exiting.")
        return
        
    print(f"\n{BLUE}Configuring standard custom port boundaries...{RESET}")
    start_port = 25560
    end_port = 25600
    
    print(f"{YELLOW}[*] Sweeping ports {start_port} to {end_port} concurrently...{RESET}\n")
    start_time = time.time()
    
    # Pack tasks to run in parallel
    tasks = [check_port(host, p) for p in range(start_port, end_port + 1)]
    results = await asyncio.gather(*tasks)
    
    open_ports = [p for p in results if p is not None]
    elapsed = round(time.time() - start_time, 2)
    
    print(f"\n{BLUE}-----------------------------------------------------------------------------------------{RESET}")
    print(f"{GREEN}[+] Sweep Finished in {elapsed} seconds!{RESET}")
    print(f"Total active ports discovered: {len(open_ports)}")
    if open_ports:
        print(f"Open ports found: {', '.join(map(str, open_ports))}")
    print(f"{BLUE}-----------------------------------------------------------------------------------------{RESET}")

if __name__ == "__main__":
    if sys.platform == 'win32': asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
