# Question pour un Disciple ✨  

> Jeu de quiz biblique multi‑joueurs inspiré de *Question pour un Champion*, réalisé pour l’Église de **Jeunes Prodiges Sherbrooke – Impact Centre Chrétien Sherbrooke**.

---

## 🎬 Aperçu animé
<p align="center">
  <img src="static/assets/demo-display.gif" alt="Animation écran projection" width="70%" />
</p>

---

## 📌 Présentation du projet

| Détail | Description |
| :-- | :-- |
| **Créateur** | Jonathan Kakesa Nayaba – CEO, Cognito Inc. |
| **Contact** | ✉️ cognito943@gmail.com · 🌐 [cognito-inc.ca](https://cognito-inc.ca) |
| **Réseaux** | [GitHub](https://github.com/JonathanK-N) · [Facebook](https://www.facebook.com/) |
| **Création** | Septembre 2024 |
| **Temps de développement** | ~ 120 h (design, back-end, front-end & QA) |
| **Technologies** | Flask · Flask-SocketIO · PyPDF2 · HTML/CSS · Vanilla JS |
| **Hébergement** | Railway |

---

## 🚀 Fonctionnalités phares

- **Gestion multi-salles** : animateur, joueurs, écran de projection sur des URLs dédiées.  
- **Buzzers en temps réel** : Socket.IO gère le premier appui et verrouille les autres.  
- **Chrono dynamique** : 20 secondes avec sons, pause et reprise automatiques.  
- **Classement live + podium animé** : affichage final du top 3 avec animation séquentielle.  
- **Console animateur complète** :
  - démarrage/arrêt, validation des réponses ;
  - gestion du chronomètre et du buzzer ;
  - ajout/suppression de questions ;
  - **import PDF** : l’animateur charge ses questionnaires (format Q/R) pour enrichir la base.
- **Expérience joueur** : interface mobile, feedback instantané, score actualisé en direct.  
- **Résilience** : reconnexion transparente des joueurs (nom identique ⇒ reprise automatique).  

---

## 🧰 Installation & lancement

```bash
# 1. Cloner le dépôt
git clone https://github.com/JonathanK-N/question-pour-un-disciple.git
cd question-pour-un-disciple

# 2. Créer l'environnement Python (recommandé)
python -m venv .venv
source .venv/bin/activate  # (Windows) .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Démarrer l'application
python app.py
```

Par défaut, l’application écoute sur `http://0.0.0.0:5000` (Railway/Heroku compatible).  
En local, ouvrir `http://localhost:5000`.

---

## 🧑‍💼 Rôles & interfaces

| Rôle | URL | Description |
| :-- | :-- | :-- |
| **Animateur** | `/room/<nom>/admin` | Gère joueurs, questions, chrono, validations. Import PDF possible. |
| **Joueur** | `/room/<nom>/player` | Saisit son nom, voit son score, buzzer responsive. |
| **Écran projection** | `/room/<nom>/display` | Vue publique : question actuelle, chrono, classement, podium. |

> **Astuce :** changer `<nom>` pour créer plusieurs salles isolées (ex. `/room/sherbrooke`).

---

## 📝 Format d’import PDF

Le module d’import attend des questions structurées dans le document PDF :

```
Question: Qui a écrit l’Apocalypse ?
Réponse: L’apôtre Jean

Question 2 - Quel est le premier miracle de Jésus ?
Réponse 2: L’eau changée en vin à Cana
```

Le parseur accepte :
- préfixes `Question`, `Question 1`, `Q:` (insensible à la casse) ;
- préfixes `Réponse`, `Reponse`, `Answer`.

Chaque paire question/réponse devient un élément dans `data/questions.json` et est immédiatement visible dans le panneau animateur.

---

## 🗂️ Arborescence (extrait)

```
question-pour-un-disciple/
├── app.py                # Flask + Socket.IO + routes d’import PDF
├── requirements.txt      # Dépendances (Flask, SocketIO, PyPDF2…)
├── data/
│   └── questions.json    # Base de questions persistante
├── static/
│   ├── script.js         # Logique client admin initiale
│   ├── style.css         # Thème bleu/or
│   ├── buzzer.mp3 …
│   └── assets/           # (À créer) GIFs/visuels README
└── templates/
    ├── admin.html        # Console animateur
    ├── display.html      # Podium & écran public
    ├── player.html       # Interface joueur
    └── ...               # Pages auxiliaires
```

---

## 🔧 Scripts utiles

| Commande | Description |
| :-- | :-- |
| `python app.py` | Lancer le serveur en développement. |
| `pip install -r requirements.txt` | Installer/mettre à jour les dépendances. |
| `python -m venv .venv` | Créer un environnement virtuel Python. |

---

## 🛠️ Roadmap envisagée

- [ ] Mode “série éliminatoire” (Top 16 → Top 8 → Finale).  
- [ ] Éditeur web de questionnaires avec export PDF.  
- [ ] Integration scoreboard Chromecast / OBS.  
- [ ] Traduction complète en anglais & espagnol.  

---

## 👨‍💻 Auteur

> **Jonathan Kakesa Nayaba**  
> CEO – Cognito Inc.  
> Créateur de solutions numériques pour la communauté chrétienne francophone.

- 🌐 [cognito-inc.ca](https://cognito-inc.ca)  
- 📧 cognito943@gmail.com  
- 🐙 [github.com/JonathanK-N](https://github.com/JonathanK-N)  
- 👍 [facebook.com](https://www.facebook.com/)

---

## 🙏 Remerciements

Merci à toute l’équipe **Jeunes Prodiges Sherbrooke** pour la vision, les tests et l’énergie communiquée tout au long du développement. Ce jeu est pensé pour édifier, connecter et célébrer la connaissance de la Parole au sein de l’Église.

---

<p align="center">
  <img src="static/assets/logo-icc-sherbrooke.png" alt="Impact Centre Chrétien Sherbrooke" width="180" />
  <br/><i>“À Celui qui est puissant pour faire infiniment au-delà de tout ce que nous demandons ou pensons.”</i> – Éphésiens 3:20
</p>

