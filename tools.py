from PyQt6 import QtWidgets, QtCore
#A function to close connection with databases.
def close_db(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()

#A function to display error for inputs.
def create_error(parent, error_text, y, x, width, height):
    error = QtWidgets.QLabel(parent)
    error.setText(f'(?) {error_text}')
    error.setGeometry(x, y, width, height)
    error.setObjectName('error_frame')
    error.setStyleSheet('style.css')
    error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    error.show()
    timer = QtCore.QTimer()
    timer.singleShot(1700, error.deleteLater)
    