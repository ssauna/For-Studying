import sys
import subprocess
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import pygetwindow as gw
from screeninfo import get_monitors

class MultiAppViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Multi Application Viewer')
        self.setGeometry(0, 0, 1080, 1920)

        main_layout = QVBoxLayout()
        content_layout = QHBoxLayout()

        # 유튜브 프레임
        youtube_frame = QFrame(self)
        youtube_layout = QVBoxLayout(youtube_frame)
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("https://www.youtube.com"))
        youtube_layout.addWidget(self.web_view)
        youtube_frame.setLayout(youtube_layout)

        # 유튜브 프레임 위치 및 크기 설정
        youtube_frame.setFixedSize(600, 400)
        youtube_frame.move(0, 0)

        # 버튼 프레임
        button_frame = QFrame(self)
        button_layout = QVBoxLayout(button_frame)

        btn_load_youtube = QPushButton('Load YouTube', self)
        btn_load_youtube.clicked.connect(self.load_youtube)
        button_layout.addWidget(btn_load_youtube)

        btn_excel = QPushButton('Open Excel', self)
        btn_excel.clicked.connect(self.open_excel)
        button_layout.addWidget(btn_excel)

        btn_word = QPushButton('Open Word', self)
        btn_word.clicked.connect(self.open_word)
        button_layout.addWidget(btn_word)

        btn_outlook = QPushButton('Open Outlook', self)
        btn_outlook.clicked.connect(self.open_outlook)
        button_layout.addWidget(btn_outlook)

        button_frame.setLayout(button_layout)
        button_frame.move(800, 0)  # 버튼 프레임의 위치 조정

        # 레이아웃 설정
        content_layout.addWidget(youtube_frame)
        content_layout.addWidget(button_frame)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def load_youtube(self):
        subprocess.Popen(r'"C:\Program Files\Google\Chrome\Application\chrome_proxy.exe" --profile-directory=Default --app-id=agimnkijcaahngcdmfeangaknmldooml')
        time.sleep(5)  # YouTube 창이 열릴 시간을 확보
        try:
            youtube_window = gw.getWindowsWithTitle("YouTube")[0]
            youtube_window.moveTo(monitor_x, monitor_y)
            youtube_window.resizeTo(600, 400)
        except IndexError:
            print("YouTube 창을 찾을 수 없습니다.")

    def open_program(self, path, window_title, x, y, width, height):
        subprocess.Popen(path)
        time.sleep(5)  # 프로그램이 실행될 시간을 확보
        try:
            window = gw.getWindowsWithTitle(window_title)[0]
            window.moveTo(x, y)
            window.resizeTo(width, height)
        except IndexError:
            print(f"Could not find window with title: {window_title}")

    def open_excel(self):
        self.open_program("C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE", "Excel", monitor_x, monitor_y + 540, 540, 690)

    def open_word(self):
        self.open_program("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE", "Word", monitor_x + 540, monitor_y + 540, 540, 690)

    def open_outlook(self):
        self.open_program("C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.EXE", "Outlook", monitor_x, monitor_y + 1230, 1080, 690)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    monitors = get_monitors()
    if len(monitors) < 2:
        raise Exception("2번 모니터를 찾을 수 없습니다.")
    monitor_info = monitors[1]
    monitor_x, monitor_y = monitor_info.x, monitor_info.y

    viewer = MultiAppViewer()
    viewer.move(monitor_x, monitor_y)  # 창을 2번 모니터에 배치
    viewer.show()

    sys.exit(app.exec_())
