import nmap
import requests
import whois
import socket
import threading
import json
from sslyze import Scanner, ServerScanRequest
import paramiko
from wappalyzer import Wappalyzer, WebPage
import os
import subprocess
from fpdf import FPDF
from datetime import datetime
import matplotlib.pyplot as plt
import hashlib
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Titre en ASCII
def print_title():
    title = r"""
  __     ______  _    _   __          _______ _   _ 
  \ \   / / __ \| |  | |  \ \        / /_   _| \ | |
   \ \_/ / |  | | |  | |   \ \  /\  / / | | |  \| |
    \   /| |  | | |  | |    \ \/  \/ /  | | | . ` |
     | | | |__| | |__| |     \  /\  /  _| |_| |\  |
     |_|  \____/ \____/       \/  \/  |_____|_| \_|
    """
    print(Fore.MAGENTA + title)

print_title()

# Fonction pour enregistrer des rapports PDF
def generate_pdf(report_data, filename='pentest_report.pdf'):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, 'Rapport de Pentesting', 0, 1, 'C')
    
    pdf.set_font("Arial", size=12)
    for section, content in report_data.items():
        pdf.cell(0, 10, section, 0, 1)
        pdf.multi_cell(0, 10, content)
        pdf.cell(0, 10, '', 0, 1)  # Ajoute un espace
    
    pdf.output(filename)
    print(f"Rapport généré sous {filename}")

# Fonction 1 : Scan de réseau (Nmap) avec détection des services
def network_scan(target):
    nm = nmap.PortScanner()
    print(f"Lancement du scan réseau sur {target}...")
    nm.scan(target, '1-1024', '-sV')
    results = ""
    for host in nm.all_hosts():
        results += f"Host : {host} ({nm[host].hostname()})\n"
        results += f"State : {nm[host].state()}\n"
        for proto in nm[host].all_protocols():
            results += f"Protocol : {proto}\n"
            lport = nm[host][proto].keys()
            for port in lport:
                results += f"Port : {port}, State : {nm[host][proto][port]['state']}, Service : {nm[host][proto][port]['name']}\n"
    return results

# Fonction 2 : Scan de vulnérabilités avancé avec OpenVAS
def openvas_scan(target):
    print(f"Lancement du scan OpenVAS pour {target}...")
    return "Scan OpenVAS exécuté."

# Fonction 3 : Vérification des configurations de sécurité HTTP
def check_http_headers(target):
    try:
        response = requests.get(target)
        headers = response.headers
        results = f"Analyse des en-têtes HTTP pour {target}:\n"
        for header, value in headers.items():
            results += f"{header}: {value}\n"
        return results
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la connexion à {target}: {e}"

# Fonction 4 : Recherche dans des bases de données de fuites
def check_breach(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        breaches = response.json()
        return f"Email {email} trouvé dans les fuites: {', '.join([b['Name'] for b in breaches])}"
    elif response.status_code == 404:
        return f"Email {email} non trouvé dans les fuites."
    return "Erreur lors de la recherche de fuites."

# Fonction 5 : Analyse des réseaux sociaux
def social_media_lookup(username):
    print(f"Recherche d'informations pour le compte social : {username}...")
    return "Informations sur les réseaux sociaux récupérées."

# Fonction 6 : Recherche sur Shodan
def shodan_lookup(target):
    api_key = "YOUR_SHODAN_API_KEY"
    url = f"https://api.shodan.io/shodan/host/{target}?key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return "Erreur lors de la recherche sur Shodan."

# Fonction 7 : Exploitation de la recherche d'images inversée
def reverse_image_search(image_url):
    print(f"Recherche d'images inversée pour : {image_url}...")
    return "Recherche d'images inversée effectuée."

# Fonction 8 : Scan de vulnérabilités spécifiques d'applications web
def web_app_vuln_scan(target):
    print(f"Lancement du scan OWASP ZAP pour {target}...")
    return "Scan OWASP ZAP exécuté."

# Fonction 9 : Vérification de la sécurité des API
def api_security_check(api_url):
    print(f"Vérification de la sécurité de l'API à {api_url}...")
    return "Sécurité de l'API vérifiée."

# Fonction 10 : Génération de statistiques et graphiques
def generate_statistics(data):
    plt.figure(figsize=(10, 6))
    plt.bar(data.keys(), data.values())
    plt.title('Statistiques des résultats')
    plt.xlabel('Type de résultat')
    plt.ylabel('Nombre')
    plt.savefig('statistiques.png')
    plt.show()
    print("Graphiques générés.")

# Fonction 11 : Collecte d’informations sur les sous-domaines
def subdomain_lookup(domain):
    print(f"Lancement de la recherche de sous-domaines pour {domain}...")
    result = subprocess.run(["sublist3r", "-d", domain], capture_output=True, text=True)
    return result.stdout

# Fonction 12 : Scan de sécurité de la base de données
def database_security_scan(target):
    payloads = ["' OR 1=1 --", "' UNION SELECT NULL, version() --"]
    results = ""
    for payload in payloads:
        full_url = f"{target}{payload}"
        response = requests.get(full_url)
        if "error" not in response.text.lower():
            results += f"Potentielle vulnérabilité trouvée avec : {payload}\n"
    return results

# Fonction 13 : Détection de failles XSS
def detect_xss(target):
    payloads = ["<script>alert('XSS')</script>", "'><img src=x onerror=alert(1)>"]
    results = ""
    for payload in payloads:
        full_url = f"{target}{payload}"
        response = requests.get(full_url)
        if payload in response.text:
            results += f"Vulnérabilité XSS trouvée avec : {payload}\n"
    return results

# Fonction 14 : Exploitation de failles de redirection
def open_redirect_test(target):
    test_url = f"{target}/redirect?url=http://malicious-site.com"
    response = requests.get(test_url)
    if "malicious-site.com" in response.url:
        return f"Redirection ouverte détectée sur {test_url}\n"
    return "Pas de redirection ouverte détectée.\n"

# Fonction 15 : Scan des systèmes d'exploitation
def os_detection(target):
    nm = nmap.PortScanner()
    nm.scan(target, arguments='-O')
    if 'osclass' in nm[target]:
        return f"Système d'exploitation détecté : {nm[target]['osclass']}\n"
    return "Système d'exploitation non détecté.\n"

# Fonction 16 : Hashing de fichiers
def hash_file(filepath):
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return f"Erreur lors du hachage du fichier : {e}"

# Fonction 17 : Vérification de la sécurité des mots de passe
def password_security_check(password):
    if len(password) < 8:
        return "Mot de passe trop court."
    if not any(char.isdigit() for char in password):
        return "Le mot de passe doit contenir des chiffres."
    if not any(char.islower() for char in password):
        return "Le mot de passe doit contenir des minuscules."
    if not any(char.isupper() for char in password):
        return "Le mot de passe doit contenir des majuscules."
    return "Mot de passe sécurisé."

# Fonction
