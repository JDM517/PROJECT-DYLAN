import urllib.request
import json
import time
import os

# Terminal Visual Colors
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def fetch_mojang_profile(username):
    """Queries Mojang servers for a profile using a robust two-stage verification fallback."""
    # Stage 1: Standard Direct API Path
    url = f"https://mojang.com{username}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except Exception:
        pass

    # Stage 2: Batch Fallback Path (Bypasses Case-Sensitivity Locks)
    batch_url = "https://mojang.com"
    try:
        post_data = json.dumps([username]).encode('utf-8')
        req = urllib.request.Request(
            batch_url, 
            data=post_data, 
            headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status == 200:
                profiles = json.loads(response.read().decode())
                if profiles and len(profiles) > 0:
                    return profiles[0]
    except Exception:
        pass
    return None

def run_single_lookup():
    """Handles an individual username query."""
    username = input("\nEnter Minecraft username: ").strip()
    if not username:
        return
        
    print(f"[*] Querying Mojang servers for profile: '{username}'...")
    data = fetch_mojang_profile(username)
    
    if data:
        uuid = data["id"]
        # Format the UUID with standard hyphens for standard read styles
        formatted_uuid = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
        
        print(f"\n{GREEN}███████████████████████████████████████████{RESET}")
        print(f"{GREEN}  [+] ACCOUNT VERIFIED AND PARSED!{RESET}")
        print(f"  Official Name: {data['name']}")
        print(f"  Raw UUID:      {uuid}")
        print(f"  Clean UUID:    {formatted_uuid}")
        print(f"-------------------------------------------")
        print(f"  3D Body Render Link:")
        print(f"  https://crafatar.com{uuid}")
        print(f"  Raw Texture File Download:")
        print(f"  https://crafatar.com{uuid}")
        print(f"{GREEN}███████████████████████████████████████████{RESET}\n")
    else:
        print(f"\n{RED}[-] Error: Account profile details could not be found.{RESET}\n")

def run_bulk_lookup():
    """Reads usernames from a file and runs an automated bulk tracker."""
    filename = input("\nEnter filename containing usernames (e.g., players.txt): ").strip()
    if not filename:
        return
        
    if not os.path.exists(filename):
        print(f"{RED}[-] Error: File '{filename}' not found!{RESET}")
        return
        
    with open(filename, "r", encoding="utf-8") as f:
        usernames = [line.strip() for line in f if line.strip()]
        
    print(f"{YELLOW}[*] Loaded {len(usernames)} usernames. Starting batch tracker...{RESET}")
    print(f"{YELLOW}[*] Applying rate-limiting safe windows (1-second delays)...{RESET}\n")
    
    success_count = 0
    with open("tracked_uuids.txt", "w", encoding="utf-8") as out_f:
        for user in usernames:
            data = fetch_mojang_profile(user)
            if data:
                success_count += 1
                uuid = data["id"]
                output = f"{data['name']} -> {uuid}"
                print(f"{GREEN}[FOUND] {output}{RESET}")
                out_f.write(output + "\n")
                out_f.flush()
            else:
                print(f"{RED}[NOT FOUND] {user}{RESET}")
            time.sleep(1.0)
            
    print(f"\n{BLUE}--- Bulk Tracker Complete ---{RESET}")
    print(f"[+] Successfully tracked {success_count} accounts.")
    print("Results directory saved to: tracked_uuids.txt")

def main():
    # Styled Internal Header
    print(f"{BLUE}")
    print("=========================================================================================")
    print("  ██████╗ ██╗      █████╗ ██╗   ██╗███████╗██████╗     ██╗     ██████╗  ██████╗ ██╗  ██╗██╗  ")
    print("  ██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗    ██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║  ")
    print("  ██████╔╝██║     ███████║ ╚████╔╝ █████╗  ██████╔╝    ██║     ██║   ██║██║   ██║█████╔╝ ██║  ")
    print("  ██╔═══╝ ██║     ██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██╗    ██║     ██║   ██║██║   ██║██╔═██╗ ██║  ")
    print("  ██║     ███████╗██║  ██║   ██║   ███████╗██║  ██║    ███████╗╚██████╔╝╚██████╔╝██║  ██╗██║  ")
    print("  ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ")
    print("=========================================================================================")
    print(f"{RESET}")
    print(" 1. Check Single Username")
    print(" 2. Bulk Check List From File")
    print(f"{BLUE}========================================================================================={RESET}")
    
    try:
        choice = int(input("Select mode (1-2): "))
        if choice == 1:
            run_single_checker() if 'run_single_checker' in globals() else run_single_lookup()
        elif choice == 2:
            run_bulk_lookup()
        else:
            print("Invalid choice.")
    except (ValueError, KeyboardInterrupt):
        print("\nExiting.")

if __name__ == "__main__":
    main()

