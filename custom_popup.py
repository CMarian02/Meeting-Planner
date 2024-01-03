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
    def __init__(self, team_name, selected_date):
        super().__init__()
        self.team_name = team_name
        self.selected_date = selected_date
        self.window_title = 'Create Meeting'
        self.setWindowTitle(self.window_title)
        self.setWindowIcon(QtGui.QIcon('img/favicon.png'))
        self.setFixedSize(400, 300)
        self.title_input = QtWidgets.QLineEdit(self)
        self.title_input.setGeometry(10, 10, 380, 50)
        self.title_input.setPlaceholderText('Title')
        self.title_input.setObjectName('title_input')
        self.description_input = QtWidgets.QLineEdit(self)
        self.description_input.setGeometry(10, 70, 380, 50)
        self.description_input.setPlaceholderText('Description')
        self.description_input.setObjectName('description_input')
        self.date_input = QtWidgets.QDateEdit(self)
        self.date_input.setMinimumDate(self.selected_date)
        self.date_input.setGeometry(10, 130, 280, 50)
        self.date_input.setObjectName('date_input')
        self.time_input = QtWidgets.QTimeEdit(self)
        self.time_input.setDisplayFormat('HH:mm')
        # self.time_input.setMinimumTime(QtCore.QTime.currentTime()) #TODO: when you switch day in another, you can add every time.
        # self.time_input.setMaximumTime(QtCore.QTime(23, 59)) #TODO: when you switch day in another, you can add every time.
        self.time_input.setGeometry(10, 200, 280, 50)
        self.time_input.setObjectName('time_input')
        self.create_button = QtWidgets.QPushButton('Create', self)
        self.create_button.setGeometry(10, 260, 280, 50)
        self.create_button.setObjectName('create_button')
        self.create_button.clicked.connect(self.create_meeting)
    
    def create_meeting(self):
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        if len(self.title_input.text()) < 3 or len(self.title_input.text()) > 11:
            create_error(self, 'Title must be between 3 and 10 characters!', 10, 10, 280, 50)
        elif len(self.description_input.text()) < 3 or len(self.description_input.text()) > 21:
            create_error(self, 'Description must be between 3 and 20 characters!', 10, 70, 280, 50)
        elif self.date_input.date() == self.selected_date and self.time_input.time() < QtCore.QTime.currentTime():
            create_error(self, 'You cannot create meeting in the past!', 10, 130, 280, 50)
        else:
            cursor.execute(f"INSERT INTO meetings VALUES ('{self.team_name}', '{self.date_input.date().day()}', '{self.date_input.date().month()}', '{self.date_input.date().year()}', '{self.title_input.text()}', '{self.description_input.text()}', '{self.time_input.time().toString('HH:mm')}')")
            close_db(connection, cursor)
            create_error(self, 'Meeting created successfully!', 10, 10, 280, 50)
            self.close()