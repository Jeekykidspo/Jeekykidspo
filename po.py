import pywifi
import psutil
import getpass
from colorama import init, Fore, Back, Style
import requests
import itertools
import http.server
import socketserver
import threading
import os
import webbrowser
import subprocess

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

# Crée un objet pywifi
wifi = pywifi.PyWiFi()

# Crée un réseau Wi-Fi
profile = pywifi.Profile()
profile.ssid = wifi_name
if password:
    profile.auth = pywifi.const.AUTH_ALG_PMK
    profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
    profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
    profile.key = password
else:
    profile.auth = pywifi.const.AUTH_ALG_OPEN
    profile.akm.append(pywifi.const.AKM_TYPE_WPA)
    profile.cipher = pywifi.const.CIPHER_TYPE_WEP

# Enregistre le profil
wifi.interfaces()[0].add_network_profile(profile)

# Active le réseau Wi-Fi
wifi.interfaces()[0].connect(profile)

print(Fore.GREEN + "Réseau Wi-Fi créé avec succès !")

# Crée une page HTML
html = """
<html>
  <head>
    <title>Connexion au réseau Wi-Fi</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        background-color: #f0f0f0;
      }
      .container {
        width: 300px;
        margin: 50px auto;
        padding: 20px;
        background-color: #fff;
        border: 1px solid #ddd;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      }
      .header {
        text-align: center;
        margin-bottom: 20px;
      }
      .header h1 {
        font-size: 24px;
        font-weight: bold;
        color: #333;
      }
      .form {
        margin-top: 20px;
      }
      .form input[type="email"], .form input[type="password"] {
        width: 100%;
        height: 40px;
        margin-bottom: 20px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
      }
      .form input[type="submit"] {
        width: 100%;
        height: 40px;
        background-color: #4CAF50;
        color: #fff;
        padding: 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
      }
      .form input[type="submit"]:hover {
        background-color: #3e8e41;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>Connexion au réseau Wi-Fi</h1>
      </div>
      <form class="form" action="" method="post">
        <input type="email" name="email" placeholder="Adresse e-mail">
        <input type="password" name="password" placeholder="Mot de passe">
        <input type="submit" value="Se connecter">
      </form>
    </div>
  </body>
</html>
"""

# Enregistrez la page HTML dans un fichier
with open("index.html", "w") as f:
    f.write(html)

# Créez un serveur HTTP simple pour servir la page HTML
def serve_http():
    with socketserver.TCPServer(("", 8080), http.server.SimpleHTTPRequestHandler) as httpd:
        print("Serving HTTP on port 8080...")
        httpd.serve_forever()

# Démarrez le serveur HTTP dans un thread séparé
threading.Thread(target=serve_http).start()

# Red irige l'utilisateur vers la page HTML
webbrowser.open("http://localhost:8080/index.html")

# Utilisez le module subprocess pour exécuter des commandes système sans nécessiter d'accès root
def execute_command(command):
    try:
        subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + "Erreur lors de l'exécution de la commande : " + str(e))

# Exécutez des commandes système pour configurer le réseau Wi-Fi
execute_command("ip link set wlan0 up")
execute_command("ip addr add 192.168.1.1/24 dev wlan0")
execute_command("ip link set wlan0 mtu 1500")
execute_command("ip link set wlan0 txqueuelen 1000")

# Affichez les informations de connexion Wi-Fi
print(Fore.GREEN + "Informations de connexion Wi-Fi :")
print(Fore.CYAN + "Adresse IP : 192.168.1.1")
print(Fore.CYAN + "Masque de sous-réseau : 255.255.255.0")
print(Fore.CYAN + "Passerelle par défaut : 192.168.1.1")
