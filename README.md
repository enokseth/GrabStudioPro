# 🎧 GrabStudioPro

**GrabStudioPro** est une application graphique professionnelle permettant de télécharger des vidéos YouTube en audio de haute qualité (MP3, WAV, FLAC, OGG) ou en MP4.  
Elle utilise `yt-dlp`, `ffmpeg`, et PyQt5 pour offrir une interface moderne avec gestion de métadonnées, vignettes, historique, et choix de formats.

---

## 📦 Fonctionnalités principales

- 🎵 Téléchargement audio : MP3, WAV, FLAC, OGG
- 🎥 Téléchargement vidéo : MP4 HD
- 🧠 Analyse automatique des métadonnées YouTube
- 🖼️ Affichage de la miniature
- 📁 Choix du dossier de sauvegarde
- 🧾 Historique des téléchargements
- 🖱️ Interface moderne avec PyQt5

---

## 🛠️ Installation et build (développeurs)

### 1. Cloner le projet

```bash
git clone https://github.com/votre-utilisateur/GrabStudioPro.git
cd GrabStudioPro
```

## 2. Créer un environnement virtuel (optionnel mais recommandé)

```bash
python -m venv env
source env/bin/activate  # sous Windows: env\Scripts\activate
```

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 🚀 Lancer l'application en mode développement

```bash
python main.py
```

## 🔧 Compilation en .exe avec PyInstaller

```bash
pyinstaller --noconfirm --windowed --icon=icon.ico --name GrabStudio dist\main.py
```

### Développé par Enok Seth
### GitHub : @enokseth
