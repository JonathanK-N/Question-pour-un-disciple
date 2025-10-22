<div align="center">

# 🎯 Question pour un Disciple

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=22&duration=3000&pause=1000&color=2E86AB&center=true&vCenter=true&width=600&lines=Jeu+de+Quiz+Biblique+Multi-joueurs;Inspiré+de+Question+pour+un+Champion;Pour+l'Église+Jeunes+Prodiges+Sherbrooke" alt="Typing SVG" />

[![Made with Flask](https://img.shields.io/badge/Made%20with-Flask-1f425f.svg?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-black?style=for-the-badge&logo=socket.io&badgeColor=010101)](https://socket.io/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://python.org)
[![Railway](https://img.shields.io/badge/Railway-131415?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app)

</div>

---

## 🎬 Aperçu du Projet

<div align="center">

### 🎮 **Démo Interactive Complète**

<table>
<tr>
<td align="center" width="33%">

**🎯 Console Animateur**
<br/>
<img src="https://via.placeholder.com/400x300/2E86AB/FFFFFF?text=Console+Animateur" alt="Console Animateur" width="100%" />
<br/>
<sub>Gestion complète du jeu</sub>

</td>
<td align="center" width="33%">

**📱 Interface Joueur**
<br/>
<img src="https://via.placeholder.com/250x400/F39C12/FFFFFF?text=Interface+Joueur" alt="Interface Joueur" width="80%" />
<br/>
<sub>Buzzer temps réel</sub>

</td>
<td align="center" width="33%">

**🖥️ Écran Projection**
<br/>
<img src="https://via.placeholder.com/400x250/E74C3C/FFFFFF?text=Ecran+Projection" alt="Écran Projection" width="100%" />
<br/>
<sub>Affichage public</sub>

</td>
</tr>
</table>

### 🎪 **Flux de Jeu Animé**

```mermaid
sequenceDiagram
    participant A as 🎯 Animateur
    participant S as 🖥️ Serveur
    participant J as 🎮 Joueur
    participant E as 📺 Écran
    
    A->>S: Démarre question
    S->>E: Affiche question + chrono
    S->>J: Active buzzer
    J->>S: Appuie buzzer 🔴
    S->>A: Notifie premier joueur
    A->>S: Valide réponse ✅
    S->>E: Met à jour score
    S->>J: Feedback instantané
```

### 🚀 **Fonctionnalités en Action**

<div align="center">

| 🎯 **Fonctionnalité** | ⚡ **Temps Réel** | 📱 **Mobile** | 🎪 **Visuel** |
|:---:|:---:|:---:|:---:|
| Buzzer instantané | ✅ Socket.IO | ✅ Responsive | ✅ Animations |
| Chronomètre 20s | ✅ Synchronisé | ✅ Tactile | ✅ Effets sonores |
| Classement live | ✅ Auto-update | ✅ Optimisé | ✅ Podium animé |
| Multi-salles | ✅ Isolées | ✅ QR Code | ✅ URLs dédiées |

</div>

</div>

---

## 🎮 **Essayez Maintenant !**

<div align="center">

### 🌐 **Démo Live**

[![Démo Live](https://img.shields.io/badge/🎯_Démo_Live-Essayer_Maintenant-success?style=for-the-badge&logo=rocket)](https://question-pour-un-disciple.railway.app)

**Ou créez votre propre salle :**

🎯 **Animateur :** `https://votre-url.com/room/VOTRE_SALLE/admin`  
🎮 **Joueurs :** `https://votre-url.com/room/VOTRE_SALLE/player`  
📺 **Projection :** `https://votre-url.com/room/VOTRE_SALLE/display`

</div>

---

## ⚡ Installation Locale

<details>
<summary>🚀 <strong>Installation en 1 minute</strong></summary>

```bash
# 📥 Cloner le projet
git clone https://github.com/JonathanK-N/question-pour-un-disciple.git
cd question-pour-un-disciple

# 🐍 Environnement Python
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 📦 Dépendances
pip install -r requirements.txt

# 🎮 Lancement
python app.py
```

**🌐 Accès :** `http://localhost:5000`

</details>

---

## 🎯 Fonctionnalités Principales

<table>
<tr>
<td width="50%">

### 🎮 **Gameplay Temps Réel**
- 🔴 **Buzzers instantanés** avec Socket.IO
- ⏱️ **Chronomètre 20s** avec effets sonores
- 🏆 **Classement live** et podium animé
- 🔄 **Reconnexion automatique** des joueurs

</td>
<td width="50%">

### 🛠️ **Gestion Avancée**
- 👨💼 **Console animateur** complète
- 📄 **Import PDF** de questionnaires
- 🏠 **Multi-salles** isolées
- 📱 **Interface mobile** responsive

</td>
</tr>
</table>

---

## 🎭 Rôles & Interfaces

<div align="center">

| 👤 **Rôle** | 🔗 **URL** | 📝 **Description** |
|:---:|:---:|:---|
| 🎯 **Animateur** | `/room/<nom>/admin` | Console de contrôle complète |
| 🎮 **Joueur** | `/room/<nom>/player` | Interface de jeu mobile |
| 🖥️ **Projection** | `/room/<nom>/display` | Écran public pour audience |

</div>

> 💡 **Astuce :** Remplacez `<nom>` par votre salle (ex: `/room/sherbrooke`)

---

## 📊 Architecture Technique

<details>
<summary>🏗️ <strong>Stack Technologique</strong></summary>

```mermaid
graph TB
    A[Client Web] --> B[Flask Server]
    B --> C[Socket.IO]
    B --> D[PyPDF2]
    B --> E[JSON Database]
    C --> F[Real-time Events]
    D --> G[PDF Import]
    E --> H[Questions Storage]
```

**Technologies :**
- 🐍 **Backend :** Flask + Flask-SocketIO
- 🎨 **Frontend :** HTML5 + CSS3 + Vanilla JS
- 📄 **PDF :** PyPDF2 pour l'import
- 💾 **Data :** JSON persistant
- 🚀 **Deploy :** Railway compatible

</details>

---

## 📁 Structure du Projet

<details>
<summary>🗂️ <strong>Arborescence détaillée</strong></summary>

```
question-pour-un-disciple/
├── 🐍 app.py                 # Serveur Flask principal
├── 📋 requirements.txt       # Dépendances Python
├── 📊 data/
│   └── 📝 questions.json     # Base de données questions
├── 🎨 static/
│   ├── 📜 script.js          # Logique client
│   ├── 🎨 style.css          # Styles CSS
│   ├── 🔊 buzzer.mp3         # Effets sonores
│   └── 🖼️ assets/           # Images & GIFs
└── 📄 templates/
    ├── 👨💼 admin.html         # Console animateur
    ├── 🖥️ display.html        # Écran projection
    ├── 🎮 player.html         # Interface joueur
    └── 🏠 index.html          # Page d'accueil
```

</details>

---

## 📄 Import PDF

<details>
<summary>📋 <strong>Format des questionnaires</strong></summary>

**Structure attendue :**
```
Question: Qui a écrit l'Apocalypse ?
Réponse: L'apôtre Jean

Question 2 - Quel est le premier miracle de Jésus ?
Réponse 2: L'eau changée en vin à Cana
```

**Formats acceptés :**
- ✅ `Question:` / `Q:` / `Question 1`
- ✅ `Réponse:` / `Reponse:` / `Answer:`
- ✅ Insensible à la casse

</details>

---

## 🛣️ Roadmap

- [ ] 🏆 Mode tournoi éliminatoire
- [ ] ✏️ Éditeur web de questions
- [ ] 📺 Intégration OBS/Chromecast
- [ ] 🌍 Support multilingue
- [ ] 📈 Statistiques avancées
- [ ] 🎵 Thèmes musicaux

---

## 👨💻 Créateur

<div align="center">

<img src="https://github.com/JonathanK-N.png" width="100" style="border-radius: 50%;" />

**Jonathan Kakesa Nayaba**  
*CEO - Cognito Inc.*

[![Website](https://img.shields.io/badge/Website-cognito--inc.ca-blue?style=flat-square&logo=google-chrome)](https://cognito-inc.ca)
[![Email](https://img.shields.io/badge/Email-cognito943%40gmail.com-red?style=flat-square&logo=gmail)](mailto:cognito943@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-JonathanK--N-black?style=flat-square&logo=github)](https://github.com/JonathanK-N)

*Créateur de solutions numériques pour la communauté chrétienne francophone*

</div>

---

## 📈 Statistiques du Projet

<div align="center">

![GitHub repo size](https://img.shields.io/github/repo-size/JonathanK-N/question-pour-un-disciple?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/JonathanK-N/question-pour-un-disciple?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/JonathanK-N/question-pour-un-disciple?style=for-the-badge)

**⏱️ Temps de développement :** ~120 heures  
**📅 Création :** Septembre 2024  
**🎯 Objectif :** Édifier la communauté chrétienne

</div>

---

## 🙏 Remerciements

<div align="center">

**Merci à l'équipe Jeunes Prodiges Sherbrooke**  
*Pour la vision, les tests et l'énergie communiquée*

<img src="static/assets/logo-icc-sherbrooke.png" alt="Impact Centre Chrétien Sherbrooke" width="150" />

*"À Celui qui est puissant pour faire infiniment au-delà de tout ce que nous demandons ou pensons."*  
**— Éphésiens 3:20**

---

⭐ **N'oubliez pas de mettre une étoile si ce projet vous plaît !** ⭐

</div>