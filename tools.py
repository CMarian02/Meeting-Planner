from PyQt6 import QtWidgets, QtCore
def close_db(conn, cursor):
    close_db.__doc__ = 'A function to close connection with databases.'
    conn.commit()
    cursor.close()
    conn.close()

def create_error(parent, error_text, y, x, width, height):
    create_error.__doc__ = 'A function to display error for inputs.'
    error = QtWidgets.QLabel(parent)
    error.setText(f'(?) {error_text}')
    error.setGeometry(x, y, width, height)
    error.setObjectName('error_frame')
    error.setStyleSheet('style.css')
    error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    error.show()
    timer = QtCore.QTimer()
    timer.singleShot(1700, error.deleteLater)
    