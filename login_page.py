from PyQt5 import QtWidgets, QtCore
from tools import *
import sqlite3, sys

class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meetings Planner")
        self.resize(800,650)
        self.setMinimumSize(QtCore.QSize(800, 650))
        self.setMaximumSize(QtCore.QSize(800, 650))
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        self.left_panel = QtWidgets.QLabel(self.centralwidget)
        self.left_panel.setGeometry(150, 150, 250, 400)
        self.left_panel.setObjectName('left_panel')
        self.right_panel = QtWidgets.QLabel(self.centralwidget)
        self.right_panel.setGeometry(410, 150, 250, 400)
        self.right_panel.setObjectName('right_panel')

        self.app_logo = QtWidgets.QLabel(self.centralwidget)
        self.app_logo.setGeometry(175, 250, 200, 200)
        self.app_logo.setObjectName('app_logo')
        self.login_logo = QtWidgets.QLabel(self.centralwidget)
        self.login_logo.setGeometry(430, 120, 200, 200)
        self.login_logo.setObjectName('login_logo')

        self.username_input = QtWidgets.QLineEdit(self.centralwidget)
        self.username_input.setGeometry(435, 320, 200, 40)
        self.username_input.setPlaceholderText('Username')
        self.username_input.setObjectName('login_input')
        self.password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.password_input.setGeometry(435, 380, 200, 40)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setObjectName('login_input')
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.login_button = QtWidgets.QPushButton('LOGIN', self.centralwidget)
        self.login_button.setGeometry(435, 450, 200, 50)
        self.login_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.login_button.setObjectName('login_button')
        self.login_button.clicked.connect(self.login_account)
        self.version_text = QtWidgets.QLabel('v0.0.1', self.centralwidget)
        self.version_text.setGeometry(765, 630, 70, 20)
        self.version_text.setObjectName('version_text')

    def login_account(self):
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()

        for username in cursor.execute('SELECT username FROM users'):
            if username[0] == self.username_input.text():
                for password in cursor.execute('SELECT password FROM users WHERE username=(?)', (self.username_input.text(),)):
                    if password[0] == self.password_input.text():
                        for role in cursor.execute('SELECT admin_role FROM users WHERE username=(?)', (self.username_input.text(),)):
                            if role[0] == 'Yes':
                                print(f'loggin successfully, welcome back admin, {username[0]}')
                            else:
                                print(f'loggin successfully, welcome back user {username[0]}')
                    else:
                        create_error(self,'Your username or your password was wrong!', 500, 410, 250, 20)
            else:
                create_error(self, 'Your username or your password was wrong!', 500, 410, 250, 20)

#Running App
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    with open('style/style.css', 'r') as f:
        stylesheet = f.read()
    app.setStyleSheet(stylesheet)
    window = MyApp()
    window.show()
    sys.exit(app.exec())