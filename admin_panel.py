from PyQt6 import QtWidgets, QtCore, QtGui
from tools import * 
import sqlite3

class AdminPage(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.add_user_frame = AddUserFrame()
        self.delete_user_frame = DeleteUserFrame(self.username)
        self.setWindowTitle('Meeting Planner')
        self.setFixedSize(1000, 850)
        self.setWindowIcon(QtGui.QIcon('img/favicon.png'))
        self.stack_container = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack_container)
        self.stack_container.addWidget(self.add_user_frame)
        self.stack_container.addWidget(self.delete_user_frame)
        self.stack_container.setCurrentWidget(self.add_user_frame)
        self.profile_logo = QtWidgets.QLabel(self)
        self.profile_logo.setGeometry(100, 100, 200, 200)
        self.profile_logo.setObjectName('profile_logo')
        self.version_text = QtWidgets.QLabel('v0.0.2', self)
        self.version_text.setGeometry(965, 830, 70, 20)
        self.version_text.setObjectName('version_text')
        self.add_user_button = QtWidgets.QPushButton('ADD USER', self)
        self.add_user_button.setGeometry(10, 300, 100, 50)
        self.add_user_button.setObjectName('sidebar_active_button')
        self.add_user_button.clicked.connect(lambda: self.switch_frame(1))
        self.delete_user_button = QtWidgets.QPushButton('DELETE USER', self)
        self.delete_user_button.setGeometry(10, 500, 100, 50)  
        self.delete_user_button.setObjectName('sidebar_button')
        self.delete_user_button.clicked.connect(lambda: self.switch_frame(2))
        for button in [self.add_user_button, self.delete_user_button]:
            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
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
        self.left_border.setGeometry(120, 0, 4, 850)
        self.left_border.setObjectName('left_border')
        self.top_border = QtWidgets.QLabel(self)
        self.top_border.setGeometry(120, 120, 880, 4)
        self.top_border.setObjectName('top_border')
    
    def switch_frame(self, page_number: int):
        if page_number == 1:
            self.stack_container.setCurrentWidget(self.add_user_frame)
            self.add_user_button.setObjectName('sidebar_active_button')
            self.add_user_button.setStyleSheet('style.css')
            self.delete_user_button.setObjectName('sidebar_button')
            self.delete_user_button.setStyleSheet('style.css')
            
        elif page_number == 2:
            self.stack_container.setCurrentWidget(self.delete_user_frame)
            self.delete_user_button.setObjectName('sidebar_active_button')
            self.delete_user_button.setStyleSheet('style.css')
            self.add_user_button.setObjectName('sidebar_button')
            self.add_user_button.setStyleSheet('style.css')

class AddUserFrame(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_title = QtWidgets.QLabel('ADD NEW USER', self)
        self.main_title.setGeometry(400, 220, 300, 50)
        self.main_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_title.setObjectName('main_title')
        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setGeometry(438, 300, 200, 40)
        self.username_input.setPlaceholderText('username')
        self.username_input.setObjectName('default_input')
        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setGeometry(438, 360, 200, 40)
        self.password_input.setPlaceholderText('password')
        self.password_input.setObjectName('default_input')
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.team_input = QtWidgets.QLineEdit(self)
        self.team_input.setGeometry(438, 420, 200, 40)
        self.team_input.setPlaceholderText('team')
        self.team_input.setObjectName('default_input')
        self.role_input = QtWidgets.QLineEdit(self)
        self.role_input.setGeometry(438, 480, 200, 40)
        self.role_input.setPlaceholderText('role')
        self.role_input.setObjectName('default_input')
        self.add_user_button = QtWidgets.QPushButton('ADD USER', self)
        self.add_user_button.setGeometry(438, 540, 200, 50)
        self.add_user_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.add_user_button.setObjectName('create_button')
        self.add_user_button.clicked.connect(self.add_user)

    def add_user(self):
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        if len(self.username_input.text()) <= 1 or len(self.password_input.text()) <= 1 or len(self.team_input.text()) <= 1 or len(self.role_input.text()) <= 1:
            create_error(self, 'You have to fill all inputs!', 600, 410, 250, 20)
        else:
            for user in cursor.execute('SELECT username FROM users'):
                if user[0] == self.username_input.text().lower():
                    create_error(self, 'This username is already taken!', 600, 410, 250, 40)
                    for input in [self.username_input, self.password_input, self.team_input, self.role_input]:
                        input.clear()
                    break
            else:
                cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?)', (self.username_input.text(), self.password_input.text(), self.team_input.text(), self.role_input.text()))
                connection.commit()
                create_error(self, 'User added successfully!', 600, 410, 250, 40)
                for input in [self.username_input, self.password_input, self.team_input, self.role_input]:
                        input.clear()
        close_db(connection, cursor)

class DeleteUserFrame(QtWidgets.QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.main_title = QtWidgets.QLabel('DELETE USER', self)
        self.main_title.setGeometry(400, 220, 300, 50)
        self.main_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_title.setObjectName('main_title')
        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setGeometry(438, 300, 200, 40)
        self.username_input.setPlaceholderText('username')
        self.username_input.setObjectName('default_input')
        self.delete_user_button = QtWidgets.QPushButton('DELETE USER', self)
        self.delete_user_button.setGeometry(438, 540, 200, 50)
        self.delete_user_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.delete_user_button.setObjectName('create_button')
        self.delete_user_button.clicked.connect(self.delete_user)

    def delete_user(self):
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        if len(self.username_input.text()) <= 1:
            create_error(self, 'You have to fill all inputs!', 600, 410, 250, 20)
        else:
            for user in cursor.execute('SELECT username FROM users'):
                if user[0] == self.username_input.text().lower():
                    if user[0] == self.username:
                        create_error(self, 'You can\'t delete yourself!', 600, 410, 250, 40)
                        self.username_input.clear()
                        break
                    else:
                        cursor.execute('DELETE FROM users WHERE username=(?)', (self.username_input.text().lower(),))
                        connection.commit()
                        create_error(self, 'User deleted successfully!', 600, 410, 250, 40)
                        self.username_input.clear()
                        break
            else:
                create_error(self, 'This username doesn\'t exist!', 600, 410, 250, 40)
                self.username_input.clear()
        close_db(connection, cursor)
