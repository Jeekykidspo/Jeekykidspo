import subprocess
from colorama import init, Fore, Back, Style
import requests
import itertools
import http.server
import socketserver
import threading
import os
import webbrowser

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
    # Configure le réseau Wi-Fi using subprocess
    subprocess.run(["termux-setup-storage"], check=True)
    subprocess.run(["am", "start", "-n", "com.termux/com.termux.app.TermuxActivity", "-e", "termux-wifi-enable " + wifi_name + " " + password], check=True)
else:
    # Configure le réseau Wi-Fi sans mot de passe
    subprocess.run(["termux-setup-storage"], check=True)
    subprocess.run(["am", "start", "-n", "com.termux/com.termux.app.TermuxActivity", "-e", "termux-wifi-enable " + wifi_name], check=True)

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

    # Ouvre le navigateur web par défaut
    webbrowser.open("http://localhost:{PORT}".format(PORT=PORT))

    # Attend que l'utilisateur appuie sur Entrée
    input(Fore.CYAN + "Appuyez sur Entrée pour continuer...")

    # Ferme le serveur HTTP
    httpd.shutdown()
    httpd.server_close()

    # Supprime le fichier HTML
    os.remove("index.html")

    # Affiche le message de fin
    print(Fore.GREEN + "Fin du programme !")
