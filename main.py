import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

form_class = uic.loadUiType("test.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 위젯을 matplotlib 캔버스로 교체
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # UI에서 widgetForChart 위젯을 가져와 layout 설정
        layout = QVBoxLayout(self.widgetForChart)
        layout.addWidget(self.canvas)

        # CSV 파일에서 데이터 읽기
        data = pd.read_csv("data.csv")

        # 차트 그리기
        self.plot(data)

    def plot(self, data):
        self.ax.clear()  # 기존 그래프 지우기

        # date 값을 문자열로 변환하여 10/15 형식으로 만들기
        data['date'] = pd.to_datetime(data['date'], format='%m%d')  # 월과 일을 인식하도록 변환
        data['date'] = data['date'].dt.strftime('%m/%d')  # 원하는 형식으로 변환

        # Y축에서 과학적 표기법 비활성화
        self.ax.get_yaxis().get_major_formatter().set_scientific(False)

        self.ax.plot(data['date'], data['allsum'], marker='o')  # 변환된 date 사용
        self.ax.set_xlabel('Date')  # x축 라벨 설정
        self.ax.set_ylabel('All Sum')  # y축 라벨 설정
        self.figure.tight_layout()  # 그래프가 겹치지 않도록 여백 자동 조정
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()