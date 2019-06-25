import sys
from functools import reduce

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QScrollArea, QVBoxLayout, QPushButton

from lyric_parser import LyricParser
from netrequest import NeteaseRequest
from spotifydbus import SpotifyDBus


class SpotifyricsWin(QWidget):
    """Spotifyrics GUI Window."""
    refresh_btn: QPushButton
    scroll_area: QScrollArea
    layout: QVBoxLayout
    lyric_label: QLabel

    def __init__(self):
        """Init """
        super().__init__()
        self.netease_req = NeteaseRequest()
        self.parser = LyricParser()
        self.spotifydbus = SpotifyDBus()
        self.not_found_text = 'Not Found Any Lyrics!'
        self.lyric = self.not_found_text
        self.current_playing = ''
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 500, 600)
        self.setWindowTitle('Spotifyircs')

        self.lyric_label = QLabel()
        self.lyric_label.setText(self.lyric)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.lyric_label)

        self.refresh_btn = QPushButton()
        self.refresh_btn.setText('Refresh')
        self.refresh_btn.clicked.connect(self.refresh)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.refresh_btn)
        self.setLayout(self.layout)

        self.show()

    @pyqtSlot()
    def refresh(self):
        keywords = self.spotifydbus.get_keywords()
        if keywords == self.current_playing:
            pass
        self.current_playing = keywords
        self.lyric = self.not_found_text
        original_lyric, transed_lyric = self.netease_req.get_lyrics(keywords)
        lyric_dict = self.parser.parse(original_lyric, transed_lyric)
        if lyric_dict:
            self.lyric = reduce(lambda x, y: x + y, lyric_dict.values())
        self.lyric_label.setText(self.lyric)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    spotifyrics = SpotifyricsWin()
    sys.exit(app.exec_())
