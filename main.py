import sys
import os

from mutagen.mp3 import MP3
from interface import Ui_MainWindow
from support import Support
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon


class MediaPlayer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.data, self.play_mod = [], 2
        self.player = QMediaPlayer(self)
        self.playlist = QMediaPlaylist(self)
        self.player.setPlaylist(self.playlist)
        self.player_music, self.load_music = False, False
        self.horizontalSlider.sliderReleased.connect(self.change_time)
        self.player.positionChanged.connect(self.print_time_music)
        self.playlist.currentIndexChanged.connect(self.len_music)
        self.download_btn.clicked.connect(self.download_file)
        self.listWidget.itemClicked.connect(self.play_music)
        self.playPause_btn.clicked.connect(self.run_pause)
        self.playBack_btn.clicked.connect(self.run_back)
        self.playForward_btn.clicked.connect(self.run_forward)
        self.stopButton.clicked.connect(self.stop_music)
        self.downloadCatalog_btn.clicked.connect(self.download_playlist)
        self.support_btn.clicked.connect(self.support)
        self.savePlaylist_btn.clicked.connect(self.save_playlist)
        self.replay_btn.clicked.connect(self.replay)
        self.random_btn.clicked.connect(self.random)

    def change_time(self):
        if bool(self.data):
            self.player.setPosition(self.horizontalSlider.sliderPosition() * 1000)
        else:
            self.horizontalSlider.setSliderPosition(0)

    def download_playlist(self):
        try:
            catalog = QFileDialog.getExistingDirectory(self, str("Open Directory"),
                                                       "/home",
                                                       QFileDialog.ShowDirsOnly
                                                       | QFileDialog.DontResolveSymlinks)
            for file in os.listdir(catalog):
                try:
                    if file[file.rfind('.') + 1:] != 'mp3':
                        continue
                    elif os.path.join(catalog, file) in self.data:
                        continue
                    self.data.append(os.path.join(catalog, file))
                    self.listWidget.addItem(file[:file.rfind('.')])
                    url = QUrl.fromLocalFile(os.path.join(catalog, file))
                    self.playlist.addMedia(QMediaContent(url))
                except Exception:
                    continue
            self.run_pause()
        except Exception:
            pass

    def print_time_music(self):
        time = int(self.player.position() / 1000)
        # a = self.horizontalSlider.value() + 1
        self.horizontalSlider.setSliderPosition(time)
        minutes = int((time - time % 60) / 60)
        seconds = int(time % 60)
        if seconds < 10 and minutes < 10:
            self.timePlaying.setText(f'0{minutes}:0{seconds}')
        elif seconds >= 10 and minutes < 10:
            self.timePlaying.setText(f'0{minutes}:{seconds}')
        elif seconds >= 10 and minutes >= 10:
            self.timePlaying.setText(f'{minutes}:{seconds}')
        else:
            self.timePlaying.setText(f'{minutes}:0{seconds}')

    def download_file(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Download Music',
                                               '/home', '(*.mp3)')[0]
            if fname in self.data:
                raise TypeError
            self.data.append(fname)
            music = fname[fname.rfind('/') + 1:fname.rfind('.')]
            self.listWidget.addItem(music)
            url = QUrl.fromLocalFile(fname)
            self.playlist.addMedia(QMediaContent(url))
        except Exception:
            pass

    def play_music(self):
        music = self.listWidget.currentRow()
        if not self.playlist.currentIndex() == music:
            self.playlist.setCurrentIndex(music)
            self.player.play()
            self.load_music = True
            self.player_music = True
            self.len_music()

    def stop_music(self):
        self.player.stop()
        self.horizontalSlider.setSliderPosition(0)

    def len_music(self):
        music = MP3(self.data[self.playlist.currentIndex()])
        self.listWidget.setCurrentRow(self.playlist.currentIndex())
        minutes = int((music.info.length - music.info.length % 60) / 60)
        seconds = int(music.info.length % 60)
        self.horizontalSlider.setMaximum(int(music.info.length))
        self.horizontalSlider.setSliderPosition(0)
        if seconds < 10 and minutes < 10:
            len_m = f'0{minutes}:0{seconds}'
        elif seconds > 10 and minutes < 10:
            len_m = f'0{minutes}:{seconds}'
        elif seconds < 10 and minutes > 10:
            len_m = f'{minutes}:0{seconds}'
        else:
            len_m = f'{minutes}:{seconds}'
        self.lenTimeMusic.setText(len_m)

    def run_pause(self):
        if bool(self.data):
            if self.player_music:
                self.player.pause()
                self.player_music = False
            else:
                if not self.load_music:
                    try:
                        self.playlist.setCurrentIndex(0)
                        self.load_music = True
                        self.player.play()
                        self.player_music = True
                        self.len_music()
                    except Exception:
                        pass
                else:
                    self.player.play()
                    self.player_music = True
            self.listWidget.setCurrentRow(self.playlist.currentIndex())

    def run_back(self):
        if bool(self.data):
            if self.playlist.currentIndex() - 1 < 0:
                index = len(self.data) - 1
            else:
                index = self.playlist.currentIndex() - 1
            self.playlist.setCurrentIndex(index)
            self.player.play()
            self.listWidget.setCurrentRow(index)
            self.len_music()

    def run_forward(self):
        if bool(self.data):
            if self.playlist.currentIndex() + 1 > len(self.data) - 1:
                index = 0
            else:
                index = self.playlist.currentIndex() + 1
            self.playlist.next()
            self.player.play()
            self.listWidget.setCurrentRow(index)
            self.len_music()

    def save_playlist(self):
        pass

    def replay(self):
        if bool(self.data):
            try:
                if self.play_mod == 2:
                    self.playlist.setPlaybackMode(1)
                    self.play_mod = 1
                    self.replay_btn.setIcon(QIcon('contents/restart2.png'))
                elif self.play_mod == 1:
                    self.play_mod = 3
                    self.playlist.setPlaybackMode(3)
                    self.replay_btn.setIcon(QIcon('contents/restart3.png'))
                else:
                    self.play_mod = 2
                    self.playlist.setPlaybackMode(2)
                    self.replay_btn.setIcon(QIcon('contents/restart.png'))
            except Exception:
                pass

    def random(self):
        if bool(self.data):
            if self.play_mod != 4:
                self.playlist.setPlaybackMode(4)
                self.play_mod = 4
                self.random_btn.setIcon(QIcon('contents/random2.png'))
                self.replay_btn.setIcon(QIcon('contents/restart.png'))
            else:
                self.play_mod = 2
                self.playlist.setPlaybackMode(2)
                self.replay_btn.setIcon(QIcon('contents/restart.png'))
                self.random_btn.setIcon(QIcon('contents/random.png'))
    
    def support(self):
        self.support = Support()
        self.support.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    App = MediaPlayer()
    App.show()
    sys.exit(app.exec_())
