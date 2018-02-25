from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *


class Media(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        self.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("F:/VTS_01_2.avi")))
        self.mediaPlayer.play()

        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    m = Media()
    m.resize(640, 480)
    m.show()
    sys.exit(app.exec_())

