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

        # Example 데이터 설정
        data = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 14, 12, 15, 13]
        })

        # 차트 그리기
        self.plot(data)

    def plot(self, data):
        self.ax.clear()  # 기존 그래프 지우기
        self.ax.plot(data['x'], data['y'], marker='o')
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()