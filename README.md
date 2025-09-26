# Question pour un Disciple

Système de quiz en direct avec gestion de buzzers, chrono et classement.

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Ajouter un fichier son buzzer.mp3 dans le dossier static/

3. Lancer l'application :
```bash
python app.py
```

## Utilisation

1. **Animateur** : Ouvrir http://localhost:5000 sur l'ordinateur principal
2. **Joueurs** : Se connecter via http://IP_ORDINATEUR:5000/buzzer_page/NomJoueur sur smartphone
3. Cliquer sur "Démarrer le jeu" pour commencer
4. Les joueurs buzzent, l'animateur valide les réponses
5. Résultats automatiques à la fin

## Fonctionnalités

- ✅ Chrono 50 secondes avec pause/reprise
- ✅ Buzzers en temps réel (premier arrivé)
- ✅ Son de buzzer sur PC animateur
- ✅ Classement en direct
- ✅ Interface professionnelle bleu/or
- ✅ Podium final automatique
- ✅ Compatible réseau local WiFi

## Structure

- `app.py` : Backend Flask + SocketIO
- `templates/` : Pages HTML (jeu, buzzer, résultats)
- `static/` : CSS, JS et son buzzer
- `data/questions.json` : Base de questions