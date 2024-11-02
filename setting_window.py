from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("setting.ui", self)
        self.setWindowTitle("Settings")