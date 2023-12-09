from PyQt6 import QtWidgets, QtCore, QtGui
from tools import *
from custom_popup import *
import sqlite3


class UserPage(QtWidgets.QMainWindow):
    def __init__(self, username, team):
        super().__init__()
        self.username = username
        self.team = team
        self.view_frame = ViewMeetingsFrame(self.username, self.team)
        self.plan_frame = PlanMeetingsFrame(self.username, self.team)
        self.teams_frame = ViewTeamsFrame(self.username, self.team)
        self.setWindowTitle('Meetings Planner')
        self.resize(1000, 850)
        self.setMaximumSize(QtCore.QSize(1000, 850))
        self.setMinimumSize(QtCore.QSize(1000, 850))
        self.setWindowIcon(QtGui.QIcon('img/favicon.png'))
        self.stack_container = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack_container)
        self.stack_container.addWidget(self.view_frame)
        self.stack_container.addWidget(self.plan_frame)
        self.stack_container.addWidget(self.teams_frame)
        self.stack_container.setCurrentWidget(self.view_frame)
        self.profile_logo = QtWidgets.QLabel(self)
        self.profile_logo.setGeometry(100, 100, 200, 200)
        self.profile_logo.setObjectName('profile_logo')
        self.version_text = QtWidgets.QLabel('v0.0.2', self)
        self.version_text.setGeometry(965, 830, 70, 20)
        self.version_text.setObjectName('version_text')
        self.view_mett_button = QtWidgets.QPushButton('View Meetings', self)
        self.view_mett_button.setGeometry(10, 300, 100, 50)
        self.view_mett_button.setObjectName('sidebar_active_button')
        self.view_mett_button.clicked.connect(lambda: self.switch_frame(1))
        self.view_mett_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.plan_meeting_button = QtWidgets.QPushButton('Plan Meeting', self)
        self.plan_meeting_button.setGeometry(10, 400, 100, 50)
        self.plan_meeting_button.setObjectName('sidebar_button')
        self.plan_meeting_button.clicked.connect(lambda: self.switch_frame(2))
        self.plan_meeting_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.view_your_teams = QtWidgets.QPushButton('View Your Teams', self)
        self.view_your_teams.setGeometry(10, 500, 100, 50)  
        self.view_your_teams.setObjectName('sidebar_button')
        self.view_your_teams.clicked.connect(lambda: self.switch_frame(3))
        self.view_your_teams.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.welcome_message = QtWidgets.QLabel(f'Welcome back in your account, {username}', self)
        self.welcome_message.setGeometry(150, 35, 820, 50)
        self.welcome_message.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.welcome_message.setObjectName('welcome_message')
        self.profile_icon = QtWidgets.QLabel(self)
        self.profile_icon.setGeometry(10, 15, 100, 100)
        self.profile_icon.setObjectName('profile_icon')
        self.profile_icon_text = QtWidgets.QLabel(f'{username[0].upper()}', self)
        self.profile_icon_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.profile_icon_text.setGeometry(10, 15, 100, 100)
        self.profile_icon_text.setObjectName('profile_icon_text')
        self.left_border = QtWidgets.QLabel(self)
        self.left_border.setGeometry(120, 0, 2, 850)
        self.left_border.setObjectName('left_border')
        self.top_border = QtWidgets.QLabel(self)
        self.top_border.setGeometry(120, 120, 880, 2)
        self.top_border.setObjectName('top_border')

    def switch_frame(self, page_number: int):
        if page_number == 1:
            self.stack_container.setCurrentWidget(self.view_frame)
            self.view_mett_button.setObjectName('sidebar_active_button')
            self.view_mett_button.setStyleSheet('style.css')
            for button in [self.plan_meeting_button, self.view_your_teams]:
                button.setObjectName('sidebar_button')
                button.setStyleSheet('style.css')
        elif page_number == 2:
            self.stack_container.setCurrentWidget(self.plan_frame)
            self.plan_meeting_button.setObjectName('sidebar_active_button')
            self.plan_meeting_button.setStyleSheet('style.css')
            for button in [self.view_mett_button, self.view_your_teams]:
                button.setObjectName('sidebar_button')
                button.setStyleSheet('style.css')
        elif page_number == 3:
            self.stack_container.setCurrentWidget(self.teams_frame)
            self.view_your_teams.setObjectName('sidebar_active_button')
            self.view_your_teams.setStyleSheet('style.css')
            for button in [self.view_mett_button, self.plan_meeting_button]:
                button.setObjectName('sidebar_button')
                button.setStyleSheet('style.css')


        

class PlanMeetingsFrame(QtWidgets.QFrame):
    def __init__(self, username, team):
        super().__init__()
        self.username = username
        self.team = team
        self.calendar_widget = QtWidgets.QCalendarWidget(self)
        self.calendar_widget.setGeometry(150, 150, 820, 670)
        self.calendar_widget.setObjectName('calendar_widget')
        self.calendar_widget.setGridVisible(True)
        self.calendar_widget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar_widget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames)
        self.calendar_widget.setFirstDayOfWeek(QtCore.Qt.DayOfWeek.Monday)
        self.calendar_widget.setDateEditEnabled(False)
        self.check_mettings(self.team) 
        
    
    def check_mettings(self, team):
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        for meeting_date in cursor.execute('SELECT day, month, year FROM meetings WHERE team=(?)', (team.lower(),)):
            self.target_date = QtCore.QDate(meeting_date[2], meeting_date[1], meeting_date[0])
            self.special_date_format = self.calendar_widget.dateTextFormat(self.target_date)
            self.special_date_format.setBackground(QtGui.QBrush(QtGui.QColor('#6D6B6D')))
            self.special_date_format.setForeground(QtGui.QBrush(QtGui.QColor('#c49f9f')))
            self.calendar_widget.setDateTextFormat(self.target_date, self.special_date_format)
        close_db(connection, cursor)

   

class ViewTeamsFrame(QtWidgets.QFrame):
    def __init__(self, username, team):
        super().__init__()
        pass

class ViewMeetingsFrame(QtWidgets.QFrame):
    def __init__(self, username, team):
        super().__init__()
        self.username = username
        self.team = team
        self.calendar_widget = QtWidgets.QCalendarWidget(self)
        self.calendar_widget.setGeometry(150, 150, 820, 670)
        self.calendar_widget.setObjectName('calendar_widget')
        self.calendar_widget.setGridVisible(True)
        self.calendar_widget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar_widget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.HorizontalHeaderFormat.SingleLetterDayNames)
        self.calendar_widget.setFirstDayOfWeek(QtCore.Qt.DayOfWeek.Monday)
        self.calendar_widget.setDateEditEnabled(False)
        self.check_mettings(self.team) 
        self.calendar_widget.clicked.connect(lambda: self.check_date(self.team))
    
    def check_mettings(self, team):
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        for meeting_date in cursor.execute('SELECT day, month, year FROM meetings WHERE team=(?)', (team.lower(),)):
            self.target_date = QtCore.QDate(meeting_date[2], meeting_date[1], meeting_date[0])
            self.special_date_format = self.calendar_widget.dateTextFormat(self.target_date)
            self.special_date_format.setBackground(QtGui.QBrush(QtGui.QColor('#811717')))
            self.special_date_format.setForeground(QtGui.QBrush(QtGui.QColor('#c49f9f')))
            self.calendar_widget.setDateTextFormat(self.target_date, self.special_date_format)
        close_db(connection, cursor)

    def check_date(self, team):
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        selected_day = self.calendar_widget.selectedDate().day()
        selected_month = self.calendar_widget.selectedDate().month()
        selected_year = self.calendar_widget.selectedDate().year()
        today_date = QtCore.QDate.currentDate()
        for meeting_date in cursor.execute('SELECT day, month, year FROM meetings WHERE team=(?)', (team.lower(),)):
            if meeting_date[0] == selected_day and meeting_date[1] == selected_month and meeting_date[2] == selected_year:
                for meeting_details in cursor.execute('SELECT title, description, hour FROM meetings WHERE team=(?) AND day=(?) AND month=(?) AND year=(?)', (team.lower(), selected_day, selected_month, selected_year)):
                    self.meeting_date = f'{selected_day}/{selected_month}/{selected_year}'
                    self.pop_up_message = MeetingDetails('Meeting Details', meeting_details[0], meeting_details[1], meeting_details[2], self.meeting_date)
                    self.pop_up_message.show()
        close_db(connection, cursor)