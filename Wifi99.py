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
import http.client

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

# Crée un élément de réseau Wi-Fi
wifi_elt = Dot11Elt(ID=0, info=wifi_name)

# Crée un réseau Wi-Fi
packet = Dot11Beacon()
packet /= wifi_elt  # Ajoute la couche Dot11Elt au paquet Dot11Beacon

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
        font-size : 24px;
        font-weight: bold;
        margin-bottom: 10px;
      }
      .header p {
        font-size: 16px;
        color: #666;
      }
      .form {
        margin-top: 20px;
      }
      .form label {
        display: block;
        margin-bottom: 10px;
      }
      .form input[type="text"], .form input[type="password"] {
        width: 100%;
        height: 40px;
        margin-bottom: 20px;
        padding: 10px;
        border: 1px solid #ccc;
      }
      .form input[type="submit"] {
        width: 100%;
        height: 40px;
        background-color: #4CAF50;
        color: #fff;
        padding: 10px;
        border: none;
        border-radius: 10px;
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
        <p>Entrez vos informations de connexion pour accéder au réseau Wi-Fi.</p>
      </div>
      <form class="form">
        <label for="ssid">Nom du réseau Wi-Fi :</label>
        <input type="text" id="ssid" name="ssid" value="{wifi_name}">
        <label for="password">Mot de passe :</label>
        <input type="password" id="password" name="password">
        <input type="submit" value="Se connecter">
      </form>
    </div>
  </body>
</html>
""".format(wifi_name=wifi_name)

# Crée un serveur HTTP
PORT = 8080

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(Fore.GREEN + "Serveur HTTP démarré sur le port {PORT} !".format(PORT=PORT))
    threading.Thread(target=httpd.serve_forever).start()

# Ouvre la page HTML dans un navigateur web
webbrowser.open("http://127.0.0.1:{PORT}".format(PORT=PORT))

print(Fore.GREEN + "Connexion réussie !")
