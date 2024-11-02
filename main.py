import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from refresh_window import RefreshWindow

form_class = uic.loadUiType("test.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 위젯을 matplotlib 캔버스로 교체
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.figure_2, self.ax_2 = plt.subplots()
        self.canvas_2 = FigureCanvas(self.figure_2)

        # UI에서 widgetForChart 위젯을 가져와 layout 설정
        layout = QVBoxLayout(self.widgetForChart)
        layout.addWidget(self.canvas)

        layout_2 = QVBoxLayout(self.widgetForChart_2)
        layout_2.addWidget(self.canvas_2)

        # CSV 파일에서 데이터 읽기
        data = pd.read_csv("data.csv")
        data_st = pd.read_csv("daily stock.csv")

        # 차트 그리기
        self.plot(data)
        self.st_plot(data_st)

        #pushbuttn_2에 창 연결
        self.pushButton_2.clicked.connect(self.handle_pushButton_2)


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
        self.ax.plot(data['date'], data['allsum'])
        self.canvas.draw()

    def st_plot(self, data_st):
        self.ax_2.clear()  # 기존 그래프 지우기

        # date 값을 문자열로 변환하여 10/15 형식으로 만들기
        data_st['날짜'] = data_st['날짜'].astype(str)
        # data_st['날짜'] = pd.to_datetime(data_st['날짜'], format='%Y%m%d')  # 월과 일을 인식하도록 변환
        # data_st['날짜'] = data_st['날짜'].dt.strftime('%Y/%m/%d')  # 원하는 형식으로 변환

        # Y축에서 과학적 표기법 비활성화
        formatter = self.ax_2.get_yaxis().get_major_formatter()
        formatter.set_scientific(False)

        self.ax_2.plot(data_st['날짜'], data_st['가격'], marker='x')  # 변환된 date 사용
        self.ax_2.set_xlabel('날짜')  # x축 라벨 설정
        self.ax_2.set_ylabel('가격')  # y축 라벨 설정
        self.figure_2.tight_layout()  # 그래프가 겹치지 않도록 여백 자동 조정
        self.canvas_2.draw()


    def handle_pushButton_2(self):
        # pushButton_2 클릭 시 수행할 작업
        print("pushButton_2 클릭됨!")
        # 예: RefreshWindow 창 열기
        self.refresh_window = RefreshWindow()
        self.refresh_window.show()

    def open_refresh_window(self):
        # 새로고침 창 열기
        self.refresh_window = RefreshWindow()  # 외부 모듈에서 가져온 클래스 사용
        self.refresh_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()




