import sys
import os
from urllib.parse import urlparse, parse_qs
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFileDialog, QMessageBox, QHBoxLayout,
    QFrame, QTextEdit, QListWidget, QListWidgetItem, QStackedLayout
)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import requests
from io import BytesIO
import yt_dlp
from pydub.utils import which
import imageio_ffmpeg as ffmpeg_helper

# Détection FFmpeg
DEFAULT_FFMPEG = which("ffmpeg") or which("ffmpeg.exe") or ffmpeg_helper.get_ffmpeg_exe()
if not DEFAULT_FFMPEG or not os.path.isfile(DEFAULT_FFMPEG):
    QMessageBox.critical(None, "FFmpeg introuvable",
                         f"Impossible de localiser ffmpeg."
                         f"\nInstallez via `pip install imageio-ffmpeg` ou ajoutez ffmpeg au PATH."
                         f"\nTentative d'utilisation : {DEFAULT_FFMPEG}")
    sys.exit(1)

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grab Studio")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(800, 600)
        self.history = []  # liste des téléchargements

        # Layout principal
        main_layout = QHBoxLayout(self)

        # Menu latéral
        self.menu_frame = QFrame()
        self.menu_frame.setFixedWidth(200)
        self.menu_frame.setStyleSheet("background-color: #2c3e50; color: white;")
        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setContentsMargins(5,5,5,5)
        # Boutons menu
        self.btn_download_view = QPushButton("Téléchargement")
        self.btn_history_view  = QPushButton("Historique")
        for btn in (self.btn_download_view, self.btn_history_view):
            btn.setStyleSheet("padding:10px;color:white;background:#34495e;border:none;text-align:left;")
        self.btn_download_view.clicked.connect(lambda: self.switch_view(0))
        self.btn_history_view.clicked.connect(lambda: self.switch_view(1))
        menu_layout.addWidget(self.btn_download_view)
        menu_layout.addWidget(self.btn_history_view)
        menu_layout.addStretch()

        # Zone de contenu avec empilement de vues
        self.stack = QStackedLayout()
        self.stack.addWidget(self.create_download_view())
        self.stack.addWidget(self.create_history_view())

        # Conteneur principal
        container = QFrame()
        container.setLayout(self.stack)

        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(container)

    def create_download_view(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20,20,20,20)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://www.youtube.com/watch?v=ID_VIDEO")
        self.url_input.textChanged.connect(self.update_metadata)

        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(320,180)
        self.thumbnail_label.setScaledContents(True)

        self.video_title = QLabel("Titre: -")
        self.video_duration = QLabel("Durée: -")
        self.video_bitrate = QLabel("Bitrate: -")

        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP3","WAV","FLAC","OGG","MP4"])

        self.download_button = QPushButton("Télécharger")
        self.download_button.clicked.connect(self.download_media)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("font-weight:bold;")

        self.debug_console = QTextEdit()
        self.debug_console.setReadOnly(True)
        self.debug_console.setFixedHeight(100)
        self.debug_console.setStyleSheet("background:#1e1e1e;color:#fff;font-family:Consolas;font-size:12px;")

        for w in (self.url_input, self.thumbnail_label, self.video_title,
                  self.video_duration, self.video_bitrate,
                  QLabel("Format de sortie:"), self.format_combo,
                  self.download_button, self.status_label,
                  QLabel("Console de debug:"), self.debug_console):
            layout.addWidget(w)
        layout.addStretch()
        return frame

    def create_history_view(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20,20,20,20)
        self.history_list = QListWidget()
        layout.addWidget(QLabel("Historique des téléchargements:"))
        layout.addWidget(self.history_list)
        return frame

    def switch_view(self, index):
        self.stack.setCurrentIndex(index)

    def log(self,msg):
        self.debug_console.append(msg)

    def is_valid_youtube_url(self,url):
        try:
            p=urlparse(url)
            if "youtu.be" in p.netloc and len(p.path.strip("/"))==11: return True
            if "youtube.com" in p.netloc and p.path=="/watch" and "v" in parse_qs(p.query): return True
        except Exception as e:
            self.log(f"URL validation error: {e}")
        return False

    def clean_url(self,url):
        p=urlparse(url)
        if "youtu.be" in p.netloc: return f"https://youtu.be{p.path}"
        if "youtube.com" in p.netloc:
            q=parse_qs(p.query)
            if "v" in q: return f"https://www.youtube.com/watch?v={q['v'][0]}"
        return url

    def update_metadata(self):
        raw = self.url_input.text().strip()
        self.debug_console.clear()
        self.log(f"Metadata pour: {raw}")
        if not self.is_valid_youtube_url(raw):
            for lbl in (self.thumbnail_label,self.video_title,self.video_duration,self.video_bitrate):
                lbl.clear()
            self.video_title.setText("Titre: -")
            self.video_duration.setText("Durée: -")
            self.video_bitrate.setText("Bitrate: -")
            return
        try:
            url=self.clean_url(raw)
            self.log(f"URL nettoyée: {url}")
            opts={'quiet':True,'skip_download':True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                self.info = ydl.extract_info(url,download=False)
            title,duration=self.info.get('title','-'),self.info.get('duration',0)
            mins,secs=divmod(duration,60)
            abr= next((f.get('abr') for f in self.info.get('formats',[]) if f.get('abr')), '-')
            self.video_title.setText(f"Titre: {title}")
            self.video_duration.setText(f"Durée: {mins}m {secs}s")
            self.video_bitrate.setText(f"Bitrate: {abr}")
            thumb=self.info.get('thumbnail')
            if thumb:
                data=requests.get(thumb).content
                pix=QPixmap(); pix.loadFromData(data)
                self.thumbnail_label.setPixmap(pix.scaled(self.thumbnail_label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
                self.log("Miniature affichée")
        except Exception as e:
            self.log(f"Erreur metadata: {e}")
            self.status_label.setText("Erreur metadata (voir console)")

    def download_media(self):
        raw=self.url_input.text().strip()
        fmt=self.format_combo.currentText().lower()
        self.log(f"Début download: {raw}, fmt={fmt}")
        if not self.is_valid_youtube_url(raw):
            self.log("URL invalide pour download")
            self.status_label.setText("URL invalide.")
            return
        folder=QFileDialog.getExistingDirectory(self,"Choisir dossier de sauvegarde")
        if not folder:
            self.log("Download annulé, dossier non sélectionné")
            return
        url=self.clean_url(raw)
        opts={'ffmpeg_location':DEFAULT_FFMPEG,'outtmpl':os.path.join(folder,'%(title)s.%(ext)s')}
        if fmt=='mp4': opts['format']='bestvideo+bestaudio/best'
        else:
            opts['format']='bestaudio'
            opts['postprocessors']=[{
                'key':'FFmpegExtractAudio',
                'preferredcodec':fmt,
                'preferredquality':'192',
            }]
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                self.status_label.setText("Téléchargement en cours...")
                ydl.download([url])
            name = f"{self.info['title']}.{fmt}"
            self.history.append(name)
            self.history_list.addItem(QListWidgetItem(name))
            self.status_label.setText("Téléchargement terminé !")
            self.log(f"Téléchargé: {name}")
        except Exception as e:
            self.log(f"Erreur download: {e}")
            self.status_label.setText("Erreur download (voir console)")
            QMessageBox.critical(self,"Erreur",str(e))

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=YouTubeDownloader()
    window.show()
    sys.exit(app.exec_())
