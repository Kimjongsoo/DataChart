import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QSpinBox, QPushButton
)
from PyQt5.QtCore import QTimer

class RefreshWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("refresh window")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.setFixedSize(500, 150)  # 너비 400px, 높이 300px로 고정
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2


        # 메인 위젯과 레이아웃 설정
        self.main_widget = QWidget()
        self.layout = QVBoxLayout(self.main_widget)

        # 새로고침 주기 설정 UI
        self.label = QLabel("새로고침 주기 (초):")
        self.spin_box = QSpinBox()
        self.spin_box.setRange(1, 60)  # 주기 범위: 1초 ~ 60초
        self.spin_box.setValue(5)  # 기본값: 5초
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.spin_box)

        # 확인 및 취소 버튼 설정
        self.button_layout = QHBoxLayout()
        self.ok_button = QPushButton("확인")
        self.cancel_button = QPushButton("취소")
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_layout)

        # 버튼 이벤트 연결
        self.ok_button.clicked.connect(self.apply_refresh)
        self.cancel_button.clicked.connect(self.close)

        self.setCentralWidget(self.main_widget)

        # 타이머 설정 (새로고침 기능)
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_action)

    def apply_refresh(self):
        # 새로고침 주기를 설정하고 타이머 시작
        refresh_frequency = self.spin_box.value() * 1000  # 밀리초로 변환
        self.timer.start(refresh_frequency)
        self.close()  # 창 닫기

    def refresh_action(self):
        # 새로고침 시 실행할 작업
        print("새로고침 실행 중...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RefreshWindow()
    window.show()
    sys.exit(app.exec_())
