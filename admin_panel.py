from PyQt6 import QtWidgets, QtCore, QtGui
from tools import * 


class AdminPage(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle('Meetings Planner')
        self.resize(1000, 850)
        self.setMaximumSize(QtCore.QSize(1000, 850))
        self.setMinimumSize(QtCore.QSize(1000, 850))
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.profile_logo = QtWidgets.QLabel(self.centralwidget)
        self.profile_logo.setGeometry(100, 100, 200, 200)
        self.profile_logo.setObjectName('profile_logo')
        self.version_text = QtWidgets.QLabel('v0.0.1', self.centralwidget)
        self.version_text.setGeometry(965, 830, 70, 20)
        self.version_text.setObjectName('version_text')