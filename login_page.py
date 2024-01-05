from PyQt6 import QtWidgets, QtCore
from tools import *
from admin_panel import *
from user_panel import *
import sqlite3, sys

class LoginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meeting Planner")
        self.setFixedSize(800,650)
        self.setWindowIcon(QtGui.QIcon('img/favicon.png'))
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.left_panel = QtWidgets.QLabel(self.centralwidget)
        self.left_panel.setGeometry(150, 150, 240, 440)
        self.left_panel.setObjectName('left_panel')
        self.right_panel = QtWidgets.QLabel(self.centralwidget)
        self.right_panel.setGeometry(410, 150, 250, 440)
        self.right_panel.setObjectName('right_panel')
        self.app_logo = QtWidgets.QLabel(self.centralwidget)
        self.app_logo.setGeometry(150, 290, 200, 200)
        self.app_logo.setObjectName('app_logo')
        self.login_logo = QtWidgets.QLabel(self.centralwidget)
        self.login_logo.setGeometry(430, 120, 200, 200)
        self.login_logo.setObjectName('login_logo') 
        self.username_input = QtWidgets.QLineEdit(self.centralwidget)
        self.username_input.setGeometry(435, 320, 200, 40)
        self.username_input.setPlaceholderText('username')
        self.username_input.setObjectName('login_input')
        self.password_input = QtWidgets.QLineEdit(self.centralwidget)
        self.password_input.setGeometry(435, 380, 200, 40)
        self.password_input.setPlaceholderText('password')
        self.password_input.setObjectName('login_input')
        self.password_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.login_button = QtWidgets.QPushButton('LOGIN', self.centralwidget)
        self.login_button.setGeometry(435, 500, 200, 50)
        self.login_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.login_button.setObjectName('login_button')
        self.login_button.clicked.connect(self.login_account)
        self.version_text = QtWidgets.QLabel('v0.0.2', self.centralwidget)
        self.version_text.setGeometry(765, 630, 70, 20)
        self.version_text.setObjectName('version_text')

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Enter or event.key() == QtCore.Qt.Key.Key_Return:
            self.login_account()

    def login_account(self):
        connection = sqlite3.connect('data/users.db')
        cursor = connection.cursor()
        for username in cursor.execute('SELECT username FROM users'):
            if username[0] == self.username_input.text().lower():
                for password in cursor.execute('SELECT password FROM users WHERE username=(?)', (self.username_input.text().lower(),)):
                    if password[0] == self.password_input.text():
                        for role in cursor.execute('SELECT team_role FROM users WHERE username=(?)', (self.username_input.text().lower(),)):
                            if role[0] == 'Yes':
                                print(f'loggin successfully, welcome back admin, {username[0]}')
                                self.close()
                                self.displayed_page = AdminPage(self.username_input.text())
                                self.displayed_page.show()
                            else:
                                for team in cursor.execute('SELECT team FROM users WHERE username=(?)', (self.username_input.text().lower(),)):
                                    self.close()
                                    self.displayed_page = UserPage(self.username_input.text(), team[0], role[0])
                                    self.displayed_page.show()
                    else:
                        create_error(self,'Your username or password was wrong!', 550, 410, 250, 20)
            else:
                create_error(self, 'Your username or password was wrong!', 550, 410, 250, 20)
        close_db(connection, cursor)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    with open('style/style.css', 'r') as f:
        stylesheet = f.read()
    app.setStyleSheet(stylesheet)
    window = LoginPage()
    window.show()
    sys.exit(app.exec())