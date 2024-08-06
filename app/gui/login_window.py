from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from app.utils.security import verify_password
from app.gui.main_window import MainWindow

class LoginWindow(QWidget):
    login_successful = pyqtSignal(str)

    def __init__(self, database):
        super().__init__()
        self.database = database
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.setWindowIcon(QIcon('path/to/icon.png'))  # Add an icon to the window

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        login_button = QPushButton('Login')
        login_button.setStyleSheet("background-color: #4CAF50; color: white;")

        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        login_button.clicked.connect(self.attempt_login)
        self.password_input.returnPressed.connect(self.attempt_login)  # Allow login on Enter key

        self.setLayout(layout)
        self.setWindowTitle('EMS Board ID Generator - Login')
        self.setGeometry(300, 300, 300, 150)
        self.setStyleSheet("QWidget { background-color: #f0f0f0; }")

    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        try:
            if verify_password(username, password):
                self.login_successful.emit(username)
                self.open_main_window(username)
            else:
                QMessageBox.warning(self, 'Login Failed', 'Invalid username or password.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred during login: {str(e)}')

    def open_main_window(self, username):
        try:
            self.main_window = MainWindow(self.database, username)
            self.main_window.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to open main window: {str(e)}')