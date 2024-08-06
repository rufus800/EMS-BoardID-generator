from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QMessageBox, 
                             QTabWidget, QComboBox, QFileDialog, QDateEdit, QProgressBar, QStatusBar)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from app.core.board_manager import BoardManager
from app.core.id_generator import IDGenerator
import csv
import serial

class MainWindow(QMainWindow):
    def __init__(self, database, username):
        super().__init__()
        self.database = database
        self.username = username
        self.board_manager = BoardManager(database)
        self.id_generator = IDGenerator(database)
        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon('path/to/icon.png'))  # Add an icon to the window
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.create_data_entry_tab(), "Data Entry")
        self.tab_widget.addTab(self.create_data_view_tab(), "Data View")

        main_layout.addWidget(self.tab_widget)

        self.connection_status = QLabel("Board Status: Not Connected")
        main_layout.addWidget(self.connection_status)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle(f'EMS Board ID Generator - Logged in as {self.username}')
        self.setGeometry(100, 100, 800, 600)
        
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.check_board_connection()

    def create_data_entry_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.board_name_input = QLineEdit()
        self.board_name_input.setPlaceholderText("Enter board name")
        layout.addWidget(QLabel("Board Name:"))
        layout.addWidget(self.board_name_input)

        self.board_type_input = QComboBox()
        self.board_type_input.addItems(["Type A", "Type B", "Type C"])
        layout.addWidget(QLabel("Board Type:"))
        layout.addWidget(self.board_type_input)

        self.manufacturer_input = QLineEdit()
        self.manufacturer_input.setPlaceholderText("Enter manufacturer name")
        layout.addWidget(QLabel("Manufacturer:"))
        layout.addWidget(self.manufacturer_input)

        self.manufacture_date_input = QDateEdit()
        self.manufacture_date_input.setDate(QDate.currentDate())
        layout.addWidget(QLabel("Manufacture Date:"))
        layout.addWidget(self.manufacture_date_input)

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Enter any additional notes here")
        layout.addWidget(QLabel("Notes:"))
        layout.addWidget(self.notes_input)

        generate_button = QPushButton("Generate ID")
        generate_button.clicked.connect(self.generate_id)
        generate_button.setStyleSheet("background-color: #4CAF50; color: white;")
        layout.addWidget(generate_button)

        tab.setLayout(layout)
        return tab

    def create_data_view_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search boards...")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_boards)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        self.board_table = QTableWidget()
        self.board_table.setColumnCount(6)
        self.board_table.setHorizontalHeaderLabels(['ID', 'Name', 'Type', 'Manufacturer', 'Manufacture Date', 'Notes'])
        self.board_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only
        layout.addWidget(self.board_table)

        button_layout = QHBoxLayout()
        export_button = QPushButton("Export to CSV")
        import_button = QPushButton("Import from CSV")
        export_button.clicked.connect(self.export_to_csv)
        import_button.clicked.connect(self.import_from_csv)
        button_layout.addWidget(export_button)
        button_layout.addWidget(import_button)
        layout.addLayout(button_layout)

        tab.setLayout(layout)
        self.load_board_data()
        return tab

    def generate_id(self):
        try:
            board_info = {
                'name': self.board_name_input.text(),
                'type': self.board_type_input.currentText(),
                'manufacturer': self.manufacturer_input.text(),
                'manufacture_date': self.manufacture_date_input.date().toString(Qt.ISODate),
                'notes': self.notes_input.toPlainText()
            }
            
            if not all([board_info['name'], board_info['manufacturer']]):
                raise ValueError("Board name and manufacturer are required fields.")

            unique_id = self.id_generator.generate_unique_id(board_info)
            board_info['id'] = unique_id

            if self.board_manager.store_board_info(board_info):
                QMessageBox.information(self, 'Success', f'Board information stored successfully. Generated ID: {unique_id}')
                self.load_board_data()
                self.clear_input_fields()
            else:
                raise Exception("Failed to store board information.")
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))

    def clear_input_fields(self):
        self.board_name_input.clear()
        self.board_type_input.setCurrentIndex(0)
        self.manufacturer_input.clear()
        self.manufacture_date_input.setDate(QDate.currentDate())
        self.notes_input.clear()

    def load_board_data(self):
        try:
            boards = self.board_manager.get_all_boards()
            self.update_board_table(boards)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to load board data: {str(e)}')

    def update_board_table(self, boards):
        self.board_table.setRowCount(len(boards))
        for row, board in enumerate(boards):
            for col, key in enumerate(['id', 'name', 'type', 'manufacturer', 'manufacture_date', 'notes']):
                self.board_table.setItem(row, col, QTableWidgetItem(str(board[key])))
        self.board_table.resizeColumnsToContents()

    def search_boards(self):
        search_term = self.search_input.text().lower()
        try:
            all_boards = self.board_manager.get_all_boards()
            filtered_boards = [board for board in all_boards if search_term in str(board).lower()]
            self.update_board_table(filtered_boards)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Search failed: {str(e)}')

    def export_to_csv(self):
        try:
            file_name, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV Files (*.csv)")
            if file_name:
                boards = self.board_manager.get_all_boards()
                with open(file_name, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=['id', 'name', 'type', 'manufacturer', 'manufacture_date', 'notes'])
                    writer.writeheader()
                    for board in boards:
                        writer.writerow(board)
                QMessageBox.information(self, 'Success', 'Data exported successfully.')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Export failed: {str(e)}')

    def import_from_csv(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(self, "Import from CSV", "", "CSV Files (*.csv)")
            if file_name:
                with open(file_name, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        self.board_manager.store_board_info(row)
                self.load_board_data()
                QMessageBox.information(self, 'Success', 'Data imported successfully.')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Import failed: {str(e)}')

    def check_board_connection(self):
        try:
            with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
                self.connection_status.setText("Board Status: Connected")
                self.connection_status.setStyleSheet("color: green;")
        except serial.SerialException:
            self.connection_status.setText("Board Status: Not Connected")
            self.connection_status.setStyleSheet("color: red;")
        except Exception as e:
            self.connection_status.setText(f"Board Status: Error - {str(e)}")
            self.connection_status.setStyleSheet("color: orange;")