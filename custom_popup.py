from PyQt6 import QtWidgets, QtCore, QtGui

class MeetingDetails(QtWidgets.QWidget):
    def __init__(self, window_title, meeting_title, meeting_description, meeting_time, meeting_date):
        super().__init__()
        self.window_title = window_title
        self.meeting_title = meeting_title
        self.meeting_date = meeting_date
        self.meeting_time = meeting_time
        self.meeting_description = meeting_description
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(QtGui.QIcon('img/favicon.png'))
        self.setFixedSize(300, 200)
        self.title = QtWidgets.QLabel(f'Meeting Title: {self.meeting_title}', self)
        self.title.setGeometry(10, 10, 280, 50)
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setObjectName('popup_title')
        self.description = QtWidgets.QLabel(f'Meeting Description: {self.meeting_description}', self)
        self.description.setGeometry(10, 50, 280, 50)
        self.description.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.description.setObjectName('popup_description')
        self.meeting_date = QtWidgets.QLabel(f'Meeting Date: {self.meeting_date} {self.meeting_time}', self)
        self.meeting_date.setGeometry(10, 90, 280, 50)
        self.meeting_date.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.meeting_date.setObjectName('popup_meeting_date')
        self.close_button = QtWidgets.QPushButton('Close', self)
        self.close_button.setGeometry(10, 150, 280, 50)
        self.close_button.setObjectName('popup_close_button')
        self.close_button.clicked.connect(self.close)
        with open('style/style.css', 'r') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)

   
class ErrorFrame(QtWidgets.QWidget):
    def __init__(self, window_title, error_message):
        super().__init__()
        self.window_title = window_title
        self.error_message = error_message
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(QtGui.QIcon('img/favicon.png'))
        self.setFixedSize(300, 200)
        self.error_message = QtWidgets.QLabel(self.error_message, self)
        self.error_message.setGeometry(10, 10, 280, 50)
        self.error_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.error_message.setObjectName('error_message')
        self.close_button = QtWidgets.QPushButton('Close', self)
        self.close_button.setGeometry(10, 150, 280, 50)
        self.close_button.setObjectName('error_close_button')
        self.close_button.clicked.connect(self.close)
        with open('style/style.css', 'r') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)

class CreateMeeting(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.window_title = 'Create Meeting'
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(QtGui.QIcon('img/favicon.png'))
        