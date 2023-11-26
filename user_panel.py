from PyQt6 import QtWidgets, QtCore, QtGui
from tools import * 


class UserPage(QtWidgets.QMainWindow):
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
        self.version_text.setGeometry(965, 680, 70, 20)
        self.version_text.setObjectName('version_text')
        self.create_button = QtWidgets.QPushButton('CREATE MEETING', self.centralwidget)
        self.create_button.setGeometry(100, 100, 200, 200)
        self.create_button.setObjectName('create_button')
        self.view_button = QtWidgets.QPushButton('VIEW MEETINGS', self.centralwidget)
        self.view_button.setGeometry(100, 400, 200, 200)
        self.view_button.setObjectName('view_button')