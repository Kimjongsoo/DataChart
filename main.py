import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from refresh_window import RefreshWindow

form_class = uic.loadUiType("test.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("DataChart")

        matplotlib.rc('font', family='Malgun Gothic')
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

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
        self.data = pd.read_csv("data.csv")
        self.data_st = pd.read_csv("daily stock.csv")

        # 차트 그리기
        self.plot()
        self.st_plot()

        # 툴팁 초기화
        self.annot = self.ax.annotate(
            "", xy=(0, 0), xytext=(10, 10),
            textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"))
        self.annot.set_visible(False)

        self.annot_st = self.ax_2.annotate(
            "", xy=(0, 0), xytext=(10, 10),
            textcoords="offset points", bbox=dict(boxstyle="round", fc="w"),
            arrowprops=dict(arrowstyle="->"))
        self.annot_st.set_visible(False)


        # 마우스 이동 이벤트 연결
        self.canvas.mpl_connect('motion_notify_event', self.hover)
        self.canvas_2.mpl_connect('motion_notify_event', self.hover_st)


        #pushbuttn_2에 창 연결
        self.pushButton_2.clicked.connect(self.handle_pushButton_2)


    def plot(self):
        self.ax.clear()  # 기존 그래프 지우기

        # date 값을 문자열로 변환하여 10/15 형식으로 만들기
        self.data['date'] = pd.to_datetime(self.data['date'], format='%m%d')  # 월과 일을 인식하도록 변환
        self.data['date'] = self.data['date'].dt.strftime('%m/%d')  # 원하는 형식으로 변환

        # Y축에서 과학적 표기법 비활성화
        self.ax.get_yaxis().get_major_formatter().set_scientific(False)
        self.ax.plot(self.data['date'], self.data['allsum'], marker='o')  # 변환된 date 사용

        self.scatter_points = self.ax.scatter(self.data['date'], self.data['allsum'],  color='b', alpha=0.6, marker='o')
        self.ax.set_xlabel('Date')  # x축 라벨 설정
        self.ax.set_ylabel('All Sum')  # y축 라벨 설정
        self.figure.tight_layout()  # 그래프가 겹치지 않도록 여백 자동 조정
        self.ax.plot(self.data['date'], self.data['allsum'])
        self.canvas.draw()

    def st_plot(self):
        self.ax_2.clear()  # 기존 그래프 지우기

        # date 값을 문자열로 변환하여 10/15 형식으로 만들기
        self.data_st['날짜'] = self.data_st['날짜'].astype(str)
        # data_st['날짜'] = pd.to_datetime(data_st['날짜'], format='%Y%m%d')  # 월과 일을 인식하도록 변환
        # data_st['날짜'] = data_st['날짜'].dt.strftime('%Y/%m/%d')  # 원하는 형식으로 변환

        # Y축에서 과학적 표기법 비활성화
        formatter = self.ax_2.get_yaxis().get_major_formatter()
        formatter.set_scientific(False)

        self.ax_2.plot(self.data_st['날짜'], self.data_st['가격'])
        self.scatter_points_st= self.ax_2.scatter(self.data_st['날짜'], self.data_st['가격'],color='b', alpha=0.6, marker='x')
        self.ax_2.set_xlabel('날짜')  # x축 라벨 설정
        self.ax_2.set_ylabel('가격')  # y축 라벨 설정
        self.figure_2.tight_layout()  # 그래프가 겹치지 않도록 여백 자동 조정
        self.canvas_2.draw()

    def hover(self, event):
        if event.inaxes == self.ax:
            # 산포도 점에서 가장 가까운 점 찾기
            cont, ind = self.scatter_points.contains(event)
            if cont:
                index = ind["ind"][0]  # 첫 번째 점의 인덱스 가져오기
                x = self.data['date'][index]
                y = self.data['allsum'][index]

                # 툴팁 위치 및 텍스트 설정
                self.annot.xy = (x, y)
                self.annot.set_text(f'Date: {x}\nAll Sum: {y}')
                self.annot.set_visible(True)
                self.canvas.draw_idle()  # 툴팁이 보이도록 업데이트
            else:
                self.annot.set_visible(False)
                self.canvas.draw_idle()  # 툴팁 숨기기

    def hover_st(self, event):
        if event.inaxes == self.ax_2:
            # 산포도 점에서 가장 가까운 점 찾기
            cont, ind = self.scatter_points_st.contains(event)
            if cont:
                index = ind["ind"][0]  # 첫 번째 점의 인덱스 가져오기
                x = self.data_st['날짜'][index]
                y = self.data_st['가격'][index]

                # 툴팁 위치 및 텍스트 설정
                self.annot_st.xy = (x, y)
                self.annot_st.set_text(f'Date: {x}\nAll Sum: {y}')
                self.annot_st.set_visible(True)
                self.canvas_2.draw_idle()  # 툴팁이 보이도록 업데이트
            else:
                self.annot_st.set_visible(False)
                self.canvas_2.draw_idle()  # 툴팁 숨기기


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