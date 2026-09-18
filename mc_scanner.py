import asyncio
import time
import sys
from dns.asyncresolver import Resolver
from dns.exception import DNSException

# Interface Color Variables
GREEN = '\033[92m'
CYAN = '\033[96m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

TARGET_DOMAIN = 'mcserver.us'
TIMEOUT_LIMIT = 120.0
CONCURRENT_LIMIT = 1000

def generate_words(choice):
    """Dynamically builds word list permutations based on the chosen tier choice."""
    base_words = ['play', 'mc', 'pvp', 'survival', 'smp', 'vanilla', 'factions', 'skyblock', 'towny', 'anarchy', 'creative', 'prison', 'bedwars', 'modded', 'network', 'craft', 'lobby', 'hub', 'pixelmon', 'cobblemon', 'mine', 'block', 'realm', 'build', 'node', 'server', 'vps', 'host', 'proxy']
    if choice == 1:
        return base_words
    elif choice == 2:
        words = list(base_words)
        for i in range(1, 80):
            words.extend([f'mc{i}', f'smp{i}', f'node{i}', f'play{i}', f'server{i}'])
        return words[:500]
    else:
        print('Generating 500,000+ word matrix in memory...')
        words = list(base_words)
        for i in range(1, 50001):
            words.extend([f'mc{i}', f'smp{i}', f'node{i}', f'play{i}', f'server{i}', f'craft{i}'])
        locs = ['us', 'eu', 'uk', 'ca', 'au', 'na', 'sa', 'asia']
        types = ['pvp', 'smp', 'mc', 'play', 'vanilla', 'craft', 'survival']
        for loc in locs:
            for t in types:
                for num in range(1, 301):
                    words.append(f'{t}-{loc}{num}')
                    words.append(f'{loc}{num}-{t}')
        return words

async def scan_subdomain(resolver, sub, target_domain, start_time, file_handle):
    """Performs parallel async resolution checks against the target path grids."""
    if time.time() - start_time >= TIMEOUT_LIMIT: return
    full_host = f'{sub}.{target_domain}'
    srv_host = f'_minecraft._tcp.{full_host}'
    try:
        a_records = await resolver.resolve(full_host, 'A')
        ips = [r.to_text() for r in a_records]
        res_str = f'[IP Found] {full_host} -> ' + ', '.join(ips)
        print(f"{GREEN}{res_str}{RESET}")
        file_handle.write(res_str + '\n')
        file_handle.flush()
    except DNSException: pass
    try:
        srv_records = await resolver.resolve(srv_host, 'SRV')
        for r in srv_records:
            srv_str = f'[SRV Found] {full_host} -> {r.priority} {r.weight} {r.port} {r.target}'
            print(f"{CYAN}{srv_str}{RESET}")
            file_handle.write(srv_str + '\n')
            file_handle.flush()
    except DNSException: pass

async def main():
    # Thick block font banner configured specifically to read "MC SCANNER"
    print(f"{BLUE}")
    print("=========================================================================================")
    print("  ███╗   ███╗ ██████╗███████╗ ██████╗ ██████╗███╗   ██╗███╗   ██╗███████╗██████╗  ")
    print("  ████╗ ████║██╔════╝██╔════╝██╔════╝██╔════╝████╗  ██║████╗  ██║██╔════╝██╔══██╗ ")
    print("  ██╔████╔██║██║     ███████╗██║     ██║     ██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝ ")
    print("  ██║╚██╔╝██║██║     ╚════██║██║     ██║     ██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗ ")
    print("  ██║ ╚═╝ ██║╚██████╗███████║╚██████╗╚██████╗██║ ╚████║██║ ╚████║███████╗██║  ██║ ")
    print("  ╚═╝     ╚═╝ ╚═════╝╚══════╝ ╚═════╝ ╚═════╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ")
    print("=========================================================================================")
    print(f"{RESET}")
    
    print(f"{BLUE}STEP 1: SELECT SCAN WORDLIST SIZE{RESET}")
    print(" 1. Quick Scan (100 words)")
    print(" 2. Medium Scan (500 words)")
    print(" 3. Deep Scan (500,000+ words)")
    print(f"{BLUE}-----------------------------------------------------------------------------------------{RESET}")
    
    try:
        choice = int(input("Select wordlist size (1-3): "))
        if choice < 1 or choice > 3: raise ValueError
        
        print(f"\n{BLUE}STEP 2: SELECT TARGET HOSTING NETWORK{RESET}")
        print(" 1. mcserver.us       (Default Premium Host)")
        print(" 2. aternos.me        (Massive Free Community Host)")
        print(" 3. falixsrv.me       (Modded & Custom Paper Host)")
        print(" 4. playit.gg         (Global Player Self-Hosted Tunnels)")
        print(" 5. minekeep.gg       (Community Host Network)")
        print(" 6. bisect.host       (BisectHosting Premium Clusters)")
        print(" 7. wisehost.gg       (Wise Hosting Gaming Nodes)")
        print(" 8. apexmc.co         (Apex Hosting Premium Servers)")
        print(" 9. scalacube.media   (ScalaCube Routing Nodes)")
        print(" 10. nodecraft.gg     (Nodecraft Hardware Clusters)")
        print(" 11. SCAN ALL         (Run ALL 10 hosting networks at the exact same time)")
        print(" 12. Custom Domain     (Type your own entry)")
        print(f"{BLUE}-----------------------------------------------------------------------------------------{RESET}")
        
        net_choice = int(input("Select hosting network (1-12): "))
        if net_choice < 1 or net_choice > 12: raise ValueError
        
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
            custom_domain = input("\nEnter custom target domain (e.g., ploudos.me): ").strip()
            target_domains.append(custom_domain if custom_domain else "mcserver.us")
            
    except (ValueError, KeyboardInterrupt):
        print("\nInvalid input. Exiting.")
        return

    words = generate_words(choice)
    total_checks = len(words) * len(target_domains)
    print(f"Total entries to check across targets: {total_checks}")
    
    start_time = time.time()
    resolver = Resolver()
    resolver.timeout = 1.0
    resolver.lifetime = 1.0
    
    print(f"--- Scan Started targeting: {', '.join(target_domains)} ---")
    with open("found_servers.txt", "a", encoding="utf-8") as f:
        semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)
        async def worker(sub, dom):
            async with semaphore:
                if time.time() - start_time < TIMEOUT_LIMIT:
                    await scan_subdomain(resolver, sub, dom, start_time, f)
                    
        tasks = [worker(word, domain) for word in words for domain in target_domains]
        for next_task in asyncio.as_completed(tasks):
            if time.time() - start_time >= TIMEOUT_LIMIT:
                print(f"\n{BLUE}--- 2 Minutes Reached! Stopping Scan ---{RESET}")
                break
            await next_task
            
    print("--- Scan Process Safely Closed ---")

if __name__ == '__main__':
    if sys.platform == 'win32': asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
