import random
import string
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_logo():
    logo = f'''
{Fore.RED} 
   Ecole Direct Multitool for Alpine Ios Beta                                                        ░                                                                                              
    '''
    print(logo)

def ping_ip():
    print("IP Pinger")
    ip_address = input("Enter IP address to ping: ")
    
    operating_system = platform.system().lower()
    
    if operating_system == "windows":
        response = os.system(f"ping -n 4 {ip_address}")
    else:
        response = os.system(f"ping -c 4 {ip_address}")
    
    if response == 0:
        print(f"{Fore.GREEN}{ip_address} is reachable.")
    else:
        print(f"{Fore.RED}{ip_address} is not reachable.")

def website_lookup():
    print("Website Lookup")
    website_url = input("Enter website URL to lookup: ")
    
    try:
        ip_address = socket.gethostbyname(website_url)
        print(f"The IP address of {Fore.CYAN}{website_url} is {Fore.GREEN}{ip_address}")
    except socket.gaierror:
        print(f"Could not resolve the IP address for {Fore.CYAN}{website_url}")

def display_ip_config():
    print("IP Configuration")
    operating_system = platform.system().lower()
    
    if operating_system == "windows":
        response = os.system("ipconfig")
    else:
        response = os.system("ifconfig")
    
    print(response)

def generate_chat(length):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_chat():
    num_codes = 1
    code_length = 6
    
    print(f"{Fore.MAGENTA}Gen possible chat...:")
    for _ in range(num_codes):
        steam_code = generate_chat(code_length)
        print(f"{Fore.CYAN}https://www.ecoledirecte.com/{Fore.GREEN}{steam_code}/chat")

def main():
    print_logo()
    
    while True:
        print("\nMenu:")
        print(f"1. {Fore.RED}Exit")
        print(f"2. {Fore.MAGENTA}Cartographie du site complet")
        print(f"3. {Fore.MAGENTA}Lien phishing")
        print(f"4. {Fore.MAGENTA}Brute force ecole direct accounts. marche pas.")
        print(f"5. {Fore.MAGENTA}Gen possible chat ecole direct")
        
        choice = input("Entre ton choix: ")
        
        if choice == "1":
            print(f"{Fore.MAGENTA}Exit...")
            break
        elif choice == "2":
            ping_ip()
        elif choice == "3":
            website_lookup()
        elif choice == "4":
            display_ip_config()
        elif choice == "5":
            generate_chat()
        else:
            print(f"{Fore.RED}Invalid choice. Please select a valid option.")

if _name_ == "__main__":
    main()
