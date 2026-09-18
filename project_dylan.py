import os
import sys

# Interface Color Variables
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def main_menu():
    banner = r"""
██████╗ ██████╗  ██████╗  ██████╗███████╗ ██████╗████████╗    ██████╗ ██╗   ██╗██╗      ██████╗ ███╗   ██╗
██╔══██╗██╔══██╗██╔═══██╗ ██╔════╝██╔════╝██╔════╝╚══██╔══╝    ██╔══██╗╚██╗ ██╔╝██║      ██╔══██╗████╗  ██║
██████╔╝██████╔╝██║   ██║ ██║     █████╗  ██║        ██║       ██║  ██║ ╚████╔╝ ██║      ███████║██╔██╗ ██║
██╔═══╝ ██╔══██╗██║   ██║ ██║     ██╔══╝  ██║        ██║       ██║  ██║  ╚██╔╝  ██║      ██╔══██║██║╚██╗██║
██║     ██║  ██║╚██████╔╝ ╚██████╗███████╗╚██████╗   ██║       ██████╔╝   ██║   ███████╗██║  ██║██║ ╚████║
╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═════╝╚══════╝ ╚═════╝   ╚═╝       ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    """
    while True:
        print(f"{BLUE}{banner}{RESET}")
        print(f"{BLUE}===================================================================================================={RESET}")
        print(" 1. Mass Network Scanner (Executes mc_scanner.py)")
        print(" 2. Live Packet Ping Checker (Executes mc_ping.py)")
        print(" 3. Target Custom Port Sweeper (Executes mc_portscan.py)")
        print(" 4. Direct Logs Bulk Online Validator (Executes mc_bulk_check.py)")
        print(" 5. Mojang Account Profile UUID Tracker (Executes mc_player_lookup.py)")
        print(" 6. High-Speed Async Port Stress Tester (Executes mc_stress.py)")
        print(" 7. CLOSE TOOLKIT")
        print(f"{BLUE}===================================================================================================={RESET}")
        
        try:
            choice = int(input("Select tool to open (1-7): "))
            if choice < 1 or choice > 7:
                raise ValueError
        except (ValueError, KeyboardInterrupt):
            print("\nInvalid choice.")
            continue

        if choice == 1:
            print(f"\n{YELLOW}[*] Spawning Mass Network Scanner...{RESET}")
            os.system("python mc_scanner.py")
        elif choice == 2:
            print(f"\n{YELLOW}[*] Spawning Live Packet Checker...{RESET}")
            os.system("python mc_ping.py")
        elif choice == 3:
            print(f"\n{YELLOW}[*] Spawning Target Port Sweeper...{RESET}")
            os.system("python mc_portscan.py")
        elif choice == 4:
            print(f"\n{YELLOW}[*] Spawning Bulk Online Validator...{RESET}")
            os.system("python mc_bulk_check.py")
        elif choice == 5:
            print(f"\n{YELLOW}[*] Spawning Profile UUID Tracker...{RESET}")
            os.system("python mc_player_lookup.py")
        elif choice == 6:
            print(f"\n{YELLOW}[*] Spawning High-Speed Async Port Stress Tester...{RESET}")
            os.system("python mc_stress.py")
        else:
            print("\nClosing Toolkit. Goodbye!")
            break
        
        input(f"\n{YELLOW}Sub-tool execution complete. Press Enter to pull up the Master Toolkit Menu...{RESET}")

if __name__ == '__main__':
    main_menu()
