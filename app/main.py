import sys
from PyQt5.QtWidgets import QApplication
from app.gui.login_window import LoginWindow
from app.core.database import Database

def main():
    app = QApplication(sys.argv)
    
    # Initialize database connection
    db = Database()
    
    # Create and show the login window
    login_window = LoginWindow(db)
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()