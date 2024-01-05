from PyQt6 import QtWidgets, QtCore, QtGui
import sqlite3
from tools import *

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
        self.setFixedSize(400, 230)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.meeting_details_title = QtWidgets.QLabel('MEETING DETAILS', self)
        self.meeting_details_title.setGeometry(10, 10, 380, 40)
        self.meeting_details_underline = QtWidgets.QLabel(self)
        self.meeting_details_underline.setGeometry(10, 40, 380, 2)
        self.meeting_details_underline.setObjectName('meeting_details_underline')
        self.meeting_title = QtWidgets.QLabel(F'MEETING TITLE: {self.meeting_title}', self)
        self.meeting_title.setGeometry(10, 40, 380, 50)
        self.meeting_description = QtWidgets.QLabel(F'MEETING DESCRIPTION: {self.meeting_description}', self)
        self.meeting_description.setGeometry(10, 70, 380, 50)
        self.meeting_date = QtWidgets.QLabel(F'MEETING DATE: {self.meeting_date}', self)
        self.meeting_date.setGeometry(10, 100, 380, 50)
        self.meeting_time = QtWidgets.QLabel(F'MEETING TIME: {self.meeting_time}', self)
        self.meeting_time.setGeometry(10, 130, 380, 50)
        for item in [self.meeting_title, self.meeting_description, self.meeting_date, self.meeting_time, self.meeting_details_title]:
            item.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            item.setObjectName('meeting_info')
        self.close_button = QtWidgets.QPushButton('CLOSE', self)
        self.close_button.setGeometry(10, 180, 380, 40)
        self.close_button.setObjectName('close_button')
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
        self.setFixedSize(300, 130)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.error_message = QtWidgets.QLabel(self.error_message, self)
        self.error_message.setGeometry(10, 10, 280, 50)
        self.error_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.error_message.setObjectName('error_message')
        self.close_button = QtWidgets.QPushButton('Close', self)
        self.close_button.setGeometry(10, 70, 280, 50)
        self.close_button.setObjectName('close_button')
        self.close_button.clicked.connect(self.close)
        with open('style/style.css', 'r') as f:
            stylesheet = f.read()
        self.setStyleSheet(stylesheet)

class CreateMeeting(QtWidgets.QWidget):
    def __init__(self, team_name, selected_date):
        super().__init__()
        self.team_name = team_name
        self.selected_date = selected_date
        self.window_title = 'Create Meeting'
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(QtGui.QIcon('img/favicon.png'))
        self.setFixedSize(400, 360)
        self.title_input = QtWidgets.QLineEdit(self)
        self.title_input.setGeometry(10, 10, 380, 50)
        self.title_input.setPlaceholderText('Title')
        self.title_input.setObjectName('createmeet_input')
        self.description_input = QtWidgets.QLineEdit(self)
        self.description_input.setGeometry(10, 70, 380, 50)
        self.description_input.setPlaceholderText('Description')
        self.description_input.setObjectName('createmeet_input')
        self.date_input = QtWidgets.QDateEdit(self)
        self.date_input.setMinimumDate(self.selected_date)
        self.date_input.setGeometry(10, 130, 380, 50)
        self.date_input.setObjectName('date_input')
        self.time_input = QtWidgets.QTimeEdit(self)
        self.time_input.setDisplayFormat('HH:mm')
        # if selected_date == QtCore.QDate.currentDate(): #TODO: Now we not use this, because we can't create meeting in same day as today.
        #     self.time_input.setMinimumTime(QtCore.QTime.currentTime()) 
        #     self.time_input.setMaximumTime(QtCore.QTime(23, 59)) 
        self.time_input.setGeometry(10, 200, 380, 50)
        self.time_input.setObjectName('time_input')
        self.create_button = QtWidgets.QPushButton('Create', self)
        self.create_button.setGeometry(10, 305, 380, 50)
        self.create_button.setObjectName('create_button')
        self.create_button.clicked.connect(self.create_meeting)
    
    def create_meeting(self):
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        if len(self.title_input.text()) < 3 or len(self.title_input.text()) > 11:
            create_error(self, 'Title must be between 3 and 10 characters!', 250, 50, 320, 50)
        elif len(self.description_input.text()) < 3 or len(self.description_input.text()) > 21:
            create_error(self, 'Description must be between 3 and 20 characters!', 250, 50, 320, 50)
        else:
            cursor.execute(f"INSERT INTO meetings VALUES ('{self.team_name}', '{self.date_input.date().day()}', '{self.date_input.date().month()}', '{self.date_input.date().year()}', '{self.title_input.text()}', '{self.description_input.text()}', '{self.time_input.time().toString('HH:mm')}')")
            close_db(connection, cursor)
            self.close()