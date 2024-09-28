import os
import subprocess
from colorama import Fore, Style

def clear_console():
    os.system('clear' if os.name == 'posix' else 'cls')

def display_title():
    title = r"""
      _    _ _       _       _    _           _   _          _   _           
     | |  | | |     | |     | |  | |         | | | |        | | | |          
     | |  | | | ___ | |_    | |  | | ___  ___| |_| |__   __| |_| |__   __ _ 
     | |  | | |/ _ \| __|   | |  | |/ _ \/ __| __| '_ \ / _` | | '_ \ / _` |
     | |__| | | (_) | |_    | |__| |  __/ (__| |_| | | | (_| | | | | | (_| |
      \____/|_|\___/ \__|    \____/ \___|\___|\__|_| |_|\__,_|_|_| |_|\__, |
                                                                       __/ | 
                                                                      |___/  
    """
    print(Fore.MAGENTA + title + Style.RESET_ALL)

def display_options():
    print(Fore.GREEN + "=== Outil de Pentesting Éthique OSINT ===" + Style.RESET_ALL)
    print(Fore.CYAN + "Choisissez une option parmi les suivantes :" + Style.RESET_ALL)
    
    print(Fore.YELLOW + "=" * 60)
    print(Fore.CYAN + "{:<3} {:<60}".format("No", "Outil"))
    print(Fore.YELLOW + "=" * 60)
    
    options = [
        "1. Recherche d'IP (whois)",
        "2. Vérification de domaine (dig)",
        "3. Recherche WHOIS",
        "4. Extraction d'informations DNS (dig)",
        "5. Recherche d'email (theHarvester)",
        "6. Analyse de réseaux sociaux (snscrape)",
        "7. Analyse de site web (nikto)",
        "8. Recherche de vulnérabilités (nmap)",
        "9. Scanner de ports (nmap)",
        "10. Recherche d'historique de domaine (domainhistory)",
        "11. Analyse de metadata de fichiers (exiftool)",
        "12. Recherche de fuites de données (haveibeenpwned)",
        "13. Analyse de contenu de forum (scrapy)",
        "14. Recherche d'informations sur des personnes (Maltego)",
        "15. Agrégation de nouvelles (newsboat)",
        "16. Recherche de mots-clés (Google dorking)",
        "17. Analyse de réputation (Google)",
        "18. Recherche de liens brisés (broken-link-checker)",
        "19. Récupération d'informations sur le serveur (curl)",
        "20. Vérification d'IP malveillante (ipinfo.io)",
        "21. Analyse de comportement des utilisateurs (piwik)",
        "22. Recherche d'images inversée (Google Images)",
        "23. Surveillance des médias sociaux (twint)",
        "24. Analyse de fichiers publics (shodan)",
        "25. Évaluation de sécurité de réseau (netstat)",
        "26. Recherche de fichiers vulnérables (grep)",
        "27. Extraction de données publiques (BeautifulSoup)",
        "28. Utilisation de l'API Shodan",
        "29. Suivi des activités en ligne (Google Alerts)",
        "30. Générateur de rapports OSINT (markdown)",
        "31. Recherche de sous-domaines (sublist3r)",
        "32. Analyse de la sécurité des API (OWASP ZAP)",
        "33. Récupération d'informations sur les certificats SSL (sslscan)",
        "34. Vérification de la conformité RGPD (RGPD Checker)",
        "35. Recherche de vulnérabilités spécifiques (CVE Search)",
        "36. Exécution de scripts personnalisés (custom scripts)"
    ]
    
    for option in options:
        print(Fore.CYAN + "{:<3} {:<60}".format(option.split('.')[0], option.split('. ')[1]) + Style.RESET_ALL)

def execute_tool(choice):
    try:
        if choice == 1:
            domain = input("Entrez l'adresse IP à rechercher : ")
            subprocess.run(["whois", domain])
        elif choice == 2:
            domain = input("Entrez le domaine à vérifier : ")
            subprocess.run(["dig", domain])
        elif choice == 3:
            domain = input("Entrez le domaine pour la recherche WHOIS : ")
            subprocess.run(["whois", domain])
        elif choice == 4:
            domain = input("Entrez le domaine pour l'extraction DNS : ")
            subprocess.run(["dig", "+short", domain])
        elif choice == 5:
            domain = input("Entrez le domaine pour la recherche d'emails : ")
            subprocess.run(["theHarvester", "-d", domain, "-b", "all"])
        elif choice == 6:
            username = input("Entrez le nom d'utilisateur à rechercher : ")
            subprocess.run(["snscrape", "twitter-users", username])
        elif choice == 7:
            url = input("Entrez l'URL du site à analyser : ")
            subprocess.run(["nikto", "-h", url])
        elif choice == 8:
            target = input("Entrez l'adresse IP ou le domaine à analyser : ")
            subprocess.run(["nmap", "--script=vuln", target])
        elif choice == 9:
            target = input("Entrez l'adresse IP ou le domaine à scanner : ")
            subprocess.run(["nmap", target])
        elif choice == 10:
            domain = input("Entrez le domaine pour l'historique : ")
            subprocess.run(["domainhistory", domain])
        elif choice == 11:
            file_path = input("Entrez le chemin du fichier : ")
            subprocess.run(["exiftool", file_path])
        elif choice == 12:
            email = input("Entrez l'email à vérifier : ")
            subprocess.run(["curl", f"https://haveibeenpwned.com/api/v2/breachedaccount/{email}"])
        elif choice == 13:
            forum_url = input("Entrez l'URL du forum à analyser : ")
            subprocess.run(["scrapy", "crawl", forum_url])
        elif choice == 14:
            person = input("Entrez le nom de la personne à rechercher : ")
            subprocess.run(["maltego", person])
        elif choice == 15:
            subprocess.run(["newsboat"])
        elif choice == 16:
            keyword = input("Entrez le mot-clé pour la recherche : ")
            print(f"Utilisez Google pour la recherche de dorking avec : {keyword}")
        elif choice == 17:
            print("Analyse de réputation en utilisant Google.")
        elif choice == 18:
            url = input("Entrez l'URL pour vérifier les liens brisés : ")
            subprocess.run(["broken-link-checker", url])
        elif choice == 19:
            url = input("Entrez l'URL pour récupérer des informations : ")
            subprocess.run(["curl", url])
        elif choice == 20:
            ip = input("Entrez l'adresse IP à vérifier : ")
            subprocess.run(["curl", f"https://ipinfo.io/{ip}"])
        elif choice == 21:
            print("Utilisez piwik pour analyser le comportement des utilisateurs.")
        elif choice == 22:
            image_url = input("Entrez l'URL de l'image pour recherche inversée : ")
            print(f"Utilisez Google Images pour recherche inversée de {image_url}.")
        elif choice == 23:
            username = input("Entrez le nom d'utilisateur Twitter à surveiller : ")
            subprocess.run(["twint", "-u", username])
        elif choice == 24:
            print("Utilisez shodan pour analyser les fichiers publics.")
        elif choice == 25:
            subprocess.run(["netstat", "-an"])
        elif choice == 26:
            pattern = input("Entrez le modèle de fichier à rechercher : ")
            subprocess.run(["grep", "-r", pattern, "."])
        elif choice == 27:
            print("Utilisez BeautifulSoup pour extraire des données publiques.")
        elif choice == 28:
            print("Utilisez l'API Shodan pour obtenir des informations.")
        elif choice == 29:
            print("Configurez Google Alerts pour le suivi des activités en ligne.")
        elif choice == 30:
            print("Générateur de rapports OSINT utilisant Markdown.")
        elif choice == 31:
            domain = input("Entrez le domaine pour rechercher des sous-domaines : ")
            subprocess.run(["sublist3r", "-d", domain])
        elif choice == 32:
            url = input("Entrez l'URL de l'API à analyser : ")
            subprocess.run(["zap-cli", "start", url])
        elif choice == 33:
            domain = input("Entrez le domaine pour récupérer les certificats SSL : ")
            subprocess.run(["sslscan", domain])
        elif choice == 34:
            domain = input("Entrez le domaine pour vérifier la conformité RGPD : ")
            subprocess.run(["rgpd-checker", domain])
        elif choice == 35:
            cve = input("Entrez le numéro CVE à rechercher : ")
            subprocess.run(["cve-search", cve])
        elif choice == 36:
            script_path = input("Entrez le chemin du script Python à exécuter : ")
            subprocess.run(["python3", script_path])
        else:
            print(Fore.RED + "Choix invalide." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'exécution de l'outil : {e}" + Style.RESET_ALL)

def select_option():
    while True:
        try:
            choice = int(input(Fore.MAGENTA + "\nEntrez le numéro de l'outil que vous souhaitez utiliser : " + Style.RESET_ALL))
            if 1 <= choice <= 36:
                execute_tool(choice)
                break  # Exit loop after successful execution
            else:
                print(Fore.RED + "Choix invalide. Veuillez choisir un numéro entre 1 et 36." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Entrée non valide. Veuillez entrer un nombre." + Style.RESET_ALL)

if __name__ == "__main__":
    clear_console()
    display_title()
    display_options()
    select_option()

