# 🤖 PrevNames Bot - Un Bot Discord pour Suivre les Anciens Pseudonymes

**PrevNames** est un bot Discord conçu pour suivre les anciens pseudonymes des utilisateurs. Il utilise une base de données SQLite pour stocker les pseudonymes et est prêt à être hébergé sur [Render](https://render.com/), avec une configuration simple pour rester actif grâce à [UptimeRobot](https://uptimerobot.com/).

## 🚀 Fonctionnalités

- 🔄 **Suivi des changements de pseudonymes** des utilisateurs
- 🗂️ **Stockage dans une base de données SQLite**
- 📄 **Affichage interactif** des anciens noms avec une pagination
- 🌐 **Hébergement facile** sur Render avec un script `keep_alive.py`

## ⚙️ Prérequis

Avant de commencer, tu auras besoin de :

- Un compte [Render](https://render.com/) pour héberger ton bot
- Un compte [UptimeRobot](https://uptimerobot.com/) pour garder le bot en ligne
- Le **token** de ton bot Discord
- Un fichier `config.json` contenant au moins :

```json
{
  "prefix": "+"
}
```

## 📦 Installation

### 1. Cloner le dépôt

Clone le dépôt et accède au répertoire :

```bash
git clone https://github.com/xDatabaseDev/prevnames
cd prevnames
```

### 2. Configuration de Render

1. Sur [Render](https://dashboard.render.com/), crée un **Nouveau Web Service**.
2. Sélectionne ton dépôt GitHub.
3. Dans **Environment Variables**, ajoute la variable suivante :

   - `token` : Le token de ton bot Discord.

4. Assure-toi que la commande de démarrage est :

   ```bash
   python3 prevnames.py
   ```

### 3. Script Keep-Alive

Le fichier `keep_alive.py` est déjà en place pour maintenir le bot actif avec un serveur Express minimal. Il est utilisé pour envoyer des requêtes ping régulières via UptimeRobot.

```python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Le bot est en ligne."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
```

### 4. UptimeRobot

1. Crée un compte sur [UptimeRobot](https://uptimerobot.com/).
2. Ajoute un nouveau **HTTP Monitor** avec l'URL de ton service Render (par exemple, `https://ton-service.onrender.com/`).
3. UptimeRobot pinguera régulièrement l'URL pour garder ton bot actif.

## 📋 Commandes Principales

### 1. Afficher les anciens pseudonymes

```bash
+prevname [@utilisateur]
```

Cette commande affiche les anciens pseudonymes d'un utilisateur spécifique, ou de l'utilisateur qui exécute la commande s'il n'y a pas de mention.

### 2. Effacer l'historique des pseudonymes

```bash
+clear
```

Cette commande supprime tous les anciens pseudonymes de l'utilisateur exécutant la commande.

### 3. Aide

```bash
+help
```

Affiche une liste des commandes disponibles avec des descriptions.

## 🛠️ Technologies Utilisées

- [Discord.py](https://discordpy.readthedocs.io/) - Framework pour les bots Discord
- [SQLite3](https://www.sqlite.org/index.html) - Base de données légère
- [Flask](https://flask.palletsprojects.com/) - Serveur web minimal pour le keep-alive

## 🎯 Contribuer

Les contributions sont les bienvenues ! Si tu souhaites améliorer le bot ou ajouter des fonctionnalités, ouvre une pull request ou signale un problème.

## 📝 Licence

Ce projet est sous licence MIT - consulte le fichier [LICENSE](./LICENSE) pour plus d'informations.

---

### 🚀 Héberge ton bot et garde une trace des anciens pseudonymes !

---
