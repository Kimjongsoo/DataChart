import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from setting_window import SettingsWindow
import numpy as np

form_class = uic.loadUiType("test.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DataChart")

        # 위젯을 matplotlib 캔버스로 교체
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # UI에서 widgetForChart 위젯을 가져와 layout 설정
        layout = QVBoxLayout(self.widgetForChart)
        layout.addWidget(self.canvas)

        # CSV 파일에서 데이터 읽기
        self.data = pd.read_csv("data.csv")

        # 차트 그리기
        self.plot()

        self.pushButton_2.clicked.connect(self.open_settings_window)

    def plot(self):
        self.ax.clear()  # 기존 그래프 지우기

        # date 값을 문자열로 변환하여 10/15 형식으로 만들기
        self.data['date'] = pd.to_datetime(self.data['date'], format='%m%d')  # 월과 일을 인식하도록 변환
        self.data['date'] = self.data['date'].dt.strftime('%m/%d')  # 원하는 형식으로 변환

        # Y축에서 과학적 표기법 비활성화
        self.ax.get_yaxis().get_major_formatter().set_scientific(False)

        # 선 그래프 그리기
        self.ax.plot(self.data['date'], self.data['allsum'], marker='o', color='b')
        self.ax.set_xlabel('Date')  # x축 라벨 설정
        self.ax.set_ylabel('All Sum')  # y축 라벨 설정
        self.ax.set_xticks(range(len(self.data)))  # X축 눈금을 데이터 길이에 맞춤
        self.ax.set_xticklabels(self.data['date'], rotation=0)

        # 산포도 추가 (툴팁 활성화용)
        self.scatter = self.ax.scatter(range(len(self.data)), self.data['allsum'], color='b', alpha=0)  # 투명한 점 추가

        # 툴팁 설정
        self.annot = self.ax.annotate(
            "", xy=(0, 0), xytext=(10, 10),
            textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)

        # 마우스 이벤트 연결
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)

        self.figure.tight_layout()  # 그래프가 겹치지 않도록 여백 자동 조정
        self.canvas.draw()

    def open_settings_window(self):
        self.settings_window = SettingsWindow()
        self.settings_window.exec_()

    def update_annot(self, ind):
        # 툴팁 위치 및 텍스트 업데이트
        pos = self.scatter.get_offsets()[ind["ind"][0]]
        self.annot.xy = pos
        date = self.data['date'].iloc[ind["ind"][0]]
        allsum = self.data['allsum'].iloc[ind["ind"][0]]
        text = f"Date: {date}\nAll Sum: {allsum}"
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.8)

    def on_hover(self, event):
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, ind = self.scatter.contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.canvas.draw_idle()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()